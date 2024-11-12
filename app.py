from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv
from flask_socketio import SocketIO, join_room, send, leave_room, emit
from routes import init_routes  # routes.py의 init_routes 함수 가져오기
from flask_jwt_extended import JWTManager

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
app.config['SESSION_COOKIE_SECURE'] = False  # HTTP에서도 세션 허용
app.config['SESSION_COOKIE_HTTPONLY'] = True  # 자바스크립트에서 세션 쿠키 접근 차단

# JWT 설정 추가
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

mysql = MySQL(app)
jwt = JWTManager(app)  # 여기서 JWTManager 초기화

# Blueprint 라우트 등록
init_routes(app, mysql)

CHAT_ROOMS = ["데이터통신", "알고리즘", "객체지향언어", "자료구조", "프로그래밍언어", "오픈소스"]

@app.route('/')
def home():
    return render_template('main.html')

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
            return "<script>alert('비밀번호가 일치하지 않습니다. 다시 입력해 주세요.'); window.history.back();</script>"
        
        # 회원가입 로직 (DB에 저장)
        return redirect(url_for('login'))  # 가입 후 로그인 페이지로 리디렉션
    return render_template('signUp.html')

# 채팅방 목록 페이지
@app.route('/group_chat')
def group_chat():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # 로그인 안 된 사용자는 로그인 페이지로 리디렉션
    return render_template('groupChat.html', rooms=CHAT_ROOMS)  # 로그인 된 경우 그룹 채팅 페이지 렌더링
# 그룹 채팅방 렌더링
@app.route('/chat/<room>')
def chat_room(room):
    if room not in CHAT_ROOMS:  # 채팅방이 CHAT_ROOMS에 존재하는지 확인
        return "존재하지 않는 채팅방입니다.", 404   # 없으면 404 오류 리턴
    return render_template('chatInterface.html', room=room) # 존재하면 html 렌더링

# WebSocket : 클라이언트 연결
@socketio.on('join')    
def handle_join(data):  # 이벤트 처리 함수
    username = session.get('username') # 사용자 이름 불러오기
    room = data.get('room') # 채팅방 이름 불러오기
    join_room(room) # 사용자가 채팅방 참가
    
# 방에 있는 모든 사용자에게 입장 메시지 브로드캐스트
    emit('receive_message', {
        'sender': '안내',
        'message': f'{username}님이 {room} 방에 입장하셨습니다.'
    }, to=room)

# WebSocket : 메세지 전송
@socketio.on('send_message')
def handle_send_message(data):
    room = data.get('room')
    message = data.get('message')
    sender = session.get('user_id')

    if not room or not message:
        print("[Server Log] Invalid room or message.")
        return

    print(f"[Server Log] Broadcasting message to room {room}: {message} by {sender}")

    # 메시지 브로드캐스트
    socketio.emit('receive_message', {
        'sender': sender,
        'message': message
    }, to=room)


# 1:1 채팅방 선택 페이지
@app.route('/personalChat')
def personalChat():
    if 'user_id' not in session or 'username' not in session:
        return redirect(url_for('login'))  # 로그인 안 된 사용자는 로그인 페이지로 리디렉션
    return render_template('personalChat.html')

# 채팅방 페이지
@app.route('/chatInterface/<room>')
def chatInterface(room):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    username = session.get('username', 'Guest')
    return render_template('chatInterface.html', username=username, room=room)

# 방 나가기
@socketio.on('leave')
def on_leave(data):
    username = session.get('username')
    room = data['room']
    leave_room(room)
    send(f"{username}님이 채팅방을 나갔습니다.", to=room)

# 메시지 전송 라우트
@app.route('/sendMessage', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401

    data = request.json
    sender_id = session['user_id']
    receiver_id = data.get('receiver_id')
    message = data.get('message')

    print(f"Sender ID: {sender_id}, Receiver ID: {receiver_id}, Message: {message}")
    # DB에 메시지 저장
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO messages (sender_id, receiver_id, message) VALUES (%s, %s, %s)",
            (sender_id, receiver_id, message)
        )
        mysql.connection.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        print(f"DB Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
