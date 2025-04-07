import streamlit as st
import mysql.connector
import os

# Configure Page
st.set_page_config(page_title="Feedback | Virtual Mood Journal", page_icon="📝")

st.title("📢 Feedback")
st.write("We appreciate your thoughts! Please share your feedback below.")

# Database connection (Use environment variables for security)
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),  
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASS", "Maseera@123"),
    database=os.getenv("DB_NAME", "mood_journal")
)
cursor = conn.cursor()

# Feedback Form
feedback = st.text_area("Your feedback:")

if st.button("Submit"):
    if feedback.strip():
        # Store feedback in the database
        cursor.execute("INSERT INTO feedback (user_id, feedback) VALUES (%s, %s)", 
                       (st.session_state.get("user_id", None), feedback))
        conn.commit()
        st.success("✅ Thank you for your feedback!")
    else:
        st.error("⚠ Please enter some feedback before submitting.")
