import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv(dotenv_path="keys.env")
gemini_api_key = os.getenv("API_KEY")
genai.configure(api_key=gemini_api_key)

# Load Manas' personality
with open("manas'mentality.txt", "r", encoding="utf-8") as file:
    friend_profile = file.read()

# Streamlit page config
st.set_page_config(page_title="Manas Mentality", layout="centered")
st.title("🧠 Dive deep into Manas Mentality")

# Create Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# Initialize chat history
if "chat" not in st.session_state:
    # Start the chat with a system message
    st.session_state.chat = model.start_chat(history=[
        {"role": "user", "parts": [f"Act like Manas. Here is his personality:\n{friend_profile}"]}
    ])

# Display past conversation
for msg in st.session_state.chat.history[1:]:
    with st.chat_message("user" if msg.role == "user" else "assistant"):
        st.markdown("".join(part.text for part in msg.parts))

# User input
prompt = st.chat_input("Talk to ManasAI...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = st.session_state.chat.send_message(prompt)
        reply = response.text
    except Exception as e:
        reply = f"⚠️ Error: {e}"

    with st.chat_message("assistant"):
        st.markdown(reply)
