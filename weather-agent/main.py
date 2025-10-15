import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
genai.configure(api_key=api_key)

chat = genai.GenerativeModel("gemini-2.5-flash").start_chat(history=[])

print("🤖 Gemini Chatbot (type 'exit' to quit)")
while True:
    user_query = input("> ")
    if user_query.lower() in {"exit", "quit"}:
        print("👋 Goodbye!")
        break

    response = chat.send_message(user_query)
    print("🤖:", response.text)
