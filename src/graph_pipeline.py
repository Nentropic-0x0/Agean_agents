from typing import List, Optional

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain_openai import ChatOpenAI

import graph_complex
from llm import initialize_llm
from src.agents import incidence_response, threat_detection, vuln_scan


class GraphState(BaseModel):
    question: Optional[str] = None
    generation: Optional[str] = None
    documents: List[str] = []

"""Observe the state of the graph and modify as needed"""
def retriver_node(state: GraphState):
    new_docs = retriever.invoke(state.question)
    new_docs = [d.page_content for d in new_docs]
    state.documents.extend(new_docs)
    return {"docs": state.documents}

def define_prompts():
    
    from prompts_config import CTIPrompts
    cti_prompts = CTIPrompts()
    threat_prompts, vuln_prompts, incidence_prompts = cti_prompts._get_agent_prompts()
    return (
        list(threat_prompts.__str__()),
        list(incidence_prompts.__str__()),
        list(vuln_prompts.__str__())
        )

def rag_prompt(agent=threat_detection):
    print(agent)  
    define_prompts=define_prompts()
    return print(define_prompts)
    reg_prompt(agent=threat_detection)
    
''''''    
    rag_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", f"{agent.name}.,
        ("human", human_prompt),
    ]
)
    
llm = initalize_llm("anthropic")


rag_chain = rag_prompt | llm | StrOutputParser()
        