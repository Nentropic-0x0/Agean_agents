import json
from typing import Any, Dict, List

from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from transformers import pipeline


class IntelligenceReportVectorizer:
    
    def __init__(self, model_type: str = "huggingface", model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the IntelligenceReportVectorizer with an embeddings model.
        :param model_type: The type of embeddings model to use ('huggingface', 'openai').
        :param model_name: The specific model to load, defaults to a HuggingFace model.
        """
        self.model_type = model_type
        self.model_name = model_name
        self.embeddings_model = self.load_model()

    def load_model(self):
        """
        Load the specified embeddings model.
        """
        if self.model_type == "huggingface":
            # Use a Hugging Face embeddings model
            return HuggingFaceEmbeddings(model_name=self.model_name)
        elif self.model_type == "openai":
            # Use OpenAI embeddings model (requires OpenAI API Key)
            return OpenAIEmbeddings()
        else:
            raise ValueError(f"Model type {self.model_type} is not supported.")

    def extract_fields(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract and normalize important fields from the intelligence report.
        :param report: The intelligence report in dictionary format.
        :return: A normalized dictionary of relevant fields.
        """
        # Extract key fields from the report for embedding generation
        fields = {
            "threat_actor": report.get("threat_actor", "unknown"),
            "malware_family": report.get("malware_family", "unknown"),
            "impact_assessment": report.get("impact_assessment", ""),
            "target_sector": report.get("target_sector", ""),
            "attack_vector": report.get("attack_vector", ""),
            "executive_summary": report.get("executive_summary", ""),
            "analyst_notes": report.get("analyst_notes", "")
        }

        # Normalize the extracted data into a single textual representation for embeddings
        normalized_text = (
            f"Threat Actor: {fields['threat_actor']}. "
            f"Malware Family: {fields['malware_family']}. "
            f"Impact Assessment: {fields['impact_assessment']}. "
            f"Target Sector: {fields['target_sector']}. "
            f"Attack Vector: {fields['attack_vector']}. "
            f"Summary: {fields['executive_summary']}. "
            f"Notes: {fields['analyst_notes']}."
        )

        return {"normalized_text": normalized_text, "fields": fields}

    def enrich_data(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optionally enrich the report with additional data, such as historical context, external threat data, etc.
        :param report: The intelligence report in dictionary format.
        :return: Enriched data (could include external threat intel, historical insights, etc.).
        """
        # Placeholder for enriching data (e.g., augment with OSINT, historical incidents)
        # Here, you could integrate with external APIs or services to add more context.
        enriched_data = {
            "historical_context": f"Similar attacks observed in {report.get('target_sector', 'various sectors')} in the past.",
            "osint_insights": "No OSINT data available."
        }

        return enriched_data

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embeddings using the chosen model.
        :param text: The input text to embed.
        :return: A list of floats representing the text embedding.
        """
        return self.embeddings_model.embed_query(text)

    def transform_report_for_vector_db(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform, enrich, and normalize an intelligence report for vector database storage.
        :param report: The intelligence report in dictionary format.
        :return: A dictionary containing enriched data and embeddings.
        """
        # Step 1: Extract and normalize fields
        extracted_data = self.extract_fields(report)
        normalized_text = extracted_data["normalized_text"]
        
        # Step 2: Enrich the report with additional data
        enriched_data = self.enrich_data(report)
        
        # Step 3: Generate the embeddings for the normalized text
        embedding = self.generate_embedding(normalized_text)
        
        # Step 4: Prepare the final object for vector database
        transformed_data = {
            "event_id": report.get("event_id"),  # Keep the event_id for linking back to ECS
            "normalized_text": normalized_text,
            "enriched_data": enriched_data,
            "embedding": embedding
        }
        
        return transformed_data

# Example usage
if __name__ == "__main__":
    # Example intelligence report data (as a dictionary)
    example_report = {
        "event_id": "1234-5678-9101-1121",
        "threat_actor": "APT29",
        "malware_family": "Emotet",
        "impact_assessment": "Critical data exfiltrated, business disruption.",
        "target_sector": "Finance",
        "attack_vector": "Phishing",
        "executive_summary": "APT29 launched a phishing campaign targeting financial institutions.",
        "analyst_notes": "The actor seems to be using Emotet as a delivery mechanism."
    }

    # Initialize the vectorizer with a Hugging Face model
    vectorizer = IntelligenceReportVectorizer(model_type="huggingface", model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Transform the report for vector database
    transformed_report = vectorizer.transform_report_for_vector_db(example_report)
    
    # Example output: embedding and enriched data ready for vector storage
    print(json.dumps(transformed_report, indent=4))