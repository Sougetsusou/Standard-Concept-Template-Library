# Template Code Edit Plan (Revised)

---

## Overview

**Strategy:** Direct-rewrite into `part_template/`, not three in-place passes on the old code.

The `demo/part_template/` directory proves the end architecture works end-to-end. Rather than carefully patching the 39 existing `code/<Category>/concept_template.py` files across three passes (risking partial application, pkl drift, and backward-compatibility fragility), we write each class fresh in the correct location and to convention from day one.

The old code is never modified — it serves only as a geometry-logic reference and is retired once its category manifest is slimmed.

---

## Why Direct Rewrite Beats In-Place Patching

| Old approach | New approach |
|---|---|
| Fix bugs in-place → risk of partial convention application | Write to convention once, correctly |
| Three sequential passes across 39 files | Single migration workflow per semantic file |
| Duplicate resolution as a separate pass (pkl churn) | MERGE/SPLIT decided at write time |
| Category files stay messy until Pass 3 | Category manifest slimmed immediately after migration |
| Conventions enforced retroactively | Conventions enforced at construction |

---

## Reference Materials

| Document | Role |
|---|---|
| `demo/part_template/*.py` | Reference implementation — convention-correct classes |
| `demo/code/Laptop/concept_template.py` | Reference slim manifest (3-line import-only file) |
| `coding_conventions.md` | Mandatory checklist for every class written |
| This document §Bug Catalogue | Per-class correctness notes from the original code review |
| This document §Duplicate Resolution | MERGE/SPLIT decision per duplicate group |

---

## Working Directory Strategy

- **Write new classes to `part_template/<semantic>.py`** — never patch `code/<Category>/`.
- **Keep `code/<Category>/concept_template.py` untouched** until all its classes are verified in `part_template/`.
- **Slim the category manifest** (replace with pure imports) only after `python visualize.py` passes.
- **`code_original/`** is a read-only archive. Never edit it.

---

## Part File Map

Target structure for `part_template/`:

```
part_template/
  __init__.py
  base.py         # Cuboidal_Base, Cylindrical_Base, Round_Base, ...
  body.py         # Simple_Cuboidal_Body, Hollow_Cuboidal_Body, Multilevel_Body, ...
  leg.py          # Regular_Leg, Star_Leg, Cuboidal_Leg, Multilevel_Leg, ...
  door.py         # Cuboidal_Door, Sunken_Door, Roller_Door, ...
  handle.py       # Torus_Handle, Ring_Handle, Trifold_Handle, Cylindrical_Handle, ...
  cover.py        # Fourfold_Cover, Regular_Cover, Cylindrical_Cover, ...
  blade.py        # Curved_Blade, Cusp_Blade, Regular_Blade, ...
  button.py       # Controller_With_Button, Regular_Controller, ...
  tray.py         # Flat_Tray, Drawer_Like_Tray, ...
  connector.py    # Cuboidal_Connector, Cylindrical_Connector, ...
  screen.py       # Hinged_Panel_Screen, Layered_Panel_Screen, ...
  wheel.py        # Standard_Wheel, ...
  window.py       # Symmetrical_Window, Asymmetrical_Window, ...
  spout.py        # Curved_Spout, Straight_Spout, Trifold_Spout, ...
  switch.py       # Lever_Switch, Round_Switch, Rotary_Switch, ...
  drawer.py       # Regular_Drawer, StorageFurniture_Drawer, ...
  shelf.py        # Regular_Shelf, ...
  support.py      # Trifold_Support, Cylindrical_Support, ...
  hinge.py        # Regular_Hinge, ...
  hook.py         # Regular_Hook, Curved_Hook, ...
  rack.py         # Curved_Rack, Regular_Rack, ...
  bracket.py      # Semi_Ring_Bracket, ...
  frame.py        # Regular_Frame, ...
  shaft.py        # Cuboidal_Shaft, Rectangular_Shaft, ...
  cap.py          # Regular_Cap, SquareEnded_Cap, ...
  plug.py         # Standard_Plug, Cuboidal_Plug, ...
  knob.py         # Regular_Knob, ...
  burner.py       # Top_With_Burner, ...
  glasses.py      # RectangularFrame_Glasses, TrapezoidalFrame_Glasses, ...
  gripper.py      # Cusp_Gripper, ...
  jaw.py          # Regular_Jaw, ...
  lever.py        # Regular_Lever, ...
  baffle.py       # Rectangular_Baffle, Curved_Baffle, ...
  board.py        # Regular_Partition, ...
  armrest.py      # Regular_Armrest, ...
  back.py         # Ladder_Back, Splat_Back, Slat_Back, ...
  seat.py         # Regular_Seat, ...
  nozzle.py       # Regular_Nozzle, Press_Nozzle, Spray_Nozzle, ...
  refill.py       # Regular_Refill, ...
  wick.py         # Regular_Wick, ...
  clip.py         # Regular_Clip, ...
  guard.py        # Regular_Guard, ...
  shell.py        # Regular_Shell, ...
  sphere.py       # Regular_Sphere, ...
  cylinder.py     # Regular_Cylinder, ...
  magazine.py     # Complex_Magazine, ...
  cabinet.py      # Regular_Cabinet, ...
  doorframe.py    # Standard_Doorframe, ...
```

