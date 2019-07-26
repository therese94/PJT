## boxoffice.csv용 - 영화대표코드, 영화명, 해당일 누적관객수 (movieCd, movieNm, audiAcc)

import requests
from pprint import pprint
from datetime import datetime, timedelta
from decouple import config
import csv

boxoffice_list = []
r = []
for i in range (500):
    boxoffice_list.append({})

for weekNum in range(50):

    targetDt = datetime(2019, 7, 13) - timedelta(weeks=weekNum)
    targetDt = targetDt.strftime('%Y%m%d')  # yyyymmdd

    key = config('API_KEY')

    weekGb = '0'

    base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json'
    api_url = f'{base_url}?key={key}&targetDt={targetDt}&weekGb={weekGb}'

    response = requests.get(api_url)
    data = response.json()



    boxoffice_prelist = data['boxOfficeResult']['weeklyBoxOfficeList']

    for i in range (10):
        dict_movie = { 'movieCd' : boxoffice_prelist[i]['movieCd'], 'movieNm' : boxoffice_prelist[i]['movieNm'], 'audiAcc' : boxoffice_prelist[i]['audiAcc']}

        for k in r:
            if k['movieCd'] == dict_movie['movieCd']:
                r.remove(k)

        r.append(dict_movie)
    

# pprint(r)



# withoutDup = []
# for k in boxoffice_list:
#     if k['movieCd'] not in withoutDup[i+1:]:
#         withoutDup.append(k)
#         print(k)
# for i in range(len(boxoffice_list)):
#     if boxoffice_list[i]['movieCd'] not in boxoffice_list[i+1:]['movieCd']:
#         withoutDup.append(boxoffice_list[i])
#     # print(boxoffice_list[i]['movieCd'])


# 
# boxoffice.csv로 저장하기 

with open('boxoffice.csv', 'w', newline='', encoding='utf-8') as f:
    # 저장할 필드의 이름을 미리 지정한다
    fieldnames = ('movieCd', 'movieNm', 'audiAcc')
    writer = csv.DictWriter(f, fieldnames = fieldnames)

    writer.writeheader()

    # Dictionary를 순회하며 key값에 맞는 value를 한줄씩 작성한다.
    for item in r:
        writer.writerow(item)






#############################################################
