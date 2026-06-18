# 🤖 AI Database Copilot (Enterprise-Grade Data Assistant)

An end-to-end Full-Stack AI application that allows non-technical business users to interact with a PostgreSQL database using natural language. It translates English to SQL, validates for security, predicts execution cost using Machine Learning, and explains the results in plain English.

## 🌟 Key Features
- **🧠 The Translator (NL2SQL):** Converts natural language queries into accurate PostgreSQL syntax using Gemini 2.5 Flash and LangGraph.
- **🛡️ The Gatekeeper (Security Check):** Uses `sqlglot` to parse the Abstract Syntax Tree (AST) and strictly blocks destructive queries (DROP, DELETE, UPDATE) to prevent SQL Injection.
- **📈 Cost Predictor (XGBoost ML):** A trained Machine Learning model that analyzes query complexity (joins, tables, conditions) to predict execution time *before* hitting the database.
- **🗣️ The Trust Builder:** Translates complex SQL logic back into simple English for business users.
- **⚡ Real-Time Execution:** Safely executes approved queries on the PostgreSQL database and renders the actual data in a dynamic React data table.

## 🛠️ Tech Stack
- **Frontend:** React, Vite, CSS3,Axios
- **Backend:** Python, FastAPI, SQLAlchemy , Uvicorn
- **AI & Orchestration:** Google Gemini API, LangGraph, LangChain
- **Machine Learning:** XGBoost, Pandas, Scikit-Learn
- **Database:** PostgreSQL

## 🚀 Architecture Workflow
User Input (English) ➡️ LangGraph Pipeline ➡️ SQL Generation ➡️ AST Security Validation ➡️ ML Cost Prediction ➡️ Database Execution ➡️ Simple English Explanation ➡️ React UI Presentation.