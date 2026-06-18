import sys
import os

# Add backend directory to path so imports work from root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from sqlalchemy import text # Naya import
from database import engine # Database connection import karna

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'agents')))
from workflow import app as agent_app

app = FastAPI(title="AI Database Copilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    user_query: str

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Database Copilot API!"}

@app.post("/api/chat")
def chat_with_agent(request: QueryRequest):
    print(f"\n📡 Frontend se query aayi: {request.user_query}")
    
    # 1. AI Pipeline chalana
    input_state = {"user_query": request.user_query}
    result = agent_app.invoke(input_state)
    
    # 2. Database mein query actually run karna (Sirf agar safe ho)
    query_result_data = []
    if result.get("is_safe"):
        try:
            with engine.connect() as conn:
                db_result = conn.execute(text(result.get("sql_query")))
                # Data ko list of dictionaries mein convert karna
                query_result_data = [dict(row) for row in db_result.mappings()]
        except Exception as e:
            print(f"Database Run Error: {e}")
            query_result_data = [{"error": "Could not execute query on database."}]

    return {
        "sql_query": result.get("sql_query"),
        "estimated_cost": result.get("estimated_cost"),
        "explanation": result.get("final_response"),
        "data": query_result_data  # 👈 Naya Data Field jo frontend ko jayega
    }