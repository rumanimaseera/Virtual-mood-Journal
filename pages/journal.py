import streamlit as st
import mysql.connector
import datetime
import calendar

# Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Maseera@123",
    database="mood_journal"
)
cursor = conn.cursor()

st.title("📖 Your Journal Entries")

# Check if the user is logged in
if "user" not in st.session_state:
    st.warning("⚠ Please log in to view your journal.")
    st.stop()

username = st.session_state["user"]

# Fetch old journal entries
cursor.execute("SELECT id, entry_text, mood, created_at FROM journal_entries")
entries = cursor.fetchall()

# Function to display calendar
def show_calendar(entries):
    today = datetime.date.today()
    current_year, current_month = today.year, today.month

    # Display Calendar for the current month
    st.subheader(f"🗓 Calendar - {calendar.month_name[current_month]} {current_year}")
    
    # Get the correct number of days in the current month
    num_days = calendar.monthrange(current_year, current_month)[1]  
    month_days = [datetime.date(current_year, current_month, day) for day in range(1, num_days + 1)]

    # Map entries to dates
    entry_dates = {entry[3].date(): entry for entry in entries}  # Only date part of 'created_at'

    # Generate the calendar
    calendar_grid = st.empty()
    calendar_html = "<table style='width:100%; border-collapse: collapse;'>"
    
    # Add headers (weekdays)
    calendar_html += "<tr>"
    for weekday in calendar.weekheader(3).split():
        calendar_html += f"<th>{weekday}</th>"
    calendar_html += "</tr>"

    # Add the days
    first_weekday = month_days[0].weekday()  # Get the starting weekday of the month
    calendar_html += "<tr>" + "<td></td>" * first_weekday  # Add empty cells for alignment

    for i, date in enumerate(month_days):
        if (i + first_weekday) % 7 == 0 and i != 0:
            calendar_html += "</tr><tr>"

        # If there's an entry on this date, add an icon to it
        if date in entry_dates:
            entry = entry_dates[date]
            entry_id, entry_text, mood, created_at = entry
            date_str = created_at.strftime("%d %b %Y")
            entry_icon = "📌"  # Placeholder icon (can be replaced with an image)

            # Add the icon for entries
            calendar_html += f"<td style='text-align:center; padding:5px;'>" \
                             f"<button style='background-color:transparent; border:none; cursor:pointer;' " \
                             f"onclick=\"window.location.href='?entry_id={entry_id}'\">" \
                             f"{entry_icon}<br>{date.day}</button>" \
                             f"</td>"
        else:
            calendar_html += f"<td style='text-align:center; padding:5px;'>{date.day}</td>"

    calendar_html += "</tr></table>"
    calendar_grid.markdown(calendar_html, unsafe_allow_html=True)

# Function to display the selected journal entry
def display_entry(entry_id):
    cursor.execute("SELECT entry_text, mood, created_at, translation, reference, mood_output FROM journal_entries WHERE id = %s", (entry_id,))
    entry = cursor.fetchone()
    
    if entry:
        entry_text, mood, created_at, translation, reference, mood_output = entry
        st.subheader(f"📝 Journal Entry from {created_at.strftime('%d %b %Y')}")
        st.write(entry_text)
        st.write(f"**Mood:** {mood}")
        st.write(f"**Translation:** {translation}")
        st.write(f"**Reference:** {reference}")
        st.write(f"**Detected Mood from ML Model:** {mood_output}")
    else:
        st.error("Entry not found!")

# Display calendar
show_calendar(entries)

# Check if an entry_id is passed via URL parameters (clicked on a date)
entry_id = st.query_params.get("entry_id", [None])[0]

if entry_id:
    # Display the entry details
    display_entry(entry_id)

# Button to add a new entry
if st.button("➕ New Entry"):
    st.switch_page("app.py")  # Redirect to the journaling page

# Feedback button
if st.button("💬 Give Feedback"):
    st.switch_page("pages/feedback.py")
