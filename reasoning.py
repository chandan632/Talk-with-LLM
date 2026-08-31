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
            "content": """
            I have 100 users.

            Each user makes 50 API requests per minute.

            How many requests per second does my system need to handle?
            Explain the calculation.
            """,
        }
    ],
)

message = response.choices[0].message

print("Answer:")
print(message.content)

print("\nReasoning:")
print(message.reasoning)