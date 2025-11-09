import pandas as pd
import re
import numpy as np

def extract_screen_hz(val):
    """
    Lấy số Hz hợp lệ từ chuỗi. 
    Trả về np.nan nếu không tìm thấy số hợp lệ.
    
    Ví dụ:
        "120Hz" -> 120
        "60Hz / 90Hz" -> 90
        "QQVGA" -> np.nan
        "8e+006" -> np.nan
    """
    if pd.isna(val):
        return np.nan

    text = str(val).lower().strip()

    # Lấy tất cả số nguyên hoặc thập phân
    nums = re.findall(r'\d+(?:\.\d+)?', text)
    if not nums:
        return np.nan

    # Lọc các số quá lớn / không hợp lệ (ví dụ > 1000Hz là sai)
    valid_nums = [float(n) for n in nums if float(n) < 1000]
    if not valid_nums:
        return np.nan

    # Lấy số lớn nhất nếu có nhiều tần số
    return max(valid_nums)

def process_screen(df):
    """
    Tạo cột 'Screen_Hz' từ cột 'screen' hoặc 'refresh_rate'.
    """
    screen_col = next((c for c in df.columns if c.lower() in ["screen", "Screen","mobile_display_features", "display_features"]), None)
    if screen_col is None:
        raise KeyError("DataFrame không có cột screen/refresh_rate.")

    df["screen"] = df[screen_col].apply(extract_screen_hz)
    return df

# Ví dụ test
if __name__ == "__main__":
    data = {
        "screen": ["120Hz", "60Hz / 90Hz", "144", None, "60 Hz", "QQVGA", "8e+006", "True-tone"]
    }
    df = pd.DataFrame(data)
    df = process_screen(df)
    print(df)
