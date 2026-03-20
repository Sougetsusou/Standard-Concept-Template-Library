# Quickstart

## 1. Generate minimal laptop corpus

```bash
python demo/scripts/generate_laptop_corpus.py
```

Optional: extract fitted Stage2 parameters from Laptop pkl (one-time)

```bash
python demo/scripts/extract_laptop_fitted_defaults.py --sample-index 0
```

Switch to another pkl sample and apply it to code defaults in one command

```bash
python demo/scripts/extract_laptop_fitted_defaults.py --sample-index 5 --apply
```

## 2. Run end-to-end laptop demo

```bash
python demo/scripts/laptop_demo.py
```

## 3. Check outputs

- Corpus: `demo/data/training_corpus/`
- Execution report: `demo/artifacts/laptop_demo_report.json`

## 4. Export/visualize mesh

```bash
python demo/scripts/visualize_laptop.py
# Optional viewer if Open3D is available
python demo/scripts/visualize_laptop.py --show
```

- Mesh export (default): `demo/artifacts/laptop_demo_mesh.obj`
- Stage2 runtime uses code-defined defaults in `demo/scripts/laptop_demo.py`.
- Current defaults are fitted once from a Laptop pkl sample and then kept in code.
