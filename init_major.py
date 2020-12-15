import requests
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
    majorName=[]

    for major in data1:
        # 전공이름 가져오기
        majorName.append(major['majorName'])


    check=[]
    if data2[0]:
        for cg in data2:
            # 분야 가져오기
            category = cg['field']
            max = 0
            for et in category:
                maxtemp = et['data']
                if float(maxtemp) > max:
                    max = float(maxtemp)
                    majorCate = et['item']
            print(majorSeq + "의 전공은 " + majorName[0])

            start = 0
            end = 2
            while True:
                if start > len(majorCate):
                    break
                else:
                    print(majorCate[start:end])
                    db.certificate.update_many(
                        {'category': {'$regex': '.*' + majorCate[start:end] + '.*'}},
                        {
                            '$push': {'major': {'$each':majorName}}
                        })
                    start = end + 1
                    end = end + 3


def getMajorSeq():
    for i in range(1, 8):
        url = "http://www.career.go.kr/cnet/openapi/getOpenApi?apiKey=35b83c07ac567a49eda274a263faa378&svcType=api&svcCode=MAJOR&contentType=json&gubun=univ_list&subject=10039"+str(i)
        res = requests.get(url)
        datas = res.json()
        data = datas['dataSearch']['content']
        for num in data:
            majorSeq = num['majorSeq']
            print(majorSeq)
            geturl2(majorSeq)


getMajorSeq()