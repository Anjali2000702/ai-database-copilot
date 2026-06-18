import csv
from datetime import datetime
from database import SessionLocal
from models import Customer, Order, OrderItem

def parse_date(date_str):
    if not date_str or date_str.strip() == "":
        return None
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

def seed_real_data():
    db = SessionLocal()
    print("🚀 Starting Data Pipeline: Seeding Real Olist Dataset...")

    LIMIT = 10000 
    CHUNK_SIZE = 2000

    try:
        # 1. Seeding Customers
        print("\n👥 Reading customers.csv...")
        customers_to_insert = []
        with open("customers.csv", mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= LIMIT: break
                customers_to_insert.append(Customer(
                    customer_id=row["customer_id"],
                    customer_unique_id=row["customer_unique_id"],
                    customer_zip_code_prefix=int(row["customer_zip_code_prefix"]),
                    customer_city=row["customer_city"],
                    customer_state=row["customer_state"]
                ))
        
        # Look-up dictionary banana data integrity ke liye (O(1) Search Speed)
        valid_customer_ids = {c.customer_id for c in customers_to_insert}

        print(f"📦 Uploading {len(customers_to_insert)} customers to Neon Cloud...")
        for chunk_start in range(0, len(customers_to_insert), CHUNK_SIZE):
            db.add_all(customers_to_insert[chunk_start:chunk_start + CHUNK_SIZE])
            db.commit()
            print(f"   ↳ Uploaded rows {chunk_start} to {chunk_start + min(CHUNK_SIZE, len(customers_to_insert)-chunk_start)}")

        # 2. Seeding Orders (with Strict Lookup Filter)
        print("\n📦 Reading orders.csv...")
        orders_to_insert = []
        with open("orders.csv", mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                if count >= LIMIT: break
                # Safety Gate: Sirf wahi orders uthao jinka customer database mein ja chuka hai
                if row["customer_id"] in valid_customer_ids:
                    orders_to_insert.append(Order(
                        order_id=row["order_id"],
                        customer_id=row["customer_id"],
                        order_status=row["order_status"],
                        order_purchase_timestamp=parse_date(row["order_purchase_timestamp"]),
                        order_approved_at=parse_date(row["order_approved_at"]),
                        order_delivered_carrier_date=parse_date(row["order_delivered_carrier_date"]),
                        order_delivered_customer_date=parse_date(row["order_delivered_customer_date"]),
                        order_estimated_delivery_date=parse_date(row["order_estimated_delivery_date"])
                    ))
                    count += 1

        valid_order_ids = {o.order_id for o in orders_to_insert}

        print(f"📦 Uploading {len(orders_to_insert)} matching orders to Neon Cloud...")
        for chunk_start in range(0, len(orders_to_insert), CHUNK_SIZE):
            db.add_all(orders_to_insert[chunk_start:chunk_start + CHUNK_SIZE])
            db.commit()
            print(f"   ↳ Uploaded rows {chunk_start} to {chunk_start + min(CHUNK_SIZE, len(orders_to_insert)-chunk_start)}")

        # 3. Seeding Order Items
        print("\n💰 Reading order_items.csv...")
        items_to_insert = []
        with open("order_items.csv", mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                if count >= LIMIT: break
                if row["order_id"] in valid_order_ids:
                    items_to_insert.append(OrderItem(
                        order_id=row["order_id"],
                        order_item_id=int(row["order_item_id"]),
                        product_id=row["product_id"],
                        seller_id=row["seller_id"],
                        shipping_limit_date=parse_date(row["shipping_limit_date"]),
                        price=float(row["price"]),
                        freight_value=float(row["freight_value"])
                    ))
                    count += 1

        print(f"📦 Uploading {len(items_to_insert)} order line items to Neon Cloud...")
        for chunk_start in range(0, len(items_to_insert), CHUNK_SIZE):
            db.add_all(items_to_insert[chunk_start:chunk_start + CHUNK_SIZE])
            db.commit()
            print(f"   ↳ Uploaded rows {chunk_start} to {chunk_start + min(CHUNK_SIZE, len(items_to_insert)-chunk_start)}")

        print("\n🎉 data pipeline completed successfully! Real Olist Records Loaded without Conflicts!")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error during seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_real_data()
    