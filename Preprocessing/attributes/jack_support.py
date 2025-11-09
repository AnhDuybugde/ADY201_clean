import pandas as pd

def process_jack_support(df):
    """
    Chuyển cột 'jack_support' về dạng nhị phân:
    - 'Có' -> 1
    - 'Không' -> 0
    - NULL hoặc giá trị khác -> None
    """
    jack_col = next((c for c in df.columns if c.lower() == "jack_support"), None)
    if jack_col is None:
        raise KeyError("DataFrame không có cột 'jack_support'.")

    def map_jack(val):
        if pd.isna(val):
            return None
        text = str(val).strip().lower()
        if text == "có":
            return 1
        elif text == "không":
            return 0
        else:
            return None

    df["jack_support"] = df[jack_col].apply(map_jack)
    return df
