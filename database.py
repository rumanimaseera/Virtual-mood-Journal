import mysql.connector
import os

# Securely fetch database credentials from environment variables
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),  
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASS", ""),
    database=os.getenv("DB_NAME", "mood_journal")
)
cursor = conn.cursor()
