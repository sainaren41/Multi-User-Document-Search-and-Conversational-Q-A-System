# Multi-User-Document-Search-and-Conversational-Q-A-System


🔍 Role-based conversational Q&A system using:
- FastAPI (Backend)
- Streamlit (Frontend)
- SQLite (Auth + Role Permissions)
- FAISS (Vector DB for search)
- Ollama (Local LLM)

## Features
- Sign up / Sign in with roles
- Role-based PDF access (manager, analyst_1, analyst_2, analyst_3)
- Conversational Q&A with source documents
- Local deployment (no cloud dependencies)

## Run Locally

### 1. Backend (FastAPI)
```bash
cd backend
uvicorn main:app --reload

### 2. Frontend (Streamlit)
cd frontend
streamlit run app.py

### 3. Requirements
pip install -r requirements.txt

