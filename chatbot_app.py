import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI()

# Initialize chat history in session
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

st.title("🤖 Roma R Chatbot")
st.markdown("Type your message and press Enter. Type `bye` to end the chat.")

user_input = st.chat_input("You:")

if user_input:
    if user_input.lower() == "bye":
        st.write("👋 Goodbye!")
    else:
        # Append user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Call OpenAI API
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            reply = f"❌ Error: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": reply})

# Show chat history
for msg in st.session_state.messages[1:]:  # skip the system message
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
