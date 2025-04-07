import streamlit as st
import base64

# 🔹 Set Streamlit Page Config (Must be the First Command)
st.set_page_config(page_title="Home | Virtual Mood Journal", page_icon="📜", layout="wide")

# Function to encode image to Base64
def get_base64_of_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Image file not found: {image_path}")
        return None

# Convert the background image
image_path = r"C:\Users\91887\VMJ_new\photos\vintage.webp"  
image_base64 = get_base64_of_image(image_path)  

# Apply background image using base64
if image_base64:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/webp;base64,{image_base64}") no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("Background image could not be loaded.")

# Page Header
st.markdown('<h1 style="text-align:center; font-size: 50px; color: #5a3820; font-family: Georgia, serif;">📜 Welcome to Virtual Mood Journal</h1>', unsafe_allow_html=True)

# Bismillah Header
st.markdown('<h1 style="text-align:center; font-size: 60px; color: #5a3820; font-family: Traditional Arabic, serif;">بِسْمِ ٱللَّٰهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ</h1>', unsafe_allow_html=True)

# Transparent Info Box
st.markdown(
    """
    <div style="
        background: rgba(90, 60, 30, 0.7);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: white;
        width: 60%;
        margin: auto;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
        font-family: 'Georgia', serif;
        ">
        Express your thoughts, understand your emotions, and receive spiritual guidance. 
        Write your daily experiences, and let our AI guide your soul with personalized duas.
    </div>
    """,
    unsafe_allow_html=True
)

# Hadith of the Day Section
st.markdown(
    """
    <div style="
        background: rgba(255, 255, 255, 0.85);
        border-left: 5px solid #5a3820;
        padding: 15px;
        margin: 40px auto;
        width: 60%;
        font-family: 'Georgia', serif;
        text-align: center;
        font-size: 18px;
        color: #3b2c20;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        ">
        <i>Prophet Muhammad (ﷺ) said:</i> <br> 
        "Verily, in the remembrance of Allah do hearts find rest." <br> <b>(Quran 13:28)</b>
    </div>
    """,
    unsafe_allow_html=True
)

# Initialize session state for navigation
if "current_section" not in st.session_state:
    st.session_state.current_section = "Home"

# Function to handle button clicks
def navigate_to(section):
    if section == "Login":
        st.switch_page("pages/authentication.py")  # Redirect to login page
    else:
        st.session_state.current_section = section

# Custom Buttons with Session State Handling
st.markdown(
    """
    <style>
    .button-container {
        display: flex;
        justify-content: center;
        gap: 25px; /* Space between buttons */
        margin-top: 20px;
        
    }
    .custom-button {
        background-color: #5a3820 !important; /* Dark brown */
        color: white !important;
        font-size: 16px;
        font-weight: bold;
        padding: 10px 15px;
        border-radius: 8px;
        text-align: center;
        border: none;
        cursor: pointer;
        transition: 0.3s;
        width: 140px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2); /* Light shadow effect */
    }
    .custom-button:hover {
        background-color: #9c6b30 !important; /* Lighter brown */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Centered button layout
col1, col2, col3 = st.columns([1, 1, 1])


with col1:
    if st.button("📖 About Us", key="about"):
        navigate_to("About Us")

with col2:
    if st.button("🔑 Login / Register", key="login"):
        navigate_to("Login")  # Redirects to authentication page

with col3:
    if st.button("🌟 Features", key="features"):
        navigate_to("Features")

# Display Sections
if st.session_state.current_section == "About Us":
    st.markdown(
        """
        <div style="
            background: rgba(90, 60, 30, 0.7);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            color: white;
            width: 60%;
            margin: auto;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
            font-family: 'Georgia', serif;
            ">
            <h2>📖 About Us</h2>
            <p>Welcome to Virtual Mood Journal, where your emotions meet faith. 
            Our AI-powered system allows you to document your thoughts while receiving 
            personalized Islamic duas for spiritual guidance.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

elif st.session_state.current_section == "Features":
    st.markdown(
        """
         <div style="
            background: rgba(90, 60, 30, 0.7);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            color: white;
            width: 60%;
            margin: auto;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
            font-family: 'Georgia', serif;
            ">
            <h2>🌟 Features</h2>
            <ul style="text-align: left;">
                <li>✍️ <b>Write and Reflect</b></li>
                <li>🤖 <b>AI-Powered Guidance</b></li>
                <li>📊 <b>Mood Analytics</b></li>
                <li>🔐 <b>Private & Secure</b></li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    
# Social Media Links
st.markdown(
    """
    <style>
    .footer {
        display: flex;
        justify-content: center;
        margin-top: 40px;
        font-size: 18px;
        font-family: 'Georgia', serif;
    }
    .social-links a {
        color: #5a3820;
        text-decoration: none;
        font-weight: bold;
        margin: 0 15px;
        font-size: 22px;
        transition: 0.3s;
    }
    .social-links a:hover {
        color: #9c6b30;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="footer">
        <div class="social-links">
            <a href="https://www.instagram.com/zyha.deen?igsh=MW51amk4eHVic280Zw==" target="_blank">Instagram</a>
            <a href="https://twitter.com/yourprofile" target="_blank">Twitter</a>
            <a href="https://linkedin.com/in/yourprofile" target="_blank">LinkedIn</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
