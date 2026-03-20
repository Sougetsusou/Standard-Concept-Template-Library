from dataclasses import dataclass
from typing import Any, Dict, List

from demo.stages.presets import PRESET_WORKFLOW


@dataclass
class Stage2Result:
    category: str
    prompt: str
    assembly_plan: List[Dict[str, Any]]


def infer_assembly(category: str, prompt: str, stage1_parts: List[Dict[str, Any]]) -> Stage2Result:
    """Deterministic mock Stage 2 that returns executable class+params plan."""
    if category not in PRESET_WORKFLOW:
        raise ValueError(f"Unsupported category for mock Stage 2: {category}")

    preset_parts = PRESET_WORKFLOW[category]["parts"]

    requested = {p["class_name"] for p in stage1_parts}
    assembly_plan = []
    for part in preset_parts:
        if part["class_name"] in requested:
            assembly_plan.append(
                {
                    "class_name": part["class_name"],
                    "params": part["params"],
                    "semantic": part["semantic"],
                }
            )

    return Stage2Result(category=category, prompt=prompt, assembly_plan=assembly_plan)
