# Template Coding Conventions

These conventions govern all template classes in `code/<Category>/concept_template.py`
(the working copies) and `part_template/` (the deduplicated library).
Every fix in the edit plan and every new class must follow them.

---

## 1. Class Skeleton

Every template class must follow this exact `__init__` structure, in this order:

```python
class Descriptive_Name(ConceptTemplate):
    """
    Semantic: <part type>
    Geometry: <one-line plain-English description of the shape produced>
    Used by: <comma-separated source categories>
    Parameters:
      param_name [field1, field2, ...]: description
      ...
    """
    def __init__(self, param_a, param_b, ..., position=[0, 0, 0], rotation=[0, 0, 0]):

        # 1. Rotation conversion (always positive, never negated)
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # 2. Record parameters
        self.param_a = param_a
        self.param_b = param_b

        # 3. Unpack into named locals
        width, height, depth = param_a

        # 4. Geometry construction
        ...

        # 5. Concatenate (or direct-assign for single mesh)
        ...

        # 6. Global transform
        self.vertices = apply_transformation(self.vertices, position, rotation)

        # 7. Final mesh + point cloud
        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = '<part type>'
```

### Rationale

The skeleton ensures a uniform reading order across all ~300 classes.
Steps 1–3 set up the state; step 4 is the only creative part; steps 5–7 are
boilerplate that should be visually identical across files so reviewers can
skip straight to the geometry logic.

---

## 2. Rotation Conversion

**Always** convert degrees to radians with the positive formula:

```python
rotation = [x / 180 * np.pi for x in rotation]
```

**Never** negate during conversion:

```python
# WRONG — introduces a sign ambiguity that downstream code must compensate for
rotation = [-x / 180 * np.pi for x in rotation]
```

If a parameter genuinely requires a sign flip, apply it explicitly after
conversion with a comment explaining the geometric reason:

```python
rotation = [x / 180 * np.pi for x in rotation]
# Negate X rotation: this part is mirrored relative to the parent's convention
rotation[0] *= -1
```

Any extra angle parameters (e.g. `screen_rotation`, `blade_rotation`) follow
the same rule — convert first, then manipulate if needed.

**Source:** `edit_plan.md` §1.3n — negated conversion in `Cuboidal_Spout`,
`RegularY/X_Switch`, `Regular_Blade` produced inconsistencies with sibling
classes that used positive conversion.

---

## 3. Parameter Unpacking

### 3a. Unpack arrays into named variables

**Always** unpack array parameters into named locals at the top of `__init__`,
before any geometry construction. Never use raw index access in geometry calls.

```python
# BAD
self.mesh = Cylinder(size[1], size[0], size[0])

# GOOD
radius, height = size[0], size[1]
self.mesh = Cylinder(height, radius, radius)
```

For multi-element params, unpack all fields:

```python
width, height, depth = size
ox, oy, oz = offset
```

**Why:** Named variables make geometric intent self-evident. The LLM learns
`height / 2` as a meaningful expression, not `size[1] / 2`. This also prevents
copy-paste index bugs (a major source of issues found in the review).

### 3b. Cast count parameters to `int` before `range()`

Parameters extracted from pkl are floats. Any parameter used as a loop count
must be cast:

```python
n = int(number_of_connector[0])
for i in range(n):
    ...
```

**Never** pass a raw float to `range()`.

**Source:** `review_notes.md` documents this crash in 12+ template files
(`Window`, `Leg`, `Layer`, `Panel`, `Nozzle`, `Switch`, `Handle`, `Hinge`,
`Connector`, `Drawer`, `Door`, `Body`).

### 3c. Collect numbered params into a list

When the signature contains `param_1, param_2, ..., param_N` (the `locals()`
hack pattern), collect them into a list at the top of `__init__` and iterate
over the list:

```python
def __init__(self, knob_1_size, knob_2_size, knob_3_size, num_knobs, ...):
    ...
    knob_sizes = [knob_1_size, knob_2_size, knob_3_size]
    for i in range(int(num_knobs[0])):
        k = knob_sizes[i]
        ...
```

**Never** use `locals()['param_%d' % (i+1)]`. It breaks static analysis,
obscures data flow, and is fragile.

**Source:** `edit_plan.md` §1.6c and `review_notes.md` — affects `Round_Switch`,
`Straight_Spout`, `Press_Nozzle`, `Standard_Cover`, `Mutiple_Layer_Body`,
`Multilevel_Body`, `Controller_With_Button`, `Top_With_Burner`.

