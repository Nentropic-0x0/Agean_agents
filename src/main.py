import os

from dotenv import find_dotenv, load_dotenv
from langchain_openai import ChatOpenAI

from utils import get_api_keys

load_dotenv(find_dotenv())

def main() -> object:
    llm = ChatOpenAI(api_key=get_api_keys("OPENAI"))
    return llm.invoke("Hello, world!")
    



if __name__ == "__main__":
    main()