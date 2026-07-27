from sentence_transformers import SentenceTransformer, util

from app.database import SessionLocal
from app.models import Complaint
from app.services.groq_client import call_groq, call_groq_json
from app.graph.state import ComplaintState

REQUIRED_FIELDS = ["product_name", "batch_number", "customer_name", "description"]

# Loaded once at import time — reused across requests, not per-call.
_embedder = SentenceTransformer("all-MiniLM-L6-v2")


def extract_fields_node(state: ComplaintState) -> dict:
    """First node: pulls structured pharma-complaint fields out of raw text."""
    system = (
        "You extract structured data from pharmaceutical customer complaints. "
        "Fields to extract: product_name, batch_number, customer_name, category, "
        "country, description (a 1-2 sentence restatement of the issue). "
        "If a field isn't present in the text, use null."
    )
    fields = call_groq_json(system, state["raw_text"])
    return {"extracted_fields": fields}


def summarize_node(state: ComplaintState) -> dict:
    """Parallel branch: 4-line plain-language summary."""
    system = "Summarize this pharmaceutical complaint in exactly 4 short lines."
    summary = call_groq(system, state["raw_text"])
    return {"summary": summary.strip()}


def check_completeness_node(state: ComplaintState) -> dict:
    """
    Parallel branch: rule-based check against REQUIRED_FIELDS.
    Rule-based (not an LLM call) because "is this key present and non-null"
    doesn't need a model — it's cheaper and more reliable this way.
    """
    fields = state.get("extracted_fields", {})
    missing = [f for f in REQUIRED_FIELDS if not fields.get(f)]
    return {"missing_fields": missing}


def classify_risk_node(state: ComplaintState) -> dict:
    """Parallel branch: risk level + reasoning."""
    system = (
        "Classify the risk of this pharmaceutical complaint as one of: "
        "Low, Medium, High, Critical. Consider patient safety, product quality "
        "impact, and regulatory implications. Respond with JSON: "
        '{"risk_level": "...", "risk_reason": "one sentence explanation"}'
    )
    result = call_groq_json(system, state["raw_text"])
    return {
        "risk_level": result.get("risk_level", "Unknown"),
        "risk_reason": result.get("risk_reason", ""),
    }


def check_duplicate_node(state: ComplaintState) -> dict:
    """
    Parallel branch: embeds the complaint description and compares
    against existing complaints in the DB via cosine similarity.
    """
    fields = state.get("extracted_fields", {})
    description = fields.get("description") or state["raw_text"]

    db = SessionLocal()
    try:
        existing = db.query(Complaint).filter(Complaint.description.isnot(None)).all()
        if not existing:
            return {"duplicate_match": None}

        new_embedding = _embedder.encode(description, convert_to_tensor=True)
        best_score, best_match = 0.0, None

        for complaint in existing:
            existing_embedding = _embedder.encode(complaint.description, convert_to_tensor=True)
            score = float(util.cos_sim(new_embedding, existing_embedding)[0][0])
            if score > best_score:
                best_score, best_match = score, complaint

        if best_score > 0.9 and best_match:
            return {
                "duplicate_match": {
                    "complaint_id": best_match.id,
                    "similarity_score": round(best_score, 3),
                }
            }
        return {"duplicate_match": None}
    finally:
        db.close()


def finalize_node(state: ComplaintState) -> dict:
    """
    Join point after the parallel branch. LangGraph merges all branch
    outputs into state automatically before this runs — this node just
    exists as an explicit endpoint so the graph has one clear exit.
    """
    return {}
