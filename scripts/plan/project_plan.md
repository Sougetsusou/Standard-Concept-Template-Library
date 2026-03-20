# Project Plan: Teaching LLM to Write Concept Template Code

---

## Objective

Fine-tune a code LLM to generalize 3D object conceptualization to unseen categories.
Given only a category name and text description, the LLM should:
1. Decompose the object into semantic parts from its own learned knowledge
2. For each part: select an existing part class or write a new one from primitives
3. Assemble a fully executable instance with concrete parameter values

---

## Architecture Overview

```
Input: category name + text description only
         │
         ▼
┌─────────────────────────────────────┐
│  Stage 1 LLM — Part generation      │
│  → decompose description into parts │
│  → for each part:                   │
│      select existing class, OR      │
│      write new class from primitives│
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Stage 2 LLM — Instance assembly    │
│  → import selected/new classes      │
│  → instantiate with parameter values│
└─────────────────────────────────────┘
         │
         ▼
    Validation: execute code, check mesh non-degenerate
    (one retry loop on failure)
```

Geometry primitives (Cuboid, Cylinder, Ring, etc.) are treated as a known API.
The LLM learns the part template pattern and part vocabulary, not Python syntax.

---

## Phase 1 — Codebase Restructuring
**Goal:** build a clean geometric taxonomy as the training corpus
**Timeline: Weeks 1–3**

### Strategy: Direct-rewrite into `part_template/`

Rather than patching the existing `code/<Category>/concept_template.py` files
in multiple passes, each class is written fresh into `part_template/` using
the old code as a geometry-logic reference only. Duplicate resolution,
convention compliance, and docstrings all happen at write time — not as
separate passes.

**Reference implementation:** `demo/part_template/` contains convention-correct
classes for Laptop (`Cuboidal_Base`, `Hinged_Panel_Screen`, `Cuboidal_Connector`,
`Cylindrical_Connector`). These are the template for every new class written.

**Detailed migration workflow:** see `scripts/plan/edit_plan.md`.
**Convention reference:** see `scripts/plan/coding_conventions.md`.

---

### Duplicate resolution

The core principle: **class names describe geometry, not category origin.**

For each duplicate group, classify as:
- **MERGE** — same primitive(s), same structure, only orientation/minor param differs
  → write one unified class with geometric name; keep old names as thin aliases for pkl compatibility
- **SPLIT** — different primitives or meaningfully different structure
  → write each variant as a separate class with a descriptive geometric name

**Audit results:**

