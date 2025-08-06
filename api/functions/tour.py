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


dashboard_tour_description = """
투어개요

  - 신청대상 : 천안시 도시재생 사업에 관심 있는 시민 누구나, 천안시 선진지 답사를 희망하는 외부 센터

  - 신청방법 : 유선통화 신청 후 공문 접수

                         수신자:  국립공주대학교 산학협력단

                                       (경유) 천안시 도시재생지원센터

                        제목: 천안시 도시재생지원센터 도시재생투어 신청

                        본문 필수 기재내용: 일시, 신청투어내용(특강,현장투어(남산or역세권), 담당자 연락처

                        붙임문서: 현장투어계획서

  - 문의사항 : 기초사업팀(041-417-4063)

  - 투어비용 : 담당자와 협의

  - 투어대상지

     · 도시재생 선도사업&동남구청사 복합개발 도시재생사업

     · 천안역세권 도시재생 뉴딜사업

     · 남산지구 도시재생 뉴딜사업

     · 봉명지구 도시재생 뉴딜사업
"""  # TODO: 실제 대시보드 정보로 대체 필요


def get_tour_information() -> str:
    return dashboard_tour_description


if __name__ == '__main__':
    # Example usage
    print("투어 정보:")
    print(get_tour_information())
