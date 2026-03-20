from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CODE_ROOT = REPO_ROOT / "code"
PART_TEMPLATE_ROOT = REPO_ROOT / "part_template"
ARTIFACT_ROOT = REPO_ROOT / "demo" / "artifacts"
CORPUS_ROOT = REPO_ROOT / "demo" / "data" / "training_corpus"

DEFAULT_CATEGORIES = ("Laptop", "Mug")
DEFAULT_SEED = 7

CATEGORY_DESCRIPTIONS = {
    "Laptop": "a clamshell laptop with flat base, hinged screen, and side connectors",
    "Mug": "a drinking mug with a hollow cylindrical body and curved handle",
}
