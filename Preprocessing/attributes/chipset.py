# chipset_utils.py
import pandas as pd
import re

# Hàm phân loại hiệu năng chipset
def performance_bin(chip):
    """
    Phân loại chipset thành High / Medium / Low / NULL
    """
    if pd.isna(chip) or str(chip).strip() == "":
        return None

    chip = str(chip).lower().strip()

    # Nếu lẫn tên hãng hoặc tên điện thoại → Low/Medium
    if "motorola edge 20 fusion" in chip:
        return "Medium"
    if any(brand in chip for brand in ["oppo", "samsung", "huawei", "xiaomi", "vivo", "realme"]):
        return "Low"

    # Snapdragon
    if "snapdragon" in chip:
        if "elite" in chip or "gen" in chip or re.search(r'\b8\d{2}\b', chip):
            return "High"
        match = re.search(r'(\d{3,4})', chip)
        if match:
            num = int(match.group(1))
            if num >= 800:
                return "High"
            elif num >= 600:
                return "Medium"
            else:
                return "Low"

    # Kirin
    if "kirin" in chip:
        match = re.search(r'(\d{3,4})', chip)
        if match:
            num = int(match.group(1))
            if num >= 900:
                return "High"
            elif num >= 800:
                return "Medium"
            else:
                return "Low"

    # MediaTek / Helio / Dimensity
    if "mediatek" in chip or "helio" in chip or "mt" in chip:
        if "dimensity" in chip:
            match = re.search(r'(\d{3,4})', chip)
            if match:
                num = int(match.group(1))
                if num >= 1000:
                    return "High"
                elif num >= 800:
                    return "Medium"
                else:
                    return "Low"
        elif "helio g" in chip:
            return "Medium"
        else:
            return "Low"

    # Exynos
    if "exynos" in chip:
        match = re.search(r'(\d{3,4})', chip)
        if match:
            num = int(match.group(1))
            if num >= 9000:
                return "High"
            elif num >= 7000:
                return "Medium"
            else:
                return "Low"

    # Apple Bionic
    if "bionic" in chip or "apple" in chip:
        return "High"

    # Google Tensor
    if "tensor" in chip or "google" in chip:
        return "High"

    # Unisoc / Spreadtrum
    if "unisoc" in chip or "spreadtrum" in chip:
        if "t610" in chip or "t700" in chip:
            return "Medium"
        return "Low"

    # ARM Cortex / quad-core
    if "cortex" in chip or "quad-core" in chip:
        return "Low"

    # Mặc định
    return "Low"

# Hàm xử lý DataFrame
def process_chipset(df):
    """
    Tạo cột Chipset_Performance dựa trên chipset.
    """
    chip_col = next((c for c in df.columns if c.lower() in ["chipset","chip_set"]), None)
    if chip_col is None:
        raise KeyError("DataFrame không có cột chipset/chip_set.")

    df["chipset"] = df[chip_col].apply(performance_bin)
    return df

# Ví dụ sử dụng
if __name__ == "__main__":
    data = {
        "chipset": ["Snapdragon 888", "Kirin 810", "Dimensity 900", "Exynos 850", "Apple A15 Bionic", None]
    }
    df = pd.DataFrame(data)
    df = process_chipset(df)
    print(df)
