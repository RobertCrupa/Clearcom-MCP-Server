from fastapi import FastAPI
from pydantic import BaseModel
from .agent import agent_chat

app = FastAPI()

# Maintain conversation history
conversation_history = []

class chatRequest(BaseModel):
    prompt: str

@app.post("/chat")
async def chat_endpoint(request: chatRequest):
    conversation_history.append(request.prompt)

    response = await agent_chat(conversation_history)

    return {"response": "\n".join(response)}