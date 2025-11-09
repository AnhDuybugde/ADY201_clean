# src/storage.py
from config import get_connection, TRACK_TABLE

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{TRACK_TABLE}' AND xtype='U')
    CREATE TABLE {TRACK_TABLE} (
        product_id NVARCHAR(50),
        name NVARCHAR(255),
        manufacturer NVARCHAR(100),
        price FLOAT,
        special_price FLOAT,
        battery NVARCHAR(255),
        camera_primary NVARCHAR(MAX),
        camera_secondary NVARCHAR(MAX),
        chipset NVARCHAR(255),
        display_size NVARCHAR(100),
        gpu NVARCHAR(255),
        memory_internal NVARCHAR(255),
        mobile_display_features NVARCHAR(MAX),
        mobile_type_of_display NVARCHAR(255),
        storage NVARCHAR(255),
        release_date DATETIME NULL,
        year INT NULL,
        nfc NVARCHAR(50),
        jack_support NVARCHAR(50),
        OS NVARCHAR(255),
        wifi NVARCHAR(255),
        sensor NVARCHAR(MAX),
        watt NVARCHAR(MAX),
        processed BIT NULL DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()
    print(f"Bảng '{TRACK_TABLE}' đã sẵn sàng.")

def insert_many(rows):
    conn = get_connection()
    cursor = conn.cursor()
    insert_query = f"""
    INSERT INTO {TRACK_TABLE} (
        product_id, name, manufacturer, price, special_price,
        battery, camera_primary, camera_secondary, chipset,
        display_size, gpu, memory_internal, mobile_display_features,
        mobile_type_of_display, storage, release_date, year,
        nfc, jack_support, OS, wifi, sensor, watt, processed
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    for row in rows:
        cursor.execute(insert_query, row)
    conn.commit()
    conn.close()
    print(f"Đã lưu {len(rows)} sản phẩm vào bảng '{TRACK_TABLE}'.")
