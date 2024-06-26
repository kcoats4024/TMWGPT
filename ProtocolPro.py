import streamlit as st
import time
import google.generativeai as genai

# Configuration
API_KEY = "your_api_key"  # Replace with your actual API key

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

# Load document
try:
    with open('SuperData_5-28.txt', 'r', encoding='utf-8') as file:
        document = file.read()
except Exception as e:
    st.error(f"Error loading document: {e}")
    st.stop()

# Streamlit app
st.title("AI Chat with Protocol Pro")
st.write("Start chatting with the AI. Type 'exit' to end the conversation.")

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [{"role": "user", "parts": [{"text": document}]}]

user_input = st.text_input("You:", key='user_input')
if user_input:
    if user_input.lower() == 'exit':
        st.stop()

    st.session_state.chat_history.append(
        {"role": "user", "parts": [{"text": user_input + " As Protocol Pro, an assistant for Triangle Microworks, please refer to and cite the provided document where applicable."}]}
    )

    # Check token count and truncate history if necessary
    while model.count_tokens(st.session_state.chat_history).total_tokens > 1048576 - 1000:
        st.session_state.chat_history.pop(1)

    # Stopwatch start
    start_time = time.time()

    # Generate response
    response = model.generate_content(st.session_state.chat_history, stream=True)
    response_text = ""

    for chunk in response:
        response_text += chunk.text

    # Stopwatch end
    end_time = time.time()
    response_time = end_time - start_time

    st.write(f"**Protocol Pro:** {response_text}")
    st.write(f"_Response time: {response_time:.2f} seconds_")

    st.session_state.chat_history.append({"role": "model", "parts": [{"text": response_text}]})

    # Clear user input
    st.session_state.user_input = ""
