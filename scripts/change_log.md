# Change Log

---

## Session 1 — Crash Fixes (Pass 1, Steps 1.2a–1.2b)

### 1.2a Empty-concat guard
Added `if not vertices_list: raise ValueError(...)` before every `np.concatenate(vertices_list)` call in classes with conditional geometry.

17 guards applied across 3 files:
- `code/Switch/concept_template.py` — 7 guards (lines 219, 264, 309, 383, 426, 495, 540)
- `code/StorageFurniture/concept_template.py` — 5 guards (lines 112, 171, 226, 322, 364)
- `code/Window/concept_template.py` — 6 guards (lines 283, 410, 521, 609, 763, 907)

Script: `scripts/apply_empty_concat_guard.py`

### 1.2b Float-in-range fix
Wrapped all `range(param[0])` calls with `int()` to prevent `TypeError` in Python 3.

117 fixes across 21 categories:
Bottle(1), Chair(6), Dispenser(2), Display(2), Door(2), Faucet(8), Globe(2), Kettle(3), KitchenPot(1), Laptop(2), Microwave(1), Mug(1), Oven(2), Safe(3), Shampoo(2), StorageFurniture(28), Switch(8), Table(33), Trashcan(1), Washingmachine(1), Window(8)

Script: `scripts/apply_int_range.py`

---

## Session 2 — Leg Dispatch Loop Rewrite (Pass 2, Step 1.6b partial)

### Leg dispatch: if/elif chain → data table + loop

Replaced the `num_legs[0]` dispatch blocks (1/2/3/4 legs, ~100 lines each) with a compact position table and a single loop (~20 lines).

**Files changed:**
| File | Class | Lines before → after |
|---|---|---|
| `code/Box/concept_template.py` | `Cuboidal_Leg` | ~115 → ~20 |
| `code/Oven/concept_template.py` | `Multilevel_Leg` | ~115 → ~20 |
| `code/Refrigerator/concept_template.py` | `Multilevel_Leg` | ~115 → ~20 |
| `code/Safe/concept_template.py` | `Cuboidal_Leg` | ~115 → ~20 |
| `code/Dishwasher/concept_template.py` | `Multilevel_Leg` | ~120 → ~22 |

**Net reduction:** ~480 lines eliminated. Zero signature changes. Zero behavior changes.

**Pattern used:**
```python
n = int(num_legs[0])
sx, sz = legs_separation[0] / 2, legs_separation[2] / 2
sy_r = legs_separation[1] / 2
leg_specs = {
    1: [(front_legs_size, [0,   -front_legs_size[1]/2,  0 ])],
    2: [(front_legs_size, [ sx, -front_legs_size[1]/2,  0 ]),
        (front_legs_size, [-sx, -front_legs_size[1]/2,  0 ])],
    3: [...],
    4: [...],
}
for leg_size, mesh_position in leg_specs[n]:
    self.mesh = Cuboid(leg_size[1], leg_size[0], leg_size[2], position=mesh_position)
    vertices_list.append(self.mesh.vertices)
    faces_list.append(self.mesh.faces + total_num_vertices)
    total_num_vertices += len(self.mesh.vertices)
```

Dishwasher's `Multilevel_Leg` uses the same pattern with an additional `top_bottom_offset` applied to all positions.

---

## Session 3 — locals() Collection Rewrite (Pass 1, Step 1.6c)

Replaced all `locals()['param_%d' % (i+1)]` dynamic lookups with explicit list collection at the top of each `__init__`. Zero signature changes.

**Files changed:**

| File | Class | Pattern |
|---|---|---|
| `code/Oven/concept_template.py` | `Controller_With_Button` | `button_sizes`, `button_offsets` lists |
| `code/Oven/concept_template.py` | `Top_With_Burner` | `burner_sizes/thicknesses/offsets/central_sizes/central_offsets` lists |
| `code/Safe/concept_template.py` | `Mutiple_Layer_Body` | `sub_clapboard_sizes`, `sub_clapboard_offsets` lists |
| `code/Washingmachine/concept_template.py` | `Controller_With_Button` | `button_sizes`, `button_offsets` lists |
| `code/Microwave/concept_template.py` | `Controller_With_Button` | `button_sizes`, `button_offsets` lists |
| `code/Switch/concept_template.py` | `Round_Switch` | `offsets` list |
| `code/Bottle/concept_template.py` | `Multilevel_Body` | `level_sizes` list |
| `code/Dispenser/concept_template.py` | `Multilevel_Body` | `level_sizes` list |
| `code/Dispenser/concept_template.py` | `Press_Nozzle` | `level_sizes` list + direct index for last level |
| `code/KitchenPot/concept_template.py` | `Multilevel_Tophandle` | `level_sizes` list |
| `code/Mug/concept_template.py` | `Multilevel_Body` | `level_top_radii`, `level_heights` lists |
| `code/Kettle/concept_template.py` | `Multilevel_Body` | `level_top_radii`, `level_heights` lists |
| `code/Kettle/concept_template.py` | `Standard_Cover` | `knob_sizes` list |
| `code/Kettle/concept_template.py` | `Straight_Spout` | `spout_radii/thinknesses/lengths/generatrix_offsets/rotations` lists |

**Net result:** 0 remaining `locals()` calls across all 39 categories.

---

## Session 4 — self.mesh Overwrite Fix (Pass 1, Step 1.6d)

Replaced all `self.X = Geometry(...)` assignments inside `for` loops with `tmp_X = Geometry(...)` local variables, and updated all subsequent `.vertices`/`.faces` references in the same loop scope. This prevents the anti-pattern where only the last iteration's mesh survives as an instance attribute.

**Automated script:** indentation-based loop detection, 367 replacements across 21 files.

**Files changed:**
Box, Chair, Dishwasher, Display, Dispenser, Globe, KitchenPot, Kettle, Laptop, Microwave, Mug, Oven, Refrigerator, Safe, StorageFurniture, Switch, Table, Trashcan, Washingmachine, Window, Bottle

**Manual fix (Session 4 end):** `code/Switch/concept_template.py` `Lever_Switch` — two `apply_transformation` calls inside the loop still referenced `self.main_mesh.vertices` after the automated rename. Fixed to `tmp_main_mesh.vertices`.

**Net result:** 0 `self.X = Geometry(...)` assignments inside loops across all 39 categories.

---

## Backup

`code_original/` — full physical copy of all 39 categories before any edits. Never modified.

---
