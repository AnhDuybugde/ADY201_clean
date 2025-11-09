import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import sys, os
import pandas as pd
import numpy as np

# Thêm thư mục gốc (Data_visualization) vào path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db_utils import load_data
from config import NUMERIC_DATA
from sklearn.feature_selection import mutual_info_regression
from sklearn.preprocessing import LabelEncoder

# Load dữ liệu
df = load_data(NUMERIC_DATA)

# X = df[["ram","battery","camera_primary","camera_secondary","screen","jack_support"]]  # biến độc lập
# y = df['price']
# mi = mutual_info_regression(X, y)
# mi_df = pd.DataFrame({'Feature': X.columns, 'MutualInfo': mi}).sort_values(by='MutualInfo', ascending=False)
# print(mi_df)

# # --- Vẽ biểu đồ ---
# corr = df.corr(method='pearson')
# plt.figure(figsize=(10,6))
# sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
# plt.title("Heatmap - Ma trận tương quan (Pearson)")

# # --- Hiển thị trên Streamlit ---
# st.pyplot(plt)
target = "price"
X = df.drop(columns=[target]).copy()
y = df[target].copy()

# 0) Hiện thông tin debug nhanh
print("Total columns:", len(X.columns))
print("Columns list:", X.columns.tolist())

# 1) Kiểm tra duplicate column names
dup_cols = X.columns[X.columns.duplicated()]
if len(dup_cols) > 0:
    print("WARNING: duplicated column names found:", dup_cols.tolist())
    # lựa chọn: giữ chỉ một cột duplicate (ở đây ta giữ lần xuất hiện đầu)
    X = X.loc[:, ~X.columns.duplicated()]
    print("After drop duplicates, total columns:", len(X.columns))

# 2) Tính Pearson chỉ cho numeric (safe)
pearson_result = {}
numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
for col in numeric_cols:
    # nếu cột toàn NaN hoặc constant, corr có thể nan -> handle
    if X[col].nunique(dropna=True) <= 1 or y.nunique(dropna=True) <= 1:
        pearson_result[col] = np.nan
    else:
        pearson_result[col] = np.corrcoef(X[col].astype(float), y.astype(float))[0, 1]

# 3) Chuẩn bị X_temp cho MI (không sửa gốc X)
X_temp = X.copy()

# 3a) map ordinal cols (tuỳ dataset)
ordinal_map = {'low': 1, 'mid': 2, 'high': 3, 'unknown': 0}
ordinal_cols = [c for c in ['os','gpu', 'chipset'] if c in X_temp.columns]

for col in ordinal_cols:
    X_temp[col] = X_temp[col].map(ordinal_map).fillna(0)

# 3b) encode tạm nominal khác (LabelEncoder)
nominal_cols = X_temp.select_dtypes(include=['object', 'category']).columns.tolist()
nominal_cols = [c for c in nominal_cols if c not in ordinal_cols]
for col in nominal_cols:
    X_temp[col] = LabelEncoder().fit_transform(X_temp[col].astype(str))

# 4) Kiểm tra NaN và convert toàn bộ X_temp sang numeric
#    Nếu có NaN, mutual_info_regression sẽ error -> ta fill tạm bằng -999 hoặc trung bình
if X_temp.isnull().any().any():
    print("Warning: NaNs found in X_temp, filling with column median for MI calc")
    for col in X_temp.columns:
        if X_temp[col].isnull().any():
            if X_temp[col].dtype.kind in 'biufc':  # numeric
                X_temp[col] = X_temp[col].fillna(X_temp[col].median())
            else:
                X_temp[col] = X_temp[col].fillna(-999)

# 5) Mutual information (sử dụng X_temp.values)
mi = mutual_info_regression(X_temp.values, y.values, random_state=42)
# đảm bảo mi tương ứng với X_temp.columns
if len(mi) != len(X_temp.columns):
    raise ValueError("Length mismatch: mi vs columns")

# 6) Gom kết quả vào DataFrame (chắc chắn không duplicate)
summary = pd.DataFrame({
    "Feature": X_temp.columns.tolist(),
    "PearsonCorr": [pearson_result.get(c, np.nan) for c in X_temp.columns],
    "MutualInfo": mi
})

# 7) Suggestion (cùng như bạn)
def suggest_model(row):
    p = abs(row["PearsonCorr"]) if not np.isnan(row["PearsonCorr"]) else 0
    m = row["MutualInfo"]
    if p >= 0.5 and m < 0.4:
        return "Linear"
    elif m >= 0.4 and p < 0.5:
        return "Non-linear"
    elif m >= 0.4 and p >= 0.5:
        return "Mixed / Tree-based"
    else:
        return "Weak"

summary["ModelSuggestion"] = summary.apply(suggest_model, axis=1)
summary = summary.sort_values(by="MutualInfo", ascending=False).reset_index(drop=True)

print(summary)
