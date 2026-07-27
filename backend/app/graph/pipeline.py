from langgraph.graph import StateGraph, START, END

from app.graph.state import ComplaintState
from app.graph.nodes import (
    extract_fields_node,
    summarize_node,
    check_completeness_node,
    classify_risk_node,
    check_duplicate_node,
    finalize_node,
)


def build_pipeline():
    graph = StateGraph(ComplaintState)

    graph.add_node("extract_fields", extract_fields_node)
    graph.add_node("summarize", summarize_node)
    graph.add_node("check_completeness", check_completeness_node)
    graph.add_node("classify_risk", classify_risk_node)
    graph.add_node("check_duplicate", check_duplicate_node)
    graph.add_node("finalize", finalize_node)

    graph.add_edge(START, "extract_fields")

    # Fan-out: these four all depend on extracted_fields but not on each other
    graph.add_edge("extract_fields", "summarize")
    graph.add_edge("extract_fields", "check_completeness")
    graph.add_edge("extract_fields", "classify_risk")
    graph.add_edge("extract_fields", "check_duplicate")

    # Fan-in: LangGraph waits for all four before running finalize
    graph.add_edge("summarize", "finalize")
    graph.add_edge("check_completeness", "finalize")
    graph.add_edge("classify_risk", "finalize")
    graph.add_edge("check_duplicate", "finalize")

    graph.add_edge("finalize", END)

    return graph.compile()


# Compiled once at import time, reused across requests
complaint_pipeline = build_pipeline()
