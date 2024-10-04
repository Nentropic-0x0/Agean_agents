from typing import Dict, Any, Optional
from functools import wraps
import logging

# Example schema imports (replace these with your actual schema classes)
from schemas import AgentMessages, AgentMetadata, ECSCybersecurity, FeedbackData, InputData, IntelligenceReports, Sessions

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Step 1: Create a schema selector function
def select_schema(schema_type: str):
    """
    Selects the schema class based on the provided schema type.

    Args:
        schema_type (str): The type of schema to select.

    Returns:
        schema: The selected schema class.
    """
    schema_map = {
        "agent_metadata": AgentMetadata,
        "ecs_cybersecurity": ECSCybersecurity,
        "intelligence_reports": IntelligenceReports,
        "sessions": Sessions,
        "input_data": InputData,
        "feedback_data": FeedbackData,
        "agent_messages": AgentMessages,
    }
    schema = schema_map.get(schema_type)
    if not schema:
        raise ValueError(f"Unknown schema type: {schema_type}")
    return schema

# Step 2: Define the schema validation decorator
def schema_validator(func):
    """
    Decorator that selects the appropriate schema and validates data against it.

    Args:
        func: The function to wrap, which receives validated data.

    Returns:
        The decorated function with schema validation.
    """
    @wraps(func)
    def wrapper(data: Dict[str, Any], *args, **kwargs):
        # Extract schema type from the data
        schema_type = data.get("schema_type")
        if not schema_type:
            raise ValueError("Schema type is required.")

        # Select the appropriate schema
        schema = select_schema(schema_type)

        # Perform the schema validation
        validation_error = validate_data(data, schema)
        if validation_error:
            raise ValueError(f"Data validation failed: {validation_error}")

        # Call the original function if validation passes
        return func(data, *args, **kwargs)

    return wrapper

# Step 3: Define the validate_data function
def validate_data(data: Dict[str, Any], schema: Any) -> Optional[str]:
    """
    Validates the given data against the selected schema.

    Args:
        data (Dict[str, Any]): Data to validate.
        schema: The schema class to validate against.

    Returns:
        Optional[str]: Returns None if validation passes, or an error message if validation fails.
    """
    try:
        schema_fields = {field.name: field for field in schema.__table__.columns}
        for field, value in data.items():
            if field in schema_fields:
                expected_type = schema_fields[field].type.python_type
                if not isinstance(value, expected_type) and value is not None:
                    return f"Field {field} should be of type {expected_type}, got {type(value)}"
        return None
    except Exception as e:
        logger.error(f"Validation error: {e}")
        return str(e)

# Step 4: Apply the LangChain tool
# Assume this is a LangChain tool that can be called in a LangChain agent pipeline

@schema_validator
def process_data(data: Dict[str, Any]):
    """
    Process the validated data after schema validation.

    Args:
        data (Dict[str, Any]): Validated data.

    Returns:
        str: Success message after processing.
    """
    logger.info(f"Processing data: {data}")
    # Simulate data processing (e.g., saving to a database)
    return "Data successfully processed."

# Example usage as a LangChain tool (within the LangChain ecosystem)
def langchain_tool(input_data: Dict[str, Any]):
    """
    LangChain tool that processes the input data by validating it using the appropriate schema.

    Args:
        input_data (Dict[str, Any]): The input data to be processed.

    Returns:
        str: The result of processing the data.
    """
    try:
        # Process the input data, applying schema validation
        return process_data(input_data)
    except Exception as e:
        return f"Error processing data: {str(e)}"

# Example Input Data
example_data = {
    "schema_type": "input_data",  # This dynamically selects the 'InputData' schema
    "session_id": "12345",
    "session_type": "Scan",
    "data": {"key": "value"}
}

# Test the LangChain tool
result = langchain_tool(example_data)
print(result)
