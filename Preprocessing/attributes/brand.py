import pandas as pd

brand_map = {
    "samsung": "Samsung", "galaxy": "Samsung",
    "xiaomi": "Xiaomi", "oppo": "Oppo", "vivo": "Vivo", "realme": "Realme",
    "huawei": "Huawei", "oneplus": "OnePlus", "google": "Google", "sony": "Sony",
    "cubot": "Cubot", "htc": "HTC", "lenovo": "Lenovo", "t-mobile": "T-Mobile",
    "tecno": "Tecno", "walton": "Walton", "infinix": "Infinix", "honor": "Honor",
    "motorola": "Motorola", "nokia": "Nokia", "zte": "ZTE", "tcl": "TCL",
    "meizu": "Meizu", "doogee": "Doogee", "nubia": "Nubia", "nothingphone": "NothingPhone",
    "itel": "Itel", "masstel": "Masstel", "viettel": "Viettel", "tesla": "Tesla"
}

def infer_brand(row):
    manufacturer = str(row.get("manufacturer", "")).strip().lower()
    name_lower = str(row.get("name", "")).lower()

    # Nếu có brand hợp lệ thì chuẩn hóa tên
    if manufacturer and manufacturer != "hãng khác":
        for keyword, brand in brand_map.items():
            if keyword in manufacturer:
                return brand
        return row["manufacturer"]  # giữ nguyên nếu không match

    # Nếu là “hãng khác” hoặc trống, thử suy ra từ name
    for keyword, brand in brand_map.items():
        if keyword in name_lower:
            return brand

    # Không xác định được thì trả về NaN
    return pd.NA