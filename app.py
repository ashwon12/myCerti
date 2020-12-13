from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import requests


app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.myCerti


# 홈 화면, 첫번째 화면
@app.route('/')
def home():
    return render_template('home.html')


# 두번째 화면
@app.route('/listPage')
def list_page():
    major = request.args.get('major')
    return render_template('listPage.html', major=major)


# 세번째 화면
@app.route('/detailPage')
def detail_page():
    certi = request.args.get('certi')
    return render_template('detailPage.html', certi=certi)


# DB에서 검색 결과를 가져오는 API
@app.route('/result', methods=['POST'])
def result_post():
    keyword = request.form['major_give']

    search_result = list(db.certificate.find({'certi': {'$regex': '.*' + keyword + '.*'}}, {'_id': False}))
    results = []
    for result in search_result:
        results.append(result)
    return jsonify({'result': 'success', 'data': results})


# 네이버 블로그 리뷰를 가져와주는 API
@app.route('/reviewData', methods=['POST'])
def reviewData():
    detail_certis = request.form['certi_give']
    print(detail_certis)
    headers = {
        'X-Naver-Client-Id': '1cZPXGnFs7VpBH7STTrV',
        'X-Naver-Client-Secret': 'O6T5Wih5G5',
    }
    params = {
        'query': detail_certis + ' 후기',
        'display': '6',
        'start': '1',
        'sort': 'sim',
    }

    response1 = requests.get('https://openapi.naver.com/v1/search/blog.json', headers=headers, params=params)
    response2 = requests.get('https://openapi.naver.com/v1/search/cafearticle.json',headers=headers, params=params)
    blog_review = response1.json()
    cafe_review = response2.json()
    return jsonify({'result': 'success', 'blogData' : blog_review,'cafeData':cafe_review})


# DB에서 시험 일정을 가져와주는 API
@app.route('/detailCerti', methods=['POST'])
def dbData():
    detail_certi = request.form['certi_give']
    data = db.certificate.find_one({'certi': detail_certi}, {'_id': False})

    return jsonify({'result': 'success', 'dbData': data})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
