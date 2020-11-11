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
        i = 0;
        for first_key in first_a_tag:
            first_keys = first_key["onclick"]
            FldCds.append(first_keys[-5:-2])
            i = i + 1
    get_certificate(FldCds)


def get_certificate(FldCds):
    jmCDs = []
    for FldCd in FldCds:
        url = 'http://q-net.or.kr/crf005.do?id=crf00501s01&gSite=Q&gId=&div=1&obligFldCd=' + FldCd
        driver.get(url)
        req = driver.page_source
        soup = BeautifulSoup(req, 'html.parser')
        wrap = soup.select("body > ul > li")
        for certificates in wrap:
            certificate = certificates.select_one('a')
            if certificate is not None:
                title = certificate.text[3:]
                jmCDs.append(certificate["href"][21:25])
                # get_details(jmCDs)




get_FldCd()
