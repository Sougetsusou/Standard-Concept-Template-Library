# Laptop Demo (Project-Style Minimal Hierarchy)

This `demo/` mirrors the project structure with only files required for the Laptop workflow.

## Hierarchy

- `demo/code/Laptop/concept_template.py` -> Laptop assembly manifest
- `demo/part_template/` -> essential part classes (`base.py`, `screen.py`, `connector.py`)
- `demo/shared/` -> minimal geometry/template utilities for execution
- `demo/scripts/laptop_demo.py` -> end-to-end runnable laptop demo
- `demo/scripts/generate_laptop_corpus.py` -> minimal Level2/Level3 corpus output
- `demo/scripts/visualize_laptop.py` -> export and optional display of merged laptop mesh
- `demo/scripts/extract_laptop_fitted_defaults.py` -> extract and normalize Laptop pkl params for fitting
- `demo/data/training_corpus/` -> generated JSONL files
- `demo/artifacts/` -> demo execution report

## Run

From repository root:

```bash
python demo/scripts/generate_laptop_corpus.py
python demo/scripts/laptop_demo.py
python demo/scripts/visualize_laptop.py
python demo/scripts/visualize_laptop.py --show
```

`laptop_demo.py` and `visualize_laptop.py` use code-defined Stage2 parameters
from `demo/scripts/laptop_demo.py` for runtime assembly.

`code/Laptop/conceptualization.pkl` remains a training-data source (as in the
project plan). We only use it for one-time fitting/extraction, then keep
the fitted values in code defaults.

To switch defaults to another pkl sample in one step:

```bash
python demo/scripts/extract_laptop_fitted_defaults.py --sample-index 5 --apply
```
