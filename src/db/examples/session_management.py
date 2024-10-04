from datetime import datetime

from sqlalchemy import (CheckConstraint, Column, DateTime, ForeignKey, String,
                        Text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Sessions(Base):
    __tablename__ = "sessions"

    session_id = Column(String, primary_key=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    session_type = Column(String, nullable=False)
    context = Column(Text, nullable=True)

    # Constraint on session_type to allow only specified values
    __table_args__ = (
        CheckConstraint("session_type IN ('Scan', 'Report', 'Notification', 'Mitigation')", name="session_type_check"),
    )

class InputData(Base):
    __tablename__ = "input_data"

    id = Column(String, primary_key=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    content = Column(Text, nullable=False)
    session_id = Column(String, ForeignKey('sessions.session_id'), nullable=False)
    context = Column(Text, nullable=True)

    session = relationship("Sessions")

class FeedbackData(Base):
    __tablename__ = "feedback_data"

    id = Column(String, primary_key=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    session_id = Column(String, ForeignKey('sessions.session_id'), nullable=False)
    feedback = Column(Text, nullable=False)

    session = relationship("Sessions")
