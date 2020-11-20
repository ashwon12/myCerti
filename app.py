from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.myCerti  # 'dbsparta'라는 이름의 db를 만듭니다.


# 처음 시작할 때 호출
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/listPage')
def listPage():
    major = request.args.get('major')
    return render_template('listPage.html', major=major)


@app.route('/detailPage')
def detailPage():
    certi = request.args.get('certi')
    return render_template('detailPage.html', certi=certi)


# 검색 결과를 보여준다.
@app.route('/result', methods=['POST'])
def result_post():
    keyword = request.form['major_give']

    search_result = list(db.certificate.find({'certi': {'$regex': '.*' + keyword + '.*'}}, {'_id': False}))
    results = []
    for result in search_result:
        results.append(result)

    return jsonify({'result': 'success', 'data': results})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
