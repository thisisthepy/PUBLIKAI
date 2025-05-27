import requests
from bs4 import BeautifulSoup


def search_website(query, site_url=None):
    """웹사이트에서 검색"""
    if site_url:
        # 특정 사이트 내 검색
        search_url = f"https://www.google.com/search?q=site:{site_url} {query}"
    else:
        # 일반 웹 검색
        search_url = f"https://www.google.com/search?q={query}"

    # 검색 결과 파싱 후 반환
    return search_results


def fetch_webpage(url):
    """웹페이지 내용 가져오기"""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()

# 사용자: "파이썬 공식 문서에서 리스트 사용법 찾아줘"
# 모델: search_website("리스트 사용법", "docs.python.org") 호출
