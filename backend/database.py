from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# ⚠️ DHYAN DEIN: 'YOUR_PASSWORD' ko hatakar apna actual PostgreSQL password likhein (jaise admin123)
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:27200@localhost:5432/copilot_db"

# Engine database se direct connection banata hai
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Session database ke sath queries execute karne ke kaam aata hai
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class jisse humari saari AI tables banengi
Base = declarative_base()