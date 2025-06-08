from browser import aio, bind, document, window

from models.config import ChatHistory
import time
import json
import re

chat_history = ChatHistory()
ws = False

MODEL_ID = "qwen3"
SERVER_URL = "127.0.0.1:23100"
WEBSOCKET_URL = f"ws://{SERVER_URL}/api/chat/streaming"
SESSION_URL = f"http://{SERVER_URL}/api/models/{MODEL_ID}/sessions/"
SESSION_UNLOAD_URL = f"http://{SERVER_URL}/api/sessions/"
__SESSION_ID = None


async def get_session_id():
    global __SESSION_ID

    response = await window.fetch(SESSION_URL, {'method': "POST"})
    if response.status != 200:
        raise Exception("Failed to create session")

    data = await response.json()
    __SESSION_ID = data['session_id']
    print(f"Session ID: {__SESSION_ID}")
    return __SESSION_ID


aio.run(get_session_id())


@bind(window, 'unload')
def on_unload(_):
    if __SESSION_ID:
        window.navigator.sendBeacon(SESSION_UNLOAD_URL + __SESSION_ID, b"")


def on_open(_):
    print("Websocket connection is now open")

    data = document['message_text'].value.strip()
    if data and __SESSION_ID:
        ws.send(json.dumps({"session_id": __SESSION_ID}))  # 세션 ID 전송
        ws.send(json.dumps(chat_history))  # chat history 전송
        ws.send(data)  # user prompt 전송
        chat_history.append("user", data)  # chat history 업데이트
        update_screen(data, True)  # 화면 업데이트
        document['message_text'].value = ""  # 입력창 초기화


thinking_found = False
def on_message(evt):
    # message received from server
    print("Message received:", evt.data)
    if evt.data == "<EOS>":
        ws.close()
        return

    if evt.data:
        global thinking_found
        if thinking_found:
            if evt.data == "</think>":
                thinking_found = False
                print("Thinking/Reasoning ended")
            else:
                update_screen(evt.data, False, think=True)
        else:
            if evt.data == "<think>":
                thinking_found = True
                print("Thinking/Reasoning started")
            else:
                if "<tool_call>" not in evt.data:  # 일반 메시지인 경우
                    update_screen(evt.data, False)
                else:
                    tool_call = json.loads(evt.data.replace("<tool_call>", "").replace("</tool_call>", ""))
                    if "history" in tool_call:
                        chat_history.raw_extend(tool_call['history'])


def on_close(_):
    global ws
    # websocket is closed
    print("Websocket connection is now closed")
    target = document['messages'].lastChild
    message_content = target.querySelector(".message-content")
    chat_history.append("assistant", message_content.textContent)  # chat history 업데이트
    message_content.innerHTML = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', message_content.innerHTML.strip())
    ws = None


thinking_started = 0
def update_screen(text: str, user_content: bool = True, think: bool = False):
    global thinking_started
    message_list = document['messages']
    if user_content:
        # user content
        user = document.createElement("li")
        message_list.appendChild(user)
        user.classList.add("message")
        user.classList.add("message-user")

        # assistant content
        asst = document.createElement("li")
        asst.classList.add("message")
        asst.classList.add("message-server")
        asst.classList.add("d-none")  # 메시지 도달 되기 전까지 안보이도록
        asst.innerHTML = '<i class="fas fa-robot icon"></i>' \
            + '<div class="think-container">' \
            + '<i class="think-desc">0초 동안 생각 중...</i>' \
            + '<button class="think-toggle" onclick="toggleThinking(this)">▼</button>' \
            + '<div class="think-content d-none"></div>' \
            + '</div>' \
            + '<span class="message-content"></span>'
        message_list.appendChild(asst)
        target = user
    else:
        target = document['messages'].lastChild
        desc = target.querySelector(".think-desc")
        if "d-none" in target.classList:
            target.classList.remove("d-none")  # 메시지 도달 되면 보이도록
            thinking_started = time.time()
        if think:
            elapsed = float(desc.innerHTML.split("초")[0])
            elapsed += float(time.time() - thinking_started)
            desc.innerHTML = f"{elapsed:.1f}초 동안 생각 중..."
            thinking_started = time.time()  # 생각 시작 시간 갱신
            target = target.querySelector(".think-content")
        else:
            desc.innerHTML = desc.innerHTML.replace("생각 중...", "생각 완료")  # 생각 완료 표시
            target = target.querySelector(".message-content")
        target.innerHTML = target.innerHTML.lstrip()

    target.innerHTML += text
    message_list.scrollTop = message_list.scrollHeight


@bind('#form', 'submit')
def ws_open(e):
    e.preventDefault()  # 기본 submit 동작 방지

    global ws
    if ws:
        return  # 챗봇이 대답하고 있는 중에 버튼을 누르면 진행 안함

    # open a web socket
    ws = window.WebSocket.new(WEBSOCKET_URL)

    # bind functions to web socket events
    ws.bind('open', on_open)
    ws.bind('message', on_message)
    ws.bind('close', on_close)
    ws.bind('error', lambda e: print("Websocket error", e))


@bind('#message_text', 'keydown')
def keydown_disable(e):
    if e.key == "Enter" and not e.shiftKey:  # shift + Enter는 줄바꿈
        e.preventDefault()  # 기본 Enter 동작 방지
        document["form"].requestSubmit()  # 폼 전송


# JavaScript 함수를 window 객체에 추가
window.toggleThinking = lambda btn: toggle_thinking(btn)

def toggle_thinking(btn):
    think_content = btn.parentElement.querySelector(".think-content")
    if "d-none" in think_content.classList:
        think_content.classList.remove("d-none")
        btn.innerHTML = "▲"
    else:
        think_content.classList.add("d-none")
        btn.innerHTML = "▼"
