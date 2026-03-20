import importlib.util
import copy
import json
import sys
from pathlib import Path

import numpy as np


DEMO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = DEMO_ROOT / "artifacts"

# === FITTED_DEFAULTS_START ===
# One-time fitted defaults extracted from code/Laptop/conceptualization.pkl
# and adapted to the new demo part templates.
FITTED_STAGE2_SOURCE = {
    "source": "code-default-fitted-from-pkl",
    "sample_id": "2bbf7f77d43b74338a331b18e58c6914",
}

FITTED_STAGE2_PLAN = [{'class_name': 'Cuboidal_Base',
  'params': {'size': [1.3, 0.06, 0.9], 'position': [-0.05, -0.14, 0.22], 'rotation': [0, 0, 0]}},
 {'class_name': 'Hinged_Panel_Screen',
  'params': {'size': [1.3, 0.76, 0.02],
             'offset': [-0.03, -0.56],
             'screen_rotation': [-17],
             'position': [-0.05, -0.14, 0.22],
             'rotation': [0, 0, 0]}},
 {'class_name': 'Cuboidal_Connector',
  'params': {'number_of_connector': [2],
             'size': [0.02, 0.02, 0.04],
             'separation': [1.11, 0.15, 0.15, 0.15],
             'offset': [-0.57, 0, -0.45],
             'connector_rotation': [19],
             'position': [-0.05, -0.14, 0.22],
             'rotation': [0, 0, 0]}}]
# === FITTED_DEFAULTS_END ===


def stage1_part_generation(prompt):
    return [
        {"semantic": "Base", "class_name": "Cuboidal_Base", "decision": "use_existing"},
        {"semantic": "Screen", "class_name": "Hinged_Panel_Screen", "decision": "use_existing"},
        {"semantic": "Connector", "class_name": "Cuboidal_Connector", "decision": "use_existing"},
    ]


def stage2_instance_assembly(parts):
    return copy.deepcopy(FITTED_STAGE2_PLAN)


def load_laptop_module():
    repo_root = DEMO_ROOT.parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    module_path = DEMO_ROOT / "code" / "Laptop" / "concept_template.py"
    spec = importlib.util.spec_from_file_location("demo_laptop_concept_template", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_merged_mesh(module, plan):
    instances = []
    for step in plan:
        cls = getattr(module, step["class_name"])
        instances.append(cls(**step["params"]))

    vertices = []
    faces = []
    offset = 0
    for obj in instances:
        v = np.asarray(obj.vertices)
        f = np.asarray(obj.faces)
        vertices.append(v)
        faces.append(f + offset)
        offset += len(v)

    merged_vertices = np.concatenate(vertices)
    merged_faces = np.concatenate(faces)

    return merged_vertices, merged_faces, [step["class_name"] for step in plan]


def execute_plan(module, plan):
    merged_vertices, merged_faces, parts_executed = build_merged_mesh(module, plan)

    checks = {
        "has_vertices": bool(merged_vertices.size > 0),
        "has_faces": bool(merged_faces.size > 0),
        "finite_vertices": bool(np.isfinite(merged_vertices).all()),
        "valid_vertex_shape": bool(merged_vertices.ndim == 2 and merged_vertices.shape[1] == 3),
        "valid_face_shape": bool(merged_faces.ndim == 2 and merged_faces.shape[1] == 3),
    }
    ok = all(checks.values())

    return {
        "mesh_ok": ok,
        "mesh_checks": checks,
        "vertex_count": int(merged_vertices.shape[0]),
        "face_count": int(merged_faces.shape[0]),
        "parts_executed": parts_executed,
    }


def main():
    prompt = "Create a practical laptop with rectangular base, hinged screen, and two side ports."
    stage1 = stage1_part_generation(prompt)
    stage2 = stage2_instance_assembly(stage1)

    module = load_laptop_module()
    report = execute_plan(module, stage2)
    report["stage2_source"] = FITTED_STAGE2_SOURCE

    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    report_path = ARTIFACT_ROOT / "laptop_demo_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    status = "PASS" if report["mesh_ok"] else "FAIL"
    print(f"[{status}] Laptop | v={report['vertex_count']} | f={report['face_count']}")
    print(f"Stage2 source: {FITTED_STAGE2_SOURCE}")
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
