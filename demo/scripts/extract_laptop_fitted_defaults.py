import argparse
import json
import pickle
import pprint
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PKL_PATH = REPO_ROOT / "code" / "Laptop" / "conceptualization.pkl"
LAPTOP_DEMO_PATH = REPO_ROOT / "demo" / "scripts" / "laptop_demo.py"

FITTED_START = "# === FITTED_DEFAULTS_START ==="
FITTED_END = "# === FITTED_DEFAULTS_END ==="


def _normalize_params(class_name, params):
    p = dict(params)

    # Some connector entries store extra trailing values in offset.
    if class_name in {"Cuboidal_Connector", "Cylindrical_Connector"}:
        offset = p.get("offset")
        if isinstance(offset, list) and len(offset) > 3:
            p["offset"] = offset[:3]

    return p


def _map_template_name(old_name):
    mapping = {
        "Regular_Base": "Cuboidal_Base",
        "Regular_Screen": "Hinged_Panel_Screen",
        "Cuboidal_Connector": "Cuboidal_Connector",
        "Cylindrical_Connector": "Cylindrical_Connector",
    }
    return mapping.get(old_name)


def extract_plan(sample_id=None, sample_index=0):
    with PKL_PATH.open("rb") as f:
        data = pickle.load(f)

    entries = []
    for row in data:
        templates = {p.get("template") for p in row.get("conceptualization", [])}
        if "Regular_Base" in templates and "Regular_Screen" in templates and (
            "Cuboidal_Connector" in templates or "Cylindrical_Connector" in templates
        ):
            entries.append(row)

    if not entries:
        raise ValueError("No Laptop entries with base+screen+connector found")

    if sample_id:
        chosen = None
        for row in entries:
            if row.get("id") == sample_id:
                chosen = row
                break
        if chosen is None:
            raise ValueError(f"Sample id not found in candidate set: {sample_id}")
    else:
        chosen = entries[sample_index % len(entries)]

    plan = []
    for part in chosen.get("conceptualization", []):
        mapped = _map_template_name(part.get("template"))
        if not mapped:
            continue
        plan.append(
            {
                "class_name": mapped,
                "params": _normalize_params(mapped, part.get("parameters", {})),
            }
        )

    if not plan:
        raise ValueError("Chosen sample had no mappable templates")

    return chosen.get("id"), plan


def apply_to_laptop_demo(sample_id, plan, laptop_demo_path):
    source = laptop_demo_path.read_text(encoding="utf-8")
    pattern = re.compile(r"# === FITTED_DEFAULTS_START ===.*?# === FITTED_DEFAULTS_END ===", re.DOTALL)

    if not pattern.search(source):
        raise ValueError(f"Could not find fitted defaults markers in {laptop_demo_path}")

    plan_literal = pprint.pformat(plan, width=100, sort_dicts=False)
    replacement = (
        f"{FITTED_START}\n"
        "# One-time fitted defaults extracted from code/Laptop/conceptualization.pkl\n"
        "# and adapted to the new demo part templates.\n"
        "FITTED_STAGE2_SOURCE = {\n"
        "    \"source\": \"code-default-fitted-from-pkl\",\n"
        f"    \"sample_id\": \"{sample_id}\",\n"
        "}\n\n"
        f"FITTED_STAGE2_PLAN = {plan_literal}\n"
        f"{FITTED_END}"
    )

    updated = pattern.sub(replacement, source)
    laptop_demo_path.write_text(updated, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Extract fitted stage2 defaults from Laptop pkl")
    parser.add_argument("--sample-id", default=None, help="Exact Laptop pkl sample id")
    parser.add_argument("--sample-index", type=int, default=0, help="Candidate index (if sample-id not set)")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply extracted defaults directly to demo/scripts/laptop_demo.py",
    )
    parser.add_argument(
        "--demo-file",
        default=str(LAPTOP_DEMO_PATH),
        help="Path to laptop_demo.py when using --apply",
    )
    parser.add_argument(
        "--output",
        default=str(REPO_ROOT / "demo" / "artifacts" / "laptop_fitted_defaults.json"),
        help="Output JSON path",
    )
    args = parser.parse_args()

    sample_id, plan = extract_plan(sample_id=args.sample_id, sample_index=args.sample_index)

    payload = {
        "stage2_source": {"source": "code/Laptop/conceptualization.pkl", "sample_id": sample_id},
        "plan": plan,
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    if args.apply:
        demo_path = Path(args.demo_file)
        apply_to_laptop_demo(sample_id=sample_id, plan=plan, laptop_demo_path=demo_path)
        print(f"Applied defaults to: {demo_path}")

    print(f"Sample id: {sample_id}")
    print(f"Written: {output_path}")


if __name__ == "__main__":
    main()
