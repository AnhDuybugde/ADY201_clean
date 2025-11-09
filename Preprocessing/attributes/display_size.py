# display_utils.py
import pandas as pd
import re
import numpy as np

# Hàm trích xuất kích thước màn hình lớn nhất (inch)
def extract_display_size(val):
    """
    Lấy số lớn nhất trong chuỗi mô tả màn hình.
    Ví dụ:
        "6.1 inch / 6.7 inch" -> 6.7
        "6,5" -> 6.5
        NULL -> np.nan
    """
    if pd.isna(val):
        return np.nan

    text = str(val).replace(",", ".")  # đổi dấu phẩy thành dấu chấm
    nums = re.findall(r'\d+(?:\.\d+)?', text)
    if not nums:
        return np.nan

    # Lấy số lớn nhất
    return max(float(n) for n in nums)

# Hàm xử lý DataFrame
def process_display(df):
    """
    Xử lý cột màn hình:
    - tìm cột 'display_size' hoặc 'screen_max'
    - tạo cột 'Display_Size_Inch' với số lớn nhất
    """
    display_col = next((c for c in df.columns if c.lower() in ["display_size", "screen_max"]), None)
    if display_col is None:
        raise KeyError("DataFrame không có cột display_size/screen_max.")

    df["display_size"] = df[display_col].apply(extract_display_size)
    return df

# Ví dụ sử dụng
if __name__ == "__main__":
    data = {
        "display_size": ["6.1 inch / 6.7 inch", "5,8\"", "6.5", None, "7 inch"]
    }
    df = pd.DataFrame(data)
    df = process_display(df)
    print(df)
