import os
from typing import Optional, Dict, List, Tuple
from dotenv import load_dotenv, find_dotenv
from google.cloud import secretmanager
import openai
from langchain_anthropic import ChatAnthropic
from llama_index import ChatOllama
from portkey_ai import Portkey
from portkey_ai.exceptions import PortkeyAPIError, PortkeyRateLimitError
from core_agent import AGEAN
from prompts_config import ThreatDetectionPrompts, VulnerabilityScannerPrompts, IncidenceResponsePrompts
import json

# CTIPrompts class to manage prompts based on security role

    def _get_agent_prompts(self) -> List[str]:
        return self.threat_prompts, self.vuln_prompts, self.incidence_prompts

    def tools_as_message(self, agent: str) -> Tuple:
        """Return all tools as a tuple of strings for tools."""
        return f"{self.agent}.{_get_agent_prompts()}", str(self)

    def __str__(self) -> str:
        s = (
            "\n==========\nBegin Infosec System Prompts\n"
            "Orion is being adapted to work within a specific cyber threat intelligence framework.\n"
            "You should embody the robot and provide responses as if you were the robot.\n---\n"
        )
        for attr in dir(self):
            if (
                not attr.startswith("_")
                and isinstance(getattr(self, attr), str)
                and getattr(self, attr).strip() != ""
            ):
                s += f"{attr.replace('_', ' ').title()}: {getattr(self, attr)}\n---\n"
        s += "End Infosec System Prompts\n==========\n"
        return s

    def call_llm_judge(self, msg: json):
        # Placeholder function to handle LLM judgment, maybe for further analysis
        pass


# Environment and secret management
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


# Retrieve LLM configuration
def get_llm_config():
    load_env()

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


# Function for handling retries and fallback using Portkey with CTIPrompts
def get_chat_completion_with_fallback(messages, model, max_tokens, cti_prompts: CTIPrompts, max_retries=3):
    """
    Attempts to get a chat completion using Anthropic, with fallback to OpenAI on failure or load balancing.
    Incorporates CTI prompts and session management via CTIPrompts class.
    """
    llm_config = get_llm_config()
    portkey_api_key = get_env_variable("PORTKEY_API_KEY")
    claude_virtual_key = get_env_variable("ANTHROPIC_VIRTUAL_KEY")
    openai_virtual_key = get_env_variable("OPENAI_VIRTUAL_KEY")

    # Initialize Portkey for Anthropic
    portkey_anthropic = Portkey(
        api_key=portkey_api_key,
        virtual_key=claude_virtual_key,
        anthropic_beta="prompt-caching-2024-07-31"
    )

    # Incorporate CTI prompts into messages
    agent_prompts, system_prompt = cti_prompts.tools_as_message("Anthropic Agent")

    # Add system prompts for context
    system_message = {
        "role": "system",
        "content": system_prompt
    }
    messages.insert(0, system_message)

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
                try:
                    chat_completion = portkey_openai.chat.completions.create(
                        messages=messages,
                        model="gpt-4-turbo",  # OpenAI model example
                        max_tokens=max_tokens
                    )
                    return chat_completion.choices[0].message.content
                except (PortkeyRateLimitError, PortkeyAPIError) as e:
                    print(f"OpenAI API error: {e}. Fallback failed.")
                    return None


# Function to set up and return the LLM based on provider
def set_llm(provider: str = "anthropic"):
    """
    Sets up the appropriate LLM provider (Anthropic, OpenAI, or Ollama) based on the provider name.
    """
    llm_config = get_llm_config()

    if provider == "anthropic":
        return ChatAnthropic(api_key=llm_config["providers"][0]["key"], model=llm_config["providers"][0]["model"], temperature=0.0)
    elif provider == "openai":
        return openai.ChatCompletion(api_key=llm_config["providers"][1]["key"], model=llm_config["providers"][1]["model"], temperature=0.0)
    elif provider == "ollama":
        return ChatOllama(model=llm_config["providers"][2]["model"])
    else:
        raise ValueError(f"Unsupported provider: {provider}")


# Example usage: Using load balancing, session management, and fallback logic
messages = [
    {"role": 'user', "content": 'Summarize the above cyber event in JSON'}
]

# Initialize CTI Prompts for session management
cti_prompts = CTIPrompts(
    user_prompt="Summarize the incident in 20 words.",
    role="Threat Detection",
    objectives="Analyze and report on security vulnerabilities.",
    about_your_capabilities="I am a system designed to assist with cybersecurity threat detection."
)

# Call the chat completion with CTI session prompts and fallback suppor
# Output the response
print(response)
