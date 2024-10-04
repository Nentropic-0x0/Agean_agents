import json
from datetime import datetime
from typing import Any, Dict, List

from core_agent import AGEAN
from src.llm import get_llm
from src.prompts_config import CTIPrompts
from src.system_prompts import _get_prompts
from langchain.agents import AgentExecutor
from logger import logger 


import json
from datetime import datetime
from typing import Dict, Any, List

class VulnerabilityScannerAgent(AGEAN):

    def __init__(self, 
                 cti=CTIPrompts(),  # Ensure CTIPrompts is correctly imported
                 name: str = "VulnerabilityScanner", 
                 llm=None,  # Default to None, assuming LLM is passed during instantiation
                 verbose: bool = True, 
                 streaming: bool = False, 
                 vuln_prompts: List[str] = None,  # Correct the prompt structure
                 accumulate_chat_history: bool = True):
        
        """
        Initializes the VulnerabilityScannerAgent with specific LLM, prompts, and behavior settings.
        """
        super().__init__(name=name, accumulate_chat_history=accumulate_chat_history, 
                         verbose=verbose, streaming=streaming,)
        self.llm = llm or get_llm()  # Assign the LLM if not provided
        self.verbose = verbose
        self.system_data = {}

        # Initialize vulnerability prompts from CTIPrompts
        self.vuln_prompts = vuln_prompts or cti.vuln_prompts._get_agent_prompts()

    # Core methods for Vulnerability Scanner Agent

    def _get_executor(self, verbose: bool) -> "AgentExecutor":
        """
        Initialize and return an AgentExecutor for the vulnerability scanning agent.
        """
        executor = AgentExecutor(agent=self.llm, tools=self._get_tools(), verbose=verbose)
        return executor

    def _receive_system_data(self, data: Dict[str, Any]):
        """
        Receives and processes system data for vulnerability scanning.
        """
        self.system_data = data
        if self.verbose:
            print(f"Received system data: {json.dumps(self.system_data, indent=2)}")

    def _to_json(self, data: Dict[str, Any]) -> str:
        """
        Converts system or vulnerability data to JSON format.
        """
        return json.dumps(data, indent=4)

    def scan_for_vulnerabilities(self) -> str:
        """
        Scans the received system data for vulnerabilities using vulnerability databases like CVE.
        """
        if not hasattr(self, 'system_data') or not self.system_data:
            raise ValueError("No system data has been received for scanning.")
        
        # Construct the query for the LLM or database
        query = f"Check for vulnerabilities in this system: {self._to_json(self.system_data)}"
        
        # Invoke the LLM to scan for vulnerabilities (assuming LLM interaction)
        response = self.invoke(query)  # invoke method should be implemented properly
        
        if self.verbose:
            print(f"Vulnerability scan result: {response}")
        
        return response

    def invoke(self, query: str) -> str:
        """
        Simulate invoking the LLM to process a query.
        """
        # Example interaction with the LLM (self.llm)
        response = self.llm.process(query)
        return response

    def get_vulnerability_info(self, cve_id: str) -> Dict[str, Any]:
        """
        Fetches detailed vulnerability information from a vulnerability database (e.g., CVE) by CVE ID.
        """
        vulnerability_info = {
            "cve_id": cve_id,
            "description": "Example vulnerability description.",
            "severity": "High",
            "affected_software": ["nginx", "openssl"],
            "recommendations": ["Upgrade to the latest version."]
        }
        
        if self.verbose:
            print(f"Fetched vulnerability info: {json.dumps(vulnerability_info, indent=2)}")
        
        return vulnerability_info

    def generate_report(self) -> str:
        """
        Generates a vulnerability scanning report based on the scan results.
        """
        if not hasattr(self, 'system_data') or not self.system_data:
            raise ValueError("No system data to generate a report from.")
        
        vulnerabilities_found = self.scan_for_vulnerabilities()
        report = {
            "scan_time": datetime.utcnow().isoformat(),
            "system": self.system_data.get("system"),
            "version": self.system_data.get("version"),
            "vulnerabilities": vulnerabilities_found,
            "recommendations": "Apply patches for the vulnerabilities listed."
        }
        
        report_json = self._to_json(report)
        if self.verbose:
            print(f"Generated report: {report_json}")
        
        return report_json

    def _get_tools(self) -> List:
        """
        Retrieve tools specific to vulnerability scanning, such as CVE fetchers or patch analyzers.
        """
        return [
            {"name": "CVE Fetcher", "description": "Fetch vulnerabilities from CVE database."},
            {"name": "Patch Analyzer", "description": "Analyze system patches."}
        ]

    def log_event(self, log_data: Dict[str, Any]):
        """
        Logs the results of the vulnerability scan for auditing and future reference.
        """
        log_json = self._to_json(log_data)
        if self.verbose:
            print(f"Logging event: {log_json}")
        # Simulate logging here
        with open("vulnerability_scan_log.json", "a") as f:
            f.write(f"{log_json}\n")
