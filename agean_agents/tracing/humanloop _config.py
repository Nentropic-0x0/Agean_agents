import os
from humanloop import Humanloop

HUMANLOOP_API_KEY = os.getenv("HUMANLOOP_API_KEY")

humanloop = Humanloop(
    api_key=HUMANLOOP_API_KEY,
)

response = humanloop.prompts.call(
    id="pr_XaG2FKauhDS2dnd7utsIQ",
    inputs={""},
    messages=[{ "role": "user", "content": "Tell a joke" }],
    provider_api_keys={
        "openai": "OPENAI_KEY_HERE"
    }
)

print(response.logs[0].output)