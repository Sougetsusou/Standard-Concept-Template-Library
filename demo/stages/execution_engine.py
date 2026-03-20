import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

from demo.config import ARTIFACT_ROOT, CODE_ROOT
from demo.evaluation.mesh_quality import check_mesh_non_degenerate


def _load_category_concept_module(category: str):
    category_dir = CODE_ROOT / category
    module_path = category_dir / "concept_template.py"
    if not module_path.exists():
        raise FileNotFoundError(f"Missing concept_template.py for {category}: {module_path}")

    shared_path = CODE_ROOT.parent / "shared"
    if str(shared_path) not in sys.path:
        sys.path.insert(0, str(shared_path))

    spec = importlib.util.spec_from_file_location(f"demo_{category.lower()}_concept_template", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to create module spec for {module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def execute_plan(category: str, assembly_plan: List[Dict[str, Any]]) -> Dict[str, Any]:
    module = _load_category_concept_module(category)

    objects = []
    for step in assembly_plan:
        class_name = step["class_name"]
        params = step["params"]
        cls = getattr(module, class_name)
        obj = cls(**params)
        objects.append({"class_name": class_name, "obj": obj})

    all_vertices = []
    all_faces = []
    total_vertices = 0
    for entry in objects:
        obj = entry["obj"]
        v = np.asarray(obj.vertices)
        f = np.asarray(obj.faces)
        all_vertices.append(v)
        all_faces.append(f + total_vertices)
        total_vertices += len(v)

    merged_vertices = np.concatenate(all_vertices) if all_vertices else np.zeros((0, 3))
    merged_faces = np.concatenate(all_faces) if all_faces else np.zeros((0, 3), dtype=int)

    ok, checks = check_mesh_non_degenerate(merged_vertices, merged_faces)

    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    artifact_path = ARTIFACT_ROOT / f"{category.lower()}_execution_report.json"
    report = {
        "category": category,
        "parts_executed": [x["class_name"] for x in objects],
        "mesh_ok": ok,
        "mesh_checks": checks,
        "vertex_count": int(merged_vertices.shape[0]),
        "face_count": int(merged_faces.shape[0]),
    }
    artifact_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
