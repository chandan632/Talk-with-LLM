import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ["GROQ_API_KEY"])

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": "Who is the current Chief Minister of Delhi? Search the web and give me the answer.",
        }
    ],
    tools=[
        {
            "type": "browser_search"
        }
    ],
)

message = response.choices[0].message

print("Answer:")
print(message.content)

print("\nReasoning:")
print(message.reasoning)

if message.executed_tools:
    print("\nTools used:")
    print(message.executed_tools)