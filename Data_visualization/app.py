import os
import sys
import streamlit as st
# Cấu hình đường dẫn 
# Đảm bảo có thể import từ thư mục gốc (Data_visualization)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.db_utils import load_data
from config import SAVING_TABLE

# Tải dữ liệu 
df = load_data(SAVING_TABLE)

# Cấu hình giao diện Streamlit 
st.set_page_config(
    page_title="Dashboard — SQL Data",
    layout="wide"
)

# Sidebar 
with st.sidebar:
    # Xác định đường dẫn tuyệt đối tới ảnh logo
    current_dir = os.path.dirname(__file__)
    logo_path = os.path.join(current_dir, "assets", "logo-fpt.jpg")

    # Kiểm tra file logo tồn tại
    if os.path.exists(logo_path):
        st.image(logo_path, width=120)
    else:
        st.warning("Logo file không tìm thấy: assets/logo-fpt.jpg")

    st.title("Data Dashboard")
    st.markdown("---")
    st.markdown("Chọn trang ở menu bên trái")

# Nội dung chính 
st.title("Trang chính")
st.markdown("""
Chào mừng đến **Visualization Dashboard**.  
Bạn có thể khám phá dữ liệu, vẽ biểu đồ, hoặc thử mô hình AI.
""")

# Hiển thị dữ liệu mẫu
if df is not None and not df.empty:
    st.write("### Dữ liệu mẫu", df.head())
else:
    st.error("Không thể tải dữ liệu. Vui lòng kiểm tra hàm `load_data()` trong utils/db_utils.py")

