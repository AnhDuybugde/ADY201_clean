import pandas as pd
from config import TRACK_TABLE
from db_utils import get_connection, create_table_if_not_exists
from attributes.price_handle import compute_final_price
from attributes.brand import infer_brand
from attributes.os import process_os
from attributes.ram import process_ram
from attributes.rom import process_rom
from attributes.battery import process_battery
from attributes.camera import process_camera
from attributes.chipset import process_chipset
from attributes.gpu import process_gpu
from attributes.display_size import process_display  
from attributes.screen import process_screen
from attributes.sensor import process_sensor
from attributes.nfc import process_nfc_column 
from attributes.jack_support import process_jack_support
from attributes.numeric import clean_numeric_column
from normalize import normalize_for_saving
from inserter import upsert_saving

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# KẾT NỐI DATABASE
conn, cursor = get_connection()
create_table_if_not_exists(cursor)
conn.commit()

# LẤY DỮ LIỆU MỚI
df_track = pd.read_sql(f"SELECT * FROM {TRACK_TABLE} WHERE processed=0 OR processed IS NULL", conn)
if df_track.empty:
    print("Không có dữ liệu mới để xử lý.")
    exit()
print(f"Có {len(df_track)} bản ghi mới.")

print(df_track.columns.tolist())

# XỬ LÝ GIÁ: ƯU TIÊN SPECIAL_PRICE (chỉ giữ record có price)
df_track = compute_final_price(df_track)

# CHUẨN HÓA 
df_track["manufacturer"] = df_track.apply(infer_brand, axis=1)
df_track = process_os(df_track)
df_track = process_ram(df_track)
df_track = process_rom(df_track)
df_track = process_battery(df_track)
df_track = process_camera(df_track)
df_track = process_chipset(df_track)
df_track = process_gpu(df_track)
df_track = process_display(df_track)
df_track = process_screen(df_track)
df_track = process_sensor(df_track)
df_track = process_nfc_column(df_track)
df_track = process_jack_support(df_track)

# Chuẩn hóa numeric
df_track = clean_numeric_column(df_track, ["ram","storage","battery","watt","price"])

# CHUẨN HÓA DỮ LIỆU TRƯỚC KHI LƯU
df_saving = normalize_for_saving(df_track)

print("Tổng dòng trong df_saving:", len(df_saving))
print("Số product_id duy nhất:", df_saving["product_id"].nunique())

# GHI LÊN BẢNG SAVING
upsert_saving(cursor, df_saving)
conn.commit()

# ----------------------------
# CẬP NHẬT PROCESSED CHO TOÀN BỘ BẢN GHI HỢP LỆ
# ----------------------------
try:
    upsert_saving(cursor, df_saving)
    conn.commit()

    cursor.execute(f"""
        UPDATE {TRACK_TABLE}
        SET processed = 1
        WHERE processed = 0 OR processed IS NULL
    """)
    conn.commit()
    print("Đã cập nhật processed = 1 cho toàn bộ bản ghi chưa xử lý.")
except Exception as e:
    conn.rollback()
    print("Lỗi trong quá trình xử lý:", e)

# ĐÓNG KẾT NỐI
cursor.close()
conn.close()