| Duplicate group | Classification | Resulting class(es) |
|---|---|---|
| `Curved_Handle` (Bucket/Kettle/Mug) | MERGE — all Torus, differ only in mesh_rotation | `Torus_Handle` |
| `Curved_Handle` (Knife) | SPLIT — uses Ring + thickness param | `Ring_Handle` |
| `Cuboidal_Door` (all variants) | MERGE — all single Cuboid, identical structure | `Cuboidal_Door` |
| `Cuboidal_Body` (Box/Dispenser/Gluestick/Lighter/Washingmachine) | SPLIT — single Cuboid | `Simple_Cuboidal_Body` |
| `Cuboidal_Body` (Dishwasher/Microwave/Oven/Refrigerator/Safe) | SPLIT — Cuboid + Rectangular_Ring hollow | `Hollow_Cuboidal_Body` |
| `Cuboidal_Handle` (Appliances) | SPLIT — Cuboid with position offset | `Offset_Cuboidal_Handle` |
| `Cuboidal_Handle` (Window) | SPLIT — multi-cuboid, layer-aware | `Window_Cuboidal_Handle` |
| `Cuboidal_Handle` (Knife/Scissors) | MERGE — identical single Cuboid | `Cuboidal_Handle` |
| `Cylindrical_Body` (Gluestick) | SPLIT — single Cylinder with x_z_ratio scaling | `Simple_Cylindrical_Body` |
| `Cylindrical_Body` (Bucket/KitchenPot/Mug/Trashcan) | SPLIT — Cylinder + Ring hollow | `Hollow_Cylindrical_Body` |
| `Cylindrical_Handle` (Door/Kettle/Knife) | MERGE — all single Cylinder, same rotation | `Cylindrical_Handle` |
| `Double_Layer_Body` (Lighter) | SPLIT — two stacked Cuboids | `Stacked_Cuboidal_Body` |
| `Double_Layer_Body` (Dishwasher/Oven/Refrigerator) | SPLIT — Cuboid + Rectangular_Ring + clapboard | `Clapboard_Cuboidal_Body` |
| `Multilevel_Body` (all) | MERGE — all stacked Cylinder + Ring, same pattern | `Multilevel_Body` |
| `Multilevel_Leg` (Dishwasher) | SPLIT — adds top_bottom_offset | `Offset_Multilevel_Leg` |
| `Multilevel_Leg` (Oven/Refrigerator) | SPLIT — standard version | `Multilevel_Leg` |
| `Regular_leg` (Chair/Table) | MERGE — both single Cuboid | `Regular_Leg` |
| `Star_leg` (Chair/Table) | MERGE — identical structure | `Star_Leg` |
| `Trifold_Handle` (all) | MERGE — all 3-Cuboid structure | `Trifold_Handle` |
| `Curved_Blade` (Knife/Scissors) | MERGE — both Cuboid + quarter Cylinder | `Curved_Blade` |
| `RotaryX/Y/Z_Switch` | MERGE — axis only differs | `Rotary_Switch(axis=)` + aliases |
| `UShapedXZ/YZ_Base` | MERGE — plane only differs | `UShaped_Base(plane=)` + aliases |
| Remaining groups | audit geometry → merge or split with geometric name | TBD |

---

### Week 1 — Write all part classes into `part_template/`

Work semantic file by semantic file, highest cross-category reuse first
(body → leg → handle → door → cover → base → …).

For each class:
1. Identify geometry logic from old `code/<Category>/concept_template.py`.
2. Apply duplicate resolution (MERGE or SPLIT from table above).
3. Write the new class in `part_template/<semantic>.py` following all conventions
   and with a structured docstring.
4. Instantiate with a representative parameter set to verify geometry.

The old `code/<Category>/` files are never modified during this step.

**Deliverable:** `part_template/` fully populated (~200 classes), every class
convention-correct and docstring-complete.

---

### Week 2 — Slim category manifests + verify

For each of the 39 categories:
1. Replace `code/<Category>/concept_template.py` with a pure import manifest:

```python
# code/Box/concept_template.py
from part_template.body import Simple_Cuboidal_Body
from part_template.leg import Cuboidal_Leg
from part_template.cover import Regular_Cover, Fourfold_Cover
```

2. Run `python visualize.py` in `code/<Category>/` — geometry must be unchanged.
3. For any category whose classes were renamed (SPLIT cases), regenerate
   `conceptualization.pkl` so stored class names match the new imports.

**Deliverable:** all 39 `visualize.py` pass, all pkl files consistent with
new class names, no class definitions remain in `code/<Category>/`.

---

### Week 3 — Training corpus generation

Generalize `demo/scripts/generate_laptop_corpus.py` to all 39 categories:
1. Level 2: one JSONL entry per class in `part_template/` (docstring + implementation pair).
2. Level 3: one JSONL entry per pkl instance (category + description → part decomposition
   + imports + full instantiation).
3. Validate: all Level 3 examples are executable; Level 2 covers all ~200 classes.

**Deliverable:** validated Level 2 + Level 3 JSONL corpus, ready for Phase 2.

---

## Phase 2 — Training Data Construction
**Goal:** build a two-level training corpus with synthetic augmentation
**Timeline: Weeks 4–6**

### Week 4 — Build two-level corpus

**Level 2 — Part templates** (~200 base examples)
Source: `part_template/<semantic>.py`
Each part class → two training examples:
- (docstring → implementation): given a geometric description, write the class
- (implementation → docstring): given the class, describe what it produces

