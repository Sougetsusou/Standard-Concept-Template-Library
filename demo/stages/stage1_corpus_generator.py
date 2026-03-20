import ast
import json
from pathlib import Path
from typing import Dict, List

from demo.config import CORPUS_ROOT, PART_TEMPLATE_ROOT


def _collect_part_classes() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for py_file in sorted(PART_TEMPLATE_ROOT.glob("*.py")):
        if py_file.name == "__init__.py":
            continue
        source = py_file.read_text(encoding="utf-8")
        tree = ast.parse(source)
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                doc = ast.get_docstring(node) or ""
                semantic = "Unknown"
                for line in doc.splitlines():
                    stripped = line.strip()
                    if stripped.startswith("Semantic:"):
                        semantic = stripped.split(":", 1)[1].strip()
                        break
                rows.append(
                    {
                        "task": "write_part_class",
                        "semantic_type": semantic,
                        "class_name": node.name,
                        "source_file": py_file.name,
                        "description": doc.strip() or "No docstring",
                    }
                )
    return rows


def generate_stage1_corpus(output_path: Path = CORPUS_ROOT / "stage1_part_examples.jsonl") -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = _collect_part_classes()
    with output_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=True) + "\n")
    return output_path