---

## Migration Workflow

For each semantic file in `part_template/`:

### Step A — Identify and resolve duplicates
1. List all classes belonging to this semantic type across all 39 categories.
2. For each duplicate group, apply the MERGE/SPLIT decision from the §Duplicate Resolution table below.
   - **MERGE:** write one unified class with the geometric name, add thin backward-compatible aliases.
   - **SPLIT:** write each variant as a separate class with a descriptive geometric name.

### Step B — Write each class
1. Read the old class(es) from `code/<Category>/concept_template.py` for geometry logic.
2. Write the new class in `part_template/<semantic>.py`:
   - Apply the full class skeleton from `coding_conventions.md §1`.
   - Fix all bugs noted for this class in §Bug Catalogue below.
   - Write the structured docstring (Semantic / Geometry / Used by / Parameters).
3. Verify against the Per-Class Checklist.

### Step C — Verify and slim
1. Import the new class and instantiate with a representative parameter set.
2. Once all classes for a category are migrated, slim `code/<Category>/concept_template.py` to pure imports.
3. Run `python visualize.py` in `code/<Category>/` — geometry must be unchanged.
4. Commit: one commit per semantic file or per category.

---

## Phase Order

Work semantic files in this order (highest cross-category reuse first):

| Priority | File | Reason |
|---|---|---|
| 1 | `body.py` | Present in nearly every category; most duplicate variants |
| 2 | `leg.py` | Chair, Table, Dishwasher, Oven, Refrigerator |
| 3 | `handle.py` | Largest duplicate group; highest LLM training value |
| 4 | `door.py` | Appliances, StorageFurniture, Table |
| 5 | `cover.py` | Box, Lighter, KitchenPot, Trashcan, Gluestick |
| 6 | `base.py` | Faucet, Display, Globe, Laptop |
| 7 | `connector.py` | Laptop (already done in demo) |
| 8 | `screen.py` | Display, Laptop (already done in demo) |
| 9 | `switch.py` | Switch, Faucet |
| 10 | `spout.py` | Faucet, Kettle |
| … | remaining files | in dependency order |

---

## Per-Class Migration Checklist

Before marking any class done:

