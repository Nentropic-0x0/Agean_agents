import json
from logger import logger
from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.orm import sessionmaker
from functools import wraps

from schemas.schemas import (
    AgentMessages, AgentMetadata, ECSCybersecurity, FeedbackData, 
    InputData, IntelligenceReports, Sessions
)
from session_management import FeedbackData, InputData, Sessions

# Setup logging


# SQLAlchemy session setup (replace with your actual DB engine)
Session = sessionmaker()
session = Session()

# Input validation decorator
def validate_input(func):
    @wraps(func)
    def wrapper(data: Dict[str, Any], *args, **kwargs):
        if not isinstance(data, dict):
            raise ValueError("Input data must be a dictionary.")
        # Validate that keys exist and values are positive if needed
        for key, value in data.items():
            if value is None or (isinstance(value, (int, float)) and value <= 0):
                raise ValueError(f"Invalid value for {key}: {value}")
        return func(data, *args, **kwargs)
    return wrapper

# Schema data validator
def validate_data(data: Dict[str, Any], schema: Any) -> Optional[str]:
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

# Handle session validation or creation
def get_or_create_session(session_id: str, session_type: str, context: str = None) -> Sessions:
    session_instance = session.query(Sessions).filter_by(session_id=session_id).first()
    if session_instance:
        logger.info(f"Found existing session: {session_id}")
        return session_instance

    new_session = Sessions(session_id=session_id, session_type=session_type, context=context, timestamp=datetime.utcnow())
    session.add(new_session)
    session.commit()
    logger.info(f"Created new session: {session_id}")
    return new_session

# Main function for schema validation and data processing
@validate_input  # Applying the input validation decorator
def process_data(data: Dict[str, Any]) -> str:
    try:
        # Step 1: Determine schema type
        schema_type = data.get("schema_type")
        if not schema_type:
            raise ValueError("Schema type is required.")

        schema = get_schema_by_type(schema_type)

        # Step 2: Handle session, if provided
        session_id = data.get("session_id")
        session_type = data.get("session_type")
        if session_id and session_type:
            get_or_create_session(session_id, session_type, data.get("session_context"))

        # Step 3: Validate data against schema
        validation_error = validate_data(data, schema)
        if validation_error:
            raise ValueError(f"Data validation failed: {validation_error}")

        # Step 4: Save data to the database
        save_to_db(schema, data)

        logger.info(f"Successfully processed and saved data for schema: {schema_type}")
        return "Data successfully processed and saved."
    
    except (IntegrityError, DataError) as db_error:
        logger.error(f"Database error: {db_error}. Requesting data again.")
        session.rollback()
        return request_data_again(data)

    except ValueError as ve:
        logger.error(f"Value error: {ve}")
        return f"Failed: {ve}"

    except Exception as e:
        logger.error(f"Unexpected error: {e}. Retrying...")
        return request_data_again(data)

# Select the schema dynamically
def get_schema_by_type(schema_type: str) -> Any:
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

# Save data to the database
def save_to_db(schema: Any, data: Dict[str, Any]) -> None:
    schema_instance = schema(**data)
    session.add(schema_instance)
    session.commit()

# Retry request by simulating data fetch again
def request_data_again(data: Dict[str, Any]) -> str:
    logger.info(f"Retrying message for session: {data.get('session_id', 'unknown')}")
    return process_data(data)
'''
# Example usage
example_data = {
    "schema_type": "input_data",
    "session_id": "123",
    "session_type": "Scan",
    "data": {"key": "value"}
}

result = process_data(example_data)
print(result)
'''