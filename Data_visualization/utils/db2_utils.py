import pyodbc
import pandas as pd
from dotenv import load_dotenv
from config import SERVER, DATABASE

# Load biến môi trường từ file .env
load_dotenv()

def get_connection():
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;Encrypt=no;"
    )
    return conn, conn.cursor()

def create_table_if_not_exists(cursor, df, table_name):
    """
    Tạo bảng nếu chưa tồn tại, dựa trên cột và kiểu dữ liệu của DataFrame df
    """
    columns = []
    for col, dtype in zip(df.columns, df.dtypes):
        if pd.api.types.is_integer_dtype(dtype):
            sql_type = "INT"
        elif pd.api.types.is_float_dtype(dtype):
            sql_type = "FLOAT"
        else:
            sql_type = "NVARCHAR(255)"  # default cho string
        columns.append(f"{col} {sql_type}")

    columns_sql = ",\n".join(columns)
    query = f"""
    IF NOT EXISTS (
        SELECT * FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_NAME = '{table_name}'
    )
    CREATE TABLE {table_name} (
        {columns_sql}
    )
    """
    cursor.execute(query)