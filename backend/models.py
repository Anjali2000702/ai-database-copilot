from sqlalchemy import Column, String, Float, DateTime, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    
    customer_id = Column(String, primary_key=True, index=True)
    customer_unique_id = Column(String, index=True)
    customer_zip_code_prefix = Column(Integer)
    customer_city = Column(String)
    customer_state = Column(String)

class Order(Base):
    __tablename__ = "orders"
    
    order_id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, ForeignKey("customers.customer_id"), index=True)
    order_status = Column(String)
    order_purchase_timestamp = Column(DateTime)
    order_approved_at = Column(DateTime, nullable=True)
    order_delivered_carrier_date = Column(DateTime, nullable=True)
    order_delivered_customer_date = Column(DateTime, nullable=True)
    order_estimated_delivery_date = Column(DateTime)

class OrderItem(Base):
    __tablename__ = "order_items"
    
    # Olist mein ek order mein multiple items ho sakte hain, isliye composite key use karenge
    order_id = Column(String, ForeignKey("orders.order_id"), primary_key=True, index=True)
    order_item_id = Column(Integer, primary_key=True)
    product_id = Column(String, index=True)
    seller_id = Column(String)
    shipping_limit_date = Column(DateTime)
    price = Column(Float)
    freight_value = Column(Float)