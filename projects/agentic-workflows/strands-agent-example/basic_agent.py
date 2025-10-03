from strands import Agent, tool
from strands_tools import calculator, current_time
from strands.models.openai import OpenAIModel
from strands.handlers.callback_handler import PrintingCallbackHandler
from dotenv import load_dotenv
import os

load_dotenv()

model = OpenAIModel(
    client_args={
        "api_key": os.getenv("OPENAI_API_KEY"),
    },
    # **model_config
    model_id="gpt-4o",
    params={
        "max_tokens": 1000,
        "temperature": 0.7,
    }
)

# Define a custom tool as a Python function using the @tool decorator
@tool
def letter_counter(word: str, letter: str) -> int:
    """
    Count occurrences of a specific letter in a word.

    Args:
        word (str): The input word to search in
        letter (str): The specific letter to count

    Returns:
        int: The number of occurrences of the letter in the word
    """
    if not isinstance(word, str) or not isinstance(letter, str):
        return 0

    if len(letter) != 1:
        raise ValueError("The 'letter' parameter must be a single character")

    return word.lower().count(letter.lower())

# Create an agent with tools from the community-driven strands-tools package
# as well as our custom letter_counter tool
agent = Agent(
    tools=[calculator, current_time, letter_counter],
    model=model,
    callback_handler=PrintingCallbackHandler() #Docs say console output default but this was required.
    )

if __name__=="__main__":
    # Ask the agent a question that uses the available tools
    message = """
    I have 4 requests:

    1. What is the time right now?
    2. Calculate 3111696 / 74088
    3. Tell me how many letter R's are in the word "strawberry" 🍓
    """
    result = agent(message)
    print(result.metrics.get_summary())