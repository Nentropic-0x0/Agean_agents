import os
from dotenv import load_dotenv, find_dotenv
from google.cloud import secretmanager
from openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from llama_index import ChatOllama

def load_env():
    """
    Load environment variables from .env file if running in a local environment.
    """
    if os.getenv("ENVIRONMENT") == "DEV":
        load_dotenv(find_dotenv())

def get_env_variable(var_name: str) -> str:
    """
    Retrieves an environment variable from the current environment.
    Raises ValueError if the variable is not found.
    """
    value = os.getenv(var_name)
    if not value:
        raise ValueError(f"Environment variable {var_name} not found.")
    return value

def access_secret_version(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """
    Accesses a secret version from Google Cloud Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    try:
        response = client.access_secret_version(request={"name": name})
        secret_value = response.payload.data.decode("UTF-8")
        return secret_value
    except Exception as e:
        print(f"Error accessing secret: {e}")
        os.system("gcloud auth application-default login")
        return os.getenv(secret_id)

def get_llm_config():
    """
    Retrieves the LLM configuration, including API keys from environment variables or Google Secret Manager.
    """
    load_env()
    
    # Configure based on environment (local vs cloud)
    if os.getenv("ENVIRONMENT") == "DEV":
        claude_api_key = get_env_variable("CLAUDE_API_KEY")
        openai_api_key = get_env_variable("OPENAI_API_KEY")
    else:
        project_id = get_env_variable("GOOGLE_PROJECT_ID")
        claude_api_key = access_secret_version(project_id, "CLAUDE_API_KEY")
        openai_api_key = access_secret_version(project_id, "OPENAI_API_KEY")

    return {
        "providers": [
            {"name": "anthropic", "key": claude_api_key, "model": "claude-3-sonnet-20240229"},
            {"name": "openai", "key": openai_api_key, "model": "gpt-4o-mini"},
            {"name": "ollama", "model": "llama3.2:8b"}
        ]
    }

def set_llm(provider: str = "anthropic"):
    """
    Sets up the appropriate LLM provider (Anthropic, OpenAI, or Ollama) based on the provider name.
    """
    llm_config = get_llm_config()
    
    # Match provider with the corresponding LLM
    if provider == "anthropic":
        return ChatAnthropic(api_key=llm_config["providers"][0]["key"], model=llm_config["providers"][0]["model"],  temperature=0.0)
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
    provider = set_llm()
    
    if provider = None:
        provider = os.getenv("LLM_PROVIDER", "anthropic").lower()
    else:
        provider = provider.lower()
    
    return set_llm(provider)
