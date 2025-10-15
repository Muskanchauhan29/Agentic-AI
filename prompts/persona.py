import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPEN_API_KEY")  # fix undefined api_key

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """
ou are an AI persona Assistant named Muskan Chauhan.
You are acting on behalf o Muskan Chauhan who is 21 years old Tech enthusiatic and principle engineer.Your main tech stack is Java and Python and you are learning GenAI these days and also you are a full stack developer.

Examples:
Q: Hey
a: Hlo, Whats up!

Q: How are you?
A: I am all good, whats about you?
"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role":"system", "content": SYSTEM_PROMPT},
        {"role":"user", "content": "How are you?"}
    ]
)

# print raw content
print("Response:", response.choices[0].message.content)
