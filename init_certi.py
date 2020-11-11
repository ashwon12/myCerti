import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from pymongo import MongoClient

# mongDB 설정
client = MongoClient('localhost', 27017)
db = client.myCerti

# selenium 설정
path = "C:/Users/rhdwn/Documents/chromedriver_win32/chromedriver"
driver = webdriver.Chrome(path)


def get_FldCd():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('http://q-net.or.kr/crf005.do?id=crf00501&gSite=Q&gId=', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    first_list = soup.select("#content > div.content > div:nth-child(4) > div");
    FldCds = []
    # first_key 가져오기
    for first_number in first_list:
        first_a_tag = first_number.select("a")
        for first_key in first_a_tag:
            first_keys = first_key["onclick"]
            FldCds.append(first_keys[-5:-2])

    return FldCds


def get_certificate(FldCd):
    url = 'http://q-net.or.kr/crf005.do?id=crf00501s01&gSite=Q&gId=&div=1&obligFldCd=' + FldCd
    driver.get(url)
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    wrap = soup.select("body > ul > li")

    for certificates in wrap:
        certificate = certificates.select_one('a')
        if certificate is not None:
            jmCD = certificate["href"][21:25]
            get_details(jmCD,certificate.text[2:])


# 세부정보 가져오기
def get_details(jmCD,title):
    url = 'http://q-net.or.kr/crf005.do?id=crf00503s02&gSite=Q&gId=&jmCd=' + jmCD + '&jmInfoDivCcd=B0&jmNm=%B9%E8%B0%FC%B1%E2%B4%C9%C0%E5'
    driver.get(url)
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    wrap = soup.select("body > div.tbl_normal.tdCenter.mb0 > table > tbody > tr")

    print(title)
    division=[]
    WT_Application=[]
    WT_Exam=[]
    WT_Pass=[]
    PT_Application=[]
    PT_Exam=[]
    PT_Pass=[]

    for details in wrap:
        null_check = details.select_one('td:nth-child(2)')
        if null_check is not None:
            division.append(details.select_one('td:nth-child(1)').text.strip())
            WT_Application.append(details.select_one('td:nth-child(2)').text.strip())
            WT_Exam.append(details.select_one('td:nth-child(3)').text.strip())
            WT_Pass.append(details.select_one('td:nth-child(4)').text.strip())
            PT_Application.append(details.select_one('td:nth-child(5)').text.strip())
            PT_Exam.append(details.select_one('td:nth-child(6)').text.strip())
            PT_Pass.append(details.select_one('td:nth-child(7)').text.strip())

    doc = {
        'certi': title,
        'division': division,
        'WT_Application': WT_Application,
        'WT_Exam': WT_Exam,
        'WT_Pass': WT_Pass,
        'PT_Application': PT_Application,
        'PT_Exam': PT_Exam,
        'PT_Pass': PT_Pass
    }

    db.certificate.insert_one(doc)
    print('완료!',division)


# db에 새로운 정보 저장
def insert_db():
    db.certificate.drop()
    FldCds = get_FldCd()
    print(FldCds)
    for FldCd in FldCds:
        get_certificate(FldCd)


# 실행
insert_db()
