import pandas as pd

def pick(row, *keys):
    for k in keys:
        if k in row and pd.notna(row[k]):
            return row[k]
    return None

def normalize_for_saving(df_track):
    df_saving = pd.DataFrame({
        "product_id": df_track["product_id"],
        "name": df_track["name"],
        "manufacturer": df_track["manufacturer"],
        "OS": [pick(r, "OS", "os") for _, r in df_track.iterrows()],
        "RAM": [pick(r, "RAM", "ram", "memory_internal") for _, r in df_track.iterrows()],
        "ROM": [pick(r, "ROM", "rom", "storage") for _, r in df_track.iterrows()],
        "battery": [pick(r, "Battery", "battery", "pin") for _, r in df_track.iterrows()],
        "camera_primary": [pick(r, "camera_primary", "camera", "camera_chinh") for _, r in df_track.iterrows()],
        "camera_secondary": [pick(r, "camera_secondary", "camera_phu", "camera_truoc") for _, r in df_track.iterrows()],
        "chipset": [pick(r, "Chipset", "chipset", "cpu", "chip") for _, r in df_track.iterrows()],
        "GPU": [pick(r, "GPU", "gpu") for _, r in df_track.iterrows()],
        "display_size": [pick(r, "Display_Size", "display_size", "man_hinh") for _, r in df_track.iterrows()],
        "screen": [pick(r, "Screen", "screen","mobile_display_features", "display_features") for _, r in df_track.iterrows()],
        "mobile_type_of_display": [pick(r, "mobile_type_of_display", "display_type") for _, r in df_track.iterrows()],
        "visibility": [pick(r, "Visibility", "visibility_date", "release_date", "ra_mat", "ngay_ra_mat") for _, r in df_track.iterrows()],
        "nfc": [pick(r, "NFC", "nfc", "mobile_nfc") for _, r in df_track.iterrows()],
        "jack_support": [pick(r, "Jack_Support", "jack_support", "mobile_jack_tai_nghe") for _, r in df_track.iterrows()],
        "price": [pick(r, "price") for _, r in df_track.iterrows()]
    })
    return df_saving
