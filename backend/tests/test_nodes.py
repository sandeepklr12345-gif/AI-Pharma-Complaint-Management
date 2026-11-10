"""Graph nodes with the LLM and the database replaced by fakes."""
from types import SimpleNamespace

from app.graph import nodes


# ---------- completeness (rule based) ----------

def test_completeness_lists_every_missing_required_field():
    state = {"extracted_fields": {"product_name": "Aspirin", "batch_number": None, "description": ""}}
    result = nodes.check_completeness_node(state)
    assert result["missing_fields"] == ["batch_number", "customer_name", "description"]


def test_completeness_complete_record_has_nothing_missing():
    fields = {f: "x" for f in nodes.REQUIRED_FIELDS}
    assert nodes.check_completeness_node({"extracted_fields": fields}) == {"missing_fields": []}


def test_completeness_without_extraction_marks_all_missing():
    assert nodes.check_completeness_node({})["missing_fields"] == nodes.REQUIRED_FIELDS


# ---------- risk ----------

def test_risk_node_passes_through_model_verdict(monkeypatch):
    monkeypatch.setattr(nodes, "call_groq_json",
                        lambda system, text: {"risk_level": "Critical", "risk_reason": "Patient hospitalised."})
    assert nodes.classify_risk_node({"raw_text": "t"}) == {
        "risk_level": "Critical", "risk_reason": "Patient hospitalised."}


def test_risk_node_defaults_when_model_output_is_unusable(monkeypatch):
    monkeypatch.setattr(nodes, "call_groq_json", lambda system, text: {"_parse_error": True, "_raw": "?"})
    assert nodes.classify_risk_node({"raw_text": "t"}) == {"risk_level": "Unknown", "risk_reason": ""}


# ---------- extraction / summary ----------

def test_extract_node_returns_model_fields(monkeypatch):
    monkeypatch.setattr(nodes, "call_groq_json", lambda system, text: {"product_name": "Aspirin"})
    assert nodes.extract_fields_node({"raw_text": "t"}) == {"extracted_fields": {"product_name": "Aspirin"}}


def test_summary_is_trimmed(monkeypatch):
    monkeypatch.setattr(nodes, "call_groq", lambda system, text: "  line1\nline2  \n")
    assert nodes.summarize_node({"raw_text": "t"}) == {"summary": "line1\nline2"}


# ---------- duplicate detection ----------

class _FakeDB:
    def __init__(self, rows):
        self.rows = rows
        self.closed = False

    def query(self, *_):
        return self

    def filter(self, *_):
        return self

    def all(self):
        return self.rows

    def close(self):
        self.closed = True


def _patch_duplicate_env(monkeypatch, rows, scores):
    db = _FakeDB(rows)
    monkeypatch.setattr(nodes, "SessionLocal", lambda: db)
    monkeypatch.setattr(nodes, "_embedder", SimpleNamespace(encode=lambda text, **kw: text))
    monkeypatch.setattr(nodes, "util", SimpleNamespace(cos_sim=lambda a, b: [[scores[b]]]))
    return db


def test_duplicate_found_above_threshold(monkeypatch):
    rows = [SimpleNamespace(id=1, description="old A"), SimpleNamespace(id=2, description="old B")]
    db = _patch_duplicate_env(monkeypatch, rows, {"old A": 0.42, "old B": 0.95})
    result = nodes.check_duplicate_node({"raw_text": "raw", "extracted_fields": {"description": "new"}})
    assert result == {"duplicate_match": {"complaint_id": 2, "similarity_score": 0.95}}
    assert db.closed


def test_no_duplicate_at_or_below_threshold(monkeypatch):
    rows = [SimpleNamespace(id=1, description="old")]
    _patch_duplicate_env(monkeypatch, rows, {"old": 0.9})  # threshold is strictly greater than 0.9
    assert nodes.check_duplicate_node({"raw_text": "raw", "extracted_fields": {}}) == {"duplicate_match": None}


def test_no_duplicate_when_database_is_empty(monkeypatch):
    db = _patch_duplicate_env(monkeypatch, [], {})
    assert nodes.check_duplicate_node({"raw_text": "raw"}) == {"duplicate_match": None}
    assert db.closed
