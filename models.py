import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("GROQ_API_KEY is not set")

client = Groq(api_key=API_KEY)

response = client.models.list()
models = response.data

for model in models:
    print(f"Model ID: {model.id}")
    print(f"Object: {model.object}")
    print(f"Owned By: {model.owned_by}")
    print(f"Created: {model.created}")
    print("-" * 40)