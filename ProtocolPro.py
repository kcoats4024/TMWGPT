import streamlit as st
import google.generativeai as genai
import time

# Configuration (Replace 'YOUR_API_KEY' with your actual API key)
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

# Initialize chat session ONLY after the first user message
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Initialize user input
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# Input and button handling
def handle_input():
    if not st.session_state.chat_history:  # Check if it's the first message
        st.session_state.chat_history.append({"role": "user", "parts": [{"text": document}]})  # Add the document
        
    # Update chat history with user input
    st.session_state.chat_history.append(
        {"role": "user", "parts": [{"text": st.session_state.user_input + " As Protocol Pro, an assistant for Triangle Microworks, please refer to and cite the provided document where applicable."}]}
    )

    # Token counting and truncation
    while model.count_tokens(st.session_state.chat_history).total_tokens > context_window - 1000:
        st.session_state.chat_history.pop(1)

    # Generate response
    try:
        with st.spinner("Generating response..."):
            response = model.generate_content(st.session_state.chat_history, stream=True)
            response_text = ""
            for chunk in response:
                response_text += chunk.text
            st.write(f"**Protocol Pro:** {response_text}")
    except Exception as e:
        st.error(f"Error generating response: {e}")

    # Update chat history with response
    st.session_state.chat_history.append({"role": "model", "parts": [{"text": response_text}]})
    
    # Clear input after handling (Use callback mechanism)
    def clear_input():
        st.session_state['user_input'] = ""
    st.experimental_set_query_params(clear_input=True) 

# Input text area with on_change callback
user_input = st.text_area("You:", value=st.session_state.user_input, key='user_input', on_change=handle_input)  

if st.experimental_get_query_params().get("clear_input"):
    st.session_state['user_input'] = ""
    st.experimental_set_query_params()

# Display chat history ONLY when it's not empty
if st.session_state.chat_history:
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.write(f"**You:** {message['parts'][0]['text']}")
        else:
            st.write(f"**Protocol Pro:** {message['parts'][0]['text']}")

