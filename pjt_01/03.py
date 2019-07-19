# 영화 감독정보를 활용하여 상세 정보를 수집
# 영화인 코드 , 영화인명 , 분야 , 필모리스트


import requests
from pprint import pprint
from datetime import datetime, timedelta
from decouple import config
import csv



# boxoffice.csv 파일 읽어서 movieCd 가져오기 & 저장
with open('movie.csv', 'r', newline = '', encoding = 'utf-8' ) as f:
    reader = csv.DictReader(f)

    for row in reader:
        movieCodeList.append(row['movieCd'])

# print(movieCodeList)



for movieCd in movieCodeList:
    key = config('API_KEY')

    base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
    api_url = f'{base_url}?key={key}&movieCd={movieCd}'

    response = requests.get(api_url)
    data = response.json()
    movie_prelist.append(data['movieInfoResult']['movieInfo'])

movie_list = []
for i in range(len(movie_prelist)):
    movie_list.append({})

for i in range(len(movie_prelist)):
        movie_list[i]['movieCd'] = movie_prelist[i]['movieCd']
        movie_list[i]['movieNm'] = movie_prelist[i]['movieNm']
        movie_list[i]['movieNmEn'] = movie_prelist[i]['movieNmEn']
        movie_list[i]['watchGradeNm'] = movie_prelist[i]['audits']
        movie_list[i]['openDt'] = movie_prelist[i]['openDt']
        movie_list[i]['showTm'] = movie_prelist[i]['showTm']
        movie_list[i]['genreNm'] = movie_prelist[i]['genres']
        movie_list[i]['directors'] = movie_prelist[i]['directors']

pprint(movie_list)

# data handling

with open('director.csv', 'w', newline='', encoding='utf-8') as f:
    # 저장할 필드의 이름을 미리 지정한다
    fieldnames = ('movieCd', 'movieNm', 'movieNmEn','watchGradeNm', 'openDt', 'showTm', 'genreNm', 'directors')
    writer = csv.DictWriter(f, fieldnames = fieldnames)

    writer.writeheader()

    # Dictionary를 순회하며 key값에 맞는 value를 한줄씩 작성한다.
    for item in movie_list:
        writer.writerow(item)
