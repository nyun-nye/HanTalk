from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

bcrypt = Bcrypt()
auth_bp = Blueprint("auth", __name__)

# 회원가입 라우트
@auth_bp.route("/register", methods=["POST"])
def register(mysql):  # mysql을 매개변수로 받음
    data = request.get_json()
    username = data["username"]
    email = data["email"]
    password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    
    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        mysql.connection.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()

# 로그인 라우트
@auth_bp.route("/login", methods=["POST"])
def login(mysql):  # mysql을 매개변수로 받음
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", [email])
    user = cur.fetchone()
    if user and bcrypt.check_password_hash(user[3], password):  # user[3]은 password
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
    return jsonify({"error": "Invalid email or password"}), 401

# 라우트 초기화 함수
def init_routes(app, mysql):
    app.register_blueprint(auth_bp, url_prefix="/auth")
