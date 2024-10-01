"""AGEAN is an extensible Agent System for Cybersecurity Analysis and Workflows.
- It is defaulted to be configured for ECS (ELK Stack) schemas




"""
from typing import Dict, Optional, Tuple

from prompts_config import CTIPrompts


class Agean:
    def __init__(self, name: str="Multi-Purpose Cybersecurity Agent System", llm: str = "gpt-4o-mini", 
                 tools: Optional[List] = None, tracing: bool = True, 
                 prompts: Optional[CTIPrompts] = CTIPrompts(), verbose: bool = False, accumulate_chat_history: bool = True,
                 show_token_usage: bool=False, streaming: bool = True, blacklist: Optional[List[str]] = None):
        
        self.name = name
        self.prompts = prompts
        self.__chat_history = []
        self.__llm = llm.with_config({"streaming": streaming})
        self.__tools = tools
        self.__memory_key = "chat_history"
        self.scratchpad = "agent_scratchpad"
        self.blacklist = blacklist if blacklist else []
        self.__accumulate_chat_history = accumulate_chat_history
        self.__show_token_usage = show_token_usage
        self.__verbose = verbose
                        
        
    