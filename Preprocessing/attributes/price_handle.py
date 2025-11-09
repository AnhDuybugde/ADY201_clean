import pandas as pd

def compute_final_price(df):
    """
    Tính toán cột price cuối cùng:
    - Ưu tiên special_price nếu có giá trị hợp lệ (> 0)
    - Nếu special_price = 0 hoặc NaN, lấy từ price
    - Cuối cùng lọc bỏ những bản ghi không có giá hợp lệ (> 0)
    """
    # Ép kiểu an toàn về float
    df["price"] = pd.to_numeric(df.get("price", 0), errors="coerce").fillna(0)
    df["special_price"] = pd.to_numeric(df.get("special_price", 0), errors="coerce").fillna(0)

    # Tạo cột final_price: ưu tiên special_price nếu hợp lệ
    df["price"] = df.apply(
        lambda r: r["special_price"] if r["special_price"] > 0 else r["price"],
        axis=1
    )

    # Lọc bỏ giá <= 0 hoặc NaN
    df = df[pd.to_numeric(df["price"], errors="coerce") > 0].copy()

    print(f"Đã xử lý giá: còn lại {len(df)} bản ghi có price hợp lệ (> 0).")
    return df
