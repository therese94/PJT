import requests
import time
from pprint import pprint
import csv
from decouple import config


BASE_URL = 'https://openapi.naver.com/v1/search/movie.json'
CLIENT_ID = config('CLIENT_ID')  # 헤더에 들어가야하는 필수정보
CLIENT_SECRET = config('CLIENT_SECRET')       # 헤더에 들어가야하는 필수정보

HEADER = {
    'X-Naver-Client-id': CLIENT_ID,
    'X-Naver-Client-Secret': CLIENT_SECRET,

}

# query = '자전차왕 엄복동'
result_list = []

with open('movie.csv', 'r', newline = '', encoding = 'utf-8' ) as f:
    reader = csv.DictReader(f)

    for row in reader:
        query = row['영화명(국문)']
        openDt = row['개봉연도'][:4]
        movieCd = row['영화 대표코드']

        API_URL = f'{BASE_URL}?query={query}'
        response = requests.get(API_URL, headers=HEADER).json()
            
        movie_naver_dict = {}
        items = response.get('items')
        for item in items:
            if openDt == item.get('pubDate') and float(item.get('userRating')) >= 2.00:
                movie_naver_dict = {'영화 대표코드': movieCd, '영화제목': item.get('title') , '하이퍼텍스트 link': item.get('link'), '썸네일 이미지 URL': item.get('image'), '유저 평점': item.get('userRating')}
                pprint(movie_naver_dict)
                result_list.append(movie_naver_dict)
                time.sleep(0.05)


        # pprint(result_list)


with open('movie_naver.csv', 'w', newline='', encoding='utf-8') as f:
    # 저장할 필드의 이름을 미리 지정한다
    fieldnames = ('영화제목', '영화 대표코드', '하이퍼텍스트 link', '썸네일 이미지 URL', '유저 평점')
    writer = csv.DictWriter(f, fieldnames = fieldnames)
    writer.writeheader()

    # # Dictionary를 순회하며 key값에 맞는 value를 한줄씩 작성한다.
    for i in result_list:
        writer.writerow(i)