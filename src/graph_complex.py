import os

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import OpenAI
from langsmith import LangSmith
from dotenv import load_dotenv
load_dotenv()
from llm import initialize_llm
from agents.ThreatDetectionAgent import ThreatDetectionAgent
from agents.VulnerabilityScannerAgent import VulnerabilityScannerAgent
from agents.IncidentReportingAgent import IncidentReportingAgent
from prompts_config import CTIPrompts



from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    ToolMessage,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langgraph.graph import END, StateGraph, START

import operator
from typing import Annotated, List, Tuple
from typing_extensions import TypedDict


### Initialize Agents
def init_agents():
    threat_detection, vuln_agent, incident_agent, cti_prompts = init_agents()
    threat_detection, vuln_scan, incidence_response= CTIPrompts()._get_agent_prompts()
    return ThreatDetectionAgent(), VulnerabilityScannerAgent(), IncidentReportingAgent(), CTIPrompts()





# Initialize LangSmith (automatically picks up API key from env vars)


# Define a simple LLM Chain
def simple_chain():
    llm = initialize_llm()
    prompt = PromptTemplate.from_template(prompt_template)
    chain = LLMChain(llm=llm, prompt=prompt)

    # Run the chain with tracing enabled
    result = tracing.trace(chain.invoke({"country": "France"}))

    print(f"Result: {result}")

def _set_if_undefined(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"Please provide your {var}")


_set_if_undefined("OPENAI_API_KEY")
_set_if_undefined("TAVILY_API_KEY")

from langchain_community.tools.tavily_search import TavilySearchResults

tools = [TavilySearchResults(max_results=3)]

from langchain import hub
from langchain_openai import ChatOpenAI

from langgraph.prebuilt import create_react_agent

# Get the prompt to use - you can modify this!

prompt.pretty_print()

# Choose the LLM that will drive the agent




class PlanExecute(TypedDict):
    input: str
    plan: List[str]
    past_steps: Annotated[List[Tuple], operator.add]
    response: str


from pydantic import BaseModel, Field


class Plan(BaseModel):
    """Plan to follow in future"""

    steps: List[str] = Field(
        description="different steps to follow, should be in sorted order"
    )

from langchain_core.prompts import ChatPromptTemplate

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import GitLoader
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)

loader = GitLoader(
    clone_url="https://github.com/hslatman/",
    repo_path="./awesome-threat-intellgence",
    branch="main",
)

python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON, chunk_size=10000, chunk_overlap=100
)

docs = loader.load()
docs = [doc for doc in docs if len(doc.page_content) < 50000]