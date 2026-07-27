from typing import TypedDict, Optional


class ComplaintState(TypedDict, total=False):
    """
    The object passed between every node in the graph. Each node reads
    the keys it needs and writes the keys it produces — nodes never
    talk to each other directly.
    """
    raw_text: str

    # produced by extract_fields_node
    extracted_fields: dict

    # produced by the parallel branch nodes
    summary: str
    risk_level: str
    risk_reason: str
    missing_fields: list[str]
    duplicate_match: Optional[dict]
