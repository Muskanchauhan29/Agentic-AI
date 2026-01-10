# Chain Of Thought Prompting
from dotenv import load_dotenv
import os
import google.generativeai as genai

import requests

import json



load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")
chat = model.start_chat(history=[])


def get_weather(city: str):
    response = requests.get(f"https://wttr.in/{city}?format=3")
    if response.status_code == 200:
        return response.text
    return "Something went wrong"


available_tools ={
    "get_weather": get_weather
}

SYSTEM_PROMPT = """
    You're an expert AI Assistant in resolving user queries using chain of thought.
    You work on START, PLAN and OUPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.
    You can also call a tool if required from the list of available tools.
    for every tool call wait for the observe step which is the output from the called tool.

    Rules:
    - Strictly Follow the given JSON output format
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (which is going to the displayed to the user).

    Output JSON Format:
    { "step": "START" | "PLAN" | "OUTPUT" | "TOOL", "content": "string", "tool": "string", "input": "string" }

    Available Tools:
    - get_weather(city): Takes city name as an input string and returns the weather info about the city. 

    Example 1:
    START: Hey, Can you solve 2 + 3 * 5 / 10
    PLAN: { "step": "PLAN": "content": "Seems like user is interested in math problem" }
    PLAN: { "step": "PLAN": "content": "looking at the problem, we should solve this using BODMAS method" }
    PLAN: { "step": "PLAN": "content": "Yes, The BODMAS is correct thing to be done here" }
    PLAN: { "step": "PLAN": "content": "first we must multiply 3 * 5 which is 15" }
    PLAN: { "step": "PLAN": "content": "Now the new equation is 2 + 15 / 10" }
    PLAN: { "step": "PLAN": "content": "We must perform divide that is 15 / 10  = 1.5" }
    PLAN: { "step": "PLAN": "content": "Now the new equation is 2 + 1.5" }
    PLAN: { "step": "PLAN": "content": "Now finally lets perform the add 3.5" }
    PLAN: { "step": "PLAN": "content": "Great, we have solved and finally left with 3.5 as ans" }
    OUTPUT: { "step": "OUTPUT": "content": "3.5" }


    Example 2:
    START: Hey, What is the weather of Delhi?
    PLAN: { "step": "PLAN": "content": "Seems like user is interested in getting weather of Delhi in India" }
    PLAN: { "step": "PLAN": "content": "Lets see if we have any available tool from the list of available tools" }
    PLAN: { "step": "PLAN": "content": "Great! we have get_weather tool available for this query." }
    PLAN: { "step": "PLAN": "content": "I need to call get_weather tool for delhi as input for city" }
    PLAN: { "step": "TOOL": "tool": "get_weather", "input": "delhi" }
     PLAN: { "step": "OBSERVE": "tool": "get_weather", "output": "the temp of delhi is cloudy with 17 C" }
    OUTPUT: { "step": "OUTPUT": "content": "The current weather of delhi is 17 C with cloudy sky" }
    
"""

print("\n\n\n")

message_history = [
    { "role": "system", "content": SYSTEM_PROMPT },
]

user_query = input("👉🏻")
message_history.append({ "role": "user", "content": user_query })

prompt = f"""
{SYSTEM_PROMPT}

Respond ONLY in valid JSON:
{{
  "step": "PLAN | TOOL | OUTPUT",
  "content": "",
  "tool": "",
  "input": ""
}}

User input:
{user_query}
"""



while True:
    response = chat.send_message(prompt)
    raw = response.text

    # clean + parse Gemini output
    raw = raw.strip().replace("```json", "").replace("```", "")
    if not raw:
        print("❌ Empty response")
        continue

    parsed_result = json.loads(raw)

    if parsed_result.get("step") == "START":
        print("🔥", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "TOOL":
        tool_to_call = parsed_result.get("tool")
        tool_input = parsed_result.get("input")
        print(f"⚙️: {tool_to_call} ({tool_input})")

        tool_response = available_tools[tool_to_call](tool_input)
        print(f"⚙️ RESULT:", tool_response)

        # send observation back to Gemini
        prompt = f"""
OBSERVE:
{tool_response}

Now respond with OUTPUT in valid JSON.
"""
        continue

    if parsed_result.get("step") == "PLAN":
        print("🧠", parsed_result.get("content"))

        prompt = "Continue. Decide the next step (TOOL or OUTPUT) in valid JSON."
        continue
    
    



    if parsed_result.get("step") == "OUTPUT":
        print("🤖", parsed_result.get("content"))
        break


print("\n\n\n")