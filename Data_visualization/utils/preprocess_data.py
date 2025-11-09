import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from utils.db2_utils import get_connection
from config import SAVING_TABLE
import os

# HÀM CHÍNH TIỀN XỬ LÝ (đa chế độ)
def preprocess_data(df, mode="raw"):
    df = df.copy()

    # Định nghĩa loại cột cố định 
    numeric_features = ["ram", "rom", "battery", "camera_primary", "camera_secondary",
                        "display_size", "screen", "sensor", "watt"]
    categorical_features = ["brand", "os", "chipset", "gpu"]
    binary_features = ["nfc", "jack_support"]
    target_features = ["price"]

    # Xử lý NaN ban đầu 
    df = df.fillna({
        "brand": "Unknown",
        "os": "Unknown",
        "chipset": "Unknown",
        "gpu": "Unknown",
        "nfc": 0,
        "jack_support": 0,
    })

    # Mode: raw
    if mode == "raw":
        return df

    # Chuyển binary thành int
    for col in binary_features:
        if col in df.columns:
            df[col] = df[col].astype(int)
            
    # Chuyển numeric cột thành số và điền median 
    for col in numeric_features:
        if col in df.columns:
            df[col] = (
                df[col].astype(str)
                .str.extract(r"(\d+\.?\d*)")[0]
                .astype(float)
            )
            median_val = df[col].median(skipna=True)
            df[col] = df[col].fillna(median_val)

    # Mode: numeric 
    if mode == "numeric":
        keep_cols = categorical_features+ numeric_features + binary_features + target_features
        return df[keep_cols].copy()

    # Mode: model
    # Chuẩn hóa numeric
    scaler = StandardScaler()
    df[numeric_features] = scaler.fit_transform(df[numeric_features])

    # Encode categorical (brand, os, chipset, gpu)
    encoded_dfs = []
    for col in categorical_features:
        if col in df.columns:
            encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
            encoded = encoder.fit_transform(df[[col]])
            encoded_df = pd.DataFrame(encoded, columns=[f"{col}_{v}" for v in encoder.categories_[0]])
            encoded_dfs.append(encoded_df.astype(int))

    if encoded_dfs:
        df_encoded_cat = pd.concat(encoded_dfs, axis=1)
        df = pd.concat([df.drop(columns=categorical_features), df_encoded_cat], axis=1)

    # Xóa cột "name" nếu có
    if "name" in df.columns:
        df = df.drop(columns=["name"])

    return df


# HÀM MAIN
def main(mode="model"):
    conn, cursor = get_connection()
    df_raw = pd.read_sql(f"SELECT * FROM {SAVING_TABLE}", conn)

    if df_raw.empty:
        print("Không có dữ liệu trong DB.")
        return

    print(f"Đọc {len(df_raw)} bản ghi từ {SAVING_TABLE}.")
    id_cols = ["product_id"] if "product_id" in df_raw.columns else []
    df_input = df_raw.drop(columns=id_cols, errors="ignore")

    df_processed = preprocess_data(df_input, mode=mode)

    for col in id_cols:
        df_processed.insert(0, col, df_raw[col].values)

    # Lưu file
    output_folder = os.path.join(os.path.dirname(__file__), f"processed_data_{mode}")
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f"{mode}_data.csv")
    df_processed.to_csv(output_path, index=False)

    print(f"Dữ liệu ({mode}) đã lưu tại: {output_path}")
    print(df_processed.head())


if __name__ == "__main__":
    # mode có thể là: "raw", "numeric", "model"
    main(mode="model")