---

## 4. Geometry Construction

### 4a. Single-mesh classes: direct assignment

If the class builds exactly one geometry primitive, assign vertices and faces
directly — no list/concatenate overhead:

```python
self.main_mesh = Cylinder(height, radius, radius, position=pos)
self.vertices = self.main_mesh.vertices
self.faces = self.main_mesh.faces
```

**Source:** `edit_plan.md` §1.4g — 19 files use the full list/concatenate
boilerplate for a single mesh.

### 4b. Multi-mesh classes: list/concatenate

For classes with multiple geometry primitives, use the standard pattern:

```python
vertices_list = []
faces_list = []
total_num_vertices = 0

self.top_mesh = Cuboid(...)
vertices_list.append(self.top_mesh.vertices)
faces_list.append(self.top_mesh.faces + total_num_vertices)
total_num_vertices += len(self.top_mesh.vertices)

self.bottom_mesh = Cylinder(...)
vertices_list.append(self.bottom_mesh.vertices)
faces_list.append(self.bottom_mesh.faces + total_num_vertices)
total_num_vertices += len(self.bottom_mesh.vertices)

self.vertices = np.concatenate(vertices_list)
self.faces = np.concatenate(faces_list)
```

### 4c. Loop variables: always local, never `self`

Inside loops, use local variable names for meshes. **Never** assign to
`self.mesh` or `self.X_mesh` in a loop — only the last iteration survives.

```python
# BAD — self.mesh clobbered each iteration
for i in range(n):
    self.mesh = Cuboid(...)
    vertices_list.append(self.mesh.vertices)

# GOOD
for i in range(n):
    tmp_mesh = Cuboid(...)
    vertices_list.append(tmp_mesh.vertices)
```

**Source:** `review_notes.md` — this anti-pattern appears in nearly every
template file with loops (~25 files), affecting attributes named `self.mesh`,
`self.base_mesh`, `self.main_mesh`, `self.knob_mesh`, `self.handle_mesh`,
`self.frame_mesh`, `self.glass_mesh`, `self.tmp_mesh`, `self.bracket_mesh`,
and many more.

### 4d. Empty-concat guard on conditional geometry

Any class where `vertices_list` may be empty (conditional flags, count-gated
loops) **must** guard before `np.concatenate`:

```python
if not vertices_list:
    raise ValueError(f"{self.__class__.__name__}: no geometry was instantiated")
self.vertices = np.concatenate(vertices_list)
self.faces = np.concatenate(faces_list)
```

**Source:** `edit_plan.md` §1.2a — 13 files hit `np.concatenate([])` crashes
when all existence flags are zero.

### 4e. Uninitialized variable guard on dispatch branches

When an `if/elif` chain sets a variable used later (e.g. `mesh_position`),
**always** add a terminal `else` that raises:

```python
if condition_a:
    mesh_position = [...]
elif condition_b:
    mesh_position = [...]
else:
    raise ValueError(f"Unexpected value: {param}")
```

**Never** leave the variable potentially uninitialized.

**Source:** `edit_plan.md` §1.2c — `Cuboidal_Shaft`, `Double_Cuboidal_Shaft`
cause `UnboundLocalError` on unexpected input.

---

## 5. Symmetry and Repetition

### 5a. Bilateral symmetry: direction loop

When the same mesh is placed at 2 or 4 symmetric positions differing only in
sign, replace the copy-pasted blocks with a loop over a direction table:

```python
directions = [
    (+1, +1),   # front-left
    (+1, -1),   # behind-left
    (-1, +1),   # front-right
    (-1, -1),   # behind-right
]
for x_sign, z_sign in directions:
    pos = [x_sign * offset_x, 0, z_sign * offset_z]
    tmp_mesh = Cuboid(..., position=pos)
    vertices_list.append(tmp_mesh.vertices)
    faces_list.append(tmp_mesh.faces + total_num_vertices)
    total_num_vertices += len(tmp_mesh.vertices)
```

**Source:** `edit_plan.md` §1.6a — the single most impactful change in the
library, eliminating 60–80% of code in affected classes. 10+ classes across
`gripper`, `handle`, `cover`, `doorframe`, `back`, `baffle`, `body`, `plug`,
`board`, `base` templates.

### 5b. Existence-flag dispatch: data-driven loop

When N conditional blocks are structurally identical except for which flag
controls them and which axis/sign they use, build a descriptor list and loop:

