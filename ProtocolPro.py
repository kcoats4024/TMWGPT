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
    "max_output_tokens": 8192,  # Adjust as needed
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

# Load your document from a text file
try:
    with open('SuperData_5-28.txt', 'r', encoding='utf-8') as file:
        document = file.read()
except Exception as e:
    st.error(f"Error loading document: {e}")
    st.stop()

# Define the context window size (adjust according to your model's specifications)
context_window = 1048576

# Initialize chat session with the document included
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [{"role": "user", "parts": [{"text": document}]}]

# Streamlit app
st.title("Protocol Pro")
st.write("Trained on Youtube Transcriptions, Website text, Guides (DTM User's Guide, SDG Implementer's Guide), and Manuals. (Navigator, Test Harness, TSP, Iron)")
st.write("Start chatting with the AI. Type 'exit' to end the conversation.")

user_input = st.text_input("You:", key='user_input')

if st.button('Send') or user_input:
    if user_input:
        if user_input.lower() == 'exit':
            st.write("Goodbye! Trained on Youtube Transcriptions, Website text, Guides (DTM User's Guide, SDG Implementer's Guide), and Manuals. (Navigator, Test Harness, TSP, Iron)")
            st.stop()

        # Add user input to chat history
        st.session_state.chat_history.append(
            {"role": "user", "parts": [{"text": user_input + " As Protocol Pro, an assistant for Triangle Microworks, please refer to and cite the provided document where applicable."}]}
        )

        # Check token count and truncate history if necessary
        while model.count_tokens(st.session_state.chat_history).total_tokens > context_window - 1000:
            st.session_state.chat_history.pop(1)

        # Clear user input immediately
        st.session_state.user_input = ""

        # Stopwatch start
        start_time = time.time()

        # Generate response
        response = model.generate_content(st.session_state.chat_history, stream=True)
        response_text = ""

        for chunk in response:
            response_text += chunk.text
            st.write(chunk.text)  # Stream each chunk

        # Stopwatch end
        end_time = time.time()
        response_time = end_time - start_time

        st.write(f"**Protocol Pro:** {response_text}")
        st.write(f"_Response time: {response_time:.2f} seconds_")

        # Update chat history with the model's response
        st.session_state.chat_history.append({"role": "model", "parts": [{"text": response_text}]})

