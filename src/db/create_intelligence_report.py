import datetime
from uuid import uuid4

from sqlalchemy import (JSON, TIMESTAMP, Column, Float, ForeignKey, Integer,
                        Interval, String, Text, create_engine)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Define the base for SQLAlchemy ORM models
Base = declarative_base()

# Set up the PostgreSQL connection using SQLAlchemy
DATABASE_URL = "postgresql://user:password@localhost:5432/cybersecurity"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the IntelligenceReport class as ORM model
class IntelligenceReport(Base):
    __tablename__ = "intelligence_reports"
    
    report_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("ecs_cybersecurity.event_id"), nullable=False)
    report_generated_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)
    report_author = Column(String(255), nullable=False)
    
    # Base fields
    threat_actor = Column(String(255), nullable=True)
    malware_family = Column(String(255), nullable=True)
    target_sector = Column(String(255), nullable=True)
    affected_assets = Column(Text, nullable=True)  # List of affected assets
    attack_vector = Column(String(255), nullable=True)
    
    # Calculated/Derived fields
    risk_score = Column(Integer, nullable=True)
    impact_assessment = Column(Text, nullable=True)
    mitigation_effort = Column(Integer, nullable=True)  # Estimated hours
    estimated_cost = Column(Float, nullable=True)  # Cost in USD
    incident_duration = Column(Interval, nullable=True)
    threat_level = Column(String(50), nullable=True)
    additional_context = Column(JSONB, nullable=True)  # JSONB for structured additional context
    
    # Summary fields
    executive_summary = Column(Text, nullable=True)
    analyst_notes = Column(Text, nullable=True)
    
    def __init__(self, event_id, report_author, threat_actor=None, malware_family=None, target_sector=None,
                 affected_assets=None, attack_vector=None):
        self.event_id = event_id
        self.report_author = report_author
        self.threat_actor = threat_actor
        self.malware_family = malware_family
        self.target_sector = target_sector
        self.affected_assets = affected_assets
        self.attack_vector = attack_vector

    # Method to create a new report
    @classmethod
    def create_report(cls, session, **kwargs):
        report = cls(**kwargs)
        session.add(report)
        session.commit()
        return report

    # Method to update report and calculate derived fields
    @classmethod
    def update_report(cls, session, report_id, **kwargs):
        report = session.query(cls).filter_by(report_id=report_id).first()
        if report:
            for key, value in kwargs.items():
                setattr(report, key, value)
            report.calculate_fields()  # Recalculate derived fields
            session.commit()
        return report

    # Method to calculate derived fields
    def calculate_fields(self):
        # Example of calculating risk_score based on the threat level and other factors
        if self.threat_level == "high":
            self.risk_score = 90
        elif self.threat_level == "medium":
            self.risk_score = 60
        else:
            self.risk_score = 30

        # Example of estimating cost based on mitigation effort
        if self.mitigation_effort:
            self.estimated_cost = self.mitigation_effort * 150  # Assuming $150 per hour of effort

        # Example of calculating incident duration (if start and end times are available)
        # Here you should implement logic based on actual incident start and end timestamps
        # self.incident_duration = some_calculated_interval

    # Method to generate report (as JSON or text)
    @classmethod
    def generate_report(cls, session, report_id):
        report = session.query(cls).filter_by(report_id=report_id).first()
        if report:
            return {
                "report_id": str(report.report_id),
                "event_id": str(report.event_id),
                "generated_at": report.report_generated_at.isoformat(),
                "author": report.report_author,
                "threat_actor": report.threat_actor,
                "malware_family": report.malware_family,
                "target_sector": report.target_sector,
                "affected_assets": report.affected_assets,
                "attack_vector": report.attack_vector,
                "risk_score": report.risk_score,
                "impact_assessment": report.impact_assessment,
                "mitigation_effort": report.mitigation_effort,
                "estimated_cost": report.estimated_cost,
                "incident_duration": str(report.incident_duration) if report.incident_duration else None,
                "threat_level": report.threat_level,
                "executive_summary": report.executive_summary,
                "analyst_notes": report.analyst_notes,
                "additional_context": report.additional_context
            }
        return None

# Create the tables in the database
Base.metadata.create_all(bind=engine)

# Example usage
if __name__ == "__main__":
    # Initialize session
    session = SessionLocal()

    # Create a new intelligence report
    new_report = IntelligenceReport.create_report(session, event_id=uuid4(), report_author="Analyst123",
                                                  threat_actor="Unknown Group", malware_family="Emotet",
                                                  target_sector="Finance", affected_assets=["Server1", "Server2"],
                                                  attack_vector="Phishing")
    
    # Update the report with calculated fields
    updated_report = IntelligenceReport.update_report(session, new_report.report_id,
                                                      threat_level="high", mitigation_effort=40)
    
    # Generate the report as JSON
    report_json = IntelligenceReport.generate_report(session, new_report.report_id)
    print(report_json)
