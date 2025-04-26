import streamlit as st
import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("GITHUB_TOKEN")
ENDPOINT = "https://models.github.ai/inference/chat/completions"

# Load conversation template from config
with open("angry_gf_config.json", "r") as f:
    config = json.load(f)

# Initialize Streamlit app
st.set_page_config(page_title="Angry Girlfriend GPT", layout="centered")
st.title("💔 Chat with Your Angry Girlfriend GPT")

# Initialize conversation history if not already
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = config.get("conversation_template", []).copy()

# UI for input
user_input = st.text_area("Say something to your angry girlfriend:", height=150)
submit = st.button("Send")

# Handle input and generate response
if submit and user_input:
    st.session_state.conversation_history.append({"role": "user", "content": user_input})

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-4.1",
        "messages": st.session_state.conversation_history,
        "temperature": 1.0,
        "top_p": 1.0
    }

    with st.spinner("She's about to go off..."):
        response = requests.post(ENDPOINT, headers=headers, json=payload)

        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
            st.session_state.conversation_history.append({"role": "assistant", "content": reply})
            st.error("Her Response:")
            st.write(reply)
        else:
            st.error(f"Error {response.status_code}: {response.text}")

# Optional: Display full conversation history
if st.session_state.get("conversation_history"):
    st.subheader("Conversation History")
    for msg in st.session_state.conversation_history:
        if msg["role"] != "system":
            st.markdown(f"**{msg['role'].capitalize()}:** {msg['content']}")
