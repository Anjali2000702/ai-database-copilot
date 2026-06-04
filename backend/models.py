from sqlalchemy import Column, Integer, String, Float
from database import Base

class Customer(Base):
    __tablename__ = "customers"
    
    c_custkey = Column(Integer, primary_key=True, index=True)
    c_name = Column(String)
    c_address = Column(String)
    c_nationkey = Column(Integer)
    c_phone = Column(String)
    c_acctbal = Column(Float)
    c_mktsegment = Column(String)
    c_comment = Column(String)

class Order(Base):
    __tablename__ = "orders"
    
    o_orderkey = Column(Integer, primary_key=True, index=True)
    o_custkey = Column(Integer)
    o_orderstatus = Column(String)
    o_totalprice = Column(Float)
    o_orderdate = Column(String)
    o_orderpriority = Column(String)
    o_clerk = Column(String)
    o_shippriority = Column(Integer)
    o_comment = Column(String)