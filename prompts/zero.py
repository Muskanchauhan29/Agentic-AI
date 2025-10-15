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


# Zero shot prompting is which the model is given direct question or task without prior example.
SYSTEM_PROMPT = "You can only answer the question which are related relationship. your name is cutie.If user ask anything else just say sorry."

# Create a chat completion
response = client.chat.completions.create(
    model="gemini-2.5-flash",   # or gemini-2.0-flash when available
    messages=[
        {"role": "system", "content": "SYSTEM_PROMPTS"},
        {"role": "user", "content": "hi cutie my relationship is not going well"}
    ]
)

# Print the assistant reply
print(response.choices[0].message.content)
