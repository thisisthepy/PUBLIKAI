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


def get_shuttle_general_time_table():
    return """
# 2025학년도 학교셔틀버스 운영 안내 (2025년 5월 기준)

- **운영기간**: 학기 중 평일 운행 (평일 야간, 주말, 공휴일, 임시 공휴일, 방학, 수학능력시험일(10시 이전) 등 미운영)  
  - *추가사항*: 2025년 6월 3일이 대통령 선거로 인해 임시 공휴일로 지정되어 셔틀버스가 운영되지 않습니다.
- **운행시간표는 학교 사정에 따라 변동될 수 있음**
- **학생회 협의 요청 시**: 임시 셔틀버스 운영 가능
- **운행시간은 정기적인 점검, 학교행사, 교통상황, 정원 등에 따라 변경 가능**
- **탑승시간 준수**: 탑승시간 5분 내외 도착, 사전 대기 요망
- **운행 노선**:
  - **교내 순환**: 대덕캠퍼스 내
  - **캠퍼스 순환**: 대덕캠퍼스 ↔ 보운캠퍼스

## 셔틀버스 운행 시간표

| 구분       | 오전                                       | 오후                                       |
|------------|--------------------------------------------|--------------------------------------------|
| **교내 순환 (대덕캠퍼스 내)** | 08:20 (출발역) <br> 등교 | 8:30, 9:30, 10:30, 11:30, 13:30, 14:30, 15:30, 16:30, 17:30 |
| **캠퍼스 순환 (대덕캠퍼스 ↔ 보운캠퍼스)** | 8:10 (출발, 골프연습장) <br> → 8:50 (최차 보운캠퍼스) | 미운영 |

## 셔틀버스 운행 노선

### 교내 순환 (유성캠퍼스 내)

- **운행시간**: 08:30 ~ 17:30
- **운행노선(시간)**:  
  1. 경상학 국제문화회관 앞  
  2. 사회과학대학 입구 (한누리회관 뒤)  
  3. 서문 (공동실험실습관 앞)  
  4. 음악관 2호관 앞  
  5. 공동동물실험센터 (회차)  
  6. 예체능대학 앞  
  7. 도서관 앞 (대덕본부 앞 통로)  
  8. 공대1호관 앞  
  9. 공대2호관 뒤 → 동문주차장 → 수의과대학 앞 → 동문  
  10. 공대1호관 앞 → 공대2호관 뒤 → 도서관 앞 → 도서관 주차장 앞 → 예체능대학 앞 → 공동동물실험센터 → 음악관 2호관 앞 → 사회과학대학 입구(한누리회관 뒤)  
  11. 경상학 국제문화회관 앞 (종점)  

- **운행횟수(1일)**: 10회  
- **비고**:  
  - 오전(등교) 1회만 경상학 국제문화회관 하차(종점), 시간표 참조  
  - 학기 중 운영 (총 150일)

### 캠퍼스 순환 (대덕 ↔ 보운)

- **운행시간**:  
  - 08:10 (대덕 출발)  
  - 08:50 (보운 도착)

- **운행노선(시간)**:  
  1. 골프연습장 출발(08:10)  
  2. 종합도서관 서편(08:11)  
  3. 클러스터공학관 주차장(08:12)  
  4. 대덕회관 앞 버스정류장(08:13)  
  5. 기초과학관 정문(08:15)  
  6. 제2공학관 앞(08:18)  
  7. 다산아파트 건너편 계단식광장 → 창의도서관 → 골프연습장 도착 (08:50)

- **운행횟수(1일)**: 1회 (회차)
- **비고**: 학기 중 운영 (총 150일)

## 업데이트 내용 조회
- 학교 홈페이지 대학생활 > 학생생활서비스 > 학교셔틀버스 (https://plus.cnu.ac.kr/html/kr/sub05/sub05_050403.html) 참조
"""


def fetch_shuttle_bus_time_table_from_web(url: str = "https://plus.cnu.ac.kr/html/kr/sub05/sub05_050403.html", retry: int = 3) -> str:
    for attempt in range(retry):
        try:
            data = web_search.fetch_webpage(url, length_limit=-1)
            if "text_content" in data:
                data = data['text_content']
                spl = data.split("학년도 학교셔틀버스 운영 안내")
                data = spl[0].strip()[-5:-1] + "학년도 학교 셔틀버스 운영 안내" + spl[-1].split("페이지 관리자")[0]
                return data.strip()
        except requests.RequestException as e:
            print(f"웹 페이지 가져오기 실패: {e}. 재시도 중... ({attempt + 1}/{retry})")
    return "학교 홈페이지가 현재 접속되지 않아 셔틀버스 시간표를 가져오는 데 실패했습니다. 나중에 다시 시도해주세요."


if __name__ == '__main__':
    print("충남대학교 셔틀버스 시간표:")
    print(get_shuttle_general_time_table())
    print("\n웹에서 셔틀버스 시간표 가져오기:")
    print(fetch_shuttle_bus_time_table_from_web())
