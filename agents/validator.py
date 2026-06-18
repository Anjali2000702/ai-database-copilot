import sqlglot
from sqlglot import exp

def is_safe_query(sql_query):
    print(f"\n🛡️ Validation Agent analyzing: {sql_query}")
    try:
        # sqlglot query ko read karke uska logic tree (Abstract Syntax Tree) banata hai
        parsed_expression = sqlglot.parse_one(sql_query, read="postgres")
        
        # Un saari commands ki list jo database ka data mita ya badal sakti hain
        dangerous_commands = (exp.Drop, exp.Delete, exp.Update, exp.Insert, exp.Alter)
        
        # Check karna ki query mein kahin bhi koi dangerous command toh nahi chhupi hai
        if parsed_expression.find(dangerous_commands):
            print("❌ SECURITY ALERT: Destructive query detected! Execution Blocked.")
            return False
            
        print("✅ Query is SAFE (Read-Only).")
        return True
        
    except sqlglot.errors.ParseError as e:
        # Agar AI ne galat (invalid) SQL generate ki, toh yahan block ho jayegi
        print(f"❌ SYNTAX ERROR: Invalid SQL generated. Details: {e}")
        return False

# Agent ko test karne ke liye ek dummy run (Now using Real Olist Schema)
if __name__ == "__main__":
    print("--- Test 1: Safe Query ---")
    safe_sql = "SELECT SUM(price) FROM order_items WHERE order_id = 'e481f51cbdc54678b7cc49136f2d6af7';"
    is_safe_query(safe_sql)
    
    print("\n--- Test 2: Destructive Query ---")
    danger_sql = "DELETE FROM customers WHERE customer_city = 'sao paulo';"
    is_safe_query(danger_sql)