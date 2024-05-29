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

# Initialize model
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

# Streamlit app
st.title("Protocol Pro")
st.write("Trained on Youtube Transcriptions, Website text, Guides (DTM User's Guide, SDG Implementer's Guide), and Manuals. (Navigator, Test Harness, TSP, Iron)")

# Initialize chat session 
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Ensure the document is included in the context but not displayed as a user message
if 'document_included' not in st.session_state:
    st.session_state.chat_history.append({"role": "user", "parts": [{"text": document}]})
    st.session_state.document_included = True

# Input and button handling
def generate_response(user_input):
    # Update chat history with user input without custom instruction
    st.session_state.chat_history.append({"role": "user", "parts": [{"text": user_input}]})

    # Truncate chat history if it exceeds context window size
    while model.count_tokens(st.session_state.chat_history).total_tokens > context_window - 1000:
        st.session_state.chat_history.pop(1)  # Remove the oldest message (preserve document as first message)

    try:
        # Generate response
        with st.spinner("Generating response..."):
            response = model.generate_content(st.session_state.chat_history, stream=True)
            response_text = ""
            for chunk in response:
                response_text += chunk.text
                
            st.session_state.chat_history.append({"role": "model", "parts": [{"text": response_text}]})
            st.write(f"**Protocol Pro:** {response_text}")
    except Exception as e:
        st.error(f"Error generating response: {e}")

# Input text area 
user_input = st.text_area("You:")

# Button to trigger input handling
if st.button('Send'):
    if user_input:  # Check if input is not empty
        generate_response(user_input)

# Display chat history in correct order
for message in st.session_state.chat_history[1:]:  # Skip the first message (the document)
    if message["role"] == "user":
        st.write(f"**You:** {message['parts'][0]['text']}")
    elif message["role"] == "model":  
        st.write(f"**Protocol Pro:** {message['parts'][0]['text']}")
