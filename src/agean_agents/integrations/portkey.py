import os
from dotenv import load_dotenv, find_dotenv
from google.cloud import secretmanager
from openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from llama_index import ChatOllama
from portkey_ai import Portkey
from portkey_ai.exceptions import PortkeyAPIError, PortkeyRateLimitError
from together import Together
from llm import load_env, get_env_variable, access_secret_version, get_llm_config

def load_env():
    """
    Load environment variables from .env file if running in a local environment.
    """
    if os.getenv("ENVIRONMENT") == "DEV":
        load_dotenv(find_dotenv())
        load_env()
        get_env_variable("PORTKEY_API_KEY")
     if os.getenv("ENVIRONMENT" == "PROD")   
        access_secret_version()
        project_id = os.getenv("PROJECT_ID")
        get_env_variable("GOOGLE_SECRET_KEY")
        


# Function for handling retries and fallback using Portkey
def get_chat_completion_with_fallback(messages, model, max_tokens, max_retries=3):
    """
    Attempts to get a chat completion using Anthropic, with fallback to OpenAI on failure or load balancing.
    """
    portkey_api_key = get_env_variable("PORTKEY_API_KEY")
    claude_virtual_key = get_env_variable("ANTHROPIC_VIRTUAL_KEY")
    openai_virtual_key = get_env_variable("OPENAI_VIRTUAL_KEY")

    # Initialize Portkey for Anthropic
    portkey_anthropic = Portkey(
        api_key=portkey_api_key,
        virtual_key=claude_virtual_key,
        anthropic_beta="prompt-caching-2024-07-31"
    )

    retry_count = 0
    while retry_count < max_retries:
        try:
            # Attempt Anthropic call
            chat_completion = portkey_anthropic.chat.completions.create(
                messages=messages,
                model=model,
                max_tokens=max_tokens
            )
            return chat_completion.choices[0].message.content
        
        except (PortkeyRateLimitError, PortkeyAPIError) as e:
            retry_count += 1
            print(f"Anthropic API error: {e}. Retry {retry_count}/{max_retries}.")
        
            # If retries exhausted, fallback to OpenAI
            if retry_count == max_retries:
                print("Falling back to OpenAI after retries exhausted.")
                portkey_openai = Portkey(
                    api_key=portkey_api_key,
                    virtual_key=openai_virtual_key
                )
                chat_completion = portkey_openai.chat.completions.create(
                    messages=messages,
                    model="gpt-4-turbo",  # OpenAI model example
                    max_tokens=max_tokens
                )
                return chat_completion.choices[0].message.content

# Function to set up and return the LLM based on provider
def set_llm(provider: str = "anthropic"):
    """
    Sets up the appropriate LLM provider (Anthropic, OpenAI, or Ollama) based on the provider name.
    """
    llm_config = get_llm_config()
    
    # Match provider with the corresponding LLM
    if provider == "anthropic":
        return ChatAnthropic(api_key=llm_config["providers"][0]["key"], model=llm_config["providers"][0]["model"], temperature=0.0)
    elif provider == "openai":
        return ChatOpenAI(api_key=llm_config["providers"][1]["key"], model=llm_config["providers"][1]["model"], temperature=0.0)
    elif provider == "ollama":
        return ChatOllama(model=llm_config["providers"][2]["model"])
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def initialize_llm(provider: str = None):
    """
    Initializes the LLM based on the provider specified in the environment or defaults to OpenAI.
    """
    if provider is None:
        provider = os.getenv("LLM_PROVIDER", "anthropic").lower()
    
    return set_llm(provider)

# Example usage: Using load balancing and fallback logic
messages = [
    { "role": 'system', "content": [
        {
            "type": "text", "text": "You are a helpful assistant."
        },
        {
            "type": "text", "text": "<TEXT_TO_CACHE>",
            "cache_control": {"type": "ephemeral"}
        }
    ]},
    { "role": 'user', "content": 'Summarize the above story in 20 words' }
]

# Call the chat completion with fallback support
response = get_chat_completion_with_fallback(messages=messages, model='claude-3-sonnet-20240229', max_tokens=250)

# Output the response
print(response)