import pandas as pd

def pick(row, *keys):
    for k in keys:
        if k in row and pd.notna(row[k]):
            return row[k]
    return None

def normalize_for_saving(df_track):
    df_saving = pd.DataFrame({
        "product_id": df_track["product_id"],
        "brand": [pick(r, "manufacturer", "brand") for _, r in df_track.iterrows()],
        "os": [pick(r, "os", "OS") for _, r in df_track.iterrows()],
        "ram": [pick(r, "ram", "RAM", "memory_internal") for _, r in df_track.iterrows()],
        "rom": [pick(r, "rom", "ROM", "storage") for _, r in df_track.iterrows()],
        "battery": [pick(r, "battery", "Battery") for _, r in df_track.iterrows()],
        "camera_primary": [pick(r, "camera_primary", "camera", "camera_chinh") for _, r in df_track.iterrows()],
        "camera_secondary": [pick(r, "camera_secondary", "camera_phu", "camera_truoc") for _, r in df_track.iterrows()],
        "chipset": [pick(r, "chipset", "Chipset", "cpu") for _, r in df_track.iterrows()],
        "gpu": [pick(r, "gpu", "GPU") for _, r in df_track.iterrows()],
        "location": [pick(r, "province", "location") for _, r in df_track.iterrows()],
        "display_size": [pick(r, "display_size", "Display_Size") for _, r in df_track.iterrows()],
        "screen": [pick(r, "screen", "Screen","mobile_display_features", "display_features") for _, r in df_track.iterrows()],
        "sensor": [pick(r, "sensor", "sensors") for _, r in df_track.iterrows()],
        "watt": [pick(r, "watt", "charging_power") for _, r in df_track.iterrows()],
        "nfc": [pick(r, "nfc", "NFC") for _, r in df_track.iterrows()],
        "jack_support": [pick(r, "jack_support", "Jack_Support") for _, r in df_track.iterrows()],
        "price": pd.to_numeric(df_track["price"], errors="coerce")
    })
    return df_saving
