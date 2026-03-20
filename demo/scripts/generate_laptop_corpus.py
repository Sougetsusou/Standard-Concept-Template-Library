import ast
import json
from pathlib import Path


DEMO_ROOT = Path(__file__).resolve().parents[1]
PART_TEMPLATE = DEMO_ROOT / "part_template"
OUTPUT_DIR = DEMO_ROOT / "data" / "training_corpus"


def generate_level2():
    rows = []
    for py in sorted(PART_TEMPLATE.glob("*.py")):
        source = py.read_text(encoding="utf-8")
        tree = ast.parse(source)
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                rows.append(
                    {
                        "task": "write_part_class",
                        "semantic": node.name.split("_")[-1],
                        "class_name": node.name,
                        "source": f"part_template/{py.name}",
                    }
                )
    return rows


def generate_level3():
    return [
        {
            "task": "generate_concept_template",
            "category": "Laptop",
            "description": "a clamshell laptop with a flat base, hinged screen, and side ports",
            "parts": ["Cuboidal_Base", "Hinged_Panel_Screen", "Cuboidal_Connector"],
        }
    ]


def write_jsonl(path, rows):
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=True) + "\n")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    level2 = OUTPUT_DIR / "level2_laptop_parts.jsonl"
    level3 = OUTPUT_DIR / "level3_laptop_assembly.jsonl"

    write_jsonl(level2, generate_level2())
    write_jsonl(level3, generate_level3())

    print(f"Generated: {level2}")
    print(f"Generated: {level3}")


if __name__ == "__main__":
    main()
