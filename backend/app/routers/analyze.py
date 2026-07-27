from fastapi import APIRouter

from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.graph.pipeline import complaint_pipeline

router = APIRouter(prefix="/api", tags=["analyze"])


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_complaint(payload: AnalyzeRequest):
    result = complaint_pipeline.invoke({"raw_text": payload.text})

    return AnalyzeResponse(
        extracted_fields=result.get("extracted_fields", {}),
        summary=result.get("summary", ""),
        risk_level=result.get("risk_level", "Unknown"),
        risk_reason=result.get("risk_reason", ""),
        missing_fields=result.get("missing_fields", []),
        duplicate_match=result.get("duplicate_match"),
    )
