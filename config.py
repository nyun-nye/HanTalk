import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# Flask 앱 구성
class Config:
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB = os.getenv('MYSQL_DB')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_COOKIE_SECURE = False  # HTTP에서도 세션 허용
    SESSION_COOKIE_HTTPONLY = True  # 자바스크립트에서 세션 쿠키 접근 차단
    MYSQL_UNIX_SOCKET = '/opt/homebrew/var/mysql/mysql.sock'
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')