```python
panels = [
    (has_front[0],  front_size,  [0, 0,  depth / 2]),
    (has_back[0],   back_size,   [0, 0, -depth / 2]),
    (has_left[0],   left_size,   [-width / 2, 0, 0]),
    (has_right[0],  right_size,  [ width / 2, 0, 0]),
]
for flag, size, pos in panels:
    if not flag:
        continue
    tmp_mesh = Cuboid(size[1], size[0], size[2], position=pos)
    vertices_list.append(tmp_mesh.vertices)
    faces_list.append(tmp_mesh.faces + total_num_vertices)
    total_num_vertices += len(tmp_mesh.vertices)
```

**Source:** `edit_plan.md` §1.6b — affects `cover`, `board`, `support`,
`door`, `switch`, `doorframe`, `bracket` templates.

### 5c. Axis-variant families: merge with parameter

When 2–3 classes are identical except for which axis they operate on, merge
into a single class with an `axis` parameter. Keep the old names as thin
aliases for pkl backward compatibility:

```python
class Rotary_Switch(ConceptTemplate):
    def __init__(self, ..., axis='X'):
        ...

class RotaryX_Switch(Rotary_Switch):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, axis='X', **kwargs)
```

**Source:** `edit_plan.md` §1.6e — candidates include `RotaryX/Y/Z_Switch`,
`UShapedXZ/YZ_Base`, `FlipX/Y_Switch`, `Regular/Cylindrical_sublayer`.

---

## 6. Transform Handling

### 6a. Prefer constructor args over vertex mutation

Position and rotation of sub-meshes should be passed to the geometry
constructor, not applied post-hoc via `apply_transformation` on `.vertices`:

```python
# BAD — opaque multi-step mutation
self.mesh = Cylinder(height, radius, radius)
self.mesh.vertices = apply_transformation(self.mesh.vertices, pos, rot)

# GOOD — position/rotation expressed at construction
self.mesh = Cylinder(height, radius, radius, position=pos, rotation=rot)
```

The only exception is **pivot rotations** — where the rotation center is not
the mesh's own origin. In that case, use a local variable and add a comment:

```python
tmp_mesh = Cuboid(h, w, d, position=local_pos)
# Pivot rotation around parent joint at origin
tmp_mesh.vertices = apply_transformation(tmp_mesh.vertices, [0, 0, 0], pivot_rot)
vertices_list.append(tmp_mesh.vertices)
```

**Source:** `edit_plan.md` §1.4b — 11 files use post-construction vertex
mutation where constructor args would suffice.

### 6b. Name intermediate transforms in multi-step chains

When multiple sequential transforms are unavoidable (e.g. composing a pivot
with a parent rotation), **name** each step:

```python
# Step 1: align to local frame
tmp_mesh.vertices = apply_transformation(tmp_mesh.vertices, [0, 0, 0], local_rot)
# Step 2: place at arm endpoint
tmp_mesh.vertices = apply_transformation(tmp_mesh.vertices, arm_offset, [0, 0, 0])
# Step 3: pivot about shoulder joint
tmp_mesh.vertices = apply_transformation(tmp_mesh.vertices, [0, 0, 0], shoulder_rot)
```

**Never** chain 3–4 unnamed `apply_transformation` calls.

**Source:** `edit_plan.md` §1.6d — affects `Star_leg`, all `Regular*_Switch`,
`Trifold/ShowerRose/Quadfold_Spout`, all `Glasses` classes, `Cap` classes.

### 6c. Document non-default transform flags

The default global transform is `apply_transformation(v, position, rotation)`.
Any use of `offset_first=True` or a non-default `rotation_order` must have a
one-line comment explaining why:

```python
# offset_first: base is translated to mounting point before joint rotation
self.vertices = apply_transformation(self.vertices, position, rotation,
                                     offset_first=True)

# rotation_order="YXZ": matches Faucet-family gimbal convention
self.vertices = apply_transformation(self.vertices, position, rotation,
                                     rotation_order="YXZ")
```

**Source:** `review_notes.md` — inconsistent flag usage across sibling classes
(e.g. Faucet switches all use `"YXZ"` while Switch-source switches use the
default, with no explanation anywhere).

---

## 7. Dispatch and Control Flow

### 7a. Use `if/elif`, not sequential `if`

When branching on a single variable's value, use `if/elif/elif`, not
independent `if` blocks that all evaluate:

