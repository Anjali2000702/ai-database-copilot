import os
from typing import TypedDict
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
import sqlglot
from sqlglot import exp

# Humara naya ML model import kar rahe hain
from cost_predictor import predict_query_cost

# 1. API Setup
load_dotenv("../backend/.env")
api_key = os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)

# 2. State Definition (Isme 'estimated_cost' add kiya hai)
class AgentState(TypedDict):
    user_query: str
    sql_query: str
    is_safe: bool
    estimated_cost: str
    final_response: str

# 3. Agent 1: The Translator
def generate_sql_node(state: AgentState):
    print("\n[Agent 1] Translator 🧠 : English ko SQL mein badal raha hai...")
    schema = """
    Table: customers (c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment)
    Table: orders (o_orderkey, o_custkey, o_orderstatus, o_totalprice, o_orderdate, o_orderpriority, o_clerk, o_shippriority, o_comment)
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"Convert English to PostgreSQL query. Schema: {schema}. ONLY return SQL, no markdown."),
        ("human", "{user_query}")
    ])
    chain = prompt | llm
    response = chain.invoke({"user_query": state["user_query"]})
    return {"sql_query": response.content.strip()}

# 4. Agent 2: The Gatekeeper
def validate_sql_node(state: AgentState):
    print("[Agent 2] Gatekeeper 🛡️ : SQL ki safety check kar raha hai...")
    sql = state["sql_query"]
    try:
        parsed = sqlglot.parse_one(sql, read="postgres")
        dangerous_commands = (exp.Drop, exp.Delete, exp.Update, exp.Insert, exp.Alter)
        
        if parsed.find(dangerous_commands):
            print("❌ Gatekeeper Alert: Destructive query mili! Execution Blocked.")
            return {"is_safe": False, "final_response": "Security Alert: System blocked a dangerous query.", "estimated_cost": "N/A"}
            
        print("✅ Gatekeeper: Query bilkul safe hai.")
        return {"is_safe": True}
    except Exception as e:
        return {"is_safe": False, "final_response": "Error: AI generated invalid SQL.", "estimated_cost": "N/A"}

# 5. Agent 3: Cost Predictor (ML)
def predict_cost_node(state: AgentState):
    print("[Agent 3] Cost Predictor 📈 : Query execution time predict kar raha hai...")
    time_ms = predict_query_cost(state["sql_query"])
    return {"estimated_cost": f"{time_ms} ms"}

# 6. Agent 4: The Trust Builder
def explain_sql_node(state: AgentState):
    print("[Agent 4] Trust Builder 🗣️ : Query ko English mein samjha raha hai...")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Explain this SQL query simply for a business user in 1-2 lines."),
        ("human", "Explain: {sql_query}")
    ])
    chain = prompt | llm
    response = chain.invoke({"sql_query": state["sql_query"]})
    return {"final_response": response.content.strip()}

# 7. Routing Logic
def route_query(state: AgentState):
    if state["is_safe"]:
        return "predict_cost_node"  # Safe hai toh ab pehle Cost predict karo
    else:
        return END

# 8. LangGraph Pipeline Banana
workflow = StateGraph(AgentState)

workflow.add_node("generate_sql_node", generate_sql_node)
workflow.add_node("validate_sql_node", validate_sql_node)
workflow.add_node("predict_cost_node", predict_cost_node)
workflow.add_node("explain_sql_node", explain_sql_node)

# Flow Setup (Agent 1 -> 2 -> 3 -> 4)
workflow.set_entry_point("generate_sql_node")
workflow.add_edge("generate_sql_node", "validate_sql_node")
workflow.add_conditional_edges("validate_sql_node", route_query)
workflow.add_edge("predict_cost_node", "explain_sql_node")
workflow.add_edge("explain_sql_node", END)

app = workflow.compile()

# 9. Final Test Run
if __name__ == "__main__":
    test_input = {"user_query": "What is the total price of orders placed by customer ID 1?"}
    print(f"🗣️ User Request: {test_input['user_query']}")
    
    result = app.invoke(test_input)
    
    print("\n🎯 FINAL ENTERPRISE PIPELINE OUTPUT:")
    print("-" * 60)
    print(f"💻 Generated SQL : {result.get('sql_query')}")
    print(f"⏱️ Estimated Time: {result.get('estimated_cost')}")
    print(f"📝 Explanation   : {result.get('final_response')}")
    print("-" * 60)