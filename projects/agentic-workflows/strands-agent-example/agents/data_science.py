"""
A very basic data science agent.

Author: Andy McMahon
Date: 3rd Oct 2025.
"""
from strands import Agent
from strands_tools import calculator, current_time
from strands.models.openai import OpenAIModel
from strands.handlers.callback_handler import PrintingCallbackHandler
from tools.data_science import ds_tools #get_data
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

agent = Agent(
    model=model,
    tools=[ds_tools]
)

#print(agent.__dict__)