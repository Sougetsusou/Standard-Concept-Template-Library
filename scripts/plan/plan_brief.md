# Plan: Teaching LLMs to Write 3D Concept Template Code

## Goal

Fine-tune a code LLM that, given only a **category name and text description**,
produces **executable Python code** assembling a 3D object from parametric
part templates — generalizing to object categories never seen during training.

## Problem

ConceptFactory (NeurIPS 2024) defines ~250 part-template classes across
39 object categories. Each class composes geometry primitives (Cuboid, Cylinder,
Ring, …) into a semantic part (Handle, Body, Leg, …) with pose and size
parameters. Currently, adding a new category requires a human to manually
select parts and write the assembly code.

## Approach

A two-stage LLM pipeline, trained on a restructured version of the existing
template library:

```
  "laptop with hinged screen and side ports"
                    │
                    ▼
       ┌────────────────────────┐
       │  Stage 1: Part Gen     │  Decompose → for each part,
       │                        │  select from library OR write new
       └────────────────────────┘
                    │
                    ▼
       ┌────────────────────────┐
       │  Stage 2: Assembly     │  Import classes, instantiate
       │                        │  with concrete parameter values
       └────────────────────────┘
                    │
                    ▼
          Execute → validate mesh
          (one retry on failure)
```

## Phases

### Phase 1 — Codebase Restructuring 

The raw codebase has 30 name collisions, ~50 crash-level bugs, and heavy
duplication across categories. Three sequential passes clean it into a
training-ready corpus:

| Pass | Scope | Key actions |
|------|-------|-------------|
| **1. Bug fixes** | No signature changes | Fix crashes (`range(float)`, empty `np.concatenate`, uninitialized vars), fix silent geometry bugs (wrong indices, missing radian conversion), refactor copy-paste blocks into loops |
| **2. Renames** | Signature + pkl changes | Disambiguate 30 incompatible duplicate class names, eliminate `locals()` hacks |
| **3. Consolidate** | Structural | Merge 7 identical duplicate groups into shared module, extract base classes for axis-variant families |

After all passes: ~200 unique, documented, correctly-named part classes
in `part_template/`, organized by semantic type. Each category's
`concept_template.py` becomes an import-only manifest.

### Phase 2 — Training Data 

Two-level corpus extracted from the cleaned library + pkl annotation files:

| Level | Content | Size |
|-------|---------|------|
| **Level 2** — Part templates | Docstring ↔ class implementation pairs | ~200 base + ~2000 synthetic |
| **Level 3** — Full assemblies | Category description → part decomposition + instantiation code | ~3900 (39 cat × ~100 pkl entries) |

Synthetic augmentation: sample parameter variations from pkl distributions,
auto-generate natural-language descriptions, pair with instantiation code.

Hold out 6 structurally unusual categories (Eyeglasses, Foldingrack, Pliers,
Stapler, Pen, Clip) as the generalization test set.

### Phase 3 — Fine-tuning 

Base model: DeepSeek-Coder or CodeLlama 7B. Staged curriculum:

| Stage | Data | Goal | Metric |
|-------|------|------|--------|
| **A** | Level 2 only | Write valid part classes from descriptions | Execution success rate |
| **B** | Level 3 | Produce full assemblies from category descriptions | Execution success + Chamfer distance |
| **C** | Combined | Single model handles both | End-to-end success on val set |

Ablations (Week 10): A-only vs A+B vs A+B+C; with/without synthetic
augmentation; with/without docstrings.

### Phase 4 — Evaluation (TBD)

| Test | Input | Metrics |
|------|-------|---------|
| **Held-out categories** (6) | Category name + description | Execution success, part decomposition accuracy, Chamfer distance |
| **Novel categories** (3–5) | Text description only (no ground truth) | Execution success + human plausibility (1–5) |
| **Vocabulary coverage** | — | % of novel parts served by existing classes vs written new |

### Phase 5 — Deployment 

Wrap the trained model in an inference API:
`generate_concept_template(category, description) → executable Python code`,
with one-retry validation loop.

## Timeline

```
Wk 1─2     Wk 3       Wk 4─5           Wk 6    Wk 7+
──────┬──  ──────┬──    ──────┬──      ───┬──     ───┬──
 Code │     Data │      Train │       Eval│  TBD(RL?)│
 Fix  │     Build│      A→B→C │     Deploy│          │
──────┘    ──────┘     ───────┘        ───┘       ───┘
```

## Key Design Decisions

1. **Geometry primitives as a fixed API.** The LLM learns the part-template
   pattern and vocabulary, not low-level mesh construction.
2. **Two-stage pipeline over monolithic generation.** Part selection/creation
   is decoupled from parameter-value assignment — each stage has a smaller
   output space.
3. **Docstrings as the retrieval mechanism.** The LLM matches natural-language
   part descriptions to library classes via structured docstrings, not by
   memorizing class names.
4. **Execution-gated training.** Every training example is runnable code.
   The validation loop at inference mirrors this — the model learns to produce
   code that passes the same check.
