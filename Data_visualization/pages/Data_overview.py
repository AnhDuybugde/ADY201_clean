import streamlit as st
import sys, os
# Thêm thư mục gốc (Data_visualization) vào path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db_utils import load_data
from config import NUMERIC_DATA, SAVING_TABLE, RAW_DATA, MODEL_DATA, TRACK_TABLE

TRACK = load_data(TRACK_TABLE)
SAVING = load_data(SAVING_TABLE)
DF_R = load_data(RAW_DATA)
DF_NUM = load_data(NUMERIC_DATA)
DF_MOD = load_data(MODEL_DATA)


st.title("Tổng quan dữ liệu") 
st.write(DF_R.shape)
st.write(DF_R.head(20))

st.write(DF_NUM.shape)
st.write(DF_NUM.head(20))
st.dataframe(DF_NUM.dtypes)




# Lấy dữ liệu
# Hiển thị bảng và thông tin cơ bản
if st.checkbox("### Raw Data:"):
    st.write(TRACK.shape)
    st.dataframe(TRACK.head(20))
    st.dataframe(TRACK.dtypes)

# Hiển thị type of data
if st.checkbox("### Lightly process data:"):
    st.write(SAVING.shape)
    st.dataframe(SAVING.dtypes)
    st.write(SAVING.head(20))

if st.checkbox("### Model data:"):
    st.write(DF_MOD.shape)
    st.write(DF_MOD.head(20))
    st.dataframe(DF_MOD.dtypes)

# Thống kê mô tả
if st.checkbox("Hiện thống kê mô tả:"):
    st.write(DF_NUM.describe())
