from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


# 처음 시작할 때 호출
@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
