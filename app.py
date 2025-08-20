from fastapi import FastAPI, WebSocket, Request, HTTPException
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

import gradio as gr
import spaces

from typing import List, Optional, Dict
import traceback
import asyncio
import json
import os

import mimetypes
from pathlib import Path
import urllib.parse

from api.settings import STATIC_DIR, MODEL_LIST, Session
from api.system import system_prompt, welcome_message
from api.models.config import ChatHistory


class Message(BaseModel):
    role: str
    content: str


class FileInfo(BaseModel):
    name: str
    url: str
    size: Optional[str] = None
    type: Optional[str] = None
    year: Optional[str] = None


app = FastAPI()
app.mount("/dashboard", StaticFiles(directory=STATIC_DIR, html=True), name="dashboard")
app.mount("/data", StaticFiles(directory="data"), name="data")


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


@app.get("/api/pdf/files")
async def get_pdf_files() -> Dict[str, List[FileInfo]]:
    """ Get all PDF files grouped by year """
    pdf_dir = Path("data/pdf")
    files_by_year = {}
    
    if not pdf_dir.exists():
        return {}
    
    def extract_year_from_path(file_path: Path) -> str:
        """Extract year from file path or filename"""
        path_str = str(file_path)
        
        # Check for year in path (e.g., "2024년", "2025년")
        import re
        year_match = re.search(r'(20\d{2})년?', path_str)
        if year_match:
            return f"{year_match.group(1)}년"
        
        # Check for year in filename (e.g., "2024_document.pdf")
        filename_match = re.search(r'(20\d{2})', file_path.name)
        if filename_match:
            return f"{filename_match.group(1)}년"
        
        return "기타"
    
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f}TB"
    
    # Recursively find all PDF files
    for pdf_file in pdf_dir.rglob("*.pdf"):
        if pdf_file.is_file():
            year = extract_year_from_path(pdf_file)
            
            # Calculate relative path from data directory
            relative_path = pdf_file.relative_to(Path("data"))
            file_url = f"/data/{relative_path.as_posix()}"
            
            file_info = FileInfo(
                name=pdf_file.name,
                url=file_url,
                size=format_file_size(pdf_file.stat().st_size),
                type="PDF",
                year=year
            )
            
            if year not in files_by_year:
                files_by_year[year] = []
            files_by_year[year].append(file_info)
    
    # Sort files within each year by name
    for year in files_by_year:
        files_by_year[year].sort(key=lambda x: x.name)
    
    return files_by_year


@app.get("/api/pdf/files/{year}")
async def get_pdf_files_by_year(year: str) -> List[FileInfo]:
    """ Get PDF files for a specific year """
    all_files = await get_pdf_files()
    return all_files.get(year, [])


@app.get("/api/pdf/download")
async def download_pdf_file(file_path: str):
    """ Download a PDF file with proper headers """
    try:
        # 보안을 위해 data/pdf 경로만 허용
        if not file_path.startswith('/data/pdf/') and not file_path.startswith('data/pdf/'):
            raise HTTPException(status_code=400, detail="Invalid file path")
        
        # 절대 경로 구성
        if file_path.startswith('/'):
            file_path = file_path[1:]  # 앞의 '/' 제거
        
        full_path = Path(file_path)
        
        if not full_path.exists() or not full_path.is_file():
            raise HTTPException(status_code=404, detail="File not found")
        
        # 파일명에서 확장자 추출
        filename = full_path.name
        
        # Content-Type 설정
        content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        
        # 한글 파일명을 위한 URL 인코딩
        encoded_filename = urllib.parse.quote(filename.encode('utf-8'))
        
        return FileResponse(
            path=str(full_path),
            filename=filename,
            media_type=content_type,
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading file: {str(e)}")


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
async def chat_with_streaming(websocket: WebSocket):
    """ Chat via Websocket endpoint """
    await websocket.accept()

    try:
        session_id = json.loads(await websocket.receive_text()).get("session_id")
        session = Session(session_id=session_id)
    except Exception:
        traceback.print_exc()
        await websocket.close(code=1008, reason="Invalid session ID or model not found.")
        return

    chat_history = ChatHistory()
    chat_history.extend(json.loads(await websocket.receive_text()))
    user_prompt = await websocket.receive_text()

    @spaces.GPU(duration=300)
    def run():
        model, model_name = session.model, session.model_name
        yield from model.chat(
            chat_history,
            user_prompt,
            system_prompt(model_name),
            print_output=True,
        )
        del model
    
    for token in run():
        await websocket.send_text(token)
        await asyncio.sleep(0.0001)  # 0.1ms delay between tokens

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
