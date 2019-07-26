

# Project 2 파이썬을 활용한 데이터 수집2

### Movie Thumbnail Poster Web Crawling Using Naver Open API 

(NAVER OPEN API를 활용한  영화 썸네일 이미지 크롤링)



** 준비사항

3.7 이상 버전 python / 

0. 요약

> movie.csv준비 > movie_naver.py 작성 > movie_naver.csv 생성 > movie_image.py작성 > 썸네일 이미지 저장

1. movie_naver.py 작성

> project1 의 movie.csv파일을 준비

```python
# 필요한 모듈을 임포트
import requests
import time
from pprint import pprint
import csv
```



```python
# 필요한 정보를 변수에 저장
BASE_URL = 'https://openapi.naver.com/v1/search/movie.json'
CLIENT_ID = config('CLIENT_ID')  # 헤더에 들어가야하는 필수정보
CLIENT_SECRET = config('CLIENT_SECRET')       # 헤더에 들어가야하는 필수정보

HEADER = {
    'X-Naver-Client-id': CLIENT_ID,
    'X-Naver-Client-Secret': CLIENT_SECRET,

}
```

중요한 정보는 decouple 모듈을 사용해 config함 --> .env파일에 저장

```python

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
```

