from browser import aio, bind, document, window

from models.config import ChatHistory
import json

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


def on_message(evt):
    # message received from server
    print("Message received:", evt.data)
    if evt.data == "<EOS>":
        ws.close()
        return

    if evt.data:
        update_screen(evt.data, False)


def on_close(_):
    global ws
    # websocket is closed
    print("Websocket connection is now closed")
    target = document['messages'].lastChild
    chat_history.append("assistant", target.textContent)  # chat history 업데이트
    ws = None


def update_screen(text: str, user_content: bool = True):
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
        asst.innerHTML = '<i class="fas fa-robot icon"></i>'  # 아이콘을 왼쪽에 추가
        message_list.appendChild(asst)
        target = user
    else:
        target = document['messages'].lastChild
        if "d-none" in target.classList:
            target.classList.remove("d-none")  # 메시지 도달 되면 보이도록

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
