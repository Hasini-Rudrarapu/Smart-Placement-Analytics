from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv(".env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

response = client.chat.completions.create(
    model="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    max_tokens=50,
    messages=[
        {"role": "user", "content": "Say hello"}
    ]
)

print(response.choices[0].message.content)