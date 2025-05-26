import urllib.request
import urllib.parse
import json
import re

def clean_html(raw_html):
    """HTML 태그 제거 함수"""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def search_naver_blog(query, display=10):
    client_id = "SwljxgBgdggGbgH3Zpqf"
    client_secret = "uhe_h6zAXK"
    encText = urllib.parse.quote(query)
    url = f"https://openapi.naver.com/v1/search/blog?query={encText}&display={display}"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(request)
        if response.getcode() == 200:
            response_body = response.read()
            data = json.loads(response_body.decode('utf-8'))

            results = []
            for item in data.get('items', []):
                results.append({
                    "제목": clean_html(item.get("title", "")),
                    "링크": item.get("link", ""),
                    "설명": clean_html(item.get("description", "")),
                    "블로거명": item.get("bloggername", ""),
                    "작성일자": item.get("postdate", "")
                })
            return results
        else:
            print("HTTP 오류 코드:", response.getcode())
            return []
    except Exception as e:
        print("요청 처리 중 오류 발생:", e)
        return []

# 검색 실행
print("🔍 네이버 블로그 맛집 검색 결과")
query = "경성대 맛집"
results = search_naver_blog(query, display=5)

# 결과 출력
for idx, item in enumerate(results, 1):
    print(f"\n[{idx}] {item['제목']}")
    print("📎 링크:", item['링크'])
    print("📝 설명:", item['설명'])
    print("👤 블로거명:", item['블로거명'])
    print("📅 작성일자:", item['작성일자'])
