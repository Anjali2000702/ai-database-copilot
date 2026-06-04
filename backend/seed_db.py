from database import SessionLocal
from models import Customer, Order

# Database connection start karte hain
db = SessionLocal()

def seed_data():
    # Check karte hain ki pehle se data toh nahi hai
    if db.query(Customer).count() > 0:
        print("Data already exists! Skipping...")
        return

    print("Loading TPC-H dummy data...")

    # Customers ka data add kar rahe hain
    c1 = Customer(c_custkey=1, c_name="Customer#000000001", c_address="Address 1", c_nationkey=15, c_phone="25-989-741-2988", c_acctbal=711.56, c_mktsegment="BUILDING", c_comment="Regular")
    c2 = Customer(c_custkey=2, c_name="Customer#000000002", c_address="Address 2", c_nationkey=1, c_phone="11-719-748-3364", c_acctbal=121.65, c_mktsegment="AUTOMOBILE", c_comment="VIP")
    
    db.add_all([c1, c2])
    db.commit() # Changes ko database mein save karna

    # Orders ka data add kar rahe hain
    o1 = Order(o_orderkey=1, o_custkey=1, o_orderstatus="O", o_totalprice=173665.47, o_orderdate="2025-01-01", o_orderpriority="1-URGENT", o_clerk="Clerk#001", o_shippriority=0, o_comment="Quick")
    o2 = Order(o_orderkey=2, o_custkey=2, o_orderstatus="F", o_totalprice=46929.18, o_orderdate="2025-01-15", o_orderpriority="2-HIGH", o_clerk="Clerk#002", o_shippriority=0, o_comment="Standard")

    db.add_all([o1, o2])
    db.commit()

    print("Data loaded successfully!")

# Function ko run karna
seed_data()
db.close()