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

system_message: ChatCompletionMessageParam = {
    "role": "system",
    "content": "You are a helpful assistant that provides information about Indian politics."
}

while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the chat!")
        break

    user_message: ChatCompletionMessageParam = {
        "role": "user",
        "content": user_input
    }

    messages: list[ChatCompletionMessageParam] = [system_message, user_message]

    response = client.chat.completions.create(model=model, messages=messages)

    assitance_message = response.choices[0].message

    print("Assistant:", assitance_message.content)

    messages.append({
        "role": "assistant",
        "content": assitance_message.content
    })