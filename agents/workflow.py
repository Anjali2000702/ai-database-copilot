import os
import sys
from typing import TypedDict
from langgraph.graph import StateGraph, END

# 1. Cross-Folder Import Setup (Taaki backend folder seedha agents folder ko read kar sake)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# 2. Humare Update Kiye Hue Real Agents ko Import Karna
from agents.nl2sql import generate_sql
from agents.validator import is_safe_query
from agents.cost_predictor import predict_query_cost
from agents.explanation import explain_query

# 3. State Definition
class AgentState(TypedDict):
    user_query: str
    sql_query: str
    is_safe: bool
    estimated_cost: str
    final_response: str

# 4. Agent 1: The Translator Node
def generate_sql_node(state: AgentState):
    print("\n[Node 1] Translator 🧠 : English ko SQL mein badal raha hai...")
    # Seedha import kiya hua agent function call kar rahe hain
    sql = generate_sql(state["user_query"])
    return {"sql_query": sql}

# 5. Agent 2: The Gatekeeper Node
def validate_sql_node(state: AgentState):
    print("[Node 2] Gatekeeper 🛡️ : SQL ki safety check kar raha hai...")
    safe = is_safe_query(state["sql_query"])
    if not safe:
        return {"is_safe": False, "final_response": "Security Alert: System blocked a dangerous or invalid query.", "estimated_cost": "N/A"}
    return {"is_safe": True}

# 6. Agent 3: Cost Predictor Node
def predict_cost_node(state: AgentState):
    print("[Node 3] Cost Predictor 📈 : Query execution time predict kar raha hai...")
    time_ms = predict_query_cost(state["sql_query"])
    return {"estimated_cost": f"{time_ms} ms"}

# 7. Agent 4: The Trust Builder Node
def explain_sql_node(state: AgentState):
    print("[Node 4] Trust Builder 🗣️ : Query ko English mein samjha raha hai...")
    explanation = explain_query(state["sql_query"])
    return {"final_response": explanation}

# 8. Routing Logic (LangGraph Edge)
def route_query(state: AgentState):
    if state["is_safe"]:
        return "predict_cost_node"  # Safe hai toh aage badho
    else:
        return END  # Dangerous hai toh pipeline yahin rok do

# 9. LangGraph Pipeline Banana
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

# 10. Final Test Run (Using Real Olist Dataset)
if __name__ == "__main__":
    test_input = {"user_query": "Show me the total price of all orders placed in the city of 'sao paulo'."}
    print(f"🗣️ User Request: {test_input['user_query']}")
    
    result = app.invoke(test_input)
    
    print("\n🎯 FINAL ENTERPRISE PIPELINE OUTPUT:")
    print("-" * 60)
    print(f"💻 Generated SQL : {result.get('sql_query')}")
    print(f"⏱️ Estimated Time: {result.get('estimated_cost')}")
    print(f"📝 Explanation   : {result.get('final_response')}")
    print("-" * 60)