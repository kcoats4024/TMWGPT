import streamlit as st
import google.generativeai as genai
import time

# Configuration
API_KEY = st.secrets["KYLEGEMINIAPIKEY"]
genai.configure(api_key=API_KEY)

generation_config = {
    "temperature": 0.5,
    "top_p": 0.9,
    "top_k": 50,
    "max_output_tokens": 8192, 
    "response_mime_type": "text/plain",
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-latest",
        safety_settings=safety_settings,
        generation_config=generation_config,
    )
except Exception as e:
    st.error(f"Error initializing model: {e}")
    st.stop()

# Load your document
with open('SuperData_5-28.txt', 'r', encoding='utf-8') as file:
    document = file.read()

# Define context window size
context_window = 1048576

# Initialize chat session (Ensure 'user' is the first role for initial message)
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [{"role": "user", "parts": [{"text": document}]}]

# Initialize user input
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# Streamlit app
st.title("Protocol Pro")
st.write("Trained on Youtube Transcriptions, Website text, Guides (DTM User's Guide, SDG Implementer's Guide), and Manuals. (Navigator, Test Harness, TSP, Iron)")

# Input and button handling
def handle_input(user_input):  
    # Update chat history
    st.session_state.chat_history.append(
        {"role": "user", "parts": [{"text": user_input + " As Protocol Pro, an assistant for Triangle Microworks, please refer to and cite the provided document where applicable."}]}
    )
    # ... (rest of your response generation logic)

user_input = st.text_area("You:", value=st.session_state.user_input, key='user_input')

if st.button('Send'):
    if st.session_state.user_input != "":  # Check if input is not empty
        handle_input(st.session_state.user_input)
        st.session_state.user_input = ""  # Clear input after handling



