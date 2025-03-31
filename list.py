import random

# 노래 목록
songs = ["노래1", "노래2", "노래3", "노래4"]
print("현재 노래 목록:", songs)

# 리스트의 각 요소 출력
for i, song in enumerate(songs):
    print(f"{i+1}번째 노래: {song}")

# 노래 추천
print("노래를 추천해드릴게요!")
recommended_song = random.choice(songs)
print(f"추천하는 곡은 '{recommended_song}' 입니다!")

# 개별 변수로 노래 저장
song_a, song_b, song_c, song_d = songs
print(f"개별 변수로 저장된 노래들: {song_a}, {song_b}, {song_c}, {song_d}")