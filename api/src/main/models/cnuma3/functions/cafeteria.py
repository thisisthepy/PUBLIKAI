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


def get_cafeteria_menu(date: str, retry: int = 3) -> str:
    url = f"https://mobileadmin.cnu.ac.kr/food/index.jsp?searchYmd={date}&searchLang=OCL04.10&searchView=cafeteria&searchCafeteria=OCL03.02&Language_gb=OCL04.10"

    for attempt in range(retry):
        try:
            data = web_search.fetch_webpage(url, length_limit=-1)
            if "text_content" in data:
                data = data["text_content"]
                data = data.split("요일별 식단메뉴에 대한 안내제공")[-1].strip()
                data = data.split("하나. 구내식당 식재료 원산지입니다")[0].strip()
                return f"""# 요일별 식단메뉴에 대한 안내제공 - {date}
**참고사항**
항상 메뉴가 동일하며 라면&간식, 양식, 스낵, 한식, 일식, 중식이 제공됩니다.
저녁에는 한식과 중식만 운영이 되고 있으며, 주말에는 식당이 운영되지 않습니다.


## 학생 식당별 메뉴 테이블 정보
""" + data
        except requests.RequestException as e:
            print(f"웹 페이지 가져오기 실패: {e}. 재시도 중... ({attempt + 1}/{retry})")
    return "학교 홈페이지가 현재 접속되지 않거나 아직 정보가 업로드 되지 않은 날짜입니다. 나중에 다시 시도해주세요."


def get_dorm_cafeteria_menu(week: int = 1, retry: int = 3) -> str:
    try:
        week = int(week)
    except ValueError:
        return "주는 숫자로 입력해주세요. 예: 1"

    url = f"https://dorm.cnu.ac.kr/html/kr/sub03/sub03_0304.html?mode=sch&page={week}"

    for attempt in range(retry):
        try:
            data = web_search.fetch_webpage(url, length_limit=-1)
            if "text_content" in data:
                data = data["text_content"]
                data = "오늘의식단 " + data.split("오늘의식단")[-1].strip()
                data = data.split("충남대학교 관련사이트")[0].strip()
                return data
        except requests.RequestException as e:
            print(f"웹 페이지 가져오기 실패: {e}. 재시도 중... ({attempt + 1}/{retry})")
    return "기숙사 홈페이지가 현재 접속되지 않아 식단을 가져오는 데 실패했습니다. 나중에 다시 시도해주세요."


if __name__ == '__main__':
    # Example usage
    print("이번주 학생생활관 식당 메뉴:")
    print(get_dorm_cafeteria_menu(1))

    print("\n지난주 학생생활관 식당 메뉴:")
    print(get_dorm_cafeteria_menu(2))  # Previous week

    print("\n오늘 학생회관 식당 메뉴:")
    print(get_cafeteria_menu("2025.06.20"))
