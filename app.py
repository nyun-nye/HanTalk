from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

app = Flask(__name__)

# MySQL 설정
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

mysql = MySQL(app)

@app.route('/')
def home():
    return "Homepage"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 로그인 처리 로직 추가
        username = request.form['username']
        password = request.form['password']
        # 로그인 로직 (DB 확인, 세션 설정 등)
        return redirect(url_for('home'))  # 로그인 후 홈페이지로 리디렉션
    return render_template('login.html')

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        # 회원가입 처리 로직 추가
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # 회원가입 로직 (DB에 저장)
        return redirect(url_for('login'))  # 가입 후 로그인 페이지로 리디렉션
    return render_template('signUp.html')

if __name__ == "__main__":
    app.run(debug=True)
