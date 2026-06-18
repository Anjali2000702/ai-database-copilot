import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# 1. API Key Load Karna (Dynamic Absolute Path)
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, "..", "backend", ".env")
load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key

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
    
    return response.content.strip()

# 5. Test Run (Now using Real Olist Schema)
if __name__ == "__main__":
    # Hum naye Olist database ki query bhej kar check kar rahe hain
    test_sql = "SELECT SUM(price) FROM order_items WHERE order_id = 'e481f51cbdc54678b7cc49136f2d6af7';"
    explain_query(test_sql)