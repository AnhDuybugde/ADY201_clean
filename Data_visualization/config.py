import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=r"C:\Users\jloy5\ADY201\.env")

print("SERVER:", os.getenv("SERVER"))
print("DATABASE:", os.getenv("DATABASE"))
print("TRACK_TABLE:", os.getenv("TRACK_TABLE"))
print("SAVING_TABLE:", os.getenv("SAVING_TABLE"))
print("RAW_DATA:", os.getenv("RAW_DATA"))
print("NUMERIC_DATA:", os.getenv("NUMERIC_DATA"))
print("MODEL_DATA:", os.getenv("MODEL_DATA"))

SERVER = os.getenv("SERVER")
DATABASE = os.getenv("DATABASE")
TRACK_TABLE = os.getenv("TRACK_TABLE")
SAVING_TABLE = os.getenv("SAVING_TABLE")
RAW_DATA = os.getenv("RAW_DATA") 
NUMERIC_DATA = os.getenv("NUMERIC_DATA") 
MODEL_DATA = os.getenv("MODEL_DATA") 

if not all([SERVER, DATABASE, TRACK_TABLE, SAVING_TABLE, RAW_DATA, NUMERIC_DATA, MODEL_DATA]):
    raise ValueError("Thiếu cấu hình trong file .env. Vui lòng kiểm tra.")
