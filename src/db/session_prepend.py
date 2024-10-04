import uuid
from datetime import datetime, timezone


class SessionManager:
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.session_created_at = datetime.now(timezone.utc).isoformat()

    def create_prepend(self):
        return {
            "session_id": self.session_id,
            "session_created_at": self.session_created_at,
            "message_timestamp": datetime.now(timezone.utc).isoformat()
        }

    def prepare_message(self, message_payload):
        prepend = self.create_prepend()
        return {
            "prepend": prepend,
            "payload": message_payload
        }

    def store_message(self, message):
        # This is where you'd interact with your database
        prepend = message["prepend"]
        payload = message["payload"]
        
        # Store prepend and payload separately
        # For example, using SQLAlchemy:
        # new_message = Message(
        #     session_id=prepend["session_id"],
        #     session_created_at=prepend["session_created_at"],
        #     message_timestamp=prepend["message_timestamp"],
        #     payload=json.dumps(payload)
        # )
        # db.session.add(new_message)
        # db.session.commit()

        print(f"Stored message with prepend: {prepend}")
        print(f"Payload: {payload}")

# Usage
session_manager = SessionManager()

# Example message
message_payload = {
    "event_type": "user_login",
    "user_id": "user123",
    "ip_address": "192.168.1.1"
}

# Prepare and store the message
prepared_message = session_manager.prepare_message(message_payload)
session_manager.store_message(prepared_message)