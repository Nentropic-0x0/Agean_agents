from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv, find_dotenv
from utils import get_api_keys
from typing import Dict

load_dotenv(find_dotenv())

def main() -> object:
    llm = ChatOpenAI(api_key=get_api_keys("OPENAI"))
    return llm.invoke("Hello, world!")
    
def call_llm_and_validate(query: str):
    openai = OpenAI()
    # Step 1: Make a call to the LLM (e.g., OpenAI GPT-4)
    response = openai.Completion.create(
        engine="gpt-4o-mini",  # Use your preferred engine
        prompt=f"Summarize the following query and provide key points:\n{query}",
        max_tokens=150
    )

    # Get the response text (in this example, assume the response is JSON-formatted)
    response_text = response["choices"][0]["text"].strip()

    # Step 2: Simulate the response being parsed into the schema structure
    # In a real-world scenario, you might receive JSON that is parsed into a dict
    try:
        # Mock the response as if the LLM returned a well-structured JSON
        llm_output = {
            "summary": "This is a summary of the query.",
            "key_points": ["Key point 1", "Key point 2"],
            "confidence_score": 0.95
        }

        # Step 3: Validate the LLM response against the schema
        validated_response = LLMResponseSchema(**llm_output)
        print("Validated Response:", validated_response)
        
    except ValidationError as e:
        # Handle schema validation errors
        print("Validation Error:", e.json())


if __name__ == "__main__":
    main()