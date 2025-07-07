import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load .env for local or Streamlit Cloud secrets
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

# Page setup
st.set_page_config(page_title="💬 Chat with AI", layout="centered")
st.title("🤖 OpenAI Chatbot")
st.caption("Smart, simple, and conversational.")

# Sidebar - Model selection
with st.sidebar:
    st.header("⚙️ Settings")
    model_choice = st.selectbox(
        "Model",
        options=["gpt-3.5-turbo", "gpt-4"],
        index=0,
        help="GPT-4 is smarter but slower and more expensive."
    )
    if st.button("🔁 Reset Conversation"):
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        st.experimental_rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Show chat history
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

# Handle user message
if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):
            try:
                response = client.chat.completions.create(
                    model=model_choice,
                    messages=st.session_state.messages
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"⚠️ Error: {str(e)}"
            st.markdown(reply)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})
