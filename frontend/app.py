import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("Multi-User Document Search and Conversational Q&A System")

if "token" not in st.session_state:
    st.session_state.token = None

# Sign Up

with st.expander("Sign Up"):
    with st.form("signup_form"):
      new_email = st.text_input("New Email", key="new_email")
      new_password = st.text_input("New Password", type="password", key="new_password")
      new_role = st.selectbox("Role", ["manager", "analyst_1", "analyst_2", "analyst_3"], key="new_role")
      signup_btn = st.form_submit_button("Sign Up")
      if signup_btn:
            try:
                response = requests.post(f"{API_URL}/signup", json={
                    "email": new_email,
                    "password": new_password,
                    "role": new_role
                })
                if response.status_code == 200:
                    st.success("User created successfully! Please log in.")
                else:
                    try:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                    except Exception:
                        st.error(f"Error: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error(" Backend is not running. Start FastAPI with: `uvicorn backend.main:app --reload`")


# Log In

if st.session_state.token is None:
    with st.form("login_form"):
        email = st.text_input("Email", key="email")
        password = st.text_input("Password", type="password", key="password")
        login_btn = st.form_submit_button("Login")
        if login_btn:
            try:
                # OAuth2PasswordRequestForm expects x-www-form-urlencoded
                response = requests.post(f"{API_URL}/token", data={
                    "username": email,
                    "password": password
                })
                if response.status_code == 200:
                    token = response.json().get("access_token")
                    if token:
                        st.session_state.token = token
                        st.success("Logged in successfully!")
                else:
                    try:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                    except Exception:
                        st.error(f"Error: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error(" Could not connect to backend. Is FastAPI running?")


# Chat Interface

if st.session_state.token:
    query = st.text_input("Your Question")
    if query:
        resp = requests.post(f"{API_URL}/chat",
                             params={"query": query},
                             headers={"Authorization": f"Bearer {st.session_state.token}"})
        if resp.status_code == 200:
            st.write(" **Answer:**", resp.json()["answer"])
            st.write(" **Sources:**", resp.json()["sources"])
        else:
            try:
                st.error(resp.json()["detail"])
            except Exception:
                st.error(resp.text)