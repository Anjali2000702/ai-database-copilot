import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# 1. API Key Load Karna (Dynamic Absolute Path to avoid terminal errors)
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, "..", "backend", ".env")
load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")

# Safety net for LangChain
if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key

# 2. Gemini Initialize Karna (Setting temperature=0.0 for factual queries)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key, temperature=0.0)

# 3. 🧠 Real-World Brazilian E-Commerce (Olist) Schema
schema = """
Table: customers
Columns: 
  - customer_id (VARCHAR, Primary Key) : Unique alphanumeric identifier for each customer order instance.
  - customer_unique_id (VARCHAR) : Unique core identity of the customer.
  - customer_zip_code_prefix (Integer) : Zip code area code.
  - customer_city (VARCHAR) : City name (stored strictly in lower case like 'sao paulo', 'rio de janeiro').
  - customer_state (VARCHAR) : State abbreviation code (stored in upper case like 'SP', 'RJ', 'MG').

Table: orders
Columns: 
  - order_id (VARCHAR, Primary Key) : Unique alphanumeric identifier for each order.
  - customer_id (VARCHAR, Foreign Key -> customers.customer_id) : Links to the customer row.
  - order_status (VARCHAR) : Status of order (e.g., 'delivered', 'shipped', 'invoiced', 'canceled').
  - order_purchase_timestamp (TIMESTAMP) : The exact date & time order was placed.
  - order_approved_at (TIMESTAMP) : Order payment approval timestamp.
  - order_delivered_carrier_date (TIMESTAMP) : Handover date to carrier courier.
  - order_delivered_customer_date (TIMESTAMP) : Actual delivery date to the end customer.
  - order_estimated_delivery_date (TIMESTAMP) : Expected delivery date shown to user.

Table: order_items
Columns: 
  - order_id (VARCHAR, Primary Key, Foreign Key -> orders.order_id) : Order identifier.
  - order_item_id (Integer, Primary Key) : Sequential item number within the same order (1, 2, 3 etc).
  - product_id (VARCHAR) : Alphanumeric product identifier.
  - seller_id (VARCHAR) : Alphanumeric seller identifier.
  - shipping_limit_date (TIMESTAMP) : Shipping limit constraint.
  - price (Float) : Individual item product cost in Brazilian Real.
  - freight_value (Float) : Shipping cost / freight value.

Join Strategy Matrix:
- To query sales metrics or item performance by city or state, JOIN 'orders' with 'customers' ON orders.customer_id = customers.customer_id, then JOIN with 'order_items' ON orders.order_id = order_items.order_id.
- Total order value or total sales equals SUM(order_items.price).
- Always use LOWER(customer_city) = LOWER('user_input') when filtering city columns to eliminate casing mismatches.
"""

# 4. Production System Prompt Template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", f"You are an expert PostgreSQL developer. Your job is to convert English requests into valid PostgreSQL queries based on the Olist E-commerce schema provided below.\n\nHere is the database schema:\n{schema}\n\nONLY return the executable raw SQL query string. Do NOT include markdown code blocks like ```sql, and do not explain the query. Do not invent columns or tables."),
    ("human", "{user_query}")
])

# 5. The Translation Function (LangChain Pipeline syntax)
def generate_sql(user_query):
    print(f"\n🗣️ User Query: {user_query}")
    print("⏳ AI soch raha hai aur SQL generate kar raha hai...")
    
    # LangChain LCEL pipeline expressions
    chain = prompt_template | llm
    
    # AI ko chain invoke karke response catch karna
    response = chain.invoke({"user_query": user_query})
    
    sql_query = response.content.strip()
    
    # Absolute safety sweep to ensure no markdown wrapping slips through
    if sql_query.startswith("```sql"):
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
    elif sql_query.startswith("```"):
        sql_query = sql_query.replace("```", "").strip()

    print("\n✨ Generated SQL Query:")
    print("-" * 50)
    print(sql_query)
    print("-" * 50)
    
    return sql_query

# 6. Clean Test Run
if __name__ == "__main__":
    # Naye dataset ke matching complex query check karna
    test_query = "Show me the total price of all orders placed in the city of 'sao paulo'."
    generate_sql(test_query)