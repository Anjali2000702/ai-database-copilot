import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# 1. API Key Load Karna
load_dotenv("../backend/.env")
api_key = os.getenv("GEMINI_API_KEY")

# 2. Gemini Initialize Karna (Hum best model use kar rahe hain)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)

# 3. 🧠 Database Schema (Yeh AI ko batayega ki database kaisa dikhta hai)
schema = """
Table: customers
Columns: c_custkey (Integer, Primary Key), c_name (String), c_address (String), c_nationkey (Integer), c_phone (String), c_acctbal (Float), c_mktsegment (String), c_comment (String)

Table: orders
Columns: o_orderkey (Integer, Primary Key), o_custkey (Integer), o_orderstatus (String), o_totalprice (Float), o_orderdate (String), o_orderpriority (String), o_clerk (String), o_shippriority (Integer), o_comment (String)
"""

# 4. System Prompt Banana
prompt_template = ChatPromptTemplate.from_messages([
    ("system", f"You are an expert PostgreSQL developer. Your job is to convert English requests into valid PostgreSQL queries.\n\nHere is the database schema:\n{schema}\n\nONLY return the SQL query. Do not include markdown formatting like ```sql, and do not explain the query."),
    ("human", "{user_query}")
])

# 5. The Translation Function
def generate_sql(user_query):
    print(f"\n🗣️ User Query: {user_query}")
    print("⏳ AI soch raha hai aur SQL generate kar raha hai...")
    
    # LangChain pipe syntax: Prompt ko LLM se connect karna
    chain = prompt_template | llm
    
    # AI ko query bhej kar response lena
    response = chain.invoke({"user_query": user_query})
    
    print("\n✨ Generated SQL Query:")
    print("-" * 50)
    print(response.content.strip())
    print("-" * 50)

# 6. Test Run
if __name__ == "__main__":
    # Yahan hum AI se ek realistic business question pooch rahe hain
    test_query = "Show me the total price of all orders placed by the customer named 'Customer#000000002'."
    generate_sql(test_query)