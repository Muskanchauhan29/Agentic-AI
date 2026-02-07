from dotenv import load_dotenv
from mem0 import Memory
import os
from openai import OpenAI

# --------------------
# ENV SETUP
# --------------------

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not found")

client = OpenAI(api_key=OPENAI_API_KEY)

# --------------------
# MEMORY CONFIG (QDRANT DOCKER)
# --------------------
config = {
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": OPENAI_API_KEY,
            "model": "text-embedding-3-small"
        }
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
            "host": "vector-db",   # 👈 docker service name
            "port": 6333
        }
    }
}

mem_client = Memory.from_config(config)

print("🧠 Memory Agent started")
print("Type 'exit' or 'quit' to stop\n")

# --------------------
# MAIN LOOP
# --------------------
while True:
    try:
        user_query = input("> ").strip()

        if user_query.lower() in ("exit", "quit"):
            print("👋 Bye!")
            break

        # --------------------
        # 1. SEARCH MEMORY
        # --------------------
        memories = mem_client.search(
            user_id="mussu",
            query=user_query,
            limit=10
        )

        memory_context = "\n".join(
            m.get("memory", "")
            for m in memories
            if isinstance(m, dict)
        )

        # --------------------
        # 2. BUILD PROMPT (CRITICAL FIX)
        # --------------------
        messages = [
            {
                "role": "system",
                "content": (
                    "You have long-term memory about the user.\n"
                    "Use it to answer personal questions accurately.\n\n"
                    f"MEMORY:\n{memory_context}"
                )
            },
            {
                "role": "user",
                "content": user_query
            }
        ]

        # --------------------
        # 3. CALL LLM
        # --------------------
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages
        )

        ai_response = response.choices[0].message.content
        print("AI:", ai_response)

        # --------------------
        # 4. SAVE MEMORY (FACT-AWARE)
        # --------------------
        mem_client.add(
            user_id="mussu",
            messages=[
                {"role": "user", "content": user_query},
                {"role": "assistant", "content": ai_response}
            ]
        )

        print("🧠 memory saved\n")

    except KeyboardInterrupt:
        print("\n👋 Interrupted")
        break

    except Exception as e:
        print("❌ Error:", e)
