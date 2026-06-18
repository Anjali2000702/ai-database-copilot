import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# .env file ko load karna zaroori hai
load_dotenv()

# Cloud database ka link uthana
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Engine create karna (Neon PostgreSQL ke liye)
#engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, pool_recycle=1800)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()