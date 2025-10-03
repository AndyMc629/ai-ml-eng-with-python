from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from strands import Agent
from strands_tools import calculator, http_request
from .basic_agent import agent

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/stream")
async def stream_response(request: PromptRequest):
    async def generate():
        # agent = Agent(
        #     tools=[calculator, http_request],
        #     callback_handler=None
        # )

        try:
            async for event in agent.stream_async(request.prompt):
                if "data" in event:
                    # Only stream text chunks to the client
                    yield event["data"]
        except Exception as e:
            yield f"Error: {str(e)}"

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}