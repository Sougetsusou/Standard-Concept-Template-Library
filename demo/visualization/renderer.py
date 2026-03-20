from typing import Any, Dict


def summarize_report(report: Dict[str, Any]) -> str:
    """Return a compact text summary for CLI/examples."""
    status = "PASS" if report.get("mesh_ok") else "FAIL"
    parts = ", ".join(report.get("parts_executed", []))
    return (
        f"[{status}] {report.get('category')} | "
        f"parts={parts} | v={report.get('vertex_count')} | f={report.get('face_count')}"
    )
