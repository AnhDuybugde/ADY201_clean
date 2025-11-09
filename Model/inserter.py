import pandas as pd

def overwrite_table(cursor, df, table_name):
    """
    Xóa bảng cũ (nếu có), tạo bảng mới dựa trên df,
    và insert toàn bộ dữ liệu.
    """
    # Drop bảng nếu tồn tại
    cursor.execute(f"IF OBJECT_ID('{table_name}', 'U') IS NOT NULL DROP TABLE {table_name}")

    # Tạo bảng mới
    columns = []
    for col, dtype in zip(df.columns, df.dtypes):
        if pd.api.types.is_integer_dtype(dtype):
            sql_type = "INT"
        elif pd.api.types.is_float_dtype(dtype):
            sql_type = "FLOAT"
        else:
            sql_type = "NVARCHAR(255)"
        columns.append(f"[{col}] {sql_type}")  # thêm [] để tránh lỗi tên cột đặc biệt
    columns_sql = ", ".join(columns)
    cursor.execute(f"CREATE TABLE {table_name} ({columns_sql})")

    # Chuyển NaN -> None
    df = df.where(pd.notna(df), None)

    # Insert dữ liệu
    col_names = ", ".join([f"[{c}]" for c in df.columns])
    placeholders = ", ".join(["?"] * len(df.columns))
    for _, row in df.iterrows():
        values = tuple(row[c] for c in df.columns)
        cursor.execute(f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})", values)
