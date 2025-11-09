import pandas as pd
import re
import numpy as np

# B1. Làm sạch cột OS
def clean_os(os_value):
    """Chuẩn hóa giá trị hệ điều hành (lowercase, xử lý missing)."""
    if pd.isna(os_value) or str(os_value).strip() == "":
        return None
    
    text = str(os_value).lower().strip()
    
    # Nếu chỉ có chữ "android" mà không có version
    if "android" in text and not re.search(r'\d+', text):
        return None
    
    return text

# B2. Trích xuất phiên bản OS (dạng số)
def extract_version(os_value):
    """Lấy version số từ chuỗi OS, ví dụ 'Android 13' → 13."""
    if os_value is None:
        return None
    
    nums = re.findall(r'\d+', str(os_value))
    return int(max(nums, key=int)) if nums else None

# B3. Gộp nhóm (binning)
def bin_os(row):
    """Phân loại OS theo cấp độ (High / Mid / Low / None)."""
    os_value = row["OS_Cleaned"]
    version = row["OS_Version"]

    if os_value is None:
        return None

    text = str(os_value).lower()

    # --- Android & các UI dựa trên Android ---
    if any(ui in text for ui in ["android", "miui", "coloros", "funtouch", "realme ui", "emui", "oxygenos"]):
        if version is None:
            return None
        elif version >= 13:
            return "High"
        elif 10 <= version <= 12:
            return "Mid"
        else:
            return "Low"

    # --- iOS ---
    elif "ios" in text:
        if version is None:
            return None
        elif version >= 17:
            return "High"
        elif 15 <= version <= 16:
            return "Mid"
        else:
            return "Low"

    # --- HarmonyOS ---
    elif "harmony" in text:
        if version is None:
            return None
        elif version >= 3:
            return "Mid"
        else:
            return "Low"

    # --- Windows, KaiOS, v.v. ---
    elif "windows" in text or "kai" in text:
        return "Low"

    return None

# B4. Hàm chính — dùng trong pipeline
def process_os(df):
    """
    Chuẩn hóa + binning cột OS trong DataFrame.
    Kết quả cuối cùng ghi đè trực tiếp lên cột OS.
    Chỉ còn giá trị: High, Mid, Low, hoặc None.
    """
    # Tự động nhận tên cột OS bất kể chữ hoa/chữ thường
    os_col = next((c for c in df.columns if c.lower() == "os"), None)
    if os_col is None:
        raise KeyError("DataFrame không có cột 'OS' hoặc 'os'.")

    # Làm sạch
    df["OS_Cleaned"] = df[os_col].apply(clean_os)
    # Lấy version
    df["OS_Version"] = df["OS_Cleaned"].apply(extract_version)
    # Binning và ghi đè lên cột gốc
    df[os_col] = df.apply(bin_os, axis=1)
    # Xóa cột trung gian
    df.drop(columns=["OS_Cleaned", "OS_Version"], inplace=True)

    return df

# Ví dụ test nhanh
if __name__ == "__main__":
    data = {
        "os": ["Android 13", "iOS 16", "HarmonyOS 2", "Windows 10", None, "Android", "iOS 18"]
    }
    df = pd.DataFrame(data)
    df = process_os(df)
    print(df)
