from fastapi import FastAPI, WebSocket, Request, HTTPException
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

from typing import List, Optional
import traceback
import asyncio
import json
import os

from .settings import STATIC_DIR, WEBPACK_DIR, MODEL_LIST, Session
from .models.config import ChatHistory
import requests
import re
from bs4 import BeautifulSoup
import html

from .models.graduation_rag.rag import GraduationRAG

DATA_DIR = "data/graduation" 
markdown_files = {
    year: os.path.join(DATA_DIR, f"grad_{year}.md")
    for year in range(2020, 2026)
}
# RAG 시스템 초기화
rag_system = GraduationRAG(md_files_by_year=markdown_files)


def extract_info(html_content):
    """
    HTML 코드에서 게시글 정보를 추출하여 딕셔너리 리스트로 반환
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    posts = []
    events = []

    # b-title-box 클래스를 가진 div 요소들을 찾음
    title_boxes = soup.find_all('div', class_='b-title-box')
    calen_boxes = soup.find_all('div', class_='calen_box')
    if title_boxes:
        for box in title_boxes:
            post_info = {}

            # 제목과 링크 추출
            title_link = box.find('a')
            if title_link:
                post_info['title'] = title_link.get_text(strip=True)
                post_info['href'] = title_link.get('href', '')

            # 날짜 추출 (b-date 클래스를 가진 span 요소)
            date_span = box.find('span', class_='b-date')
            if date_span:
                post_info['date'] = date_span.get_text(strip=True)

            # 필수 정보가 모두 있는 경우에만 추가
            if 'title' in post_info and 'href' in post_info and 'date' in post_info:
                posts.append(post_info)
            
        return posts
    if calen_boxes:
        for calen_box in calen_boxes:
            list_items = calen_box.select('div.fr_list ul li') 
            for item in list_items:
                event_info = {}

                date_strong = item.find('strong') 
                if date_strong:
                    event_info['date'] = date_strong.get_text(strip=True)
                
                description_span = item.find('span', class_='list') 
                if description_span:
                    event_info['description'] = description_span.get_text(strip=True)

                if 'date' in event_info and 'description' in event_info:
                    events.append(event_info)
        return events
    
url_dict = {
    "graudate_data" : "https://plus.cnu.ac.kr/html/kr/sub05/sub05_051202.html",
    "ai_notice" : "https://ai.cnu.ac.kr/ai/board/notice.do",
    "cse_notice" : "https://computer.cnu.ac.kr/computer/notice/bachelor.do",
    "eng_notice" : "https://eng.cnu.ac.kr/eng/information/notice.do",
    "cnu_notice" : "https://plus.cnu.ac.kr/_prog/_board/?code=sub07_0701&site_dvs_cd=kr&menu_dvs_cd=0701",
    "calendar" : "https://plus.cnu.ac.kr/_prog/academic_calendar/?site_dvs_cd=kr&menu_dvs_cd=05020101",
    "food" : "https://mobileadmin.cnu.ac.kr/food/index.jsp",
    "bus" : "https://plus.cnu.ac.kr/html/kr/sub05/sub05_050403.html"
}

def get_graduate_data(url: str):
    '''
    Uesr Prompt 들어오게 바꿔야함.
    '''
    if not rag_system.retriever:
        return "There is no Data"
    
    # RAG 시스템의 answer_question 메소드 호출
    return rag_system.answer_question(url)

def get_ai_notice(url: str):
    url = url_dict["ai_notice"]
    data = (requests.get(url).text
            .replace("\n", "")
            .replace("  ", "")
            .replace("\r", "")
            .replace("\t", ""))
    return extract_info(data)

def get_cse_notice(url: str):
    url = url_dict["cse_notice"]
    data = (requests.get(url).text
            .replace("\n", "")
            .replace("  ", "")
            .replace("\r", "")
            .replace("\t", ""))
    return extract_info(data)

def get_eng_notice(url: str):
    url = url_dict["eng_notice"]
    data = (requests.get(url).text
            .replace("\n", "")
            .replace("  ", "")
            .replace("\r", "")
            .replace("\t", ""))
    return extract_info(data)

def get_cnu_notice(url: str):
    url = url_dict["cnu_notice"]
    data = (requests.get(url).text
            .replace("\n", "")
            .replace("  ", "")
            .replace("\r", "")
            .replace("\t", ""))
    return extract_info(data)

def get_calendar(url: str):
    url = url_dict["calendar"]
    data = (requests.get(url).text
            .replace("\n", "")
            .replace("  ", "")
            .replace("\r", "")
            .replace("\t", ""))
    return extract_info(data)

def get_food(url: str):
    url = url_dict["food"]
    data = (requests.get(url).text
            .replace("\n", "")
            .replace("  ", "")
            .replace("\r", "")
            .replace("\t", ""))
    return extract_info(data)

def get_bus(url: str):
    url = url_dict["bus"]
    data = (requests.get(url).text
            .replace("\n", "")
            .replace("  ", "")
            .replace("\r", "")
            .replace("\t", ""))
    return extract_info(data)

class Message(BaseModel):
    role: str
    content: str


app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR, html=True), name="static")
app.mount("/webpack", StaticFiles(directory=WEBPACK_DIR, html=True), name="webpack")


@app.get("/")
def root():
    """ Redirect to the chat page """
    #return RedirectResponse(url="/chat")
    return FileResponse(os.path.join(WEBPACK_DIR, "index.html"))


@app.get("/composeResources/{path:path}")
def resource(path: str):
    """ Redirect to the chat page """
    return RedirectResponse(
        url=f"/webpack/composeResources/{path}",
        status_code=301
    )


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
        chat_history.extend([h.model_dump() for h in history])

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

    def parse_all_tool_calls_from_content(content: str) -> list[dict]:
        tool_calls_data = []

        for match in re.finditer(r'<tool_call>\s*(\{.*?\})\s*</tool_call>', content, re.DOTALL):
            json_string = match.group(1)
            try:

                parsed_func = json.loads(json_string)

                tool_calls_data.append(parsed_func)

            except json.JSONDecodeError as e:

                print(f"Warning: Failed to parse JSON from tool_call: {json_string}. Error: {e}")
                continue

        return tool_calls_data

    while True:
        answer = ""
        for token in model.chat(chat_history, user_prompt, print_output=True):
            answer+=token
            await websocket.send_text(token)
            await asyncio.sleep(0.0001)  # 0.1ms delay between tokens

        user_prompt = ""
        if "<tool_call>" not in answer:
            break
        # tool_call parsing
        parsed = parse_all_tool_calls_from_content(answer)

        tool_call_info = parsed[0]
        result = get_ai_notice(tool_call_info['arguments']["url"])

        chat_history.append("assistant", dict(tool_calls=dict(function=tool_call_info)))
        chat_history.append("tool", result)


    del model

    await websocket.send_text("<EOS>")  # EOS toke to signal the end of the conversation
    await websocket.close()


if __name__ == '__main__':
    uvicorn.run(
        app, host="127.0.0.1", port=23100,
        ws_ping_interval=120, ws_ping_timeout=60, ws_per_message_deflate=False, timeout_keep_alive=600
    )
