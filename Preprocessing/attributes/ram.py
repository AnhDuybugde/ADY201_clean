import pandas as pd
import numpy as np
import re

# Hàm trích xuất RAM cơ bản (chỉ số đầu tiên)
def extract_ram_basic(val):
    """
    Lấy số RAM cơ bản từ chuỗi, bỏ qua RAM mở rộng.
    Ví dụ:
        "12 GB" -> 12
        "6GB + Mở rộng 6GB" -> 6
        NULL -> np.nan
    """
    if pd.isna(val):
        return np.nan

    # Lấy tất cả các số trong chuỗi
    num_str = re.findall(r'\d+\.?\d*', str(val))
    if num_str:
        num = float(num_str[0])
        return int(num) if num.is_integer() else num
    return np.nan

# Hàm chính để pipeline gọi
def process_ram(df, col_name="memory_internal"):
    """
    Xử lý cột RAM:
    - Chỉ lấy số đầu tiên
    - Trả về cột 'ram' dạng float / None
    """
    if col_name not in df.columns:
        raise KeyError(f"DataFrame không có cột '{col_name}'")
    
    df["ram"] = df[col_name].apply(extract_ram_basic)
    return df

# Test nhanh
if __name__ == "__main__":
    data = {
        "memory_internal": [
            None, "12 GB", "16 GB", "2 GB", "6GB + Mở rộng 6GB", "8GB + Mở rộng 10GB"
        ]
    }
    df = pd.DataFrame(data)
    df = process_ram(df)
    print(df)
