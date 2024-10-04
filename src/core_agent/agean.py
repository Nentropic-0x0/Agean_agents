from typing import Any, AsyncIterable, Dict, List, Optional, Tuple

from langchain.agents import AgentExecutor
from langsmith import LangSmith

from src.llm import llm_config, model
from src.prompts_config import CTIPrompts
from src.tools import CTITools


class AGEAN:
    def __init__(self, name: str = "Multi-Purpose Cybersecurity Agent System", 
                 tools: Optional[List] = None, tracing: bool = True, 
                 verbose: bool = False, accumulate_chat_history: bool = True,
                 show_token_usage: bool = False, streaming: bool = True, 
                 blacklist: Optional[List[str]] = None):
        self.tracing = LangSmith()
        self.__name = name
        self.__chat_history = []
        self.__llm = llm_config(streaming=streaming)
        self.__tools = self._get_tools(packages=None, tools=tools, blacklist=blacklist)
        self.__memory_key = "chat_history"
        self.__scratchpad = "agent_scratchpad"
        self.__accumulate_chat_history = accumulate_chat_history
        self.__show_token_usage = show_token_usage if not streaming else False
        self.__verbose = verbose
        self.__invoke = invoke()


    def process_query(self, query: str) -> str:
        return query.strip().lower()
        
    @property
    def chat_history(self):
        """Return chat history."""
        return self.__chat_history
    
    @property
    def invoke_llm(self, query:List[str]):

    def invoke(self, query: str) -> str:
        """
        Invoke the agent with a user query and return the response.
        """
        try:
            result = self.__executor.invoke({"input": query, "chat_history": self.__chat_history})
        except Exception as e:
            return f"Error: {e}"
        
        self._record_chat_history(query, result["output"])
        return result["output"]

    async def astream(self, query: str) -> AsyncIterable[Dict[str, Any]]:
        """
        Asynchronously stream the agent's response to a user query.
        """
        if not self.__streaming:
            raise ValueError("Streaming not enabled. Use 'invoke' method or initialize with streaming=True.")
        try:
            final_output = ""
            async for event in self.__executor.astream_events(
                input={"input": query, "chat_history": self.__chat_history}, config={"run_name": "Agent"}):
                
                if event["event"] == "on_chat_model_stream":
                    yield {"type": "token", "content": event["data"]["chunk"].content}
                elif event["event"] == "on_tool_start":
                    yield {"type": "tool_start", "name": event["name"], "input": event["data"].get("input")}
                elif event["event"] == "on_chain_end":
                    if event["name"] == "Agent":
                        chain_output = event["data"].get("output", {}).get("output")
                        if chain_output:
                            final_output = chain_output
                            yield {"type": "final", "content": chain_output}
            if final_output:
                self._record_chat_history(query, final_output)
        except Exception as e:
            yield {"type": "error", "content": f"Error: {e}"}

    def _get_executor(self, verbose: bool) -> AgentExecutor:
        """
        Retrieve the executor instance for handling agent tasks.
        """
        return AgentExecutor(agent=self.__agent, tools=self.__tools, stream_runnable=self.__streaming, verbose=verbose)

    def _get_tools(self, packages: Optional[List], tools: Optional[List], blacklist: Optional[List]) -> 'AGEANTools':
        """
        Set up tools for the agent, filtering with a blacklist if necessary.
        """
        asean_tools = AGEANTools(blacklist=blacklist)
        if tools:
            asean_tools.add_tools(tools)
        if packages:
            asean_tools.add_packages(packages, blacklist=blacklist)
        return asean_tools

    def _record_chat_history(self, query: str, response: str):
        """
        Record the chat history if accumulation is enabled.
        """
        if self.__accumulate_chat_history:
            self.__chat_history.extend([{"input": query}, {"response": response}])

    def clear_chat(self):
        """Clear the agent's chat history."""
        self.__chat_history = []

    def task_handler(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Handle individual tasks from a task queue.
        """
        return tasks.pop(0) if tasks else {}

    def task_prioritize(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Prioritize tasks based on a custom prioritization strategy.
        """
        priorities = []
        while tasks:
            task = self.task_handler(tasks)
            priorities.append(task)
        return priorities

    def map_to_ecs(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map an incoming event to Elastic Common Schema (ECS) fields for cybersecurity applications.
        """
        ecs_mapping = {
            "source_ip": event.get("source.ip"),
            "destination_ip": event.get("destination.ip"),
            "event_action": event.get("event.action"),
            "timestamp": event.get("timestamp"),
            "file_name": event.get("file.name"),
            "process_name": event.get("process.name"),
            "threat_indicator": event.get("threat.indicator"),
        }
        return {key: value for key, value in ecs_mapping.items() if value is not None}

    def fetch_cti_data(self, indicator: str) -> Dict[str, Any]:
        """
        Fetch Cyber Threat Intelligence (CTI) data for a given indicator (IP, domain, file hash).
        """
        return CTITools.fetch_threat_intelligence(indicator)

    def execute_playbook(self, playbook: str, incident_data: Dict[str, Any]) -> str:
        """
        Execute an incident response playbook with the provided incident data.
        """
        # Placeholder implementation: Customize this method for real playbook execution
        response = f"Executing {playbook} for incident {incident_data['incident_id']}"
        return response
      
                        
                    
                
            

    
    
                    
        
    