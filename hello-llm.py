import os

from dotenv import load_dotenv
from groq import Groq
from groq.types.chat import ChatCompletionMessageParam

load_dotenv()

API_KEY=os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("GROQ_API_KEY is not set")

client = Groq(api_key=API_KEY)

model="openai/gpt-oss-120b"

prompt="Who is the Chief Minister of Delhi, India?"

message: ChatCompletionMessageParam = {
    "role": "user",
    "content": prompt,
}

messages: list[ChatCompletionMessageParam] = [message]

response = client.chat.completions.create(model=model, messages=messages)

print(response.choices[0].message.content)
print("Model used:", response.model)
print("Usage:", response.usage)
print("Finish reason:", response.choices[0].finish_reason)
print("Response:", response)