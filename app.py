from fastapi import FastAPI, WebSocket, Request, HTTPException
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

import gradio as gr
import spaces

from typing import List, Optional
import traceback
import asyncio
import json
import os

from api.settings import STATIC_DIR, MODEL_LIST, Session
from api.system import system_prompt, welcome_message
from api.models.config import ChatHistory


class Message(BaseModel):
    role: str
    content: str


app = FastAPI()
app.mount("/dashboard", StaticFiles(directory=STATIC_DIR, html=True), name="dashboard")


@app.get("/")
def index():
    """ Serve the main HTML page """
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.get("/api/models")
def models():
    """ List available models """
    return MODEL_LIST


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


@app.websocket("/api/greetings")
async def greetings(websocket: WebSocket):
    """ Greet the user when they connect """
    await websocket.accept()
    _ = json.loads(await websocket.receive_text()).get("session_id")

    chat_history = ChatHistory()
    chat_history.extend(json.loads(await websocket.receive_text()))
    _ = await websocket.receive_text()

    for token in welcome_message:
        await websocket.send_text(token)
        await asyncio.sleep(0.05)  # 0.1s delay between tokens

    await websocket.send_text("<EOS>")  # EOS token to signal the end of the conversation
    await websocket.close()


@app.websocket("/api/chat")
@spaces.GPU(duration=300)
async def chat_with_streaming(websocket: WebSocket):
    """ Chat via Websocket endpoint """
    await websocket.accept()

    try:
        session_id = json.loads(await websocket.receive_text()).get("session_id")
        session = Session(session_id=session_id)
        model, model_name = session.model, session.model_name
    except Exception:
        traceback.print_exc()
        await websocket.close(code=1008, reason="Invalid session ID or model not found.")
        return

    chat_history = ChatHistory()
    chat_history.extend(json.loads(await websocket.receive_text()))
    user_prompt = await websocket.receive_text()

    for token in model.chat(chat_history, user_prompt, system_prompt(model_name), print_output=True):
        await websocket.send_text(token)
        await asyncio.sleep(0.0001)  # 0.1ms delay between tokens

    del model

    await websocket.send_text("<EOS>")  # EOS token to signal the end of the conversation
    await websocket.close()


# Gradio dummy interface (Hugging Face Spaces compatibility)
def dummy_function(text):
    return "This is a dummy interface. Please use the main chat interface."


gradio_interface = gr.Interface(
    fn=dummy_function,
    inputs="text",
    outputs="text",
    title="API Server",
    description="This server provides WebSocket API at /api/chat"
)

# Mount Gradio interface to FastAPI
app = gr.mount_gradio_app(app, gradio_interface, path="/gradio")


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