Training format:
```
### Task: write_part_class
### Semantic type: Handle
### Description: arc-shaped handle formed from a partial torus, oriented vertically
### Existing classes: [Torus_Handle, Ring_Handle, Trifold_Handle, Cylindrical_Handle, ...]
### Decision: use_existing: Torus_Handle
### Instantiation:
Torus_Handle(radius=[0.05, 0.008], exist_angle=[200], position=[0.0, 0.05, 0.0], rotation=[0, 0, 90])
```

```
### Task: write_part_class
### Semantic type: Keyboard
### Description: flat tapered surface, thicker at back than front
### Existing classes: [Regular_Base, ...]
### Decision: write_new: Tapered_Keyboard
### Code:
class Tapered_Keyboard(ConceptTemplate):
    ...
```

**Level 3 — Full instance assembly** (~3900 base examples)
Source: slimmed `code/<Category>/concept_template.py` + `conceptualization.pkl`
Each pkl entry → one training example:
(category name + text description) → (part decomposition + imports + full instantiation)

Training format:
```
### Task: generate_concept_template
### Category: Laptop
### Description: a clamshell laptop with a flat rectangular keyboard base,
                 a thin screen panel hinged at the back, and two side ports
### Output:
# Part decomposition:
#   Base:      Cuboidal_Base — flat cuboid keyboard/trackpad base
#   Screen:    Hinged_Panel_Screen — thin panel tilted open from hinge
#   Connector: Cuboidal_Connector — rectangular side ports

from part_template.base import Cuboidal_Base
from part_template.screen import Hinged_Panel_Screen
from part_template.connector import Cuboidal_Connector

base = Cuboidal_Base(size=[0.32, 0.06, 0.9], position=[0.0, -0.14, 0.22], rotation=[0.0, 0.0, 0.0])
screen = Hinged_Panel_Screen(size=[1.3, 0.76, 0.02], offset=[-0.03, -0.56], screen_rotation=[-17], ...)
ports = Cuboidal_Connector(number_of_connector=[2], size=[0.02, 0.02, 0.04], ...)
```

~3900 Level 3 examples (39 categories × ~100 pkl instances each).
The pkl is the primary training data source. See `demo/data/training_corpus/`
for a validated example of the Level 2 and Level 3 format for Laptop.

### Week 5 — Synthetic augmentation

For each part class, sample parameter variations from the pkl distribution:
1. Sample valid parameter ranges (min/max per param from pkl data)
2. Instantiate the class, render point cloud
3. Auto-generate natural language description from parameter values
   ("arc handle, wide span, thin cross-section, oriented vertically")
4. Pair description with instantiation code

Target: ~10 variants × ~200 classes = ~2000 synthetic Level 2 examples.

### Week 6 — Dataset assembly + train/test split

Hold out 6 categories from all training data (generalization test set):
- Eyeglasses, Foldingrack, Pliers, Stapler, Pen, Clip
  (structurally unusual — stress-test generalization most)

Split:
- Train: 33 categories, Level 2 + Level 3 + synthetic augmentation
- Val: 3-4 categories (monitor overfitting)
- Test: 6 held-out categories (never seen during training)

**Deliverable:** structured JSONL files for Level 2 and Level 3, splits documented.

---

## Phase 3 — Fine-tuning
**Goal:** staged fine-tuning from part grammar to full pipeline
**Timeline: Weeks 7–10**

**Base model:** DeepSeek-Coder or CodeLlama 7B.
Already understands Python — fine-tuning teaches the template pattern and part vocabulary.

### Week 7 — Stage A: Part-level fine-tuning
Fine-tune on Level 2 data only.
Goal: LLM writes a valid part class given a semantic type + description.
Metric: execution success rate on val set part classes.

### Week 8 — Stage B: Assembly-level fine-tuning
Fine-tune Stage A checkpoint on Level 3 data.
Goal: LLM produces a fully executable instance given a category description.
Metric: execution success + Chamfer distance on val set instances.

### Week 9 — Stage C: End-to-end fine-tuning
Fine-tune Stage B checkpoint on combined Level 2 + Level 3 data.
Goal: single model handles both part writing and assembly.
Metric: end-to-end execution success on val set.

