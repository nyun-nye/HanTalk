# config.py 파일
from dotenv import load_dotenv
import os

load_dotenv()  # .env 파일 로드

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DB = os.getenv("MYSQL_DB", "chat_service")
    MYSQL_UNIX_SOCKET = os.getenv("MYSQL_SOCKET", "/opt/homebrew/var/mysql/mysql.sock")    
