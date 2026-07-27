from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(String, unique=True, index=True)  # human-facing ID, e.g. CMP-2026-0001
    customer_name = Column(String)
    product_name = Column(String)
    batch_number = Column(String)
    category = Column(String)
    description = Column(Text)
    country = Column(String)
    status = Column(String, default="New")  # New / Under Review / Closed
    severity = Column(String)  # user-set severity at intake

    # AI-generated fields — populated from the LangGraph pipeline, editable by the user
    ai_risk_level = Column(String)          # Low / Medium / High / Critical
    ai_risk_reason = Column(Text)
    ai_summary = Column(Text)
    ai_missing_fields = Column(Text)        # comma-separated list from completeness check
    ai_is_duplicate = Column(Boolean, default=False)
    ai_duplicate_of_id = Column(Integer, ForeignKey("complaints.id"), nullable=True)
    ai_duplicate_score = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    attachments = relationship("ComplaintAttachment", back_populates="complaint")


class ComplaintAttachment(Base):
    __tablename__ = "complaint_attachments"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"))
    file_name = Column(String)
    file_type = Column(String)  # pdf / email / image
    extracted_text = Column(Text)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    complaint = relationship("Complaint", back_populates="attachments")
