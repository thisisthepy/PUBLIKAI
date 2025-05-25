from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
from pydantic import BaseModel
import asyncio
import uvicorn
import json

from model import llama3
from model.llama3 import ChatHistory

token_streamer = llama3.token_streamer

class Message(BaseModel):
    role: str
    content: str

app = FastAPI()


@app.get("/hello")
def hello():
    return "".join(token for token in token_streamer(*llama3.chat(ChatHistory(), "안녕?")))


@app.post("/chat")
async def chat(user_prompt: str, history: Optional[List[Message]] = None):
    """ Chat endpoint """

    chat_history = ChatHistory()
    if history:
        chat_history.extend(history)
    return "".join(token for token in token_streamer(*llama3.chat(chat_history, user_prompt)))


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """ Websocket endpoint """

    await websocket.accept()

    chat_history = ChatHistory()
    chat_history.extend(json.loads(await websocket.receive_text()))
    user_prompt = await websocket.receive_text()

    for token in token_streamer(*llama3.chat(chat_history, user_prompt)):
        await websocket.send_text(token)
        await asyncio.sleep(0.001)  # 1ms delay between tokens

    await websocket.send_text("<EOS>")  # EOS toke to signal the end of the conversation
    await websocket.close()


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
