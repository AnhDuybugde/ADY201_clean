import pandas as pd
import numpy as np

def count_sensors(val):
    """
    Đếm số lượng sensor từ chuỗi, phân tách bằng dấu phẩy.
    Trả về 0 nếu giá trị rỗng hoặc null.
    """
    if pd.isna(val):
        return 0
    text = str(val).strip()
    if not text:
        return 0
    # Tách theo dấu phẩy và loại bỏ khoảng trắng
    sensors = [s.strip() for s in text.split(',') if s.strip()]
    return len(sensors)

def process_sensor(df):
    """
    Tạo cột 'sensor_count' từ cột 'sensor' hoặc 'mobile_cam_bien'.
    """
    sensor_col = next((c for c in df.columns if c.lower() in ["sensor", "sensors"]), None)
    if sensor_col is None:
        raise KeyError("DataFrame không có cột 'sensor' hoặc 'mobile_cam_bien'.")
    
    df["sensor"] = df[sensor_col].apply(count_sensors)
    return df

# Ví dụ test
if __name__ == "__main__":
    data = {
        "sensor": [
            "Accelerometer, Gyroscope, Proximity",
            "",
            None,
            "Accelerometer",
            "Gyroscope, Proximity"
        ]
    }
    df = pd.DataFrame(data)
    df = process_sensor(df)
    print(df)
