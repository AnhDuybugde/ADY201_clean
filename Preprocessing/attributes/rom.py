# rom_utils.py
import pandas as pd
import re
import numpy as np

# Hàm trích xuất ROM/Storage cơ bản
def extract_rom_basic(val):
    """
    Lấy số ROM/Storage cơ bản từ chuỗi.
    Ví dụ:
        "128 GB" -> 128
        "1 TB" -> 1024
        None -> np.nan
    """
    if pd.isna(val):
        return np.nan
    
    text = str(val).lower().strip()

    # Lấy số (hỗ trợ cả số thập phân)
    nums = re.findall(r'\d+(?:\.\d+)?', text)
    if not nums:
        return np.nan
    
    num = float(nums[0])

    # Chuyển đổi đơn vị
    if "tb" in text:
        return int(num * 1024)  # TB -> GB
    elif "gb" in text:
        return int(num)
    else:
        return int(num)  # fallback: coi như GB

# Hàm xử lý DataFrame
def process_rom(df):
    """
    Xử lý cột ROM trong DataFrame:
    - Dò cột rom_preprocessed (không phân biệt chữ hoa/thường)
    - Tạo cột 'ROM' gọn, NaN cho giá trị NULL
    """
    rom_col = next((c for c in df.columns if c.lower() == "storage"), None)
    if rom_col is None:
        raise KeyError("DataFrame không có cột 'rom_preprocessed'.")
    
    df["rom"] = df[rom_col].apply(extract_rom_basic)
    return df

# Ví dụ sử dụng
if __name__ == "__main__":
    data = {
        "storage": [
            None, "128 GB", "256 GB", "512 GB", "1 TB", "2 TB"
        ]
    }
    df = pd.DataFrame(data)

    df = process_rom(df)
    print(df)
