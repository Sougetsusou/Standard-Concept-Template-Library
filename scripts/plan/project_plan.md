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

### Week 1 — Geometric audit + unify duplicate classes

The core principle: **class names describe geometry, not category origin.**

For each duplicate group across categories, classify as:
- **MERGE** — same primitive(s), same structure, only orientation/minor param differs
  → unify into one class, expose orientation as a parameter
- **SPLIT** — different primitives or meaningfully different structure
  → give each variant a descriptive geometric name

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
| Remaining groups | audit geometry → merge or split with descriptive name | TBD |

For MERGE: write one unified class, delete duplicates, patch pkl files.
For SPLIT: rename in-place with descriptive name, patch pkl files.

**Deliverable:** every class name is a geometric description. pkl files consistent.

---

### Week 2 — Reorganize into semantic part files

Move all part classes from `code/<Category>/concept_template.py` into
`part_template/` organized by semantic type:

```
part_template/
  __init__.py
  body.py         # Simple_Cuboidal_Body, Hollow_Cuboidal_Body,
                  #   Multilevel_Body, Stacked_Cuboidal_Body, ...
  leg.py          # Cuboidal_Leg, Regular_Leg, Star_Leg,
                  #   Multilevel_Leg, Offset_Multilevel_Leg, ...
  door.py         # Cuboidal_Door, Sunken_Door, Roller_Door, ...
  handle.py       # Torus_Handle, Ring_Handle, Trifold_Handle,
                  #   Cylindrical_Handle, Cuboidal_Handle, ...
  cover.py        # Fourfold_Cover, Regular_Cover, Cylindrical_Cover, ...
  blade.py        # Curved_Blade, Cusp_Blade, Regular_Blade, ...
  button.py       # Controller_With_Button, Regular_Controller, ...
  tray.py         # Flat_Tray, Drawer_Like_Tray, ...
  connector.py    # Cuboidal_Connector, Cylindrical_Connector, ...
  screen.py       # Hinged_Panel_Screen, Layered_Panel_Screen, ...
  base.py         # Cuboidal_Base, Cylindrical_Base, Round_Base, ...
  wheel.py        # Standard_Wheel, ...
  window.py       # Symmetrical_Window, Asymmetrical_Window, ...
  spout.py        # Curved_Spout, Straight_Spout, ...
  switch.py       # Lever_Switch, Round_Switch, Rotary_Switch, ...
  ... (~50 files total)
```

Each file is a self-contained geometric vocabulary for that semantic part type.
No class definitions remain in `code/<Category>/concept_template.py`.

**Deliverable:** all classes in part_template/, all 39 visualize.py still run correctly.

---

### Week 3 — Slim manifests + write docstrings

**Slim category files** to pure assembly manifests — imports only:
```python
# code/Box/concept_template.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'part_template'))

from body import Hollow_Cuboidal_Body
from leg import Cuboidal_Leg
from cover import Regular_Cover, Fourfold_Cover
```

**Write structured docstrings** for every part class in part_template/:
```python
class Torus_Handle(ConceptTemplate):
    """
    Semantic: Handle
    Geometry: arc-shaped handle formed from a partial torus segment
    Used by: Bucket, Kettle, Mug
    Parameters:
      radius [major, minor]: major radius of arc, cross-section radius
      exist_angle [a]: arc span in degrees
      position, rotation: global transform
    """
```

Docstrings are the selection mechanism — the LLM matches natural language
descriptions to classes via these at inference time.

**Deliverable:** all part classes have docstrings. Category manifests are import-only.

---

## Phase 2 — Training Data Construction
**Goal:** build a two-level training corpus with synthetic augmentation
**Timeline: Weeks 4–6**

### Week 4 — Build two-level corpus

**Level 2 — Part templates** (~200 base examples)
Source: `code/shared/<semantic>_templates.py`
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
Source: `code/<Category>/concept_template.py` + `conceptualization.pkl`
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
#   Base:      Regular_Base — flat cuboid keyboard/trackpad base
#   Screen:    Hinged_Panel_Screen — thin panel tilted open from hinge
#   Connector: Cuboidal_Connector — rectangular side ports

import sys, os
sys.path.insert(0, ...)
from base_templates import Regular_Base
from screen_templates import Hinged_Panel_Screen
from connector_templates import Cuboidal_Connector

