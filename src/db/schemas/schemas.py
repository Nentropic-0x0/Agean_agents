from sqlalchemy import (ARRAY, DECIMAL, JSON, TIMESTAMP, UUID, CheckConstraint,
                        Column, ForeignKey, Index, Integer, Interval, String,
                        Text, create_engine)
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Global Fields
class GlobalFieldsMixin:
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
    event_type = Column(String(50), nullable=False)
    session_id = Column(PG_UUID(as_uuid=True), ForeignKey('sessions.session_id'), nullable=False)

# Agent Metadata Table (for tracking agent information)
class AgentMetadata(Base):
    __tablename__ = "agent_metadata"

    uuid = Column(PG_UUID(as_uuid=True), primary_key=True)
    agent_type = Column(String(255), nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
    from_agent = Column(PG_UUID(as_uuid=True), nullable=False)
    to_agent = Column(PG_UUID(as_uuid=True), nullable=False)
    message_id = Column(PG_UUID(as_uuid=True), nullable=False)
    message = Column(JSON, nullable=False)

# ECS Cybersecurity Event Schema
class ECSCybersecurity(Base, GlobalFieldsMixin):
    __tablename__ = "ecs_cybersecurity"

    ecs_version = Column(String(10), default='1.12')
    event_id = Column(PG_UUID(as_uuid=True), primary_key=True)
    event_category = Column(String(255), nullable=False)
    event_outcome = Column(String(50), nullable=False)
    event_action = Column(String(255), nullable=False)
    source_ip = Column(INET, nullable=False)
    destination_ip = Column(INET, nullable=False)
    user_id = Column(PG_UUID(as_uuid=True), nullable=True)
    process_id = Column(Integer, nullable=True)
    file_path = Column(Text, nullable=True)
    threat_level = Column(String(50), nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)

# Messages exchanged between agents
class AgentMessages(Base):
    __tablename__ = "agent_messages"

    message_id = Column(PG_UUID(as_uuid=True), primary_key=True)
    from_agent = Column(PG_UUID(as_uuid=True), ForeignKey("agent_metadata.uuid"), nullable=False)
    to_agent = Column(PG_UUID(as_uuid=True), ForeignKey("agent_metadata.uuid"), nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
    message_type = Column(String(50), nullable=False)
    payload = Column(JSON, nullable=False)
    response = Column(JSON, nullable=True)

    __table_args__ = (
        Index('idx_agent_timestamp', 'from_agent', 'timestamp'),
    )

# Intelligence Reports Schema
class IntelligenceReports(Base, GlobalFieldsMixin):
    __tablename__ = "intelligence_reports"

    report_id = Column(PG_UUID(as_uuid=True), primary_key=True)
    event_id = Column(PG_UUID(as_uuid=True), ForeignKey('ecs_cybersecurity.event_id'), nullable=False)
    report_generated_at = Column(TIMESTAMP(timezone=True), nullable=False)
    report_author = Column(String(255), nullable=False)

    threat_actor = Column(String(255), nullable=True)
    malware_family = Column(String(255), nullable=True)
    target_sector = Column(String(255), nullable=True)
    affected_assets = Column(ARRAY(Text), nullable=True)
    attack_vector = Column(String(255), nullable=True)

    risk_score = Column(Integer, nullable=True)
    impact_assessment = Column(Text, nullable=True)
    mitigation_effort = Column(Integer, nullable=True)
    estimated_cost = Column(DECIMAL(12, 2), nullable=True)
    incident_duration = Column(Interval, nullable=True)
    threat_level = Column(String(50), nullable=True)
    additional_context = Column(JSON, nullable=True)

    executive_summary = Column(Text, nullable=True)
    analyst_notes = Column(Text, nullable=True)

    __table_args__ = (
        Index('idx_intelligence_report_event_id', 'event_id'),
        Index('idx_intelligence_report_risk_score', 'risk_score'),
        Index('idx_intelligence_report_threat_level', 'threat_level'),
    )

# Sessions shared across different processes
class Sessions(Base):
    __tablename__ = "sessions"

    session_id = Column(PG_UUID(as_uuid=True), primary_key=True)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
    session_type = Column(String(50), nullable=False)
    context = Column(JSON, nullable=True)

    __table_args__ = (
        CheckConstraint(session_type.in_(['Scan', 'Report', 'Notification', 'Mitigation']), name="session_type_check"),
    )

# Input Data tied to sessions
class InputData(Base):
    __tablename__ = "input_data"

    id = Column(String, primary_key=True)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
    content = Column(Text, nullable=False)
    session_id = Column(PG_UUID(as_uuid=True), ForeignKey('sessions.session_id'), nullable=False)
    context = Column(JSON, nullable=True)

# Feedback Data associated with sessions
class FeedbackData(Base):
    __tablename__ = "feedback_data"

    id = Column(String, primary_key=True)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
    session_id = Column(PG_UUID(as_uuid=True), ForeignKey('sessions.session_id'), nullable=False)
    feedback = Column(Text, nullable=False)
