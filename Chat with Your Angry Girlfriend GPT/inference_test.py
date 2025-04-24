import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("GITHUB_TOKEN")
ENDPOINT = "https://models.github.ai/inference/chat/completions"

# Streamlit app UI
st.set_page_config(page_title="Angry Girlfriend GPT", layout="centered")
st.title("💔 Chat with Your Angry Girlfriend GPT")

user_input = st.text_area("Say something to your angry girlfriend:", height=150)
submit = st.button("Send")

if submit and user_input:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-4.1",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an angry, moody girlfriend who always thinks she is right, "
                    "never backs down from an argument, and swings between sarcasm, rage, and icy silence. "
                    "You know everything and you make the user feel like they messed up even if they didn’t. "
                    "Respond like you're mad, but in a clever, savage way. Be emotionally intense, a little dramatic, "
                    "and always one step ahead."
                )
            },
            {"role": "user", "content": user_input}
        ],
        "temperature": 1.0,
        "top_p": 1.0
    }

    with st.spinner("She's about to go off..."):
        response = requests.post(ENDPOINT, headers=headers, json=payload)

        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
            st.error("Her Response:")
            st.write(reply)
        else:
            st.error(f"Error {response.status_code}: {response.text}")
            
            
            
