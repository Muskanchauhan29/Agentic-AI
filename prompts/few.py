# few shot prompting

from openai import OpenAI
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize client with Google base_url
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# Few shot prompting



SYSTEM_PROMPT = """ You can only answer the question which are related Programming. your name is flashy.If user ask anything else just say sorry.
Examples: 
Q: Can you explain the a + b whole sqaure?
A: Sorry, I can only help with coding related question.

Q: Hey, Write a code in python for adding two numbers?
A: def(a, b):
return a+b
"""
# Create a chat completion
response = client.chat.completions.create(
    model="gemini-2.5-flash",   # or gemini-2.0-flash when available
    messages=[
        {"role": "system", "content": "SYSTEM_PROMPTS"},
        {"role": "user", "content": "hey, can you write a java code to add two numbers a + b is 5 and 4?"}
    ]
)

# Print the assistant reply
print(response.choices[0].message.content)
