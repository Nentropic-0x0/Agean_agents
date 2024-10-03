import uuid
import time
import os
from datetime import datetime
from typing import Optional

class SessionManager:
    def __init__(self):
        # Global session entity
        self.tracing = os.getenv("LANGCHAIN_TRACING_V2", "false")  # Default to 'false' if the environment variable is not set
        self.sessions = []

    def start_session(self, session_type: str) -> dict:
        """Starts a new session and assigns initial attributes."""
        if session_type not in ["scan", "analysis", "report"]:
            raise ValueError("Invalid session type. Must be one of: 'scan', 'analysis', 'report'.")

        session = {
            "session_id": str(uuid.uuid4()),  # Unique identifier for the session
            "timestamp": datetime.now().isoformat(),  # Current time in ISO format
            "type": session_type,  # Session type
            "status": "in_progress",  # Default status
            "tracing": self.tracing  # Global tracing entity
        }
        
        # Store the session in the session list
        self.sessions.append(session)

        return session

    def end_session(self, session_id: str, success: bool) -> Optional[dict]:
        """Ends a session and sets the final status ('success' or 'failed')."""
        for session in self.sessions:
            if session["session_id"] == session_id:
                session["status"] = "success" if success else "failed"
                return session

        # If the session_id is not found, return None
        return None

    def get_session(self, session_id: str) -> Optional[dict]:
        """Retrieve the session details based on session_id."""
        for session in self.sessions:
            if session["session_id"] == session_id:
                return session
        return None

    def prepend_session_info(self, session_id: str, message: str) -> str:
        """Prepend the session information to a message."""
        session = self.get_session(session_id)
        if not session:
            raise ValueError(f"Session with ID {session_id} not found.")
        
        # Prepend the session information to the message
        session_info = (f"[SessionID: {session['session_id']} | "
                        f"Timestamp: {session['timestamp']} | "
                        f"Type: {session['type']} | "
                        f"Status: {session['status']} | "
                        f"Tracing: {session['tracing']}]")
        
        return f"{session_info} {message}"

# Example Usage:
if __name__ == "__main__":
    manager = SessionManager()

    # Start a new session of type "scan"
    new_session = manager.start_session("scan")
    print("New Session Started:", new_session)

    # Prepend a message with the session info
    message_with_session = manager.prepend_session_info(new_session["session_id"], "This is a log message for a scan.")
    print(message_with_session)

    # End the session as success
    completed_session = manager.end_session(new_session["session_id"], success=True)
    print("Session Completed:", completed_session)

    # Prepend a message with the updated session info
    message_with_session = manager.prepend_session_info(new_session["session_id"], "The scan has completed successfully.")
    print(message_with_session)