```python
# BAD — all branches evaluated every time
if n == 1: ...
if n == 2: ...
if n == 3: ...

# GOOD
if n == 1: ...
elif n == 2: ...
elif n == 3: ...
```

**Source:** `edit_plan.md` §1.4c — `Symmetrical_Window`, `Regular_leg`.

### 7b. No dead `else: pass` branches

Remove all `else: pass` blocks. If the else branch needs to handle an
unexpected value, raise an error (see §4e). Otherwise, omit it.

### 7c. Boolean flags: treat as truthy, not `== 1`

Existence flags from pkl are always 0 or 1. Use them directly:

```python
# BAD
if has_cover[0] == 1:

# GOOD
if has_cover[0]:
```

---

## 8. Naming

### 8a. Class names describe geometry, not category origin

Class names should convey the shape produced, not the object it came from.
When renaming duplicates, prefix with a geometric or structural adjective,
not the category name (category prefixes are acceptable only as a temporary
disambiguation in Pass 2 when the geometric difference is not yet characterized):

```
# GOOD
Hollow_Cuboidal_Body, Simple_Cuboidal_Body, Torus_Handle

# ACCEPTABLE (Pass 2 interim)
Microwave_Controller_With_Button

# BAD (permanent name)
Bucket_Handle, Globe_Base
```

### 8b. Fix known typos at point of edit

When editing a class, fix any typos in parameter names within that class.
Do not leave known typos unfixed in code you are already modifying:

```
seperation → separation
existance  → existence
level_     → lever_      (in Regular_lever)
Mutiple    → Multiple
Simplied   → Simplified
Connecter  → Connector
```

If the typo is in a class name or external-facing parameter name that
affects pkl compatibility, the fix belongs in **Pass 2** with a coordinated
pkl update.

### 8c. Consistent casing

- Class names: `Title_Case_With_Underscores` (e.g. `Cuboidal_Body`)
- Semantic labels: `'Title'` (e.g. `'Body'`, `'Handle'`)
- Parameter names: `snake_case`
- Local mesh variables: `snake_case` (e.g. `tmp_mesh`, `top_mesh_position`)

Lowercase class names like `Storagefurniture_body`, `Cylindrical_body`
should be renamed to `StorageFurniture_Body`, `Cylindrical_Body`.

---

## 9. Avoid These Anti-Patterns

A quick-reference checklist. Each links to the convention section with the
full rule.

| Anti-pattern | Fix | Section |
|---|---|---|
| `self.mesh = X(...)` inside a loop | Use `tmp_mesh` local variable | §4c |
| `np.concatenate([])` crash | Empty-concat guard | §4d |
| `range(float_param)` | `range(int(...))` | §3b |
| `locals()['param_%d' % i]` | Collect into a list at top of `__init__` | §3c |
| `size[0]`, `offset[1]` in geometry calls | Unpack into named variables | §3a |
| Single-mesh list/concatenate | Direct assignment | §4a |
| Negated rotation conversion | Positive conversion, then explicit flip | §2 |
| 4 copy-pasted bilateral blocks | Direction-table loop | §5a |
| N copy-pasted existence-flag blocks | Data-driven loop | §5b |
| `if/if/if` on single variable | `if/elif/elif` | §7a |
| `else: pass` | Remove, or raise on unexpected value | §7b |
| Post-construction vertex mutation | Constructor `position=`/`rotation=` | §6a |
| Unnamed chained transforms | Named intermediate steps with comments | §6b |
| Undocumented `offset_first`/`rotation_order` | Add a one-line comment | §6c |
| `if/elif` with no `else`, variable used after | Terminal `else: raise` | §4e |
| Zero-vector epsilon hack | `if np.linalg.norm(v) < 1e-8: raise` | §6a |

---

## 10. Editing Workflow

These conventions interact with the three-pass strategy in `edit_plan.md`:

- **Pass 1** fixes should follow all conventions above, but must not change
  class names, parameter names, or signatures. Rename internal variables
  freely; only the external interface is frozen.
- **Pass 2** fixes may change names and signatures. Apply naming conventions
  (§8) and, where the signature change is approved, restructure parameters
  (§3c, flat stride rewrites).
- **Pass 3** consolidates duplicates into `part_template/`. Consolidated
  classes must have the full structured docstring (§1) and follow every
  convention above.

After editing a category:

1. Run `python visualize.py` in `code/<Category>/` to verify geometry.
2. Spot-check the class against this checklist.
3. Commit per-category or per-pass.
