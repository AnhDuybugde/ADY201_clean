# battery_utils.py
import pandas as pd
import re
import numpy as np

# Hàm trích xuất dung lượng pin
def extract_battery_capacity(val):
    """
    Lấy số dung lượng pin từ chuỗi.
    Ví dụ:
        "5000 mAh" -> 5000
        "4500" -> 4500
        "500" -> None (dưới 1000 mAh không hợp lệ)
        None -> None
    """
    if pd.isna(val):
        return np.nan
    
    text = str(val).replace('.', '').replace(',', '').strip()
    
    # Lấy tất cả số
    nums = re.findall(r'\d+', text)
    if not nums:
        return np.nan
    
    val_int = int(nums[0])
    
    # Chỉ giữ giá trị >= 1000
    if val_int < 1000:
        return np.nan
    
    return val_int

# Hàm xử lý DataFrame
def process_battery(df):
    """
    Xử lý cột battery trong DataFrame:
    - Dò cột 'battery' (không phân biệt chữ hoa/thường)
    - Tạo cột 'Battery' gọn, NaN cho giá trị pin không hợp lệ
    """
    battery_col = next((c for c in df.columns if c.lower() == "battery"), None)
    if battery_col is None:
        raise KeyError("DataFrame không có cột 'battery'.")
    
    df["battery"] = df[battery_col].apply(extract_battery_capacity)
    return df

# Ví dụ sử dụng
if __name__ == "__main__":
    data = {
        "battery": [
            None, "5000 mAh", "4500", "900", "5500", "4.000 mAh"
        ]
    }
    df = pd.DataFrame(data)

    df = process_battery(df)
    print(df)
