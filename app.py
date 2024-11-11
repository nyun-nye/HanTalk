from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv
from flask_socketio import SocketIO, join_room, send

# 환경 변수 로드
load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app)    # socketio 객체 생성 && flask 연결

# MySQL 설정
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

mysql = MySQL(app)

CHAT_ROOMS = ["데이터통신", "알고리즘", "객체지향언어", "자료구조", "프로그래밍언어", "오픈소스"]
@app.route('/')
def home():
    return "Homepage"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 로그인 처리 로직 추가
        user_id = request.form['user_id']
        password = request.form['password']
        # 로그인 로직 (DB 확인, 세션 설정 등)
        return redirect(url_for('home'))  # 로그인 후 홈페이지로 리디렉션
    return render_template('login.html')

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        # 회원가입 처리 로직 추가
        name = request.form['name']
        student_id = request.form['student_id']
        user_id = request.form['user_id']
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        # 비밀번호 확인 로직
       if password != password_confirm:
    flash("Passwords do not match. Please try again.")
    return render_template('signUp.html')

        
        # 회원가입 로직 (DB에 저장)
        return redirect(url_for('login'))  # 가입 후 로그인 페이지로 리디렉션
    return render_template('signUp.html')

# 채팅방 목록 페이지
@app.route('/group_chat')
def group_chat():
    return render_template('groupChat.html', rooms=CHAT_ROOMS)

# 그룹 채팅방 렌더링
@app.route('/chat/<room>')
def chat_room(room):
    if room not in CHAT_ROOMS:  # 채팅방이 CHAT_ROOMS에 존재하는지 확인
        return "존재하지 않는 채팅방입니다.", 404   # 없으면 404 오류 리턴
    return render_template('chatInterface.html', room=room) # 존재하면 html 렌더링


# WebSocket : 클라이언트 연결
@socketio.on('join')    
def handle_join(data):  # 이벤트 처리 함수
    username = data['username'] # 사용자 이름 불러오기
    room = data['room'] # 채팅방 이름 불러오기
    join_room(room) # 사용자가 채팅방 참가
    
    # 채팅방 내 알림 메세지 전송
    send(f"{username}님이 {room} 그룹채팅방에 입장했습니다.", to=room) 

# WebSocket : 메세지 전송
@socketio.on('message') 
def handle_msg(data):   # 이벤트 처리 함수
    room = data['room'] # 채팅방 이름 불러오기
    msg = data['message']   # 메세지 내용 msg에 저장
    username = data['username'] # 사용자 이름 불러오기
    send(f"[{username}]: {msg}", to=room) # 채팅방 내 사용자들에게 메세지 전송

# 1:1 채팅방 선택 페이지
@app.route('/personalChat')
def personalChat():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # 로그인 안 된 사용자는 로그인 페이지로 리디렉션
    return render_template('personalChat.html')

# 채팅방 페이지
@app.route('/chatInterface/<int:user_id>')
def chatInterface(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))  # 로그인 안 된 사용자는 로그인 페이지로 리디렉션
    return render_template('chatInterface.html', username=session['username'], receiver_id=user_id)


# WebSocket 채팅 처리
# 방 입장
@socketio.on('join')
def on_join(data):
    username = session.get('username')
    room = f"room_{session['user_id']}_{data['room']}"
    join_room(room)
    send(f"{username}님이 채팅방에 참여했습니다.", room=room)

# 메시지 전송
@socketio.on('message')
def handle_message(data):
    room = f"room_{session['user_id']}_{data['receiver']}"
    send({
        'sender': session.get('username'),
        'message': data['message'],
        'image': data.get('image')
    }, room=room)

# 방 나가기
@socketio.on('leave')
def on_leave(data):
    username = session.get('username')
    room = f"room_{session['user_id']}_{data['room']}"
    leave_room(room)
    send(f"{username}님이 채팅방을 나갔습니다.", room=room)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
    socketio.run(app, debug=True)
