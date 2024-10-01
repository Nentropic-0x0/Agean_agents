"""AGEAN is an extensible Agent System for Cybersecurity Analysis and Workflows.
- It is defaulted to be configured for ECS (ELK Stack) schemas




"""
from typing import Dict, List, Optional, Tuple
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import OpenAI
from langsmith import LangSmith

from typing import Any, AsyncIterable, Dict, Literal, Optional, Union

from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.prompts import MessagesPlaceholder
from langchain_community.callbacks import get_openai_callback
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI, ChatOpenAI

from .prompts import RobotSystemPrompts, system_prompts
from .tools import ROSATools

from src.prompts_config import CTIPrompts
tracing = LangSmith()

class Agean:
    def __init__(self, name: str="Multi-Purpose Cybersecurity Agent System", 
                 llm: str = "gpt-4o-mini", 
                 tools: Optional[List] = None, tracing: bool = True, 
                 prompts: Optional[CTIPrompts] = CTIPrompts(), verbose: bool = False, accumulate_chat_history: bool = True,
                 show_token_usage: bool=False, streaming: bool = True, blacklist: Optional[List[str]] = None):
        
        self.__name = name
        self.__prompts = prompts
        self.__chat_history = []
        self.__llm = llm.with_config({"streaming": streaming})
        self.__tools = self.get_tools(
            packages=tool_packages, tools=tools, blacklist=self.blacklist
        )
        self.__memory_key = "chat_history"
        self.__scratchpad = "agent_scratchpad"
        self.__blacklistblacklist = blacklist if blacklist else []
        self.__accumulate_chat_history = accumulate_chat_history
        self.__show_token_usage = show_token_usage if not streaming else False
        self.__verbose = verbose
        
    @property
    def chat_history(self):
        "Get Chat History"
        return self.__chat_history
    
    def clear_chat(self):
        "Clear Chat History"
        self.__chat_history = []
    
    def invoke(self, query: str) -> str:
        """
        Invoke the agent with a user query and return the response.

        This method processes the user's query through the agent, handles token usage tracking,
        and updates the chat history.

        Args:
            query (str): The user's input query to be processed by the agent.

        Returns:
            str: The agent's response to the query. If an error occurs, it returns an error message.

        Raises:
            Any exceptions raised during the invocation process are caught and returned as error messages.

        Note:
            - This method uses OpenAI's callback to track token usage if enabled.
            - The chat history is updated with the query and response if successful.
            - Token usage is printed if the show_token_usage flag is set.
        """
        
        try:
            result = self.__executor.invoke(
                {"input": query, "chat_history": self.__chat_history}
            )
        except Exception as e:
            return f"Error: {e}"
        
        self._record_chat_history(query, result["output"])
        return result["output"]
    
    async def astream(self, query: str) -> AsyncIterable[Dict[str, Any]]:
        """
        Asynchronously stream the agent's response to a user query.

        This method processes the user's query and yields events as they occur,
        including token generation, tool usage, and final output. It's designed
        for use when streaming is enabled.

        Args:
            query (str): The user's input query.

        Returns:
            AsyncIterable[Dict[str, Any]]: An asynchronous iterable of dictionaries
            containing event information. Each dictionary has a 'type' key and
            additional keys depending on the event type:
            - 'token': Yields generated tokens with 'content'.
            - 'tool_start': Indicates the start of a tool execution with 'name' and 'input'.
            - 'tool_end': Indicates the end of a tool execution with 'name' and 'output'.
            - 'final': Provides the final output of the agent with 'content'.
            - 'error': Indicates an error occurred with 'content' describing the error.

        Raises:
            ValueError: If streaming is not enabled for this ROSA instance.
            Exception: If an error occurs during the streaming process.

        Note:
            This method updates the chat history with the final output if successful.
        """
        if not self.__streaming:
            raise ValueError(
                "Streaming is not enabled. Use 'invoke' method instead or initialize ROSA with streaming=True."
            )
        try:
            final_output = ""
            async for event in self.__executor.astream_events(
                input={"input": query, "chat_history": self.__chat_history},
                config={"run_name": "Agent"},
            ):
                kind=event["event"]
                
                if kind == "on_chat_model_stream":
                    # Extract the content from the event and yield it.
                    content = event["data"]["chunk"].content
                    
                elif kind == "on_tool_start":
                    yield {
                        "type": "tool_start",
                        "name": event["name"],
                        "input": event["data"].get("input"),
                    }
                elif kind == "on_chain_end":
                    if event["name"] == "Agent":
                        chain_output = event["data"].get("output", {}).get("output")
                        if chain_output:
                            final_output = (
                                chain_output
                            )
                            yield {"type": "final", "content": chain_output}
            if final_output:
                self._record_chat_history(query, final_output)
        except Exception as e:
            yield {"type": "error", "content": f"Error: {e}"}
        
        def _get_executor(self, verbose: bool) -> AgentExecutor:
            executor = AgentExecutor(
                agent =self.__agent,
                tools=self.__tols.get_tools(),
                stream_runnable=self.__streaming,
                verbose=verbose,
                
            )
            return executor

        def _get_agent(self):
            agent = (
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                        x["intermediate_steps"]
                    ),
                    "chat_history": lambda x: x["chat_history"],
                }
                | self.__prompts
                | self.__llm_with_tools
                | OpenAIToolsAgentOutputParser()
            )
        
        def _get_tools(
            self,
            packages: Optional[List],
            tools: Optional[List],
            blacklist: Optional[List],        
            ) -> AGEANTools:
            asean_tools= AGEANTools(blacklist=blacklist)
            if tools:
                asean_tools.add_tools(tools)
            if packages:
                asean_tools.add_packages(packages, blacklist=blacklist)                         
                            
                        
                    
                
            

    
    
                    
        
    