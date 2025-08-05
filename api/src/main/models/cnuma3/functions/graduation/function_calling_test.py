import requests
from bs4 import BeautifulSoup

def extract_info(html_content):
    """
    HTML 코드에서 게시글 정보를 추출하여 딕셔너리 리스트로 반환
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    posts = []
    events = []

    # b-title-box 클래스를 가진 div 요소들을 찾음
    title_boxes = soup.find_all('div', class_='b-title-box')
    calen_boxes = soup.find_all('div', class_='calen_box')
    if title_boxes:
        for box in title_boxes:
            post_info = {}

            # 제목과 링크 추출
            title_link = box.find('a')
            if title_link:
                post_info['title'] = title_link.get_text(strip=True)
                post_info['href'] = title_link.get('href', '')

            # 날짜 추출 (b-date 클래스를 가진 span 요소)
            date_span = box.find('span', class_='b-date')
            if date_span:
                post_info['date'] = date_span.get_text(strip=True)

            # 필수 정보가 모두 있는 경우에만 추가
            if 'title' in post_info and 'href' in post_info and 'date' in post_info:
                posts.append(post_info)
            
        return posts
    if calen_boxes:
        for calen_box in calen_boxes:
            list_items = calen_box.select('div.fr_list ul li') 
            for item in list_items:
                event_info = {}

                date_strong = item.find('strong') 
                if date_strong:
                    event_info['date'] = date_strong.get_text(strip=True)
                
                description_span = item.find('span', class_='list') 
                if description_span:
                    event_info['description'] = description_span.get_text(strip=True)

                if 'date' in event_info and 'description' in event_info:
                    events.append(event_info)
        return events

def extract_calendar_events_by_calenbox(html_content):
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    events = []

    calen_boxes = soup.find_all('div', class_='calen_box')

    for calen_box in calen_boxes:

        list_items = calen_box.select('div.fr_list ul li') 

        for item in list_items:
            event_info = {}

            date_strong = item.find('strong') 
            if date_strong:
                event_info['date'] = date_strong.get_text(strip=True)
            
            description_span = item.find('span', class_='list') 
            if description_span:
                event_info['description'] = description_span.get_text(strip=True)

            if 'date' in event_info and 'description' in event_info:
                events.append(event_info)
            
    return events
def get_ai_notice(url: str):
    data = (requests.get(url).text
            .replace("\n", "")
            .replace("  ", "")
            .replace("\r", "")
            .replace("\t", ""))
    return extract_info(data)

url_dict = {
    "graudate_data" : "https://plus.cnu.ac.kr/html/kr/sub05/sub05_051202.html", 
    # "ai_notice" : "https://ai.cnu.ac.kr/ai/board/notice.do",
    # "cse_notice" : "https://computer.cnu.ac.kr/computer/notice/bachelor.do",
    # "eng_notice" : "https://eng.cnu.ac.kr/eng/information/notice.do",
    "cnu_notice" : "https://plus.cnu.ac.kr/_prog/_board/?code=sub07_0701&site_dvs_cd=kr&menu_dvs_cd=0701",
    # 인코딩 다시 "calendar" : "https://plus.cnu.ac.kr/_prog/academic_calendar/?site_dvs_cd=kr&menu_dvs_cd=05020101",
    "food" : "https://mobileadmin.cnu.ac.kr/food/index.jsp",
    "bus" : "https://plus.cnu.ac.kr/html/kr/sub05/sub05_050403.html"
}

result = get_ai_notice(url_dict["graudate_data"])


print(result)