- [ ] Structured docstring: `Semantic`, `Geometry`, `Used by`, `Parameters`
- [ ] Rotation conversion positive: `x / 180 * np.pi` — never negated
> This is the problem the convention is trying to solve. For training data quality, the LLM must be able to learn a stable meaning for rotation_X = [30] across all classes. If sibling classes flip its sign silently, the LLM sees contradictory examples and can't learn the pattern.
- [ ] All array params unpacked into named variables before any geometry call
- [ ] `int()` cast before every `range()` over a float param
- [ ] No `locals()` hack — numbered params collected into a list at top of `__init__`
- [ ] Single-primitive class: direct vertex/face assignment, no list/concatenate
- [ ] Multi-primitive class: list/concatenate with named sub-mesh variables
- [ ] Loop bodies use `tmp_mesh` local, never `self.mesh`
- [ ] Empty-concat guard on any class with conditional or loop-gated geometry
- [ ] Every `if/elif` dispatch has a terminal `else: raise ValueError(...)`
- [ ] Sequential `if/if/if` on one variable converted to `if/elif/elif`
- [ ] No `else: pass` dead branches
- [ ] Bilateral symmetry uses direction-table loop (not 2/4 copy-pasted blocks)
- [ ] Existence-flag dispatch uses data-driven loop (not N identical `if` blocks)
- [ ] Sub-mesh position/rotation passed to constructor, not applied post-hoc
- [ ] Multi-step transform chains have named comments per step
- [ ] Non-default `offset_first` or `rotation_order` has a one-line comment
- [ ] Boolean flags used as truthy (`if flag:` not `if flag == 1:`)

---

## Duplicate Resolution

Decisions from `project_plan.md` Week 1 audit. MERGE produces one class; SPLIT produces separate classes with geometric names. Aliases preserve pkl compatibility where needed.

| Duplicate group | Decision | Resulting class(es) |
|---|---|---|
| `Curved_Handle` (Bucket / Kettle / Mug) | MERGE — all Torus, differ only in mesh_rotation | `Torus_Handle` |
| `Curved_Handle` (Knife) | SPLIT — Ring + thickness | `Ring_Handle` |
| `Cuboidal_Door` (all variants) | MERGE — all single Cuboid, identical | `Cuboidal_Door` |
| `Cuboidal_Body` (Box / Dispenser / Gluestick / Lighter / Washingmachine) | SPLIT — single Cuboid | `Simple_Cuboidal_Body` |
| `Cuboidal_Body` (Dishwasher / Microwave / Oven / Refrigerator / Safe) | SPLIT — Cuboid + Rectangular_Ring hollow | `Hollow_Cuboidal_Body` |
| `Cuboidal_Handle` (Appliances) | SPLIT — Cuboid with position offset | `Offset_Cuboidal_Handle` |
| `Cuboidal_Handle` (Window) | SPLIT — multi-cuboid, layer-aware | `Window_Cuboidal_Handle` |
| `Cuboidal_Handle` (Knife / Scissors) | MERGE — identical single Cuboid | `Cuboidal_Handle` |
| `Cylindrical_Body` (Gluestick) | SPLIT — single Cylinder with scaling | `Simple_Cylindrical_Body` |
| `Cylindrical_Body` (Bucket / KitchenPot / Mug / Trashcan) | SPLIT — Cylinder + Ring hollow | `Hollow_Cylindrical_Body` |
| `Cylindrical_Handle` (Door / Kettle / Knife) | MERGE — all single Cylinder, same rotation | `Cylindrical_Handle` |
| `Double_Layer_Body` (Lighter) | SPLIT — two stacked Cuboids | `Stacked_Cuboidal_Body` |
| `Double_Layer_Body` (Dishwasher / Oven / Refrigerator) | SPLIT — Cuboid + Rectangular_Ring + clapboard | `Clapboard_Cuboidal_Body` |
| `Multilevel_Body` (all) | MERGE — all stacked Cylinder + Ring, same pattern | `Multilevel_Body` |
| `Multilevel_Leg` (Dishwasher) | SPLIT — adds top_bottom_offset | `Offset_Multilevel_Leg` |
| `Multilevel_Leg` (Oven / Refrigerator) | SPLIT — standard | `Multilevel_Leg` |
| `Regular_leg` (Chair / Table) | MERGE — both single Cuboid | `Regular_Leg` |
| `Star_leg` (Chair / Table) | MERGE — identical structure | `Star_Leg` |
| `Trifold_Handle` (all variants) | MERGE — all 3-Cuboid structure | `Trifold_Handle` |
| `Curved_Blade` (Knife / Scissors) | MERGE — both Cuboid + quarter Cylinder | `Curved_Blade` |
| `RotaryX/Y/Z_Switch` | MERGE — axis only differs | `Rotary_Switch(axis=)` + aliases |
| `UShapedXZ/YZ_Base` | MERGE — plane only differs | `UShaped_Base(plane=)` + aliases |
| `FlipX/Y_Switch` | MERGE — rotation axis only | `Flip_Switch(axis=)` + aliases |
| `Regular_sublayer` / `Cylindrical_sublayer` | MERGE — primitive only | `Regular_Sublayer(shape=)` + aliases |
| `Lever_Switch` (Faucet) | SPLIT — different geometry from Switch version | `Faucet_Lever_Switch` |
| Remaining groups (audit ongoing) | audit geometry → merge or split with geometric name | TBD |

