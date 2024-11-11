from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv
from flask_socketio import SocketIO, join_room, send, leave_room

# 환경 변수 로드
load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app)   

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
        session['username'] = username  # 세션에 사용자명 저장
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

# 메인 페이지
@app.route('/main')
def main():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # 로그인 안 된 사용자는 로그인 페이지로 리디렉션
    return render_template('main.html', username=session['username'])

# 1:1 채팅방 선택 페이지
@app.route('/personalChat')
def personalChat():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # 로그인 안 된 사용자는 로그인 페이지로 리디렉션
    return render_template('personalChat.html')

# 채팅방 페이지
@app.route('/chatInterface')
def chatInterface(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))  # 로그인 안 된 사용자는 로그인 페이지로 리디렉션
    return render_template('ChatInterface.html', username=session['username'], receiver_id=user_id)


# WebSocket 채팅 처리
# 방 입장
@socketio.on('join')
def on_join(data):
    username = session.get('username')
    room = f"room_{data['room']}"
    join_room(room)
    send(f"{username}님이 채팅방에 참여했습니다.", room=room)

# 메시지 전송
@socketio.on('message')
def handle_message(data):
    room = f"room_{data['receiver']}"
    send({
        'sender': session.get('username'),
        'message': data['message'],
        'image': data.get('image')
    }, room=room)

# 방 나가기
@socketio.on('leave')
def on_leave(data):
    username = session.get('username')
    room = f"room_{data['room']}"
    leave_room(room)
    send(f"{username}님이 채팅방을 나갔습니다.", room=room)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
    socketio.run(app, debug=True)
