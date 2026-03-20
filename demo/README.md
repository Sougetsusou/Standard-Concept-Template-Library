# Demo Workflow (Runnable MVP)

This folder contains a runnable end-to-end demo pipeline for STL-C with:

- Mock Stage 1 decomposition (deterministic)
- Mock Stage 2 assembly generation (deterministic)
- Execution on real category classes in `code/<Category>/concept_template.py`
- Mesh non-degenerate checks

## Included Categories

- Laptop
- Mug

## Run

From repository root:

```bash
python -m demo.cli generate-corpus
python -m demo.cli run-stage1 --category Laptop
python -m demo.cli run-stage2 --category Laptop
python -m demo.cli run-e2e --category Laptop
python -m demo.cli verify
```

Artifacts are written to `demo/artifacts/`.
