from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import streamlit as st
import pandas as pd
import torch
import os
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

# Redirect to home.py when the app starts
if "redirected" not in st.session_state:
    st.session_state["redirected"] = True
    with st.spinner("Redirecting to Home Page..."):
        time.sleep(1)
    st.switch_page("pages/home.py")
    
if "redirect_to_journal" in st.session_state:
    del st.session_state["redirect_to_journal"]
    st.switch_page("pages/journal.py")

# Load Emotion Detection Model (38 emotions)
@st.cache_resource
def load_model():
    model_name = "lrei/distilroberta-base-emolit"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()

# Dua CSV File
DUAS_CSV_FILE = "duas.csv"  # Ensure this file exists

@st.cache_data
def get_dua_for_mood(mood):
    """Fetches the Dua, translation, and reference for a given mood."""
    try:
        if not os.path.exists(DUAS_CSV_FILE):
            st.error("❌ ERROR: Dua CSV file not found!")
            return None, None, None

        df = pd.read_csv(DUAS_CSV_FILE, encoding="utf-8")  
        df["Mood"] = df["Mood"].str.lower().str.strip()
        mood = mood.lower().strip()

        result = df[df["Mood"] == mood]

        if result.empty:
            return None, None, None

        dua = result.iloc[0].get("Dua (Arabic)", "No Dua Available")
        translation = result.iloc[0].get("Dua Translation", "No Translation Available")
        reference = result.iloc[0].get("Dua Reference", "No Reference Available")

        return dua, translation, reference
    except Exception as e:
        st.error(f"❌ CSV Error: {e}")
        return None, None, None

# Streamlit UI
st.title("🌙 Virtual Mood Journal")
st.write("Write about your day, and we will suggest a **Dua** based on your mood.")

entry_text = st.text_area("✍️ Write about your day:", height=200)

if st.button("🔍 Analyze Mood"):
    if entry_text.strip():
        # Use Hugging Face pipeline for emotion detection
        emotion_pipeline = pipeline(
            "text-classification",
            model="lrei/distilroberta-base-emolit",
            return_all_scores=True,
            device=0 if torch.cuda.is_available() else -1  # Use GPU if available
        )

        # Get emotion predictions
        emotion_results = emotion_pipeline(entry_text)[0]

        # Get top detected emotion
        detected_emotion = max(emotion_results, key=lambda x: x['score'])
        detected_emotion_label = detected_emotion['label']
        confidence = detected_emotion['score']

        st.markdown(f"### 🎯 Detected Mood: `{detected_emotion_label.capitalize()}`")

        # Fetch Dua
        dua, translation, reference = get_dua_for_mood(detected_emotion_label)

        if dua:
            st.markdown(f"### 🕌 Recommended Dua")

            # Baby Pink Highlight for Arabic Dua
            st.markdown(f"""
                <div style="background-color: #f8d7da; padding: 10px; border-radius: 10px; border-left: 5px solid #721c24;">
                    <h4 style="color: #721c24;">📜 Arabic:</h4>
                    <p style="font-size: 18px; font-weight: bold; color: #721c24;">{dua}</p>
                </div>
                """,
                unsafe_allow_html=True)   

            # Sky Blue Highlight for Translation
            st.markdown(f"""
                <div style="background-color: #d1ecf1; padding: 10px; border-radius: 10px; border-left: 5px solid #0c5460;">
                    <h4 style="color: #0c5460;">🌍 Translation:</h4>
                    <p style="font-size: 18px; font-weight: bold; color: #0c5460;">{translation}</p>
                </div>
                """,
                unsafe_allow_html=True)

            # Cream Highlight for Reference
            st.markdown(f"""
                <div style="background-color: #fff3cd; padding: 10px; border-radius: 10px; border-left: 5px solid #856404;">
                    <h4 style="color: #856404;">📖 Reference:</h4>
                    <p style="font-size: 18px; font-weight: bold; color: #856404;">{reference}</p>
                </div>
                """,
                unsafe_allow_html=True)
        else:
            st.warning(f"⚠️ No matching dua found for mood: `{detected_emotion_label}`")

        # Save the journal entry to the database
        cursor.execute("INSERT INTO journal_entries (entry_text, mood) VALUES (%s, %s)", 
                       (entry_text, detected_emotion_label))

        conn.commit()

        st.success(f"✅ Entry saved! Mood detected: {detected_emotion_label}")

    else:
        st.error("⚠️ Please enter some text before analyzing.")

# Back button
if st.button("⬅ Back to Journal"):
    st.switch_page("pages/journal.py")

# Feedback button
if st.button("💬 Give Feedback"):
    st.switch_page("pages/feedback.py")