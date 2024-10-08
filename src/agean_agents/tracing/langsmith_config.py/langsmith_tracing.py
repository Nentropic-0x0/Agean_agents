import Anthropic
import openai
from langsmith import traceable
from langsmith.wrappers import wrap_anthropic, wrap_openai

# Auto-trace LLM calls in-context
oai_client = wrap_openai(openai.Client())
anthr_client = wrap_anthropic(Anthropic.Client())

@traceable # Auto-trace this function
def pipeline(user_input: str):
    result = client.chat.completions.create(
        messages=[{"role": "user", "content": user_input}],
        model="gpt-3.5-turbo"
    )
    return result.choices[0].message.content

pipeline("Hello, world!")
# Out:  Hello there! How can I assist you today?
