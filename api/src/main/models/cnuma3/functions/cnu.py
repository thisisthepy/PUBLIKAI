"""
충남대학교 재학생을 위한 전용 Functions
Chungnam National University specific functions for students
"""

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


class CNUWebAPI:
    """충남대학교 웹사이트 API 클래스"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # 충남대 주요 사이트 URL
        self.plus_url = "https://plus.cnu.ac.kr"
        self.ai_dept_url = "https://ai.cnu.ac.kr"
        
        # 주요 페이지 URL 매핑
        self.page_urls = {
            "academic_calendar_undergrad": "/_prog/academic_calendar/?site_dvs_cd=kr&menu_dvs_cd=05020101",
            "academic_calendar_grad": "/_prog/academic_calendar/?site_dvs_cd=kr&menu_dvs_cd=05020102", 
            "shuttle_bus": "/html/kr/sub05/sub05_050403.html",
            "graduation_requirements": "/html/kr/sub02/",  # 수정된 URL
            "notices": "/html/kr/sub04/sub04_040101.html",  # 수정된 URL
            "ai_notices": "/bbs/board.php?bo_table=notice"
        }

    def fetch_page_content(self, url: str) -> Dict[str, Any]:
        """웹페이지 내용을 가져오고 파싱"""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            result = {
                "url": url,
                "status_code": response.status_code,
                "title": "",
                "content": "",
                "raw_html": response.text
            }
            
            # BeautifulSoup로 파싱
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 제목 추출
                title_tag = soup.find('title')
                if title_tag:
                    result["title"] = title_tag.get_text(strip=True)
                
                # 본문 내용 추출 (스크립트, 스타일 제거)
                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.decompose()
                
                # 텍스트 내용 정리
                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                result["content"] = ' '.join(chunk for chunk in chunks if chunk)
                
            except ImportError:
                result["content"] = "BeautifulSoup4가 필요합니다. pip install beautifulsoup4"
            
            return result
            
        except Exception as e:
            return {"error": f"페이지 가져오기 실패: {str(e)}"}


# 전역 CNU API 인스턴스
cnu_api = CNUWebAPI()


def get_cnu_notices(source: str = "대학", max_results: int = 10) -> str:
    """
    충남대학교 공지사항을 조회합니다.
    
    Args:
        source: 공지사항 소스 (대학, 인공지능학과)
        max_results: 최대 결과 수
    
    Returns:
        공지사항 목록 문자열
    """
    try:
        if source == "인공지능학과":
            base_url = cnu_api.ai_dept_url
            notice_path = cnu_api.page_urls["ai_notices"]
        else:
            base_url = cnu_api.plus_url  
            notice_path = cnu_api.page_urls["notices"]
        
        url = base_url + notice_path
        result = cnu_api.fetch_page_content(url)
        
        if "error" in result:
            return f"공지사항 조회 중 오류 발생: {result['error']}"
        
        # 공지사항 파싱
        notices = []
        notices.append(f"📢 충남대학교 {source} 공지사항")
        notices.append("=" * 50)
        
        content = result["content"]
        
        # 공지사항 패턴 검색 (일반적인 게시판 형태)
        notice_patterns = [
            r"(\d{4}[-./]\d{1,2}[-./]\d{1,2}).*?([^\n]{10,100})",
            r"([^\n]{10,100}).*?(\d{4}[-./]\d{1,2}[-./]\d{1,2})",
        ]
        
        found_notices = []
        for pattern in notice_patterns:
            matches = re.findall(pattern, content)
            if matches:
                found_notices.extend(matches[:max_results])
                break
        
        if found_notices:
            for i, (date_or_title, title_or_date) in enumerate(found_notices[:max_results], 1):
                # 날짜와 제목 구분
                if re.match(r"\d{4}[-./]\d{1,2}[-./]\d{1,2}", date_or_title):
                    date, title = date_or_title, title_or_date
                else:
                    title, date = date_or_title, title_or_date
                
                notices.append(f"{i}. {title.strip()}")
                notices.append(f"   📅 {date.strip()}")
                notices.append("")
        else:
            # 기본 안내 메시지
            notices.extend([
                "🔍 최신 공지사항을 확인하려면 다음 사이트를 방문하세요:",
                "",
                f"🌐 {source} 공지사항: {url}",
                "",
                "주요 확인사항:",
                "• 수강신청/정정 관련 공지",
                "• 학사일정 변경 안내", 
                "• 장학금 신청 안내",
                "• 졸업 관련 공지",
                "• 각종 행사 및 프로그램 안내"
            ])
        
        return "\n".join(notices)
        
    except Exception as e:
        return f"공지사항 조회 중 오류 발생: {str(e)}"



def get_cafeteria_menu(date: str = "today", cafeteria: str = "학생회관") -> str:
    """
    교내 식당 식단을 조회합니다.
    
    Args:
        date: 조회할 날짜 (today, tomorrow, YYYY-MM-DD)
        cafeteria: 식당명 (학생회관, 생활관, 교직원식당)
    
    Returns:
        식단 정보 문자열
    """
    try:
        # 날짜 처리
        if date == "today":
            target_date = datetime.now()
        elif date == "tomorrow":
            target_date = datetime.now() + timedelta(days=1)
        else:
            try:
                target_date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                return "날짜 형식이 올바르지 않습니다. YYYY-MM-DD 형식을 사용하세요."
        
        # 주말 체크
        weekday = target_date.weekday()
        if weekday >= 5:  # 토요일(5), 일요일(6)
            return f"📅 {target_date.strftime('%Y-%m-%d')} ({['월','화','수','목','금','토','일'][weekday]}요일)\n주말에는 일부 식당만 운영됩니다. 운영시간을 확인해주세요."
        
        menu_info = []
        menu_info.append(f"🍽️ {cafeteria} 식단 정보")
        menu_info.append(f"📅 {target_date.strftime('%Y-%m-%d')} ({['월','화','수','목','금','토','일'][weekday]}요일)")
        menu_info.append("=" * 50)
        
        # CNUBot 스타일의 식단 정보 (실제로는 웹크롤링이나 API 연동 필요)
        # 여기서는 기본 템플릿 제공
        if cafeteria == "학생회관":
            menu_info.extend([
                "🍛 중식 (11:30 - 14:00):",
                "• A코너: 오늘의 한식 정식",
                "• B코너: 돈까스, 치킨까스",
                "• C코너: 볶음밥, 짜장면",
                "• 샐러드바: 신선한 채소",
                "",
                "🍜 석식 (17:00 - 19:00):",
                "• A코너: 저녁 한식 정식", 
                "• B코너: 치킨, 피자",
                "• C코너: 우동, 김치찌개",
                "",
                "💰 가격: 4,000원 ~ 6,000원",
                "",
                "⚠️  정확한 식단은 학생회관 게시판이나 충남대 앱을 확인하세요."
            ])
        elif cafeteria == "생활관":
            menu_info.extend([
                "🏠 생활관 식단:",
                "",
                "🍛 중식 (11:30 - 13:30):",
                "• 오늘의 정식 메뉴",
                "• 국, 반찬 4-5가지",
                "",
                "🍜 석식 (17:30 - 19:30):",
                "• 저녁 정식 메뉴",
                "• 국, 반찬 4-5가지",
                "",
                "💰 가격: 생활관생 할인 적용",
                "",
                "⚠️  생활관생 전용 식당입니다."
            ])
        else:
            menu_info.extend([
                "🍽️ 교직원식당:",
                "",
                "🍛 중식 (11:30 - 14:00):",
                "• 오늘의 특선 메뉴",
                "• 프리미엄 정식",
                "",
                "💰 가격: 6,000원 ~ 8,000원",
                "",
                "ℹ️  교직원 및 방문객 이용 가능"
            ])
        
        return "\n".join(menu_info)
        
    except Exception as e:
        return f"식단 조회 중 오류 발생: {str(e)}"


def search_cnu_site(query: str, site: str = "plus", max_results: int = 5) -> str:
    """
    충남대학교 사이트에서 검색합니다.
    
    Args:
        query: 검색 쿼리
        site: 검색할 사이트 (plus, ai)
        max_results: 최대 결과 수
    
    Returns:
        검색 결과 문자열
    """
    try:
        if site == "ai":
            site_url = "ai.cnu.ac.kr"
            site_name = "인공지능학과"
        else:
            site_url = "plus.cnu.ac.kr"
            site_name = "충남대학교"

        # 사이트 내 검색 (site: 연산자 활용)
        search_query = f"site:{site_url} {query}"
        
        result = web_search.search_web(search_query, max_results)
        
        # 결과 포맷팅
        search_info = []
        search_info.append(f"🔍 {site_name} 사이트 검색 결과")
        search_info.append(f"검색어: {query}")
        search_info.append("=" * 50)
        search_info.append("")
        search_info.append(result)
        
        return "\n".join(search_info)
        
    except Exception as e:
        return f"사이트 검색 중 오류 발생: {str(e)}"


# 테스트 및 예시
if __name__ == '__main__':
    print("충남대학교 Functions 테스트")
    print("=" * 50)
    
    # 각 함수 테스트
    functions_to_test = [
        ("공지사항 조회", lambda: get_cnu_notices("대학", 5)),
        ("식단 조회", lambda: get_cafeteria_menu("today", "학생회관")),
        ("사이트 검색", lambda: search_cnu_site("인공지능학과 교과과정", "plus", 3))
    ]
    
    for name, func in functions_to_test:
        print(f"\n📋 {name} 테스트:")
        print("-" * 30)
        try:
            result = func()
            print(result[:500] + "..." if len(result) > 500 else result)
        except Exception as e:
            print(f"오류: {e}")
        print()
