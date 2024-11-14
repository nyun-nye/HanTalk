from flask import Blueprint, request, jsonify, current_app, session
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

bcrypt = Bcrypt()
auth_bp = Blueprint("auth", __name__)

# 회원가입 라우트
@auth_bp.route("/signUp", methods=["POST"])
def signUp():
    mysql = current_app.config['MYSQL_INSTANCE']  # MySQL 인스턴스 가져오기
    data = request.get_json()

    # 데이터 유효성 검사
    if not all(key in data for key in ("name", "student_id", "user_id", "password")):
        return jsonify({"error": "Missing required fields"}), 400

    name = data["name"]
    student_id = data["student_id"]
    user_id = data["user_id"]
    password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    
    cur = None
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users (name, student_id, user_id, password) VALUES (%s, %s, %s, %s)",
            (name, student_id, user_id, password)
        )
        mysql.connection.commit()
        return jsonify({"message": "회원가입에 성공하였습니다."}), 201
    except Exception as e:
        mysql.connection.rollback()
        current_app.logger.error(f"Error during signUp: {e}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500
    finally:
        if cur is not None:
            cur.close()

# 로그인 라우트
@auth_bp.route("/login", methods=["POST"])
def login():
    mysql = current_app.config['MYSQL_INSTANCE']
    data = request.get_json()  # 클라이언트로부터 JSON 데이터 수신
    user_id = data.get("user_id")
    password = data.get("password")
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = %s", [user_id])
    user = cur.fetchone()
    cur.close()
    
    if user and bcrypt.check_password_hash(user[4], password):  # user[4]는 password 필드
        session['user_id'] = user[3]  # 세션에 user_id 저장
        session['username'] = user[1]  # username 저장
        access_token = create_access_token(identity=user_id)
        return jsonify({"message": "로그인 성공", "access_token": access_token}), 200
    else:
        return jsonify({"error": "아이디 또는 비밀번호가 올바르지 않습니다."}), 401
@auth_bp.route('/check', methods=['GET'])
def check_login_status():
    if 'user_id' in session:
        return jsonify({'status': 'logged_in'}), 200
    return jsonify({'status': 'not_logged_in'}), 401
# 라우트 초기화 함수
def init_routes(app, mysql):
    app.config['MYSQL_INSTANCE'] = mysql  # MySQL 객체를 Flask 설정에 저장
    app.register_blueprint(auth_bp, url_prefix="/auth")
