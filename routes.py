from flask import Blueprint, request, jsonify, current_app
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
        return jsonify({"message": "User signed up successfully"}), 201
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
    data = request.get_json()
    user_id = data["user_id"]
    password = data["password"]
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = %s", [user_id])
    user = cur.fetchone()
    if user and bcrypt.check_password_hash(user[4], password):  # user[4]는 password
        access_token = create_access_token(identity=user_id)
        return jsonify(access_token=access_token), 200
    return jsonify({"error": "Invalid user_id or password"}), 401

# 라우트 초기화 함수
def init_routes(app, mysql):
    app.config['MYSQL_INSTANCE'] = mysql  # MySQL 객체를 Flask 설정에 저장
    app.register_blueprint(auth_bp, url_prefix="/auth")
