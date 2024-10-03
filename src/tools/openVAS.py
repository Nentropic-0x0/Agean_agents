from langchain.tools import BaseTool
import requests

class OpenVASScanTool(BaseTool):
    name = "openvas_scan"
    description = "Trigger a vulnerability scan using OpenVAS and fetch scan results"

    def _run(self, target: str) -> str:
        """Trigger OpenVAS scan on a target and retrieve results"""
        try:
            # Trigger the OpenVAS scan using the OpenVAS REST API (GVM API)
            response = requests.post("http://openvas-server:9390/start_scan", json={"target": target})

            if response.status_code != 200:
                return f"Error starting OpenVAS scan: {response.text}"

            scan_id = response.json().get("scan_id")

            # Check scan status and retrieve results
            result = self._get_scan_results(scan_id)
            return result
        except Exception as e:
            return str(e)