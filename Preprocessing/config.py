import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=r"C:\Users\jloy5\ADY201\.env")

SERVER = os.getenv("SERVER")
DATABASE = os.getenv("DATABASE")
TRACK_TABLE = os.getenv("TRACK_TABLE")
SAVING_TABLE = os.getenv("SAVING_TABLE")

if not all([SERVER, DATABASE, TRACK_TABLE, SAVING_TABLE]):
    raise ValueError("Thiếu cấu hình trong file .env. Vui lòng kiểm tra.")
