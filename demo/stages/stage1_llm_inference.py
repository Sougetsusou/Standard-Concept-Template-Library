from dataclasses import dataclass
from typing import Any, Dict, List

from demo.stages.presets import PRESET_WORKFLOW


@dataclass
class Stage1Result:
    category: str
    prompt: str
    parts: List[Dict[str, Any]]


def infer_parts(category: str, prompt: str) -> Stage1Result:
    """Deterministic mock Stage 1 that returns preset part decomposition."""
    if category not in PRESET_WORKFLOW:
        raise ValueError(f"Unsupported category for mock Stage 1: {category}")

    preset = PRESET_WORKFLOW[category]
    parts = []
    for part in preset["parts"]:
        parts.append(
            {
                "semantic": part["semantic"],
                "class_name": part["class_name"],
                "decision": part["decision"],
                "reason": "matched deterministic mock preset",
            }
        )

    return Stage1Result(category=category, prompt=prompt, parts=parts)
