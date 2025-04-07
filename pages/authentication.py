import streamlit as st
import mysql.connector
import time

# Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Maseera@123",
    database="mood_journal"
)
cursor = conn.cursor()

# UI Design
st.set_page_config(page_title="🔐 Authentication", layout="centered")
st.title("User Authentication")

# Selection for Login or Register
auth_mode = st.radio("Select an option:", ["Login", "Register"], horizontal=True)

if auth_mode == "Register":
    st.subheader("Create a New Account")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    
    if st.button("Register"):
        cursor.execute("SELECT * FROM users WHERE username=%s", (new_username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            st.error("❌ Username already exists. Choose a different one.")
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (new_username, new_password))
            conn.commit()
            st.success("✅ Registration Successful! You can now log in.")
            st.balloons()

if auth_mode == "Login":
    st.subheader("Log in to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        
        if user:
            st.success("✅ Login Successful! Redirecting...")
            st.session_state["user"] = username  # Store user session
            time.sleep(1)  # Wait before redirecting
            st.switch_page("pages/journal.py")  # Corrected page redirection
        else:
            st.error("❌ Invalid Credentials. Try Again.")