For every MERGE, keep the old names as **thin aliases** in the same file:

```python
class RotaryX_Switch(Rotary_Switch):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, axis='X', **kwargs)
```

---

## Bug Catalogue

Bugs found in the original code, organized by class. Use this as a per-class
correctness checklist when migrating — the direct-rewrite approach means each
bug is fixed naturally by writing to convention, but this table ensures nothing
is missed.

### Crashes (must fix)

| Class | File | Bug | Fix |
|---|---|---|---|
| All conditional-geometry classes | multiple | `np.concatenate([])` when all flags zero | Empty-concat guard (convention §4d) |
| Many loop classes | multiple | `range(float_param)` | `int()` cast (convention §3b) |
| `Cuboidal_Shaft`, `Double_Cuboidal_Shaft` | `shaft_templates.py` | `if/elif` with no `else`, variable uninitialized | Terminal `else: raise` (convention §4e) |
| `Cuboidal_Plug` | `plug_templates.py` | Trailing comma makes `mesh_position` a tuple | Remove trailing comma |

### Silent Wrong-Geometry Bugs

| Class | File | Bug | Fix |
|---|---|---|---|
| `Regular_Nozzle` | `nozzle_templates.py` | `num_of_nozzle == 2` (list vs int); `nozzle_length[0]` used for second nozzle | Compare `[0]`; use `nozzle_length[1]` for second |
| `Complex_Magazine` | `magazine_templates.py` | `behind_mesh` built with `bottom_mesh_position` | Use `behind_mesh_position` |
| `Regular_Leg` (Table) | `leg_templates.py` | Rear-leg Y uses `front_legs_size[1]` | Use `rear_legs_size[1]` |
| `Middle_Curved_Handle` | `handle_templates.py` | `exist_angle` used as list in `np.cos`/`np.sin` | Use `exist_angle[0]` |
| `PiShape_Handle` | `handle_templates.py` | `handle_z_direction` sign inverted | `= 1` when `handle == 1` |
| `Rectangular_Shaft` | `shaft_templates.py` | `layer_3` Y position formula wrong | Audit and correct Y stacking |
| `Doorframe` | `doorframe_templates.py` | `front_left_size[0]` used for right panel position | Use `front_right_size[0]` |
| `Regular_Drawer` (Table) | `drawer_templates.py` | `handle_offset[idx][0]` used for Y | Use `handle_offset[idx][1]` |
| `Regular_Cabinet` | `cabinet_templates.py` | `type_of_spaces[cabinet_idx]` indexing inconsistency; `door_handles_size[0/1/2]` wrong index | Fix to `[actual_idx]`; use `[cabinet_idx][...]` |
| `Curved_Base` | `base_templates.py` | `base_rotation` not converted to radians | Add `base_rotation = [x / 180 * np.pi for x in base_rotation]` |
| `Spray_Nozzle` | `nozzle_templates.py` | `tan`/`sin` mix in `top_offset_y` | Pick one consistent trig function |
| `Refill` | `refill_templates.py` | Dead `np.concatenate` before geometry loop; no-op rotation on symmetric Cone | Remove both |
| `Cuboidal_Spout`, `RegularY_Switch`, `RegularX_Switch`, `Regular_Blade` | multiple | Negated rotation conversion `[-x / 180 * np.pi]` | Positive conversion (convention §2) |
| `RotaryX_Switch` | `switch_templates.py` | Asymmetric `existence_of_switch[0] * -1` | Audit; fix or document |
| `Hinge` | `hinge_templates.py` | `sum(separation[0:i])` — no bounds check | Validate `len(separation) >= number_of_hinge[0] - 1` |
| `Hook`, `Curved_Rack` | `hook_templates.py`, `rack_templates.py` | Potential negative Ring inner radius | Assert `inner_radius > 0` |
| `Glasses` (all) | `glasses_templates.py` | Sentinel vertex never removed; double-append in `TrapezoidalFrame_Glasses`; magic hardcoded vertex indices | Strip sentinel; fix double-append; replace magic indices with named constants |
| `L_type_Desktop` | `body_templates.py` | Missing `super().__init__()` call | Add `super().__init__(position, rotation)` |
| `Symmetrical_Window` | `window_templates.py` | In-place mutation of shared config dicts | Copy `glass_offset` before mutating |

