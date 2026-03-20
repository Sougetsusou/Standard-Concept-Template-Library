import json
from pathlib import Path
from typing import Dict, List

from demo.config import CORPUS_ROOT
from demo.stages.presets import PRESET_WORKFLOW


def _build_rows(categories: List[str]) -> List[Dict[str, object]]:
    rows = []
    for category in categories:
        preset = PRESET_WORKFLOW.get(category)
        if not preset:
            continue
        rows.append(
            {
                "task": "generate_concept_template",
                "category": category,
                "description": preset["prompt"],
                "parts": [
                    {
                        "semantic": p["semantic"],
                        "class_name": p["class_name"],
                        "params": p["params"],
                    }
                    for p in preset["parts"]
                ],
            }
        )
    return rows


def generate_stage2_corpus(
    categories: List[str],
    output_path: Path = CORPUS_ROOT / "stage2_assembly_examples.jsonl",
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = _build_rows(categories)
    with output_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=True) + "\n")
    return output_path
