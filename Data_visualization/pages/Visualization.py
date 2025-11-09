import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import pandas as pd
from utils.db_utils import load_data
from utils.db2_utils import get_connection, create_table_if_not_exists
from utils.plot_utils import plot_chart
from utils.preprocess_data import preprocess_data
from inserter import overwrite_table
from datetime import datetime
from config import SAVING_TABLE, RAW_DATA , NUMERIC_DATA, MODEL_DATA

st.title("rawization Dashboard")

# Chọn chế độ xử lý dữ liệu
mode = st.radio(
    "Chọn chế độ xử lý dữ liệu (Processing Mode):",
    ["raw", "numeric", "model"],
    captions=[
        "raw — chỉ xử lý NaN, dùng cho biểu đồ mô tả (Histogram, Bar, Pie...)",
        "Numeric — ép kiểu số, dùng cho biểu đồ có tính toán (Scatter, Boxplot, Line...)",
        "Model — chuẩn hóa + mã hóa (encode), dùng cho huấn luyện ML hoặc Regression"
    ],
    horizontal=True,
    index=0,
    label_visibility="visible"
)


# Load dữ liệu 
df = load_data(SAVING_TABLE)

if df is None or df.empty:
    st.warning("Không có dữ liệu để hiển thị.")
    st.stop()

# Tiền xử lý theo mode 
df = preprocess_data(df, mode=mode)
st.success(f"Dữ liệu đã được xử lý theo chế độ: **{mode.upper()}**")
st.markdown("## Dữ liệu mẫu sau xử lý")
st.dataframe(df.head())

# Nút lưu dữ liệu vào SQL Server
if st.button("Lưu dữ liệu vào SQL Server"):
    TABLE_MAPPING = {
    "raw":RAW_DATA,
    "numeric":NUMERIC_DATA,
    "model":MODEL_DATA
    }

    table_name = TABLE_MAPPING[mode]

    # Tạo kết nối và con trỏ
    conn, cursor = get_connection()

    try:
        overwrite_table(cursor, df, table_name)
        conn.commit()
        st.success(f"Dữ liệu đã được lưu vào SQL Server với bảng: {table_name}")
    except Exception as e:
        st.error(f"Lưu dữ liệu thất bại: {e}")
    finally:
        cursor.close()
        conn.close()

# Gợi ý biểu đồ phù hợp theo chế độ
chart_options = {
    "raw": ["Histogram", "Bar", "Pie","Countplot"],
    "numeric": [ "Line","Bar","Pie","Histogram", "Boxplot", "Violin", "Scatter", "Heatmap (corr)"],
    "model": ["Scatter", "Boxplot", "Violin", "Pairplot", "Heatmap (corr)"]
}

st.markdown("## Vẽ biểu đồ từ dữ liệu đã xử lý")
# Chọn loại biểu đồ phù hợp
chart_type = st.selectbox(
    "Chọn loại biểu đồ muốn vẽ:",
    chart_options[mode],
    help=f"Các loại biểu đồ tương thích với chế độ '{mode}'"
)

all_cols = df.columns.tolist()

# Ẩn chọn cột nếu là heatmap
if chart_type == "Heatmap (corr)":
    x_col, y_col = None, None
    st.info("Heatmap sẽ tự động dùng toàn bộ các cột số.")
else:
    x_col = st.selectbox("Chọn cột X:", all_cols)
    y_col = st.selectbox("Chọn cột Y:", all_cols) if chart_type in ["Boxplot", "Scatter", "Bar", "Line"] else None

# --- Nút vẽ ---
if st.button("Vẽ biểu đồ"):
    st.session_state["chart_info"] = {"chart_type": chart_type, "x_col": x_col, "y_col": y_col}
    plot_chart(df, x_col, y_col, chart_type)

# --- Nút lưu ---
if "chart_info" in st.session_state:
    info = st.session_state["chart_info"]
    if st.button("Lưu biểu đồ"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{info['chart_type']}_{info['x_col']}_{info['y_col'] or 'none'}_{timestamp}.png"
        save_path = os.path.join(os.path.dirname(__file__), '..', 'plots', file_name)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plot_chart(df, info['x_col'], info['y_col'], info['chart_type'], save_path=save_path)
        st.success(f"Đã lưu biểu đồ tại: `{file_name}`")
