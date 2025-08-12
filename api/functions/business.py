import requests
from typing import Dict, Any
from datetime import datetime, timedelta
import sys
import os
import re

try:
    from ..utils import web_search
except ImportError:
    parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent)
    from utils import web_search


def get_business_information(retry: int = 3) -> str:
    url = "https://www.cheonanurc.or.kr/68"

    for attempt in range(retry):
        try:
            data = web_search.fetch_webpage(url, length_limit=-1)
            if "text_content" in data:
                data = data["text_content"].split("Copyrightⓒ")[0].strip()
                data = data.split("천안시 도시재생지원센터 site search")[-1].strip()
                return data
        except requests.RequestException as e:
            print(f"웹 페이지 가져오기 실패: {e}. 재시도 중... ({attempt + 1}/{retry})")
    return "홈페이지가 현재 접속되지 않아 사업 정보 조회에 실패했습니다.. 나중에 다시 시도해주세요."


if __name__ == '__main__':
    # Example usage
    print("사업 정보:")
    print(get_business_information())
