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


def get_program_information(upcoming_only: bool = False, retry: int = 3) -> str:
    url = "https://www.cheonanurc.or.kr/41"

    for attempt in range(retry):
        try:
            data = web_search.fetch_webpage(url, length_limit=-1)
            if "text_content" in data:
                data = data["text_content"].split("Copyrightⓒ")[0].strip()
                data = data.split("천안시 도시재생지원센터 site search")[-1].strip()
                data = data.split("진행 중")[-1].strip().split("진행 완료")
                current = data[0].strip()
                completed = "진행 완료".join(data[1:]).strip()
                
                if not current:
                    current = "현재 진행 중이거나 계획된 프로그램이 없습니다. 계속해서 관심 부탁드립니다."

                if upcoming_only:
                    return "{'신청 가능 프로그램': " + current + "}"
                else:
                    return "{'신청 가능 프로그램': " + current + ", '신청 마감 프로그램': " + completed + "}"
        except requests.RequestException as e:
            print(f"웹 페이지 가져오기 실패: {e}. 재시도 중... ({attempt + 1}/{retry})")
    return "홈페이지가 현재 접속되지 않아 센터 프로그램 조회에 실패했습니다.. 나중에 다시 시도해주세요."


def get_upcoming_programs(retry: int = 3) -> str:
    return get_program_information(upcoming_only=True, retry=retry)


def get_program_history(retry: int = 3) -> str:
    return get_program_information(upcoming_only=False, retry=retry)


if __name__ == '__main__':
    # Example usage
    print("센터 프로그램:")
    print(get_program_information())
