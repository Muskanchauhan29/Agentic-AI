from dotenv import load_dotenv
from mem0 import Memory
import os
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "config": {"api_key": OPENAI_API_KEY, "model": "text-embedding-3-small"}
    },
    "llm": {
    "provider": "openai",
    "config": {
        "api_key": OPENAI_API_KEY,
        "model": "gpt-4.1-mini"
    }
},

   "vector_store": {
    "provider": "qdrant",
    "config": {
        "path": "./qdrant_data"
    }
}
}

mem_client = Memory.from_config(config)

user_query = input("> ")

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role":"user", "content": user_query}
    ]
)

ai_response = response.choices[0].message.content

print("AI", ai_response)
mem_client.add(
    user_id="mussu",
    messages=[
        {"role":"user", "content":user_query},
        {"role":"assistant", "content":ai_response}
    ]
)

print("memory has been saved!!")