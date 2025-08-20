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


def subscribe_newsletter(email: str, name: str, retry: int = 3) -> str:
    if not email or not name:
        return "이메일과 이름을 모두 입력해야 뉴스레터를 신청할 수 있습니다."

    password = random.randint(100000, 999999)
    return f"구독 신청이 완료되었습니다. 신청 내역은 비밀번호 `{password}`를 사용하여 홈페이지에서 확인할 수 있습니다."


if __name__ == '__main__':
    # Example usage
    print("센터 뉴스:")
    print(get_center_news())
