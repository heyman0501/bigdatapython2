from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# 네이버 월요 웹툰 URL
url = 'https://comic.naver.com/webtoon?tab=mon'

# ChromeDriver 경로 설정
service = Service('chromedriver.exe')  # 필요에 따라 경로 수정
driver = webdriver.Chrome(service=service)

# 웹 페이지 열기
driver.get(url)
time.sleep(3)  # 페이지 로딩 대기

# 데이터 저장 리스트
webtoons_data = []

try:
    # 웹툰 목록 전체 ul 안의 li 요소들 (각 웹툰 항목)
    webtoon_items = driver.find_elements(By.CSS_SELECTOR, 'ul.img_list > li')

    print(f"총 {len(webtoon_items)}개의 월요 웹툰을 찾았습니다.")

    for item in webtoon_items:
        try:
            thumbnail_img = item.find_element(By.CSS_SELECTOR, 'div.thumb img')
            title_element = item.find_element(By.CSS_SELECTOR, 'dl dt a')
            artist_element = item.find_element(By.CSS_SELECTOR, 'dd.desc a')
            rating_element = item.find_element(By.CSS_SELECTOR, 'div.rating_type strong')

            thumbnail_url = thumbnail_img.get_attribute('src')
            title = title_element.text
            artist = artist_element.text
            rating = rating_element.text

            webtoons_data.append({
                '썸네일 이미지 주소': thumbnail_url,
                '타이틀': title,
                '작가명': artist,
                '평점': rating
            })

        except Exception as e:
            print(f"[오류] 웹툰 항목 처리 중 오류 발생: {e}")

finally:
    driver.quit()

# 출력 결과 확인
for webtoon in webtoons_data:
    print(webtoon)

# (선택) CSV 저장
# import pandas as pd
# df = pd.DataFrame(webtoons_data)
# df.to_csv('naver_monday_webtoons.csv', index=False, encoding='utf-8-sig')
# print("\nCSV 파일로 저장 완료: 'naver_monday_webtoons.csv'")
