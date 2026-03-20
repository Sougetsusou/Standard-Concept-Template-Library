# Quickstart

## 1. Generate training corpus artifacts

```bash
python -m demo.cli generate-corpus
```

## 2. Run full pipeline for Laptop

```bash
python -m demo.cli run-e2e --category Laptop
```

## 3. Run full pipeline for Mug

```bash
python -m demo.cli run-e2e --category Mug
```

## 4. Verify both categories

```bash
python -m demo.cli verify
```

## 5. Run tests

```bash
python -m unittest discover demo/tests
```
