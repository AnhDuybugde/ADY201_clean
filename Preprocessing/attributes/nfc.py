import pandas as pd
import numpy as np

def process_nfc_column(df):
    """
    Tạo cột 'nfc_flag' từ cột 'nfc' hoặc 'mobile_nfc'.
    """
    nfc_col = next((c for c in df.columns if c.lower() in ["nfc", "NFC"]), None)
    if nfc_col is None:
        raise KeyError("DataFrame không có cột 'nfc' hoặc 'mobile_nfc'.")

    def process_nfc(val):
        if pd.isna(val):
            return None
        text = str(val).strip().lower()
        if text.startswith("có"):
            return 1
        elif text.startswith("không"):
            return 0
        else:
            return None

    df["nfc"] = df[nfc_col].apply(process_nfc)
    return df


# Ví dụ test
if __name__ == "__main__":
    data = {
        "nfc": ["Có NFC", "Không hỗ trợ", None, "Có", "không"]
    }
    df = pd.DataFrame(data)
    df = process_nfc_column(df)
    print(df)
