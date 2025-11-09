import pyodbc
from config import SERVER, DATABASE, SAVING_TABLE

def get_connection():
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;Encrypt=no;"
    )
    return conn, conn.cursor()

def create_table_if_not_exists(cursor):
    query = f"""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{SAVING_TABLE}' AND xtype='U')
    CREATE TABLE {SAVING_TABLE} (
        product_id NVARCHAR(50) PRIMARY KEY,
        name NVARCHAR(255),
        brand NVARCHAR(100),
        os NVARCHAR(MAX),
        ram NVARCHAR(100),
        rom NVARCHAR(100),
        battery NVARCHAR(MAX),
        camera_primary NVARCHAR(MAX),
        camera_secondary NVARCHAR(MAX),
        chipset NVARCHAR(100),
        gpu NVARCHAR(100),
        display_size NVARCHAR(50),
        screen NVARCHAR(MAX),
        sensor NVARCHAR(MAX),
        watt NVARCHAR(MAX),
        nfc NVARCHAR(50),
        jack_support NVARCHAR(50),
        price FLOAT
    )
    """
    cursor.execute(query)
