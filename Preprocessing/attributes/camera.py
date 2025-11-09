# camera_utils.py
import pandas as pd
import re
import numpy as np

# Hàm trích xuất số lớn nhất trong chuỗi
def extract_max_number(val):
    """
    Trích xuất số lớn nhất từ chuỗi.
    Ví dụ:
        "12 MP + 8 MP" -> 12.0
        "48.0 MP" -> 48.0
        None -> np.nan
    """
    if pd.isna(val) or str(val).strip() == "":
        return np.nan
    
    # Thay dấu , thành . để hỗ trợ thập phân
    text = str(val).replace(",", ".")
    
    # Lấy tất cả số (có thể thập phân)
    nums = re.findall(r'\d+(?:\.\d+)?', text)
    if not nums:
        return np.nan
    
    # Trả về số lớn nhất
    return max(float(n) for n in nums)

# Hàm xử lý DataFrame cho camera
def process_camera(df):
    """
    Xử lý các cột camera_primary và camera_secondary trong DataFrame:
    - Tạo cột gọn Camera_Primary và Camera_Secondary
    - Dạng float, NaN nếu không có dữ liệu hợp lệ
    """
    for col in ["camera_primary", "camera_secondary"]:
        df_col = next((c for c in df.columns if c.lower() == col), None)
        if df_col is None:
            raise KeyError(f"DataFrame không có cột '{col}'.")
        
        out_col = "camera_primary" if col == "camera_primary" else "camera_secondary"
        df[out_col] = df[df_col].apply(extract_max_number)
    
    return df

# Ví dụ sử dụng
if __name__ == "__main__":
    data = {
        "camera_primary": ["12 MP + 8 MP", "48", None, "64.0 MP", "8,0 + 2 MP"],
        "camera_secondary": ["8 MP", None, "5 MP + 2 MP", "12.0", ""]
    }
    df = pd.DataFrame(data)

    df = process_camera(df)
    print(df)
