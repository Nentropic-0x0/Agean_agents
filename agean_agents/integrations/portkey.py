'''
Portkey LLM Management


'''
from openai import OpenAI
from portkey_ai import PORTKEY_GATEWAY_URL, createHeaders



client = OpenAI(
    api_key="OPENAI_API_KEY",
    base_url="PORTKEY_GATEWAY_URL",
    default_headers=createHeaders(
        provider="openai",
        api_key="6f20c46d-18be-4a55-9897-ed2a63edc8a2"
    )
)

chat_complete = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What's a Fractal?"}],
)

print(chat_complete.choices[0].message.content)