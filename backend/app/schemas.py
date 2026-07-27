from datetime import datetime
from pydantic import BaseModel


class UploadResponse(BaseModel):
    text: str
    file_type: str


class AnalyzeRequest(BaseModel):
    text: str


class ExtractedFields(BaseModel):
    product_name: str | None = None
    batch_number: str | None = None
    customer_name: str | None = None
    category: str | None = None
    country: str | None = None
    description: str | None = None


class AnalyzeResponse(BaseModel):
    """
    Everything the AI copilot produces in one pass — this is what
    the frontend uses to auto-fill the complaint form.
    """
    extracted_fields: ExtractedFields
    summary: str
    risk_level: str
    risk_reason: str
    missing_fields: list[str]
    duplicate_match: dict | None = None


class ComplaintCreate(BaseModel):
    complaint_id: str
    customer_name: str | None = None
    product_name: str | None = None
    batch_number: str | None = None
    category: str | None = None
    description: str | None = None
    country: str | None = None
    severity: str | None = None
    status: str = "New"
    ai_risk_level: str | None = None
    ai_risk_reason: str | None = None
    ai_summary: str | None = None
    ai_missing_fields: str | None = None
    ai_is_duplicate: bool = False
    ai_duplicate_of_id: int | None = None
    ai_duplicate_score: float | None = None


class ComplaintOut(ComplaintCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
