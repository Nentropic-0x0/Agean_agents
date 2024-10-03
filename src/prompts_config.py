from typing import Optional, Dict, List, Tuple
from src.core_agent.agean import AGEAN
from src.system_prompts import ThreatDetectionPrompts, VulnerabilityScannerPrompts, IncidenceResponsePrompts
import json

class CTIPrompts:
    def __init__(
        self,
        user_prompt: Optional[str] = None,
        assistant_prompt: Optional[str] = None,
        role: Optional[str] = None,
        about_your_capabilities: Optional[str] = None,
        objectives: Optional[str] = None,
        env_variables: Optional[str] = None,
        shared_tools: Optional[Dict[str, str]] = None,
        threat_detection: List[str] = ThreatDetectionPrompts(AGEAN).get_prompts(),
        vulnerability_scanner: List[str] = VulnerabilityScannerPrompts(AGEAN).get_prompts(),
        incidence_response: List[str] = IncidenceResponsePrompts(AGEAN).get_prompts(),      
    ):
        self.threat_detection = threat_detection
        self.vulnerability_scanner = vulnerability_scanner
        self.incidence_response = incidence_response
        self.user_prompt = user_prompt
        self.assistant_prompt = assistant_prompt
        self.role = role
        self.about_your_capabilities = about_your_capabilities
        self.objectives = objectives
        self.env_variables = env_variables
        self.shared_tools = shared_tools
    
    
        
    def _get_agent_prompts(self) -> List[str]:
        return self.threat_detection, self.vulnerability_scanner, self.incidence_response
        
    def as_message(self, agent: str) -> Tuple:
        "Return all prompts as a tuple of strings for tools"
        return self._get_agents(), str(self)
    
    def __str__(self) -> str:
        s = (
            "\n==========\nBegin Infosec System Prompts\nOrion is being adapted to work within a specific "
            "cyber threat intelligence framework. The following prompts are provided to help you understand the professional or functional role you play"
            "working with. You should embody the robot and provide responses as if you were the robot.\n---\n"
        )
        # For all string attributes, if the attribute is not None, add it to the str
        for attr in dir(self):
            if (
                not attr.startswith("_")
                and isinstance(getattr(self, attr), str)
                and getattr(self, attr).strip() != ""
            ):
                # Use the name of the variable as the prompt title (e.g. about_your_operators -> About Your Operators)
                s += f"{attr.replace('_', ' ').title()}: {getattr(self, attr)}\n---\n"
        s += "End Infosec System Prompts\n==========\n"
        return s
    
    def call_llm_judge(msg: json):