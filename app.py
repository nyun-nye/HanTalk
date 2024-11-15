from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv
from flask_socketio import SocketIO, join_room, send, leave_room, emit
from routes import init_routes  # routes.py의 init_routes 함수 가져오기
from flask_jwt_extended import JWTManager
from prometheus_client import Gauge, start_http_server, Counter, Histogram, generate_latest, REGISTRY
import threading
import time
from prometheus_flask_exporter import PrometheusMetrics

# 환경 변수 로드
load_dotenv()

app = Flask(__name__)

# Prometheus 메트릭 설정
metrics = PrometheusMetrics(app)

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

# 메시지 크기 카운터 정의
message_size_counter = Counter('message_size_bytes', 'Total message size in bytes')

# 메시지 처리 시간 히스토그램
message_processing_time = Histogram('message_processing_time_seconds', 'Time spent processing a message')

# Blueprint 라우트 등록
init_routes(app, mysql)

# 실시간 접속자 수 추적
connected_users = set()  # 접속 중인 사용자 리스트

# Prometheus 메트릭 정의
active_users = Gauge('active_users', 'Number of active users')

# Prometheus 메트릭 서버 시작 (별도의 스레드에서 실행)
def update_metrics():
    while True:
        active_users.set(len(connected_users))  # 접속 중인 사용자 수 갱신
        time.sleep(5)  # 5초마다 업데이트

# Prometheus 메트릭 서버를 별도의 스레드에서 실행
def start_prometheus():
    start_http_server(8080)  # Prometheus가 데이터를 가져갈 엔드포인트 (8080 포트)
    update_metrics()

# Prometheus 서버를 별도의 스레드에서 실행
threading.Thread(target=start_prometheus, daemon=True).start()

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/view_dashboard')
def view_dashboard():
    return redirect("http://localhost:3000/d/fe3ts8ilf2vpcc/chat-service?from=now-1h&to=now&timezone=browser&showCategory=Legend")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 로그인 처리 로직 추가
        user_id = request.form['user_id']
        password = request.form['password']
        # 로그인 로직 (DB 확인, 세션 설정 등)
        session['user_id'] = user_id
        connected_users.add(user_id)  # 접속자 리스트에 추가
        return redirect(url_for('home'))  # 로그인 후 홈페이지로 리디렉션
    return render_template('login.html')

@app.route('/logout')
def logout():
    user_id = session.get('user_id')
    if user_id in connected_users:
        connected_users.remove(user_id)  # 접속자 리스트에서 제거
    session.pop('user_id', None)  # 세션에서 사용자 정보 제거
    return redirect(url_for('home'))

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

    # 데이터베이스에서 그룹 채팅방 목록 가져오기
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, room_name FROM group_rooms")
    rooms = cur.fetchall()
    cur.close()

    return render_template('groupChat.html', rooms=rooms)

# 그룹 채팅방 렌더링
@app.route('/chat/<int:room>')
def chat_room(room):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM group_rooms WHERE id = %s", (room,))
    room_data = cur.fetchone()
    cur.close()

    if room_data is None:  # 방이 존재하지 않으면 404 반환
        return "존재하지 않는 채팅방입니다.", 404

    return render_template('chatInterface.html', room=room_data[1])  # 방 이름을 넘겨줌

# WebSocket : 클라이언트 연결
@socketio.on('join')    
def handle_join(data):  # 이벤트 처리 함수
    user_id = session.get('user_id') # 사용자 이름 불러오기
    room = data.get('room') # 채팅방 이름 불러오기
    join_room(room) # 사용자가 채팅방 참가
    
    # 방에 있는 모든 사용자에게 입장 메시지 브로드캐스트
    emit('receive_message', {
        'sender': '안내',
        'message': f'{user_id}님이 {room} 방에 입장하셨습니다.'}, to=room)

# WebSocket : 메세지 전송
@socketio.on('send_message')
def handle_send_message(data):
    room = data.get('room')
    message = data.get('message')
    sender = session.get('user_id')

    if not room or not message:
        print("[Server Log] Invalid room or message.")
        return

    # 메시지 크기 측정 (바이트 단위)
    message_size = len(message.encode('utf-8'))  # UTF-8로 인코딩된 메시지 크기(바이트)
    
    # Prometheus 메트릭에 메시지 크기 추가
    message_size_counter.inc(message_size)
    
    print(f"[Server Log] Received message to room {room}: {message} by {sender}")

    # 메시지 처리 시간 기록 (시간 측정)
    with message_processing_time.time():
        # Broadcast the message
        socketio.emit('receive_message', {
            'sender': sender,
            'message': message
        }, to=room)

# 나머지 라우트 코드 및 WebSocket 관련 코드는 그대로 유지

# Prometheus 메트릭을 노출하는 라우트
@app.route('/metrics')
def metrics():
    # Prometheus 메트릭을 출력하는 라우트
    return generate_latest(REGISTRY)

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
