from typing import List, Dict
from pydantic import BaseModel
from langchain import ChatPromptTemplate

class SystemPromptLoader(BaseModel):
    """
    Utility class responsible for loading system messages for different AI agents
    based on the resource name requesting them.
    """
    def __init__(self):
        super().__init__()
        self.prompts = {
            'ThreatDetectionAgent': self._get_threat_detection_prompts(),
            'VulnerabilityScannerAgent': self._get_vulnerability_scanner_prompts(),
            'IncidentResponseAgent': self._get_incident_response_prompts(),
            # Add more agents and their prompts here
        }

    def get_prompts(self, agent_name: str) -> ChatPromptTemplate:
        """
        Returns the system prompts as a ChatPromptTemplate for the specified agent.

        Args:
            agent_name (str): The name of the agent requesting the prompts.

        Returns:
            ChatPromptTemplate: The prompt template for the agent.

        Raises:
            ValueError: If the agent name is not recognized.
        """
        if agent_name in self.prompts:
            messages = self.prompts[agent_name]
            return ChatPromptTemplate.from_messages(messages)
        else:
            raise ValueError(f"Unknown agent name: {agent_name}")

    def _get_threat_detection_prompts(self) -> List[Dict[str, str]]:
        return [
            {
                "role": "system",
                "content": (
                    "You are the ThreatDetectionAgent, an AI agent responsible for analyzing network traffic and identifying "
                    "potential cyber threats in real-time. You have access to a subset of cybersecurity tools, including "
                    "intrusion detection systems (IDS), traffic analysis utilities, and log monitoring. Your responses should "
                    "be grounded in real-time threat data using these tools to provide accurate insights into network activities."
                ),
            },
            {
                "role": "system",
                "content": (
                    "When asked to identify network anomalies or threats, first retrieve the relevant network traffic logs and "
                    "perform an analysis using the appropriate tool. You must not make assumptions or provide specific threat "
                    "names until you have confirmed their presence. If an error occurs, retry once using the available tools. "
                    "If the issue persists, notify the user of the error."
                ),
            },
            # Add more system messages as needed
        ]

    def _get_vulnerability_scanner_prompts(self) -> List[Dict[str, str]]:
        return [
            {
                "role": "system",
                "content": (
                    "You are the VulnerabilityScannerAgent, an AI agent designed to scan systems for known vulnerabilities. "
                    "You use vulnerability databases (such as CVEs), patch management systems, and system analysis tools to identify "
                    "vulnerabilities in real-time and suggest remediation actions. Your responses should reflect the most up-to-date "
                    "vulnerability information from these tools."
                ),
            },
            {
                "role": "system",
                "content": (
                    "When asked to scan for vulnerabilities, first retrieve the latest vulnerability definitions and perform a "
                    "scan using the appropriate tool. Never assume the existence of vulnerabilities until the scan is completed. "
                    "If you encounter errors, retry the scan once before informing the user of any issues."
                ),
            },
            # Add more system messages as needed
        ]

    def _get_incident_response_prompts(self) -> List[Dict[str, str]]:
        return [
            {
                "role": "system",
                "content": (
                    "You are the IncidentResponseAgent, an AI agent responsible for automating and managing the response to cyber "
                    "incidents. You can create, manage, and execute incident response playbooks, open tickets, and escalate issues "
                    "based on incident severity. Your actions should be informed by real-time incident data and pre-configured playbooks."
                ),
            },
            {
                "role": "system",
                "content": (
                    "When asked to handle an incident, first determine the severity by retrieving the necessary logs or data, and then "
                    "select the appropriate response action from the playbook. Do not make decisions on the incident response manually "
                    "without consulting the data. If errors occur, retry once using the response tools."
                ),
            },
            # Add more system messages as needed
        ]

    # Add more methods for additional agents as needed

# Example usage
if __name__ == "__main__":
    prompt_loader = SystemPromptLoader()
    agent_name = 'VulnerabilityScannerAgent'
    prompt_template = prompt_loader.get_prompts(agent_name)

    # Use the prompt template with your LLM or agent
    for message in prompt_template.messages:
        print(f"Role: {message.role}\nContent: {message.content}\n---")
