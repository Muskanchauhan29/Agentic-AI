from fastapi import FastAPI
from ollama import Client
from huggingface_hub import whoami


app = FastAPI()
client = Client(
    host="http://localhost:11434",
)

@app.get("/")
def read_root():
    return {"hello":World"}
print(whoami())