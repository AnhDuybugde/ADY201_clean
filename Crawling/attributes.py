import json
from collections import defaultdict
from scraper import fetch_products
from parser import extract_attributes


def show_attribute_samples(max_values=5):
    products = fetch_products()
    attribute_samples = defaultdict(set)

    # Duyệt qua tất cả sản phẩm và gom các giá trị cho mỗi attribute
    for p in products:
        attrs_raw = p.get("general", {}).get("attributes")
        attrs = extract_attributes(attrs_raw)
        for k, v in attrs.items():
            if v:
                attribute_samples[k].add(str(v).strip())
    
    # In ra mỗi attribute và khoảng 5 giá trị ví dụ
    for attr, values in sorted(attribute_samples.items()):
        samples = list(values)[:max_values]
        print(f"\n🔹 {attr} ({len(values)} giá trị):")
        for val in samples:
            print(f"   - {val}")


if __name__ == "__main__":
    show_attribute_samples(max_values=5)
