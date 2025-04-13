import requests
from bs4 import BeautifulSoup
import random
import time

url = 'https://www.genie.co.kr/chart/top200'
headers = {
    'User-Agent': 'Mozilla/5.0'
}

response = requests.get(url, headers=headers)

print("==========================")
print("| 1. 지니 차트 TOP 100곡 |")
print("| 2. 지니 차트 TOP 50곡  |")
print("| 3. 지니 차트 TOP 10곡  |")
print("| 4. 지니 차트 AI 추천곡 |")
print("==========================")

n = input("[원하시는 서비스 번호를 입력하세요]: ")

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    songs = soup.select('table.list-wrap tbody tr')

    song_list = []
    for song in songs:
        title_tag = song.select_one('a.title')
        artist_tag = song.select_one('a.artist')
        rank_tag = song.select_one('td.number')

        if title_tag and artist_tag and rank_tag:
            title = title_tag.text.strip()
            artist = artist_tag.text.strip()
            rank = rank_tag.text.strip().split()[0]
            song_list.append((rank, title, artist))

    if n == "1":
        print("\n<지니 차트 TOP 100곡>")
        for song in song_list[:100]:
            print(f'{song[0]}위 | 제목: {song[1]} | 아티스트: {song[2]}')

    elif n == "2":
        print("\n<지니 차트 TOP 50곡>")
        for song in song_list[:50]:
            print(f'{song[0]}위 | 제목: {song[1]} | 아티스트: {song[2]}')

    elif n == "3":
        print("\n<지니 차트 TOP 10곡>")
        for song in song_list[:10]:
            print(f'{song[0]}위 | 제목: {song[1]} | 아티스트: {song[2]}')

    elif n == "4":
        print("\n<지니 차트 AI 추천곡>")
        time.sleep(1)
        print("[두구두구두구~ 추천 중...]")
        random_song = random.choice(song_list)
        time.sleep(1)
        print(f'[추천 곡: {random_song[1]} | 아티스트: {random_song[2]}]')

    else:
        print(f"[<{n}>번에 해당하는 서비스는 없어요. 1~4번 중에 골라주세요.]")
else:
    print(f"[웹 페이지를 불러오는 데 실패했어요. 상태 코드: {response.status_code}]")
