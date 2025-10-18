"""
A very basic data science agent.

Author: Andy McMahon
Date: 3rd Oct 2025.
"""
from strands import Agent
from strands_tools import calculator, current_time
from strands.models.openai import OpenAIModel
from strands.handlers.callback_handler import PrintingCallbackHandler

from strands_tools.browser import LocalChromiumBrowser
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

# Tools
browser = LocalChromiumBrowser()


agent = Agent(
    model=model,
    tools=[browser.browser]
)

if __name__=="__main__":
    prompt = """
    You are a researcher analyst who answers questions by going to the web and 
    carefully analysing and compressing your answers before giving a solution.
    
    You can split your initial request into sub queries and go and get individual answers
    before combining into the end answer.
    
    ----
    
    Create a nice chronological summary of the second Punic war, and for each date note something else of interest 
    at that time.
    """
    agent(prompt=prompt)