
# 📄 Multi-User Document Search & Conversational Q&A System

This project is a **role-based conversational Q&A system** built with **FastAPI** (backend), **Streamlit** (frontend), and **SQLite** (local DB).
Users can **sign up, sign in**, and based on their **role**, they are allowed to query only specific PDF documents.
The system uses **LangChain, FAISS, Sentence-Transformers, and Ollama** for embeddings, vector storage, and conversational AI.

---

## ✨ Features

* 🔑 **User Authentication**: Sign up & sign in with email + password (hashed with bcrypt).
* 👥 **Role-Based Access**:

  * `manager`: access all documents
  * `analyst_1`: access 1 document
  * `analyst_2`: access 2 documents
  * `analyst_3`: access 3 documents
    
* 📚 **Document Search**: Load multiple PDFs from subfolders automatically.
* 💬 **Conversational Q&A**: Ask natural language queries about documents.
* 🗄️ **Local Storage**: SQLite for users, permissions, and audit logs.
* 🎨 **Frontend**: Streamlit interface for login, document access, and Q&A.
* ⚡ **Backend**: FastAPI endpoints for signup, login, chat, and audit logs.
* 🛠️ **Vector Database**: FAISS for fast similarity search.
* 🤖 **Embeddings/LLM**: Sentence-Transformers for embeddings + Ollama for local inference.

---

## 📂 Project Structure

```
Multi-User-Document-Search-QA-System/
│
├── backend/
│   ├── main.py              # FastAPI app (auth, chat, document filtering, audit logs)
│   ├── db_setup.py          # SQLite DB initialization (users, documents, permissions, audit logs)
│   ├── seed_permissions.py  # Seeds roles and allowed document access
│
├── VDB_index/               # FAISS vector database storage
├── data/                    # PDF documents in subfolders
│   ├── Meta/
│   ├── Netflix/
│   ├── Amazon/
│   ├── Google/
│   ├── Microsoft/
│
├── .env                     # Environment variables (secret keys, DB path, etc.)
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
```

## 🛠️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/Multi-User-Document-Search-QA-System.git
cd Multi-User-Document-Search-QA-System
```

### 2️⃣ Create a Virtual Environment (Python 3.11.9 recommended)

```bash
python3.11 -m venv .venv
source .venv/bin/activate     # On Linux/Mac
.venv\Scripts\activate        # On Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Initialize Database

```bash
python backend/db_setup.py
python backend/seed_permissions.py
```

---

## 🚀 Running the Project

### Backend (FastAPI)

```bash
uvicorn backend.main:app --reload
```

Runs at → [http://127.0.0.1:8000](http://127.0.0.1:8000)

API Docs → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### Frontend (Streamlit)

```bash
streamlit run frontend/app.py
```

Runs at → [http://localhost:8501](http://localhost:8501)

---

## 🔑 User Roles & Access

| Role      | Documents Accessible |
| --------- | -------------------- |
| Manager   | All PDFs             |
| Analyst_1 | 1 PDF (Meta)         |
| Analyst_2 | 2 PDFs               |
| Analyst_3 | 3 PDFs               |

---

## 📦 Dependencies

See [requirements.txt](requirements.txt):

```
fastapi
uvicorn
passlib[bcrypt]
bcrypt
python-multipart
pydantic
langchain
langchain-community
faiss-cpu
sentence-transformers
pypdf
ollama
streamlit
python-dotenv
requests
```

---

## 🛡️ Security

* Passwords hashed with bcrypt (never stored in plain text).
* Role-based document access enforced in backend.

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -m "Added feature"`)
4. Push branch (`git push origin feature-name`)
5. Create a Pull Request

---

## 📜 License

MIT License – free to use and modify.
