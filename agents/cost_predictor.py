import pandas as pd
import xgboost as xgb
import warnings

# Terminal warnings ko clean rakhne ke liye
warnings.filterwarnings('ignore')

# 1. Dummy Historical Data (Past Queries)
# Features: [num_joins, num_tables, num_conditions] -> Target: execution_time_ms
data = {
    'num_joins': [0, 1, 2, 3, 1, 0, 4, 2],
    'num_tables': [1, 2, 3, 4, 2, 1, 5, 3],
    'num_conditions': [1, 2, 1, 3, 1, 0, 4, 2],
    'execution_time_ms': [10, 45, 120, 310, 50, 5, 600, 135]
}
df = pd.DataFrame(data)

# Data split kar rahe hain (X = Features, y = Target Output)
X = df[['num_joins', 'num_tables', 'num_conditions']]
y = df['execution_time_ms']

# 2. XGBoost Model Training
print("⏳ XGBoost Model train ho raha hai...")
model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=50)
model.fit(X, y)
print("✅ Model Training Complete!\n")

# 3. Cost Prediction Agent Logic
def predict_query_cost(sql_query):
    print(f"📈 Cost Predictor analyzing: {sql_query}")
    
    # Query ke structure ko analyze karke uske features extract karna
    joins = sql_query.upper().count("JOIN")
    tables = sql_query.upper().count("FROM") + joins
    conditions = sql_query.upper().count("WHERE") + sql_query.upper().count("AND")
    
    # Features ko dataframe mein convert karna prediction ke liye
    features = pd.DataFrame(
        [[joins, tables, conditions]],
        columns=['num_joins', 'num_tables', 'num_conditions']
    )
    
    # Prediction lagana
    predicted_time = model.predict(features)[0]
    
    print(f"⏱️ Estimated Execution Time: {predicted_time:.2f} ms")
    return round(float(predicted_time), 2)

# 4. Agent ko Test Karne ke liye ek dummy run (Now using Real Olist Schema)
if __name__ == "__main__":
    # Ek complex query jisme 2 JOINs aur 1 WHERE condition hai (Sao Paulo city test)
    test_sql = "SELECT SUM(oi.price) FROM order_items AS oi JOIN orders AS o ON oi.order_id = o.order_id JOIN customers AS c ON o.customer_id = c.customer_id WHERE LOWER(c.customer_city) = LOWER('sao paulo')"
    predict_query_cost(test_sql)