### Structural Anti-Patterns (fixed by convention)

These are all resolved automatically by following `coding_conventions.md` —
listed here only as a reminder of which classes are most affected.

| Anti-pattern | Most affected classes |
|---|---|
| `self.mesh` overwritten in loop | Nearly every file with loops — `panel`, `plug`, `rack`, `nozzle`, `switch`, `support`, `spout`, `lever`, `handle`, `shaft`, `leg`, `layer`, `armrest`, `back`, `base`, `body`, `cover`, `connector`, `drawer`, `door`, `hinge`, `button`, `burner` |
| Single-item `np.concatenate` | `shell`, `sphere`, `wick`, `wheel`, `screen`, `seat`, `knob`, `guard`, `clip`, `controller`, `connector`, `cover`, `body`, `board`, `baffle`, `base`, `frame`, `cylinder`, `refill` |
| `locals()` hack | `Round_Switch`, `Straight_Spout`, `Press_Nozzle`, `Standard_Cover`, `Mutiple_Layer_Body`, `Multilevel_Body`, `Controller_With_Button`, `Top_With_Burner` |
| Bilateral symmetry unrolled | `Cusp_Gripper`, all Pliers handles, `Fourfold_Cover`, `Holed_Cuboidal_Cover`, `Standard_Doorframe`, `Ladder_Back`, `Splat_Back`, `Latice_Back`, `Slat_Back`, `Rectangular_Baffle`, `Curved_Baffle`, `Standard_Body`, `Cambered_Body`, `Standard_Plug`, `Regular_Partition`, `UShapedXZ_Base`, `UShapedYZ_Base` |
| Existence-flag N-block copy-paste | `Fourfold_Cover`, `Holed_Cuboidal_Cover`, `Regular_Partition`, `Trifold_Support`, `Standard_Door`, `RotaryX_Switch`, `Standard_Doorframe`, `Semi_Ring_Bracket` |
| Post-construction vertex mutation | `jaw`, `switch`, `spout`, `support`, `lever`, `nozzle`, `glasses`, `blade`, `cap`, `door`, `base` |

---

## pkl Regeneration

After all classes for a category are migrated and verified:

- If any class was **renamed** (SPLIT with a new geometric name), regenerate `conceptualization.pkl` for that category.
- If a class was **merged** and an alias kept the old name, no pkl regeneration needed.
- Regeneration order matches the duplicate resolution table — do all categories in one batch per affected class name.

Reference: old `edit_plan.md` §2.2 has the full per-variant table of which pkl files need updating for each rename.

---

## Final Verification (per category)

1. `python visualize.py` in `code/<Category>/` renders geometry unchanged.
2. All class names referenced in `conceptualization.pkl` are importable from the slimmed manifest.
3. No `code/<Category>/concept_template.py` contains any class definition — only imports.

---

## Training Corpus Generation

Once all 39 categories are migrated:

1. Run the corpus generation script (generalizing `demo/scripts/generate_laptop_corpus.py`) for all categories.
2. Verify Level 2 JSONL (one entry per class in `part_template/`) and Level 3 JSONL (one entry per pkl instance).
3. Confirm held-out categories (Eyeglasses, Foldingrack, Pliers, Stapler, Pen, Clip) are excluded from training split.
