import requests
from typing import Dict, Any
from datetime import datetime, timedelta
import sys
import os
import re

try:
    from ...utils import web_search
except ImportError:
    parent = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    sys.path.insert(0, parent)
    from utils import web_search


def get_cnu_notices(query: str = "", retry: int = 3) -> str:
    url = f"https://plus.cnu.ac.kr/_prog/_board/?code=sub07_0702&site_dvs_cd=kr&menu_dvs_cd=0702"

    if query:
        url += f"&skey=title&GotoPage=1&sval={query}"

    for attempt in range(retry):
        try:
            data = web_search.fetch_webpage(url, length_limit=-1)
            if "text_content" in data:
                data = data["text_content"].split("페이지 관리자")[0].strip()
                data = "학사정보게시판 " + data.split("학사정보게시판 ")[-1].strip()
                return data
        except requests.RequestException as e:
            print(f"웹 페이지 가져오기 실패: {e}. 재시도 중... ({attempt + 1}/{retry})")
    return "학교 홈페이지가 현재 접속되지 않아 공지사항 조회에 실패했습니다.. 나중에 다시 시도해주세요."


def get_cnu_ai_notices(query: str = "", retry: int = 3) -> str:
    url1 = f"https://ai.cnu.ac.kr/ai/board/notice.do"
    url2 = f"https://ai.cnu.ac.kr/ai/board/news.do"

    if query:
        url1 += f"?mode=list&srSearchKey=&srSearchVal={query}"
        url2 += f"?mode=list&srSearchKey=&srSearchVal={query}"

    data1 = ""
    for attempt in range(retry):
        try:
            data1 = web_search.fetch_webpage(url1, length_limit=-1)
            if "text_content" in data1:
                data1 = data1["text_content"].split("다음 페이지로 이동하기")[0].strip().split("전체목록")[0].strip()
                data1 = "학사소식 번호 " + data1.split("건 학사소식 번호")[-1].strip()
                break
        except requests.RequestException as e:
            print(f"웹 페이지 가져오기 실패: {e}. 재시도 중... ({attempt + 1}/{retry})")

    data2 = ""
    for attempt in range(retry):
        try:
            data2 = web_search.fetch_webpage(url2, length_limit=-1)
            if "text_content" in data2:
                data2 = data2["text_content"].split("다음 페이지로 이동하기")[0].strip().split("전체목록")[0].strip()
                data2 = "일반소식 번호 " + data2.split("건 일반소식 번호")[-1].strip()
                break
        except requests.RequestException as e:
            print(f"웹 페이지 가져오기 실패: {e}. 재시도 중... ({attempt + 1}/{retry})")

    if data1 + data2:
        return data1 + "\n\n" + data2
    return "학과 홈페이지가 현재 접속되지 않아 공지사항 조회에 실패했습니다.. 나중에 다시 시도해주세요."


if __name__ == '__main__':
    # Example usage
    print("AI 공지사항:")
    print(get_cnu_ai_notices())

    print("\nAI 데브데이 공지사항:")
    print(get_cnu_ai_notices("데브데이"))

    print("\n학교 공지사항:")
    print(get_cnu_notices())

    print("\n학교 공지사항:")
    print(get_cnu_notices("등록금"))
