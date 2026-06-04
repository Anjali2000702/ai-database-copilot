import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# 1. API Key Load Karna
load_dotenv("../backend/.env")
api_key = os.getenv("GEMINI_API_KEY")

# 2. Gemini Initialize Karna
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)

# 3. System Prompt Banana
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are an Explanation Agent (The Trust Builder) for a Database Copilot. Your job is to read a PostgreSQL query and explain exactly what it does in simple, plain English for a non-technical business user. Keep it concise, friendly, and avoid using complex database jargon like 'JOIN' or 'Primary Key' if possible. Just explain the business outcome."),
    ("human", "Explain this SQL query: {sql_query}")
])

# 4. The Explanation Function
def explain_query(sql_query):
    print(f"\n🔍 Explanation Agent reading: {sql_query}")
    print("⏳ AI query ko simple English mein convert kar raha hai...")
    
    # LangChain pipe syntax
    chain = prompt_template | llm
    
    # AI ko query bhej kar response lena
    response = chain.invoke({"sql_query": sql_query})
    
    print("\n🗣️ Simple English Explanation:")
    print("-" * 50)
    print(response.content.strip())
    print("-" * 50)

# 5. Test Run
if __name__ == "__main__":
    # Hum ek safe test query bhej kar check kar rahe hain
    test_sql = "SELECT SUM(o_totalprice) FROM orders WHERE o_custkey = 1;"
    explain_query(test_sql)