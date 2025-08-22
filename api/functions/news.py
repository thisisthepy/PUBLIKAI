import requests
from typing import Dict, Any
from datetime import datetime, timedelta
import random
import sys
import os
import re

try:
    from ..utils import web_search
except ImportError:
    parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent)
    from utils import web_search


def get_center_news(retry: int = 3) -> str:
    url = "https://www.cheonanurc.or.kr/35"

    for attempt in range(retry):
        try:
            data = web_search.fetch_webpage(url, length_limit=10000)
            if "text_content" in data:
                data = data["text_content"].split("Copyrightⓒ")[0].strip()
                data = data.split("천안시 도시재생지원센터 site search")[-1].strip()
                return data
        except requests.RequestException as e:
            print(f"웹 페이지 가져오기 실패: {e}. 재시도 중... ({attempt + 1}/{retry})")
    return "홈페이지가 현재 접속되지 않아 소식 조회에 실패했습니다.. 나중에 다시 시도해주세요."


def subscribe_newsletter(nick: str, email: str, name: str, retry: int = 3, use_test_msg: bool = False) -> str:
    if not nick or not email or not name or len(nick) < 2 or "@" not in email or "." not in email or len(name) < 2:
        return "이메일과 이름을 모두 입력해야 뉴스레터를 신청할 수 있습니다."

    password = random.randint(100000, 999999)

    token_url = "https://www.cheonanurc.or.kr/ajax/make_token.cm?article_reaction_set_like"
    expire = 86400
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': "https://www.cheonanurc.or.kr/144/?q=YToxOntzOjEyOiJrZXl3b3JkX3R5cGUiO3M6MzoiYWxsIjt9&bmode=view&idx=167281093&t=board",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    token = ""
    for attempt in range(retry):
        try:
            response = requests.post(f"{token_url}&expire={expire}", headers=headers)
            if response.status_code == 200:
                token = response.json().get("token", ""), response.json().get("token_key", 0)
                break
        except requests.RequestException as e:
            print(f"토큰 생성 실패: {e}. 재시도 중... ({attempt + 1}/{retry})")

    if not token:
        return "홈페이지 접속 오류로 인해 토큰 생성에 실패했습니다. 나중에 다시 시도해주세요."

    subscribe_url = "https://www.cheonanurc.or.kr/ajax/post_comment_add.cm"
    data = dict(
        post_code="p20250811fe0c44ec6963f",
        board_code="b20220405555f5014b8d21",
        comment_token=token[0],
        comment_token_key=token[1],
        nick=nick,
        secret_pass=f"{password}",
        body=f"이메일: test@test.com\n이름: test\n\n** 챗봇 테스트중입니다.**" if use_test_msg else f"이메일: {email}\n이름: {name}\n\n** PUBLIKAI를 통해 구독 신청을 하였습니다. **",
        use_secret_comment="Y",
        menu_url="/144/"
    )
    print(f"구독 신청 데이터: {data}")
    for attempt in range(retry):
        try:
            response = requests.post(subscribe_url, data=data, headers=headers)
            if response.status_code == 200:
                result = response.json()
                if result.get("msg").lower() == "success":
                    return f"구독 신청이 완료되었습니다. 신청 내역은 비밀번호 `{password}`를 사용하여 홈페이지에서 확인할 수 있습니다."
                else:
                    return f"구독 신청 실패: {result}"
        except requests.RequestException as e:
            print(f"구독 신청 실패: {e}. 재시도 중... ({attempt + 1}/{retry})")

    return "홈페이지 접속 오류로 인해 구독 신청에 실패했습니다. 나중에 다시 시도해주세요."


if __name__ == '__main__':
    # Example usage
    print("센터 뉴스:")
    print(get_center_news())
    
    print("\n뉴스레터 구독 신청:")
    print(subscribe_newsletter("테스트", "test@test.com", "테스트 사용자", use_test_msg=True))
