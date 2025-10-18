import os
import random
from typing import Annotated, List, TypedDict, Literal

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

# Set API keys
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

class AgentState(TypedDict):
    """State schema for the RAG agent"""

    messages: Annotated[List[BaseMessage], add_messages]
    query: str
    selected_tools: List[str]
    retrieved_context: str
    tool_outputs: List[str]
    next_action: str


# Initialize vector store with your knowledge base
def setup_vector_store():
    """Set up your vector database with documents from local text file"""
    # Load your documents from local text file
    text_file_path = "src/manual.txt"  # Replace with your actual file path

    try:
        # Load the text file
        loader = TextLoader(text_file_path, encoding="utf-8")
        docs = loader.load()

        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=50
        )
        doc_splits = text_splitter.split_documents(docs)
        # Create vector store
        embeddings = OpenAIEmbeddings()
        vector_store = Chroma.from_documents(doc_splits, embeddings)

        return vector_store.as_retriever()

    except FileNotFoundError:
        print(
            f"Error: File '{text_file_path}' not found. Please check the file path."
        )
        return None
    except Exception as e:
        print(f"Error loading document: {str(e)}")
        return None


retriever = setup_vector_store()


######## TOOLS ########
@tool
def get_last_day_steps():
    """
    Get the last day's steps from the database
    """
    return random.randint(1000, 5000)


@tool
def get_last_day_average_heart_rate():
    """
    Get the last day's average heart rate from the database
    """
    return random.randint(60, 100)


@tool
def get_last_day_average_sleep_duration_in_hours():
    """
    Get the last day's average sleep duration from the database
    """
    return random.randint(3, 10)


# Tool registry for dynamic selection
tools = [
    get_last_day_steps,
    get_last_day_average_heart_rate,
    get_last_day_average_sleep_duration_in_hours,
]
tool_registry = {tool.name: tool for tool in tools}


######## TYPE DEFINITIONS ########
class RouteQuery(BaseModel):
    """Schema for routing decisions"""

    reasoning: str = Field(description="Reasoning for the routing decision")
    route: Literal["retrieval", "tools", "direct"] = Field(
        description="Where to route the query"
    )
    tools_needed: List[str] = Field(
        description="List of tools needed if route is 'tools'"
    )
    retrieval_query: str = Field(
        description="Optimized query for retrieval if route is 'retrieval'"
    )


def router_node(state: AgentState) -> AgentState:
    """Route the query to appropriate processing path"""

    system_prompt = """You are an intelligent router that decides how to process user queries.
    
    Available options:
    - 'retrieval': Query needs information from the knowledge base
    - 'tools': Query needs external tools (web search, calculations, etc.)  
    - 'direct': Query can be answered directly with general knowledge
    
    Available tools: {tools}
    
    Analyze the user query and decide the best routing approach. If tools are needed,
    specify which ones. If retrieval is needed, optimize the query for better results."""

    user_query = state["messages"][-1].content

    structured_llm = llm.with_structured_output(
        RouteQuery, method="function_calling"
    )

    response = structured_llm.invoke(
        [
            {
                "role": "system",
                "content": system_prompt.format(tools=[t.name for t in tools]),
            },
            {"role": "user", "content": user_query},
        ]
    )

    return {
        "query": user_query,
        "next_action": response.route,
        "selected_tools": response.tools_needed,
        "retrieved_context": (
            response.retrieval_query if response.route == "retrieval" else ""
        ),
    }


def tool_execution_node(state: AgentState) -> AgentState:
    """Execute selected tools"""
    tool_outputs = []
    for tool_name in state["selected_tools"]:
        if tool_name in tool_registry:
            tool = tool_registry[tool_name]
            try:
                # Use the original query for tool execution
                output = tool.invoke({"query": state["query"]})
                tool_outputs.append(f"{tool_name}: {output}")
            except Exception as e:
                tool_outputs.append(f"{tool_name}: Error - {str(e)}")

    return {"tool_outputs": tool_outputs}


def retrieval_node(state: AgentState) -> AgentState:
    """Execute retrieval from vector database"""
    query = state["retrieved_context"] or state["query"]

    try:
        # Retrieve relevant documents
        docs = retriever.invoke(query)
        context = "\n\n".join([doc.page_content for doc in docs])
        return {"retrieved_context": context}
    except Exception as e:
        return {"retrieved_context": f"Retrieval error: {str(e)}"}


def response_synthesis_node(state: AgentState) -> AgentState:
    """Synthesize final response from all available information"""

    # Prepare context from various sources
    context_parts = []

    if state.get("retrieved_context"):
        context_parts.append(
            f"Knowledge Base Context:\n{state['retrieved_context']}"
        )

    if state.get("tool_outputs"):
        tool_context = "\n".join(state["tool_outputs"])
        context_parts.append(f"Tool Outputs:\n{tool_context}")

    context = "\n\n".join(context_parts)

    system_prompt = """You are a helpful assistant that synthesizes information from multiple sources.
    
    Use the provided context to answer the user's question accurately and comprehensively.
    If using information from the context, be sure to reference it appropriately.
    If the context doesn't contain enough information, acknowledge this limitation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": f"Question: {state['query']}\n\nContext:\n{context}",
        },
    ]

    response = llm.invoke(messages)

    return {"messages": [AIMessage(content=response.content)]}


def intial_route_decision(state: AgentState) -> str:
    """Determine next node based on routing decision"""
    next_action = state.get("next_action", "direct")

    if next_action == "tools":
        return "tools"

    if next_action == "retrieval":
        return "retrieval"

    return "retrieval"


def create_rag_graph():
    """Create and compile the RAG workflow graph"""

    # Initialize the state graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("router", router_node)
    workflow.add_node("retrieval", retrieval_node)
    workflow.add_node("tools", tool_execution_node)
    workflow.add_node("synthesis", response_synthesis_node)

    # define edges
    workflow.add_edge(START, "router")
    workflow.add_conditional_edges(
        "router",
        intial_route_decision,
        {
            "retrieval": "retrieval",
            "tools": "tools",
            "synthesis": "synthesis",
        },
    )

    workflow.add_edge("retrieval", "synthesis")
    workflow.add_edge("tools", "synthesis")
    workflow.add_edge("synthesis", END)

    return workflow.compile()


# Create the graph
app = create_rag_graph()