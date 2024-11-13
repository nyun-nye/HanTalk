from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv
from flask_socketio import SocketIO, join_room, send, leave_room, emit
from routes import init_routes
from flask_jwt_extended import JWTManager
from prometheus_client import Gauge, start_http_server
import threading
import time

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
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

mysql = MySQL(app)
jwt = JWTManager(app)

# Blueprint 라우트 등록
init_routes(app, mysql)

# 전역 변수
CHAT_ROOMS = ["데이터통신", "알고리즘", "객체지향언어", "자료구조", "프로그래밍언어", "오픈소스"]
active_users_set = set()  # 현재 접속 중인 사용자 집합

# Prometheus 메트릭 정의
active_users = Gauge('active_users', 'Number of active users')
active_chat_rooms = Gauge('active_chat_rooms', 'Number of active chat rooms')

# 사용자와 채팅방 정보를 업데이트하는 함수
def update_metrics():
    while True:
        active_users.set(len(active_users_set))  # 현재 접속 중인 사용자 수
        active_chat_rooms.set(len(CHAT_ROOMS))  # 활성 채팅방 수
        time.sleep(5)  # 5초마다 업데이트

# Prometheus 메트릭 서버 시작
def start_prometheus():
    start_http_server(8080)  # Prometheus가 데이터를 가져갈 엔드포인트
    threading.Thread(target=update_metrics, daemon=True).start()

# Prometheus 서버 실행
start_prometheus()

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        # 로그인 로직 (DB 확인 후 세션 설정)
        session['user_id'] = user_id
        active_users_set.add(user_id)  # 사용자 추가
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    user_id = session.pop('user_id', None)
    if user_id:
        active_users_set.remove(user_id)  # 사용자 제거
    return redirect(url_for('login'))

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        name = request.form['name']
        student_id = request.form['student_id']
        user_id = request.form['user_id']
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        if password != password_confirm:
            return "<script>alert('비밀번호가 일치하지 않습니다. 다시 입력해 주세요.'); window.history.back();</script>"
        
        try:
            cursor = mysql.connection.cursor()
            query = """
                INSERT INTO users (name, student_id, user_id, password)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (name, student_id, user_id, password))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Error during signUp: {str(e)}")
            return "<script>alert('회원가입 중 오류가 발생했습니다. 다시 시도해 주세요.'); window.history.back();</script>"
    
    return render_template('signUp.html')

@app.route('/group_chat')
def group_chat():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, room_name FROM group_rooms")
    rooms = cur.fetchall()
    cur.close()

    return render_template('groupChat.html', rooms=rooms)

@app.route('/chat/<int:room>')
def chat_room(room):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM group_rooms WHERE id = %s", (room,))
    room_data = cur.fetchone()
    cur.close()

    if room_data is None:
        return "존재하지 않는 채팅방입니다.", 404

    return render_template('chatInterface.html', room=room_data[1])

@socketio.on('join')
def handle_join(data):
    user_id = session.get('user_id')
    room = data.get('room')
    join_room(room)

    emit('receive_message', {
        'sender': '안내',
        'message': f'{user_id}님이 {room} 방에 입장하셨습니다.'
    }, to=room)

@socketio.on('send_message')
def handle_send_message(data):
    room = data.get('room')
    message = data.get('message')
    sender = session.get('user_id')

    if not room or not message:
        print("[Server Log] Invalid room or message.")
        return

    socketio.emit('receive_message', {
        'sender': sender,
        'message': message
    }, to=room)

@app.route('/personalChat')
def personalChat():
    if 'user_id' not in session or 'username' not in session:
        return redirect(url_for('login'))
    return render_template('personalChat.html')

@app.route('/chatInterface/<room>')
def chatInterface(room):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    username = session.get('username', 'Guest')
    return render_template('chatInterface.html', username=username, room=room)

@socketio.on('leave')
def on_leave(data):
    username = session.get('username')
    room = data['room']
    leave_room(room)
    send(f"{username}님이 채팅방을 나갔습니다.", to=room)

@socketio.on('send_group_message')
def handle_group_message(data):
    room = data.get('room')
    message = data.get('message')
    sender = session.get('user_id')

    if not room or not message:
        print("[Server Log] Invalid room or message.")
        return

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO group_messages (room_id, sender_id, message) VALUES (%s, %s, %s)",
            (room, sender, message)
        )
        mysql.connection.commit()
        cur.close()

        socketio.emit('receive_group_message', {
            'sender': sender,
            'message': message
        }, to=room)
    except Exception as e:
        print(f"Error sending group message: {str(e)}")
        socketio.emit('error', {'error': str(e)}, to=room)

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
