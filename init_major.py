import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from pymongo import MongoClient

# mongDB 설정
client = MongoClient('localhost', 27017)
db = client.myCerti


def geturl2(majorSeq):
    url = "http://www.career.go.kr/cnet/openapi/getOpenApi?apiKey=35b83c07ac567a49eda274a263faa378&svcType=api&svcCode=MAJOR_VIEW&contentType=json&gubun=univ_list&majorSeq="+majorSeq
    res = requests.get(url)
    datas = res.json()
    data1 = datas['dataSearch']['content'][0]['university']
    data2 = datas['dataSearch']['content'][0]['chartData']
    for major in data1:
        majorName = major['majorName']
        print(majorName)

    for cg in data2:
        category = cg['field']
        max = 0
        for et in category:
            maxtemp = et['data']
            if float(maxtemp) > max:
                max = float(maxtemp)
                majorCate = et['item']
        print(majorCate)


def getMajorSeq():
    for i in range(1, 8):
        url = "http://www.career.go.kr/cnet/openapi/getOpenApi?apiKey=35b83c07ac567a49eda274a263faa378&svcType=api&svcCode=MAJOR&contentType=json&gubun=univ_list&subject=10039"+str(i)
        res = requests.get(url)
        datas = res.json()
        data = datas['dataSearch']['content']
        for num in data:
            majorSeq = num['majorSeq']
            geturl2(majorSeq)
            break

getMajorSeq()