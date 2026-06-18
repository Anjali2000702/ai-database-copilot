from database import engine
from models import Base

def reset_database():
    print("🔄 Connecting to Neon Cloud Database...")
    
    # 1. Purani tables ko drop/delete karna taaki schema conflict na ho
    print("🗑️ Dropping old tables (customers, orders) if they exist...")
    Base.metadata.drop_all(bind=engine)
    
    # 2. Nayi structures ke sath saari tables dubara create karna
    print("🏗️ Creating new Olist E-commerce tables (customers, orders, order_items)...")
    Base.metadata.create_all(bind=engine)
    
    print("✅ Success! New tables created successfully on Neon Cloud!")

if __name__ == "__main__":
    reset_database()