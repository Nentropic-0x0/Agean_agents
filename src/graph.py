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
from system_prompts import ThreatDetectionPrompts, VulnerabilityScannerPrompts, IncidenceResponsePrompts

from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    ToolMessage,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langgraph.graph import END, StateGraph, START

### Initialize Agents
def init_agents():
    return ThreatDetectionAgent(), VulnerabilityScannerAgent(), IncidentReportingAgent(), CTIPrompts()



threat_detection, vuln_agent, incident_agent, cti_prompts = init_agents()
threat_prompts, vuln_prompts, incident_prompts = ThreatDetectionPrompts(cti_prompts).get_prompts(), \
                                                VulnerabilityScannerPrompts(cti_prompts).get_prompts(), \ 
                                                IncidenceResponsePrompts(cti_prompts).get_prompts()

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
prompt = hub.pull("ih/ih-react-agent-executor")
prompt.pretty_print()

# Choose the LLM that will drive the agent
agent_executor = create_react_agent(llm, tools, state_modifier=prompt)

import operator
from typing import Annotated, List, Tuple
from typing_extensions import TypedDict


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

if agent == threat_detection:
    planner_prompt = ChatPromptTemplate.from_messages(
        [
            (
                threat_prompts._getprompts(),
                
            ),
            ("placeholder", "{messages}"),
        ]
    )
    planner = planner_prompt | ChatOpenAI(
        model=llm, temperature=0
    ).with_structured_output(Plan)