import json
import logging
from typing import Dict, Any, Optional
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, DataError
from schemas.schemas import ( \
    ECSCybersecurity, AgentMetadata, IntelligenceReports, Sessions, \
    InputData, FeedbackData, AgentMessages
)

# Setting up logging to track operations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Example: SQLAlchemy session setup (replace with your actual DB engine)
Session = sessionmaker()
session = Session()

def validate_data(data: Dict[str, Any], schema: Any) -> Optional[str]:
    """
    Validates that the data matches the schema's required fields and types.

    Args:
        data (Dict[str, Any]): Data to be validated.
        schema (Any): The SQLAlchemy schema class for validation.

    Returns:
        Optional[str]: An error message if validation fails, otherwise None.
    """
    try:
        # Validate required fields and types
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

def load_schema_and_fit(data: Dict[str, Any]) -> str:
    """
    Function that dynamically loads the schema based on the metadata in the JSON package,
    validates the data against the schema, and sends it to the service. If there's an error,
    it will request the same message from the origin and retry the process.

    Args:
        data (Dict[str, Any]): JSON payload received from the message queue or service.

    Returns:
        str: Status message indicating success or failure.
    """
    try:
        # Step 1: Extract relevant metadata
        schema_type = data.get("schema_type")  # Metadata from JSON to determine the schema type
        event_type = data.get("event_type", None)
        session_id = data.get("session_id", None)
        
        logger.info(f"Processing event with schema: {schema_type}, event_type: {event_type}")

        # Step 2: Select the relevant schema based on the extracted metadata
        schema = None
        if schema_type == "agent_metadata":
            schema = AgentMetadata
        elif schema_type == "ecs_cybersecurity":
            schema = ECSCybersecurity
        elif schema_type == "intelligence_reports":
            schema = IntelligenceReports
        elif schema_type == "sessions":
            schema = Sessions
        elif schema_type == "input_data":
            schema = InputData
        elif schema_type == "feedback_data":
            schema = FeedbackData
        elif schema_type == "agent_messages":
            schema = AgentMessages
        else:
            raise ValueError(f"Unknown schema type: {schema_type}")

        # Step 3: Validate the data against the schema
        validation_error = validate_data(data, schema)
        if validation_error:
            raise ValueError(f"Data validation failed: {validation_error}")

        # Step 4: Map the data to the selected schema
        schema_instance = schema(**data)  # Instantiate schema with the data
        session.add(schema_instance)

        # Step 5: Commit the transaction (save to the database)
        session.commit()

        logger.info(f"Successfully processed and saved data for schema: {schema_type}")

        return "Data successfully processed and saved."

    except (IntegrityError, DataError) as db_error:
        logger.error(f"Database error: {db_error}. Requesting data again from the origin.")
        session.rollback()  # Roll back the transaction in case of an error
        return request_data_again(data)

    except ValueError as ve:
        logger.error(f"Value error: {ve}. Unable to process schema: {schema_type}")
        return f"Failed: {ve}"

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}. Retrying...")
        return request_data_again(data)

def request_data_again(data: Dict[str, Any]) -> str:
    """
    Simulates requesting the same message from the origin again in case of an error.

    Args:
        data (Dict[str, Any]): The original data that caused the error.

    Returns:
        str: Status message after retrying.
    """
    # Simulate requesting the same message from the origin
    logger.info(f"Retrying message from origin: {data.get('message_id', 'unknown')}")

    # Simulate reprocessing the data after receiving it again
    # In a real-world scenario, this could involve making an API call or fetching the message again.
    retry_status = load_schema_and_fit(data)  # Retry processing the data

    return retry_status
