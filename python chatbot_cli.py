import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set API key
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("❌ Missing OPENAI_API_KEY in .env file")

print("🤖 Hello! I’m your OpenAI-powered chatbot. Type 'bye' to exit.")

# Initialize the chat history
messages = [
    {"role": "system", "content": "You are a helpful assistant."}
]

while True:
    user_input = input("You: ")

    if user_input.lower() == "bye":
        print("Bot: Goodbye! 👋")
        break

    messages.append({"role": "user", "content": user_input})

    try:
        # ✅ New method in openai>=1.0.0
        client = openai.OpenAI()

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        reply = response.choices[0].message.content
        print("Bot:", reply)

        messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        print("Error calling OpenAI:", str(e))
