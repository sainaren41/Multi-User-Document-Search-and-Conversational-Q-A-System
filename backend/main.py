import os
import sqlite3
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from langchain.chains import ConversationalRetrievalChain
from langchain_ollama import OllamaLLM 
from langchain.memory import ConversationBufferMemory
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

app = FastAPI()
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Load FAISS + Ollama
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vs = FAISS.load_local("F:\Multi-User Document Search and Conversational Q&A System\VDB_index", embeddings,allow_dangerous_deserialization=True)
retriever = vs.as_retriever(search_kwargs={"k": 5})
llm = OllamaLLM(model="mistral")

memory = ConversationBufferMemory(
                  memory_key="chat_history", 
                  return_messages=True,
                  output_key="answer"
                  )

qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True,
    output_key="answer"
)

# Database Helper Functions
def get_users(email: str):
  con = sqlite3.connect('users.db')
  cur = con.cursor()
  cur.execute("SELECT id, email, password_hash, role FROM users WHERE email=?", (email,))
  row = cur.fetchone()
  con.close()
  return row

def check_access(role,document_name):
  con = sqlite3.connect('users.db')
  cur = con.cursor()
  cur.execute("SELECT id FROM documents WHERE role=? AND document_name=?", (role,document_name))
  row = cur.fetchone()
  con.close()
  return row is not None

def get_allowed_documents(role):
  con = sqlite3.connect('users.db')
  cur = con.cursor()
  cur.execute("SELECT document_name FROM documents WHERE role=?", (role,))
  rows = cur.fetchall()
  con.close()
  return [row[0] for row in rows]

def filter_results(results, role):
    allowed_docs = get_allowed_documents(role)
    filtered_docs = [doc for doc in results if os.path.basename(doc.metadata.get('source', '')) in allowed_docs]
    return filtered_docs

# Pydantic Models
class SignupRequest(BaseModel):
    email: str
    password: str
    role: str

# Endpoints

@app.post("/signup")
def signup(request: SignupRequest):
    if get_users(request.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(request.password)
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)", (request.email, hashed_password, request.role))
    user_id = c.lastrowid
    conn.commit()
    conn.close()
    return {"message": "User created successfully", "user_id": user_id}


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_users(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user[2]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"access_token": user[1], "token_type": "bearer"}

@app.post("/chat")
def chat(query: str, token: str = Depends(oauth2_scheme)):
    user = get_users(token)
    if not user:
        raise HTTPException(status_code=403, detail="Invalid user")
    role = user[3]  # Assuming role is the 4th column in users table
    
    user_role = "user"  # This should be fetched from the database based on the user
    document_name = "confidential.pdf"  # This should be determined based on the query context

    results = vs.similarity_search(query, k=5)
    filtered = filter_results(results, role)

    if not filtered:
        raise HTTPException(status_code=403, detail="Access denied to the requested document")

    result = qa.combine_docs_chain.run(input_documents=filtered, question=query)
    return {
        "answer": result,
        "sources": [doc.metadata for doc in filtered]
    }