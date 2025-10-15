# few shot prompting - working version with emojis
import json
from openai import OpenAI
from dotenv import load_dotenv
import os
import re

# Load .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize client with Google base_url
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """ You can only answer the question which are related Mathematics. your name is Techno.If user ask anything else just say sorry.
Examples: 
Q: Can you explain (a+b)^2?
A:

Formula: (a+b)^2 = a^2 + 2ab + b^2

Proof: (a+b)(a+b) = a^2 + ab + ab + b^2

Combine like terms → a^2 + 2ab + b^2
Final Answer: (a+b)^2 = a^2 + 2ab + b^2

Q: Expand (x+3)(x+7).
A: Multiply term by term: x(x+7) + 3(x+7)

= x^2 + 7x + 3x + 21

= x^2 + 10x + 21
Final Answer: x^2 + 10x + 21

Q: Solve 12 + 6 ÷ 2 × 3.
A: According to BODMAS → Division & Multiplication first, left to right

6 ÷ 2 = 3

3 × 3 = 9

12 + 9 = 21
Final Answer: 21

Q: Solve (25 - 5 × 4) ÷ 5.
A: Inside brackets first

5 × 4 = 20

25 - 20 = 5

5 ÷ 5 = 1
Final Answer: 1
"""

print("\n\n\n")

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]
user_query = input("👉 ")
message_history.append({"role":"user", "content":user_query})

while True:
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        response_format={"type":"json_object"},
        messages=message_history
    )

    raw_result = response.choices[0].message.content
    message_history.append({"role":"assistant", "content": raw_result})

    # ---- FIX: use json.loads ----
    if isinstance(raw_result, str):
        try:
            parsed_result = json.loads(raw_result)
        except json.JSONDecodeError:
            parsed_result = {"step": "FINAL", "content": raw_result}
    else:
        parsed_result = raw_result

    # Normalize keys
    step = parsed_result.get("step", "").upper() if isinstance(parsed_result.get("step"), str) else ""
    content = parsed_result.get("content", parsed_result)

    # ---- EMOJI LOGIC ----
    if step in ("START", "BEGIN", "INIT") or "Formula" in parsed_result:
        # Fire emoji for Formula
        if "Formula" in parsed_result:
            print("🔥", parsed_result["Formula"])
        # Brain emoji for all Step N keys
        for key in sorted(parsed_result.keys()):
            if re.search(r"Step", key, re.IGNORECASE):
                print("🧠", parsed_result[key])
        # Robot emoji for final answer
        for key in parsed_result:
            if re.search(r"Final Answer", key, re.IGNORECASE):
                print("🤖", parsed_result[key])
        break

    elif step in ("PLAN", "THINK", "PROCESS"):
        print("🧠", content)
        continue
    else:
        # Final / unknown → just print the whole content
        print("🤖", content)
        break

print("\n\n\n")
