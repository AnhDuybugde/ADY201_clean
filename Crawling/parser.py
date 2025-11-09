# src/parser.py
import json
from datetime import datetime
from config import PROVINCE_ID

def extract_attributes(attr_raw):
    if isinstance(attr_raw, str):
        try:
            return json.loads(attr_raw)
        except:
            return {}
    elif isinstance(attr_raw, dict):
        return attr_raw
    return {}

def pick(attrs, *keys):
    for k in keys:
        if k in attrs:
            return attrs[k]
    return None

def parse_product(p):
    general = p.get("general", {})
    filterable = p.get("filterable", {})
    attrs = extract_attributes(general.get("attributes"))

    os_name = pick(attrs, "operating_system", "mobile_os_filter")
    os_version = pick(attrs, "os_version")
    os_value = f"{os_name} {os_version}".strip() if os_name else os_version

    release_raw = pick(attrs, "release_date", "visibility_date", "ra_mat", "ngay_ra_mat")
    release_date, year = None, None
    if release_raw:
        try:
            release_date = datetime.strptime(release_raw[:10], "%Y-%m-%d")
            year = release_date.year
        except:
            try:
                year = int(release_raw.strip()[:4])
            except:
                pass

    return (
        general.get("product_id"),
        general.get("name"),
        general.get("manufacturer"),
        filterable.get("price"),
        filterable.get("special_price"),
        pick(attrs, "battery", "pin"),
        pick(attrs, "camera_primary", "camera", "camera_chinh"),
        pick(attrs, "camera_secondary", "camera_phu", "camera_truoc"),
        pick(attrs, "chipset", "cpu", "chip"),
        pick(attrs, "display_size", "man_hinh", "screen_size"),
        pick(attrs, "gpu"),
        pick(attrs, "memory_internal", "ram"),
        pick(attrs, "mobile_display_features", "display_features"),
        pick(attrs, "mobile_type_of_display", "display_type"),
        pick(attrs, "storage", "rom", "bo_nho_trong"),
        release_date,
        year,
        pick(attrs, "mobile_nfc", "nfc"),
        pick(attrs, "mobile_jack_tai_nghe", "jack_support", "jack_3.5mm"),
        os_value,
        pick(attrs, "wlan", "wifi"),
        pick(attrs, "mobile_cam_bien", "sensor"),
        pick(attrs, "mobile_cong_nghe_sac", "sac", "watt"),
        0
    )
