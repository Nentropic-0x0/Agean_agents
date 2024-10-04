import json
import uuid
from datetime import datetime, timezone


def generate_cybersecurity_payload(
    session_type="Scan",
    scan_type="Vulnerability",
    target_system="Web Application Server",
    initiated_by="Automated Schedule",
    event_category="vulnerability",
    event_type="detection",
    event_outcome="success",
    event_action="alert",
    source_ip="192.168.1.100",
    destination_ip="10.0.0.5",
    file_path="/var/www/html/login.php",
    threat_level="medium",
    process_id=1234
):
    current_time = datetime.now(timezone.utc).isoformat()
    
    payload = {
        "session": {
            "session_id": str(uuid.uuid4()),
            "timestamp": current_time,
            "session_type": session_type,
            "context": {
                "scan_type": scan_type,
                "target_system": target_system,
                "initiated_by": initiated_by
            }
        },
        "event": {
            "ecs_version": "1.12",
            "event_id": str(uuid.uuid4()),
            "event_category": event_category,
            "event_type": event_type,
            "event_outcome": event_outcome,
            "event_action": event_action,
            "source_ip": source_ip,
            "destination_ip": destination_ip,
            "user_id": str(uuid.uuid4()),
            "process_id": process_id,
            "file_path": file_path,
            "threat_level": threat_level,
            "timestamp": current_time
        }
    }
    
    return payload

# Example usage
if __name__ == "__main__":
    # Generate payload with default values
    default_payload = generate_cybersecurity_payload()
    print("Default Payload:")
    print(json.dumps(default_payload, indent=2))
    
    # Generate payload with custom values
    custom_payload = generate_cybersecurity_payload(
        session_type="Report",
        scan_type="Malware",
        target_system="File Server",
        initiated_by="Manual Trigger",
        event_category="malware",
        event_type="alert",
        event_outcome="failure",
        event_action="quarantine",
        source_ip="10.0.0.50",
        destination_ip="192.168.1.5",
        file_path="/shared/documents/suspicious_file.exe",
        threat_level="high",
        process_id=5678
    )
    print("\nCustom Payload:")
    print(json.dumps(custom_payload, indent=2))