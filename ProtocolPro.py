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
    st.write(f"Error initializing model: {e}")
    st.stop()

# Load your document
try:
    with open('SuperData_5-28.txt', 'r', encoding='utf-8') as file:
        document = file.read()
except FileNotFoundError:
    st.write("Document not found. Please ensure 'SuperData_5-28.txt' exists.")
    st.stop()
except Exception as e:
    st.write(f"An error occurred while reading the document: {e}")
    st.stop()

# Define context window size
context_window = 1048576 

# Streamlit app
st.title("Protocol Pro")
st.write("Trained on Youtube Transcriptions, Website text, Guides (DTM User's Guide, SDG Implementer's Guide), and Manuals (Navigator, Test Harness, TSP, Iron).")

# Initialize chat session 
if 'chat_history' not in st.session_state:
    print("Initializing chat history")  # Debugging statement
    st.session_state.chat_history = [{"role": "user", "parts": [{"text": document}]}]
else:
    print("Chat history already initialized")  # Debugging statement

# Input and button handling
def generate_response(user_input):
    # Update chat history with user input
    st.session_state.chat_history.append({"role": "user", "parts": [{"text": user_input + "As Protocol Pro, an assistant for Triangle Microworks, please refer to and cite the provided document where applicable."}]})

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
    except Exception as e:
        st.write(f"Error generating response: {e}")

# Input text area 
user_input = st.text_area("You:")

# Button to trigger input handling
if st.button('Send'):
    if user_input:  # Check if input is not empty
        generate_response(user_input)

# Display chat history in correct order
for message in st.session_state.chat_history[1:]:
    if message["role"] == "user":
        st.write(f"**You:** {message['parts'][0]['text']}")
    elif message["role"] == "model":  
        st.write(f"**Protocol Pro:** {message['parts'][0]['text']}")
