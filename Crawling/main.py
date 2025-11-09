# src/main.py
from scraper import fetch_products
from parser import parse_product
from storage import create_table, insert_many

def main():
    print(" Bắt đầu tiến trình cào và lưu dữ liệu...\n")

    create_table()

    raw_products = fetch_products()
    parsed_rows = [parse_product(p) for p in raw_products]
    
    insert_many(parsed_rows)

    print("\n Hoàn tất toàn bộ quy trình!")

if __name__ == "__main__":
    main()
