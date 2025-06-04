from fastapi import FastAPI, WebSocket, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

from typing import List, Optional
import traceback
import asyncio
import json
import os

from .settings import STATIC_DIR, MODEL_LIST, Session
from .models.config import ChatHistory


class Message(BaseModel):
    role: str
    content: str


app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR, html=True), name="static")


@app.get("/chat")
def index():
    """ Serve the main HTML page """
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/api/models")
def models():
    """ List available models """
    return MODEL_LIST


@app.get("/api/hello")
def test_hello():
    """ Test endpoint to check if the server is running """
    temp_model = Session.load_model(model_name="default")
    response = temp_model.chat(ChatHistory(), "Hello?", stream=False, print_output=True)
    del temp_model
    Session.clean_up()
    return response


@app.post("/api/models/{model_id}/sessions/")
@app.post("/api/sessions/")
def create_session(model_id: str = "default"):
    """ Create a new session for the specified model """
    try:
        session = Session(model_id=model_id)
    except ValueError as e:
        return HTTPException(status_code=404, detail=e)

    return dict(model_id=model_id, session_id=session.session_id, message="A session is created successfully.")


@app.delete("/api/sessions/{session_id}")
@app.post("/api/sessions/{session_id}")
def delete_session(session_id: str):
    """ Delete a session by its ID """
    try:
        Session.close(session_id)
    except KeyError:
        return HTTPException(status_code=404, detail="The session is not found.")

    return dict(message="Session deleted successfully")


@app.post("/api/chat")
async def chat(request: Request, user_prompt: str, history: Optional[List[Message]] = None):
    """ Chat endpoint """
    try:
        session_id = request.headers.get("authorization")
        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID is required.")

        model = Session(session_id=session_id).model
    except ValueError:
        traceback.print_exc()
        raise HTTPException(status_code=404, detail="The session is not found.")

    chat_history = ChatHistory()
    if history:
        chat_history.extend(history)

    response = model.chat(chat_history, user_prompt, stream=False, print_output=True)
    del model
    return response


@app.websocket("/api/chat/streaming")
async def chat_with_streaming(websocket: WebSocket):
    """ Chat via Websocket endpoint """
    await websocket.accept()

    try:
        session_id = json.loads(await websocket.receive_text()).get("session_id")
        model = Session(session_id=session_id).model
    except Exception:
        traceback.print_exc()
        await websocket.close(code=1008, reason="Invalid session ID or model not found.")
        return

    chat_history = ChatHistory()
    chat_history.extend(json.loads(await websocket.receive_text()))
    user_prompt = await websocket.receive_text()

    for token in model.chat(chat_history, user_prompt):
        await websocket.send_text(token)
        await asyncio.sleep(0.0001)  # 0.1ms delay between tokens

    del model

    await websocket.send_text("<EOS>")  # EOS toke to signal the end of the conversation
    await websocket.close()


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
