import streamlit as st
import google.generativeai as genai
import tiktoken # For token counting

# Configuration
API_KEY = st.secrets["KYLEGEMINIAPIKEY"]
genai.configure(api_key=API_KEY)

# ... rest of your model configuration (same as before)

# Load your document
with open('SuperData_5-28.txt', 'r', encoding='utf-8') as file:
    document = file.read()

# Define context window size
context_window = 1048576 

# Get the encoding for Gemini
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")  

# Streamlit app
st.title("Protocol Pro")
st.write("Trained on Youtube Transcriptions, Website text, Guides (DTM User's Guide, SDG Implementer's Guide), and Manuals. (Navigator, Test Harness, TSP, Iron)")

# Initialize chat session 
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Input and button handling
def generate_response(user_input):
    if not st.session_state.chat_history:
        st.session_state.chat_history.append({"author": "user", "content": document}) 
    
    # Update chat history with user input
    st.session_state.chat_history.append({"author": "user", "content": user_input + " As Protocol Pro, an assistant for Triangle Microworks, please refer to and cite the provided document where applicable."})

    # Token counting using tiktoken
    total_tokens = sum([len(encoding.encode(msg["content"])) for msg in st.session_state.chat_history])

    # Token truncation (if needed)
    while total_tokens > context_window - 1000:  
        st.session_state.chat_history.pop(0)  
        total_tokens = sum([len(encoding.encode(msg["content"])) for msg in st.session_state.chat_history])

    try:
        # Generate response
        with st.spinner("Generating response..."):
            response = model.generate_chat(st.session_state.chat_history, stream=True)
            response_text = ""
            for chunk in response:
                response_text += chunk.content
            st.session_state.chat_history.append({"author": "model", "content": response_text})
            st.write(f"**Protocol Pro:** {response_text}")
    except Exception as e:
        st.error(f"Error generating response: {e}")


# Input text area 
user_input = st.text_area("You:")

# Button to trigger input handling
if st.button('Send'):
    if user_input:  # Check if input is not empty
        generate_response(user_input)

# Display chat history
for message in st.session_state.chat_history[1:]:  # Skip the first message (the document)
    if message["author"] == "user":
        st.write(f"**You:** {message['content']}")
    elif message["author"] == "model":  
        st.write(f"**Protocol Pro:** {message['content']}")
