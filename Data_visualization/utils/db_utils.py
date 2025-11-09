# File: utils/db_utils.py

import pyodbc
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from config import SAVING_TABLE, SERVER, DATABASE
import os
from pathlib import Path

# --- Load .env chuẩn (nếu cần chạy file này trực tiếp) ---
dotenv_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=dotenv_path)

print("DEBUG:", os.getcwd())
print("SERVER:", SERVER)
print("DATABASE:", DATABASE)
print("SAVING_TABLE:", SAVING_TABLE)

def load_data(table_name):
    """
    Kết nối SQL Server và trả về DataFrame từ table 'Phones_Saving'.
    Có thể chạy trực tiếp bằng Python để test.
    """
    if not SERVER or not DATABASE:
        raise ValueError("Cần thiết lập SERVER và DATABASE trong file .env")

    try:
        conn = pyodbc.connect(
            f"DRIVER={{SQL Server}};"
            f"SERVER={SERVER};"
            f"DATABASE={DATABASE};"
            f"Trusted_Connection=yes;"
        )
    except Exception as e:
        raise ConnectionError(f"Không thể kết nối SQL Server: {e}")

    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

# --- Wrapper cho Streamlit ---
@st.cache_data
def get_data():
    """
    Dùng khi gọi từ Streamlit để cache dữ liệu.
    """
    return load_data(table_name = SAVING_TABLE)