### Week 10 — Ablations + checkpoint selection
- Stage A-only vs A+B vs A+B+C
- With vs without synthetic augmentation
- With vs without docstrings in training data

---

## Phase 4 — Evaluation
**Goal:** measure generalization to unseen categories
**Timeline: Week 11**

### 4.1 Held-out category test (6 categories)
Input: category name + text description only (no part list, no parameter hints)
Metrics:
- Execution success rate (code runs without error)
- Part decomposition accuracy (identified parts match ground truth semantic parts)
- Part selection accuracy (correct use_existing vs write_new; correct class chosen)
- Geometric fidelity: Chamfer distance vs ground truth pkl point cloud

### 4.2 Novel category test (3-5 categories)
Manually designed categories not in any existing dataset.
Input: text description only.
Metric: execution success + human plausibility rating (1–5).

### 4.3 Part vocabulary coverage
What % of novel category parts can be served by existing classes vs require write_new?
This measures how complete the part vocabulary is.

---

## Phase 5 — Inference Pipeline
**Goal:** deployable system for new category generation
**Timeline: Week 12**

```python
def generate_concept_template(category: str, description: str) -> str:
    # Stage 1: decompose + write/select part classes
    part_classes = stage1_llm(category, description, vocab=shared_templates)

    # Stage 2: assemble full executable instance
    instance = stage2_llm(category, description, part_classes)

    # Validate + one retry on failure
    try:
        exec(instance)
        return instance
    except Exception as e:
        return stage2_llm(category, description, part_classes, error=str(e))
```

---

## Summary Timeline

| Week | Phase | Deliverable |
|------|-------|-------------|
| 1 | 1.1 | `part_template/` fully populated — all ~200 classes, convention-correct, docstring-complete |
| 2 | 1.2 | All 39 category manifests import-only, `visualize.py` passing, pkl files consistent |
| 3 | 1.3 | Level 2 + Level 3 base corpus generated and validated for all 39 categories |
| 4 | 2.1 | Level 2 + Level 3 base corpus finalized, synthetic augmentation started |
| 5 | 2.2 | Synthetic augmentation (~2000 Level 2 examples) |
| 6 | 2.3 | Final JSONL dataset, train/val/test split documented |
| 7 | 3.1 | Stage A checkpoint (part-level) |
| 8 | 3.2 | Stage B checkpoint (assembly-level) |
| 9 | 3.3 | Stage C checkpoint (end-to-end) |
| 10 | 3.4 | Ablations, best checkpoint selected |
| 11 | 4 | Evaluation on held-out + novel categories |
| 12 | 5 | Inference pipeline deployed |

---

## Open Questions

- Parameter description generation (Week 5): hand-written templates per param type,
  or a small geometry→text model? To be decided based on quality of auto-descriptions.
- Model size: 7B recommended for iteration speed; scale to 13B if 7B underfits.
- Stage C: does end-to-end fine-tuning help or hurt vs keeping Stage A and B separate?
  Key ablation in Week 10.

---

## Coding Conventions for `part_template/`

All conventions are fully specified in `scripts/plan/coding_conventions.md`.
The key principles:

- Every class follows a fixed `__init__` skeleton (rotation conversion → record params → unpack locals → geometry → concatenate → global transform → mesh/pts → semantic label).
- Rotation conversion is always positive (`x / 180 * np.pi`); sign flips applied explicitly after with a comment.
- All array params unpacked into named variables before any geometry call.
- Single-primitive classes use direct vertex/face assignment; multi-primitive classes use list/concatenate.
- Loop bodies always use `tmp_mesh` locals, never `self.mesh`.
- Empty-concat guard on any class with conditional or loop-gated geometry.
- Bilateral symmetry and existence-flag dispatch use data-driven loops, not copy-pasted blocks.
- Non-default `offset_first` or `rotation_order` flags have a one-line explanatory comment.

The `demo/part_template/` classes are the canonical reference implementation of all these conventions.

