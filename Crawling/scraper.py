# src/scraper.py
import requests
from config import URL, HEADERS, CATEGORY_ID, PROVINCE_ID, MAX_PAGES
import time

# Nếu cần, có thể giới hạn vài tỉnh để test nhanh
province_list = {
   1: "Hà Nội",
    2: "Hà Giang",
    3: "Cao Bằng",
    4: "Bắc Kạn",
    5: "Tuyên Quang",
    6: "Lào Cai",
    7: "Điện Biên",
    8: "Lai Châu",
    9: "Sơn La",
    10: "Yên Bái",
    11: "Hoà Bình",
    12: "Thái Nguyên",
    13: "Lạng Sơn",
    14: "Quảng Ninh",
    15: "Đà Nẵng",
    16: "Bắc Giang",
    17: "Phú Thọ",
    18: "Vĩnh Phúc",
    19: "TP.HCM",
    20: "Bắc Ninh",
    21: "Hải Dương",
    22: "Hải Phòng",
    23: "Hưng Yên",
    24: "Thái Bình",
    25: "Hà Nam",
    26: "Nam Định",
    27: "Ninh Bình",
    28: "Thanh Hóa",
    29: "Nghệ An",
    30: "Cần Thơ",
    31: "Hà Tĩnh",
    32: "Quảng Bình",
    33: "Quảng Trị",
    34: "Thừa Thiên Huế",
    35: "Quảng Nam",
    36: "Quảng Ngãi",
    37: "Kon Tum",
    38: "Gia Lai",
    39: "Đắk Lắk",
    40: "Đắk Nông",
    41: "Lâm Đồng",
    42: "Bình Phước",
    43: "Tây Ninh",
    44: "Bình Dương",
    45: "Đồng Nai",
    46: "Bà Rịa - Vũng Tàu",
    47: "Long An",
    48: "Tiền Giang",
    49: "Bến Tre",
    50: "Trà Vinh",
    51: "Vĩnh Long",
    52: "Đồng Tháp",
    53: "An Giang",
    54: "Kiên Giang",
    55: "Cà Mau",
    56: "Bạc Liêu",
    57: "Sóc Trăng",
    58: "Ninh Thuận",
    59: "Bình Thuận",
    60: "Khánh Hòa",
    61: "Phú Yên",
    62: "Bình Định",
    63: "Quảng Nam"
}

def fetch_products():
    all_products = []

    for province_id, province_name in province_list.items():
        print(f"\nĐang lấy dữ liệu cho {province_name} (ID = {province_id})")

        for page in range(1, MAX_PAGES + 1):
            print(f"Trang {page}...")

            payload = {
                "query": f"""
                query GetProductsByCateId{{
                    products(
                        filter: {{
                            static: {{
                                categories: ["3"],
                                province_id: {province_id},
                                stock: {{
                                    from: 0
                                }},
                                stock_available_id: [46, 56, 152, 4920],
                                filter_price: {{from: 0, to: 63990000}}
                            }},
                            dynamic: {{}}
                        }},
                        page: {page},
                        size: 500,
                        sort: [{{view: desc}}]
                    ){{
                        general{{
                            product_id
                            name
                            manufacturer
                            attributes
                            sku
                            url_key
                            categories{{
                                categoryId
                                name
                            }}
                            review{{
                                total_count
                                average_rating
                            }}
                        }},
                        filterable{{
                            price
                            special_price
                            is_installment
                            stock_available_id
                            promotion_information
                            flash_sale_types
                        }}
                    }}
                }}
                """,
                "variables": {}
            }

            try:
                res = requests.post(URL, headers=HEADERS, json=payload)
                if res.status_code != 200:
                    print(f"HTTP {res.status_code}, bỏ qua {province_name}.")
                    break

                data = res.json()
                products = data.get("data", {}).get("products", [])
                if not products:
                    print(f"Trang {page} không có dữ liệu, dừng lại.")
                    break

                for p in products:
                    p["province_id"] = province_id
                    p["province_name"] = province_name

                all_products.extend(products)
                print(f"Lấy xong trang {page}, tổng cộng {len(all_products)} sản phẩm.")
                time.sleep(1)

            except Exception as e:
                print(f"Lỗi khi lấy dữ liệu: {e}")
                break

    print(f"\nHoàn tất! Tổng cộng {len(all_products)} sản phẩm lấy được.")
    return all_products