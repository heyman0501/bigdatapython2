import requests
from bs4 import BeautifulSoup

# 멜론 차트 주소
url = "https://www.melon.com/chart/index.htm"

# 일반 웹브라우저처럼 보이도록 User-Agent 설정
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/87.0.4280.66 Safari/537.36"
    )
}

# 1. GET 요청으로 HTML 가져오기
response = requests.get(url, headers=headers)

# 2. BeautifulSoup로 파싱
soup = BeautifulSoup(response.text, "html.parser")

# 3. 'lst50'과 'lst100' 클래스가 붙은 tr 태그에서 곡 정보 찾기
#   - 멜론은 TOP 50을 lst50, 51~100위를 lst100 태그로 구분하기도 함.
chart_rows = soup.select("tr.lst50, tr.lst100")

results = []
for row in chart_rows:
    # (1) 순위
    rank_tag = row.select_one("span.rank")
    rank = rank_tag.text.strip() if rank_tag else "정보 없음"
    
    # (2) 곡명
    title_tag = row.select_one("div.ellipsis.rank01 > span > a")
    title = title_tag.text.strip() if title_tag else "정보 없음"
    
    # (3) 가수
    artist_tag = row.select_one("div.ellipsis.rank02 > a")
    artist = artist_tag.text.strip() if artist_tag else "정보 없음"
    
    results.append((rank, title, artist))

# 4. 추출 결과 출력
for rank, title, artist in results:
    print(f"{rank}위 {artist} - {title}")