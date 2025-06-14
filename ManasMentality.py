import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv(dotenv_path="keys.env")
TOGETHER_API_KEY = os.getenv("API_KEY")

# Use Together.ai as OpenAI-compatible endpoint
openai.api_key = TOGETHER_API_KEY
openai.api_base = "https://api.together.xyz/v1"

# Choose a Together-hosted model
MODEL_NAME = "meta-llama/Llama-3-8b-chat-hf"

# Load friend profile
with open("manas'mentality.txt", "r", encoding="utf-8") as file:
    friend_profile = file.read()

st.set_page_config(page_title="Manas Mentality", layout="centered")
st.title("Dive deep into Manas Mentality")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": f"You are acting as Manas. Here is his personality:\n{friend_profile}"}
    ]

# Display previous chat messages
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
prompt = st.chat_input("Talk to ManasAI...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Together API call
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=st.session_state.messages,
            temperature=0.7,
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"⚠️ Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