base = Regular_Base(size=[0.32, 0.02, 0.22], position=[0.0, -0.01, 0.0], rotation=[0.0, 0.0, 0.0])
screen = Hinged_Panel_Screen(size=[0.30, 0.01, 0.21], offset=[0.11, 0.0], screen_rotation=[110], ...)
ports = Cuboidal_Connector(number_of_connector=[2], size=[0.015, 0.008, 0.012], ...)
```

~3900 Level 3 examples (39 categories × ~100 pkl instances each).
The pkl is the primary training data source.

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
| 1 | 1.1 | Geometric audit complete, all duplicates merged/split, pkl files patched |
| 2 | 1.2 | All part classes in `code/shared/<semantic>_templates.py` |
| 3 | 1.3 | Category manifests import-only, docstrings on all part classes |
| 4 | 2.1 | Level 2 + Level 3 base corpus built |
| 5 | 2.2 | Synthetic augmentation (~2000 Level 2 examples) |
| 6 | 2.3 | Final dataset, train/val/test split |
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

## Coding Conventions for `code/part_template/`

These conventions apply to **all** files in `code/part_template/` and must be followed
when writing new classes or migrating existing ones.

### Convention 1 — Unpack parameter arrays into named variables

**Always** unpack array parameters into named local variables at the top of `__init__`,
before any geometry construction. Never use raw index access (`size[0]`, `offset[1]`)
in geometry calls.

```python
# BAD — opaque, requires cross-referencing docstring
self.mesh = Cylinder(size[1], size[0], size[0],
                     position=[0, 0, size[1] / 2])

# GOOD — self-documenting
radius, height = size[0], size[1]
self.mesh = Cylinder(height, radius, radius,
                     position=[0, 0, height / 2])
```

For multi-element params, unpack all fields:
```python
# size [w, h, d]
width, height, depth = size
# offset [x, y, z]
ox, oy, oz = offset
# separation [sx, sy, sz]
sx, sy, sz = legs_separation
```

**Rationale:** named variables make geometric intent self-evident without needing
to look up the docstring. The LLM learns `height / 2` as a meaningful expression,
not `size[1] / 2`. This is critical for training data quality.

### Convention 2 — Structured docstring on every class

Every class must have a docstring in this format:
```python
"""
Semantic: <type>
Geometry: <one-line description of the shape produced>
Used by: <comma-separated list of source categories>
Parameters:
  param_name [field1, field2, ...]: description of each field
  ...
"""
```

### Convention 3 — No single-item list/concatenate boilerplate

For classes with only one geometry primitive, assign vertices/faces directly:
```python
# BAD
vertices_list = []
faces_list = []
total_num_vertices = 0
self.mesh = Cylinder(...)
vertices_list.append(self.mesh.vertices)
faces_list.append(self.mesh.faces + total_num_vertices)
self.vertices = np.concatenate(vertices_list)
self.faces = np.concatenate(faces_list)

# GOOD
self.mesh = Cylinder(...)
self.vertices = self.mesh.vertices
self.faces = self.mesh.faces
```

For classes with multiple geometries, keep the list/concatenate pattern.

### Convention 4 — Local variables in loops, not instance attributes

Inside `for` loops, always use local `tmp_mesh` variables, never `self.mesh`:
```python
# BAD — only last iteration survives on instance
for i in range(n):
    self.mesh = Cuboid(...)
    vertices_list.append(self.mesh.vertices)

# GOOD
for i in range(n):
    tmp_mesh = Cuboid(...)
    vertices_list.append(tmp_mesh.vertices)
```

### Convention 5 — Empty-concat guard on conditional geometry

Any class where `vertices_list` may be empty (conditional or loop-driven geometry)
must guard before `np.concatenate`:
```python
if not vertices_list:
    raise ValueError(f"{self.__class__.__name__}: no geometry was instantiated")
self.vertices = np.concatenate(vertices_list)
```

### Convention 6 — Comment non-default transform flags

Any use of `offset_first=True` or non-default `rotation_order` must have a comment:
```python
# offset_first=True: translation applied before rotation (part sits on a rotated surface)
self.vertices = apply_transformation(self.vertices, position, rotation, offset_first=True)
```

