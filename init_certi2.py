# 자격증과 분야 연결시키기 #

import requests
import xml.etree.ElementTree as ET
from pymongo import MongoClient

# mongDB 설정
client = MongoClient('localhost', 27017)
db = client.myCerti

# API 가져오기
serviceKey = 'WNfV82zfE63N9iKQTqNIzmKuqKWGnq3SX5d3gm0pyH7qsEnnyZhXThmB9%2Bb7CDqG5hqJXd9KoZDAjTCMT9gyWQ%3D%3D&'
url = 'http://openapi.q-net.or.kr/api/service/rest/InquiryListNationalQualifcationSVC/getList?serviceKey='+serviceKey
res = requests.get(url)

# xml파일 파싱하기
results = []
tree = ET.fromstring(res.text) # 문자열로 된 xml을 파싱

for item in tree.findall('./body/items/item'): # body/items/item 전체 가져오기
    result = {}
    for attr in item.findall('./'): # item 하위의 모든 태그 가져오기
        result[attr.tag] = attr.text
    results.append(result)

for result in results:
    certi = result['jmfldnm']
    type = result['qualgbcd']
    category = result['mdobligfldnm'] + result['obligfldnm']

    if type =='T':
        print('자격증 ' + certi)
        print('유형 ' + type)
        print('분야 ' + category)

        db.certificate.update_one({'certi' : certi},{'$set': {'type': type}})
        db.certificate.update_one({'certi': certi}, {'$set': {'category': category}})
