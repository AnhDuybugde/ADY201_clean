import pandas as pd
import re

# Chuẩn hóa các cột numeric (RAM, ROM, watt, nfc, price…)
def clean_numeric_column(df, col_list):
    """
    Ép các cột numeric về float hợp lệ.
    - Giữ nguyên None / NaN
    - Chỉ lấy số đầu tiên nếu có
    """
    for col in col_list:
        if col in df.columns:
            def extract_number(val):
                if pd.isna(val) or val is None:
                    return None
                nums = re.findall(r'\d+\.?\d*', str(val))
                return float(nums[0]) if nums else None
            df[col] = df[col].apply(extract_number)
            df[col] = df[col].astype(float)  # ép kiểu float nếu được
    return df



# Test nhanh
if __name__ == "__main__":
    if __name__ == "__main__":
        df = pd.DataFrame({
            "ram": ["12 GB", "8GB + Mở rộng 8GB", None],
            "rom": ["256 GB", "128GB", "512 GB"],
            "battery": ["5000 mAh", "4500 mAh", None],
            "camera_primary": [
                "48 MP",
                "64MP + 8MP",
                "Không rõ, Camera chính: 48MP, f/1.78, 24mm, 2µm, chống rung quang học dịch chuyển cảm biến thế hệ thứ hai, Focus Pixels 100%"
            ],
            "camera_secondary": ["32 MP", "12MP", None],
            "display_size": ["6.5 inches", "6.8 inch", "5.9\""],
            "screen": ["AMOLED 120Hz", "OLED 90Hz", "IPS LCD"],
            "sensor": ["vân tay, gia tốc", "ánh sáng, tiệm cận", None],
            "watt": ["67W", "45 W", "30W"],
            "price": ["15000000", "12000000", "9000000"]
        })

    numeric_features = [
        "ram", "rom", "battery", "camera_primary", "camera_secondary",
        "display_size", "screen", "sensor", "watt"
    ]

    # Thêm cột thiếu (để đảm bảo có đủ các cột cần test)
    for col in numeric_features:
        if col not in df.columns:
            df[col] = None

    df = clean_numeric_column(df, numeric_features)

    # Kiểm tra kết quả
    for col in numeric_features:
        print(f"🔹 {col} → dtype: {df[col].dtype}")
        print(df[col].unique()[:5], "\n")

    print("DataFrame sau xử lý:")
    print(df)
