# Template Code Review Notes

---

## Window (3 classes from Window)

### `Symmetrical_Window`
- **Double `vertices_list`/`faces_list`/`total_num_vertices` initialization**: declared at lines 45–48, then immediately re-declared at lines 51–53 — the first set is dead code.
- **`self.frame_mesh` / `self.glass_mesh` overwritten in loop**: both instance attributes are overwritten each iteration; only the last window's meshes survive on the instance.
- **`if/if/if/if/if/if` dispatch on `number_of_window[0]`**: six separate `if` branches (1–6) instead of `if/elif` — all branches always evaluated.
- **Mutates shared `window_size` dicts in-place**: `configuration["window_size"]["glass_offset"][0]` is modified directly (line 219), which mutates the original `window_size` list entries. If the same config is reused, offsets accumulate.
- **Empty-concat crash**: if `number_of_window[0] == 0`, `window_configurations` stays empty, the mesh loop is skipped, and `np.concatenate([])` raises `ValueError`.

### `Asymmetrical_Window`
- **`float` in `range()`**: `range(number_of_window[0])` — `number_of_window[0]` is a float extracted from a param list; raises `TypeError` in Python 3.
- **`self.frame_mesh` / `self.glass_mesh` overwritten in loop**: same as above.
- **Empty-concat crash**: same as above if `number_of_window[0] == 0`.

### `VerticalSlid_Window`
- **`float` in `range()`**: same issue with `range(number_of_window[0])`.
- **`self.frame_mesh` / `self.glass_mesh` overwritten in loop**: same as above.
- **Empty-concat crash**: same as above.

---

## Wheel (3 classes from Lighter, Trashcan)

### `Standard_Wheel` (defined twice — incompatible signatures)
- **Silent class name overwrite**: Lighter defines `Standard_Wheel(self, middle_size, beside_size, ...)` (3 cylinders) and Trashcan redefines `Standard_Wheel(self, size, seperation, ...)` (2 cylinders). Trashcan version silently wins; Lighter's is unreachable.

### `Simplified_Wheel` / `Standard_Wheel` (Trashcan)
- **Single-item concatenate** (`Simplified_Wheel`): only one geometry, still wrapped in list before `np.concatenate`.
- No other significant issues.

---

## Wick (1 class from Lighter)

### `Standard_Wick`
- **Single-item concatenate**: only one geometry, still wrapped in list before `np.concatenate`. No other issues.

---

## Vessel (1 class from Refrigerator)

### `Cuboidal_Vessel`
- No significant issues. Two geometries, standard pattern, clean.

---

## Tray (7 classes from Microwave, Oven, Dishwasher, Refrigerator)

### `Flat_Tray` (defined 3 times — identical signatures and bodies)
- **Silent class name overwrite ×3**: Oven, Dishwasher, and Refrigerator each define `Flat_Tray(self, size, ...)` with identical implementations. The Refrigerator version silently wins; the other two are unreachable dead code.

### `Drawer_Like_Tray` (defined 3 times — identical signatures and bodies)
- **Silent class name overwrite ×3**: same pattern as `Flat_Tray` — Oven, Dishwasher, Refrigerator all define identical `Drawer_Like_Tray`. Refrigerator version wins.

### `Cylindrical_Tray`
- **Single-item concatenate**: only one geometry, still wrapped in list before `np.concatenate`. No other issues.

---

## Switch (17 classes from Switch, Faucet)

### `Round_Switch`
- **`locals()` hack**: uses `locals()['offset_%d'%(i+1)]` to fetch `offset_1`…`offset_4` by name — fragile, breaks static analysis.
- **`self.base_mesh` overwritten in loop**: only last switch mesh survives on instance.
- **Empty-concat crash**: if `number_of_switch[0] == 0`, loop body never runs and `np.concatenate([])` raises `ValueError`.
- **`offset_first=True`** non-default global transform flag.

### `FlipX_Switch` / `FlipY_Switch`
- **`self.mesh` overwritten in loop**: same pattern.
- **Empty-concat crash**: same.
- **`offset_first=True`** non-default flag.

### `Lever_Switch` (Switch source)
- **`self.base_mesh` / `self.main_mesh` overwritten in loop**.
- **Pre-transform on `self.main_mesh.vertices`**: two sequential `apply_transformation` calls on vertices directly instead of using constructor args.
- **Empty-concat crash**: same.
- **`offset_first=True`** non-default flag.

### `Lever_Switch` (Faucet source — defined twice, incompatible signatures)
- **Silent class name overwrite**: Switch source defines `Lever_Switch(self, number_of_switch, base_size, main_size, ...)` and Faucet redefines `Lever_Switch(self, size, R, position0, position1, position2, ...)`. Faucet version wins.
- **Epsilon hack**: `if vector[i] <= 0.00001: vector[i] += 0.00001` — same fragile zero-vector guard seen in Spout classes.
- **Pre-transform on mesh vertices**: `apply_transformation` called on `tmp_mesh.vertices` directly.
- **`rotation_order="YXZ", offset_first=True`** non-default flags.

### `SimplifiedZ_Switch` / `Knob_Switch` / `HandleY_Switch` / `HandleZ_Switch` / `TShaped_Switch` / `Cuboidal_Switch` / `RegularY_Switch` / `RegularX_Switch` / `RegularZ_Switch` / `RotaryX_Switch` / `RotaryY_Switch` / `RotaryZ_Switch` (all Faucet)
- **`rotation_order="YXZ", offset_first=True`** on all — non-default flags used consistently within Faucet classes but inconsistent with Switch-source classes in the same file.
- **`RegularY_Switch` / `RegularX_Switch`**: negated rotation conversion (`[-x / 180 * np.pi ...]`) for `rotation_X`, `rotation_Y`, `rotation_Z`, `sub_rotation` — same sign-negation-at-conversion pattern seen in `Cuboidal_Spout`.
- **`RegularZ_Switch`**: uses positive conversion (no negation) for the same params — inconsistent with `RegularY_Switch` and `RegularX_Switch` siblings.
- **`RotaryX_Switch`**: `existences = [existence_of_switch[0] * -1, existence_of_switch[1]]` — first existence flag is negated, second is not; asymmetric treatment of the two switches.
- **`TShaped_Switch`**: `self.tmp_mesh` overwritten 3 times (unrolled loop, not a real loop overwrite, but instance attribute still only holds last mesh).
- **Pre-transform on mesh vertices** throughout `RegularY_Switch`, `RegularX_Switch`, `RegularZ_Switch`, `Cuboidal_Switch`.
- **Empty-concat crash** possible in `RotaryX_Switch` if both `existence_of_switch` values are 0.

---

## Support (4 classes from Chair, Refrigerator, Faucet)

### `CuboidalRear_Support`
- **`support_rotation` converted before `rotation`**: `support_rotation` is converted degrees→radians at the top, but `rotation` is converted on the next line — inconsistent ordering vs other classes (minor style issue, functionally fine).
- **Pre-transform on `self.mesh.vertices`**: positions computed via `apply_transformation(self.mesh.vertices, ...)` directly instead of passing `position=`/`rotation=` to the geometry constructor. Breaks the standard pattern.
- **`self.mesh` overwritten in loop**: loop over `num_of_support` iterations overwrites `self.mesh` each time; only the last mesh survives on the instance.

### `Cuboidal_Support`
- **`self.mesh` overwritten in loop**: same pattern as above.

### `Trifold_Support`
- **`self.mesh_tmp` overwritten in loop**: iterates over 3 support arms, overwrites `self.mesh_tmp` each iteration.
- **Empty-concat crash**: if all `has_*` existence flags are False, `vertices_list` / `faces_list` remain empty and `np.concatenate([])` raises `ValueError`.

### `Regular_Support`
- No significant issues beyond single-item concatenate (only one geometry added unconditionally).

---

## Spout (8 classes from Kettle, Faucet)

### `Straight_Spout`
- **`locals()` hack**: iterates `for i in range(int(num_of_spout[0]))` and fetches `locals()['spout_%d_length'%(i+1)]` etc. — fragile, non-obvious, breaks static analysis.
- **`self.mesh` overwritten in loop**: only last spout mesh survives on instance.

### `Curved_Spout` (defined twice — incompatible signatures)
- **Silent class name overwrite**: Kettle defines `Curved_Spout(self, size, spout_rotation, ...)` and Faucet redefines `Curved_Spout(self, main_part_params, head_params, ...)`. The Faucet version silently wins; Kettle's version is unreachable.

### `Trifold_Spout` / `ShowerRose_Spout` / `Quadfold_Spout` (Faucet classes)
- **Epsilon hack**: `vector[i] += 0.00001` added to prevent zero-length vectors in Rodrigues rotation. Fragile workaround; should guard with a proper zero-vector check.
- **Pre-transform on mesh vertices**: `apply_transformation` called on `self.mesh.vertices` directly instead of using constructor args.
- **`Quadfold_Spout` extra sign flip**: adds `tmp_rotation[0] *= -1` when `vector[2] <= 0`, absent from `Trifold_Spout` and `ShowerRose_Spout` — inconsistent sibling behavior, likely a bug in one of them.

### `Cuboidal_Spout`
- **Negated rotation at conversion**: `rotation_mainpart = [-x / 180 * np.pi for x in rotation_mainpart]` — negates during conversion, unlike every other class. Intentional or copy-paste error unclear.
- **Pre-transform on mesh vertices**.

### `Cylindrical_Spout`
- **Negated `head_offset[1]`**: uses `-head_offset[1]` for the head mesh Y position, while `Cuboidal_Spout` uses `head_offset[1]` (positive). Inconsistent sign convention between sibling classes.

---

## Sphere (1 class from Lamp)

### `Standard_Sphere`
- **Single-item concatenate**: `np.concatenate([vertices_list])` / `np.concatenate([faces_list])` where each list contains exactly one array — unnecessary overhead, no functional bug.

---

## Shell (2 classes from Trashcan)

### `Cylindrical_Shell` / `Cuboidal_Shell`
- **Single-item concatenate**: both classes build exactly one geometry and still wrap it in `vertices_list`/`faces_list` before `np.concatenate` — unnecessary overhead, no functional bug.

---

## Shaft (6 classes from Ruler, Scissors, Pliers)

| # | Issue | Where |
|---|---|---|
| 1 | **`Regular_shaft` — single-item `np.concatenate`** — one mesh, full list/concatenate boilerplate is unnecessary. | `Regular_shaft` |
| 2 | **`Cuboidal_Shaft` / `Double_Cuboidal_Shaft` — `left_mesh_position` uninitialized if `up_down_relationship[0]` is neither 0 nor 1** — both classes use `if/elif` with no `else`. If the value is anything other than 0 or 1, `left_mesh_position` (and `right_mesh_position`) are undefined, causing `UnboundLocalError`. | `Cuboidal_Shaft`, `Double_Cuboidal_Shaft` |
| 3 | **`Double_Cuboidal_Shaft` — `left_front_mesh_position` / `right_front_mesh_position` uninitialized** — same `if/elif` without `else` for the front-mesh position blocks. | `Double_Cuboidal_Shaft` |
| 4 | **`Round_Shaft` — `self.mesh` overwritten** — the outer `Cylinder` is assigned to `self.mesh`; if `has_central_shaft[0] == 1`, `self.mesh` is reassigned to the central shaft, losing the reference to the outer cylinder. | `Round_Shaft` |
| 5 | **`Rectangular_Shaft` — `layer_3_mesh_position` uses `layer_2_size[1]` as Y base** — the layer-3 Y position is `layer_2_size[1] + layer_3_size[1] / 2`, which assumes layer 2 starts at Y=0. But layer 2 is placed at `layer_2_size[1] / 2`, so layer 3 should be at `layer_2_size[1] + layer_2_size[1] / 2 + layer_3_size[1] / 2` or similar. The current formula likely misaligns layer 3. | `Rectangular_Shaft`, line ~448 |
| 6 | **`Rectangular_Shaft` — `locals()` style avoided but fixed 3-layer cap** — accepts `layer_1/2/3_size` as separate params with `num_layers` controlling which are used. Same structural issue as `Press_Nozzle` but without the `locals()` hack; still limited to exactly 3 layers. | `Rectangular_Shaft` |

---

## Seat (2 classes from Chair)

| # | Issue | Where |
|---|---|---|
| 1 | **Both classes — single-item `np.concatenate`** — one mesh each, full list/concatenate boilerplate is unnecessary. | `Regular_seat`, `Round_seat` |
| 2 | **`Round_seat` — unpacks `size` into named attributes but `Regular_seat` does not** — `Round_seat` stores `self.radius = size[0]` and `self.height = size[1]`, while `Regular_seat` stores `self.size = size`. Inconsistent convention within the same file. | `Round_seat` vs `Regular_seat` |

---

## Screen (3 classes from Display, Laptop)

| # | Issue | Where |
|---|---|---|
| 1 | **`Regular_Screen` — single-item `np.concatenate`** — one mesh, full list/concatenate boilerplate is unnecessary. | `Regular_Screen` |
---

## Ruler (2 classes from Ruler)

| # | Issue | Where |
|---|---|---|
| 1 | **`Asymmetrical_body` — inconsistent sign in `mesh_2_position` Y formula** — `mesh_2_position[1]` uses `right_size[0] / 2 * np.sin(-body_rotation[0])` (negated angle) while `mesh_1_position[1]` uses `-left_size[0] / 2 * np.sin(body_rotation[0])` (negated coefficient). Both are mathematically equivalent (`sin(-x) == -sin(x)`), but the inconsistent form makes the symmetry hard to verify. | `Asymmetrical_body`, lines ~91–100 |
| 2 | **`separation` stored with inline comment `# offset[0]`** — the comment suggests `separation` is actually an offset parameter, implying a naming inconsistency with the original source. | Both classes |

---

## Refill (1 class from Pen)

| # | Issue | Where |
|---|---|---|
| 1 | **`np.concatenate` called twice** — `self.vertices` and `self.faces` are first concatenated at line 44–45 (only the main cylinder), then the `bottom_mesh` and `tip_mesh` are appended to `vertices_list`/`faces_list`, and `np.concatenate` is called again at lines 71–72. The first concatenate is dead — its result is immediately overwritten. Only the second concatenate produces the correct full mesh. | `Cylindrical_Refill`, lines 44–45 vs 71–72 |
| 2 | **`tip_mesh_rotation = [0, 0, np.pi]`** — a 180° Z-rotation on a `Cone` is a no-op for a symmetric cone. Likely a copy-paste artifact. | `Cylindrical_Refill`, line 63 |

---

## Rack (2 classes from Foldingrack)

| # | Issue | Where |
|---|---|---|
| 1 | **`apply_transformation` used to compute mesh center position** — `mesh_1_position = apply_transformation([size[0]/2, -size[1]/2, 0], position=[0,0,0], rotation=mesh_1_rotation)` calls the global transform utility purely to rotate a local offset vector. This is an unconventional use of `apply_transformation` as a vector-rotation helper; `adjust_position_from_rotation` is the library's intended utility for this purpose. | Both classes, position computation |
| 2 | **`Curved_rack` — potential negative Ring inner radius** — `Ring(..., edge_radius[0] - size[0], ...)` produces a negative inner radius if `size[0] >= edge_radius[0]`. No guard. Same issue as `Regular_hook`. | `Curved_rack`, lines ~105, ~114 |

---

## Plug (3 classes from Switch)

| # | Issue | Where |
|---|---|---|
| 1 | **`Cuboidal_Plug` — trailing comma makes `mesh_position` a tuple** — line 45 has `mesh_position = [...],` with a trailing comma, making it a 1-tuple containing a list instead of a plain list. `Cuboid(position=mesh_position)` receives a tuple, which may cause unexpected behavior depending on how the constructor unpacks it. | `Cuboidal_Plug`, line 45 |
| 2 | **`self.mesh` overwritten every iteration** — both `Cuboidal_Plug` and `Cylindrical_Plug` reassign `self.mesh` in the nested loop; only the last contact survives. | `Cuboidal_Plug`, `Cylindrical_Plug` |
| 3 | **`Standard_Plug` — `self.mesh` overwritten 3 times** — three sequential Cuboid constructions all assigned to `self.mesh`; only the third survives. | `Standard_Plug` |
| 4 | **`Standard_Plug` — 3-pin layout fully unrolled** — center, left-offset, and right-offset pins are three separate blocks with copy-pasted position/rotation formulas. Only the X-sign of `sub_offset[0]` and the sign of `plug_rotation[1]` differ. | `Standard_Plug` |

---

## Panel (1 class from StorageFurniture)

| # | Issue | Where |
|---|---|---|
| 1 | **`self.mesh` overwritten every iteration** — only the last panel's mesh survives on the instance. | `Regular_front_panel` |
| 2 | **`number_of_frontPanel` float in `range()`** — `number_of_frontPanel[0]` is extracted from a params list and may be a float; `range(float)` raises `TypeError` in Python 3. | `Regular_front_panel`, lines 30–31, 38 |

---

## Nozzle (6 classes from Dispenser, Shampoo, Lighter)

| # | Issue | Where |
|---|---|---|
| 1 | **`locals()` hack** — `locals()['level_' + str(i+1) + '_size']` used to iterate over `level_1_size` … `level_5_size` instead of accepting a list. Same anti-pattern as `Button`/`Burner`/`Standard_Cover`. | `Press_Nozzle`, lines ~49–58 |
| 2 | **`self.mesh` / `self.nozzle_mesh` overwritten in loop / conditional** — `self.mesh` is reassigned each iteration of the level loop; `self.nozzle_mesh` is reassigned if `num_nozzles[0] == 2`, so only the second nozzle survives on the instance. | `Press_Nozzle` |
| 3 | **`num_of_nozzle == 2` compares list to int — always False** — `num_of_nozzle` is a list (e.g. `[2]`), so `num_of_nozzle == 2` is never `True`. The second nozzle segment is dead code. The correct check is `num_of_nozzle[0] == 2`, consistent with every other existence/count check in the library. | `Regular_nozzle`, line 261 |
| 4 | **`other_nozzle_mesh` uses `nozzle_length[0]` for its size — likely bug** — even if the condition were fixed, `Cuboid(..., nozzle_length[0], ...)` at line 266 uses the first nozzle's length instead of `nozzle_length[1]` for the second segment. | `Regular_nozzle`, line 266 |
| 5 | **Pre-transform on `nozzle_mesh.vertices`** — `apply_transformation` is called directly on `self.nozzle_mesh.vertices` (and `self.other_nozzle_mesh.vertices`) to apply Y-rotation, bypassing the constructor `rotation=` argument. | `Regular_nozzle`, lines 256, 267 |
| 6 | **Dead `else: pass`** — the `else` branch of the `num_of_nozzle == 2` check is an explicit `pass` with no comment. | `Regular_nozzle`, lines 271–272 |
| 7 | **`self.part_mesh` overwritten every iteration** — only the last part's mesh survives on the instance. | `Regular_nozzle` |
| 8 | **`Spray_Nozzle` — `top_offset_y` mixes `tan` and `sin`** — `top_offset_y = -top_offset[0] * np.tan(top_rotation[0])` is then added to `top_offset[0] * np.sin(top_rotation[0])` in the Y position. The combination of `tan` and `sin` for the same offset is geometrically inconsistent; one of the two is likely wrong. | `Spray_Nozzle`, lines 152–156 |
| 9 | **Inconsistent global transform flags across 6 classes** — `Press_Nozzle` and `Spray_Nozzle` use `rotation_order='YXZ'`; `Regular_nozzle` uses `rotation_order="YXZ", offset_first=True`; `Cuboidal_Nozzle`, `Cambered_Nozzle`, `Enveloping_Nozzle` use the default. Three different conventions with no explanation. | All 6 classes |
| 10 | **`Enveloping_Nozzle` — single-item `np.concatenate`** — one mesh, full list/concatenate boilerplate is unnecessary. | `Enveloping_Nozzle` |

---

## Magazine (2 classes from Stapler)

| # | Issue | Where |
|---|---|---|
| 1 | **`behind_mesh` placed at `bottom_mesh_position` — copy-paste bug** — `behind_mesh_position` is computed on lines 106–110 (`[0, size[1]/2, thickness[0]/2]`) but the `Cuboid` constructor at line 112 passes `bottom_mesh_position` (`[0, thickness[0]/2, size[2]/2]`) instead. The rear wall is positioned at the bottom's Z coordinate rather than its own, producing a misplaced panel that overlaps the floor of the magazine. | `Complex_Magazine`, line 112 |
| 2 | **`Carved_Magazine` — redundant `rotation=[0,0,np.pi]`** — both `top_mesh` and `bottom_mesh` are constructed with a 180° Z-rotation. For a symmetric `Cuboid` / `Rectangular_Ring` this rotation is a geometric no-op. The redundant constant adds noise and suggests a misunderstanding of the primitive's orientation. | `Carved_Magazine`, lines 42, 55 |

---

## Leg (22 classes from Safe, Box, Oven, Chair, Dishwasher, StorageFurniture, Table, Eyeglasses, Refrigerator)

| # | Issue | Where |
|---|---|---|
| 1 | **`Cuboidal_Leg` ×2 (Safe, Box) — byte-for-byte identical** — Box version wins. | Safe, Box sources |
| 2 | **`Multilevel_Leg` ×3 with incompatible signatures** — Oven and Refrigerator define `Multilevel_Leg` with the same 4-parameter signature (`front_legs_size/rear_legs_size/legs_separation/num_legs`) and body as `Cuboidal_Leg`. Dishwasher defines a genuinely different class with `has_top_part/top_size/top_bottom_offset` extras. Refrigerator's simpler version (last definition) silently replaces Dishwasher's richer version, dropping the optional top-part support entirely for any caller using the Dishwasher-extended signature. | Oven (~line 310), Dishwasher (~line 999), Refrigerator (~line 2183) |
| 3 | **`Regular_leg` ×2 (Chair, Table) — different signatures** — Chair version has 8 params; Table version has 9 params (adds `additional_legs_params`). Table version wins; Chair callers lose the class. | Chair (~line 456), Table (~line 1221) |
| 4 | **`Regular_leg` — `if` instead of `if/elif` for num-legs dispatch** — all 4 `if number_of_legs[0] ==` branches are independent `if` statements inside the loop, so each iteration evaluates all 4 conditions. For `num_legs == 3`, the loop runs 3 times; iterations 0 and 1 match the `if num_legs == 3` block, but iteration 2 also tries all 4 `if` statements before reaching the matching branch. Should be `if/elif/elif/elif`. | Both `Regular_leg` versions |
| 5 | **`Regular_leg` (Table) — rear-leg Y-position uses `front_legs_size[1]` instead of `rear_legs_size[1]`** — in the 4-leg case (line ~1309), `mesh_position[1]` for rear legs is `-front_legs_size[1] / 2 * np.cos(rear_rotation[0])...`. The same block uses `rear_legs_size[0]` and `rear_legs_size[2]` for X/Z dimensions, so using `front_legs_size[1]` for the Y half-extent is likely a copy-paste bug that makes rear legs float at the wrong height. | `Regular_leg` (Table source), 4-leg rear block |
| 6 | **`Regular_with_splat_leg` / `Regular_leg_with_splat` — rear bridging bar uses `front_rotation[1]`** — in the computation for the rear front-to-rear bridging bar (existance index 1), `np.sin(front_rotation[1])` is used where `rear_rotation[1]` would be consistent with the rear leg parameters. | Both splat classes, rear bar block |
| 7 | **`bridging_bars_existance` typo** — `existance` should be `existence`. Appears in both Chair `Regular_leg_with_splat` and Table `Regular_with_splat_leg`. | Both splat classes |
| 8 | **`self.mesh` overwritten every iteration** — all classes that build legs in a loop assign `self.mesh` on each iteration; only the last survives. | All loop-based leg classes |
| 9 | **`Star_leg` (Chair) — four sequential Rodrigues matrix pre-transforms on mesh vertices** — `tilt_mat`, `sub_mat`, `cen_mat4`, `h_mat4` are applied sequentially to `self.mesh.vertices` via `np.matmul`, then `apply_transformation` for the position. Four chained in-place transforms with no intermediate variable names explaining the order. | `Star_leg` (Chair source) |
| 10 | **`Enclosed_leg`, `Regular_sublayer`, `Regular_leg` (Table) — `number_of_additional_*` float in `range()`** — the count extracted from the flat params list is a float (e.g. `additional_legs_params[0]`), and `range(float)` raises `TypeError` in Python 3. | `Enclosed_leg`, `Regular_sublayer`, `Cylindrical_sublayer`, `Regular_leg` (Table), `Regular_with_splat_leg` |
| 11 | **Opaque radian-conversion one-liner for `additional_*_params`** — `[x / 180 * np.pi if ((i > 1) and ((i - 1) % 9 in [6, 7, 8])) else x ...]` uses magic numbers 9, 6, 7, 8 with no comment. The intent is to convert every 7th/8th/9th field in a stride-9 block to radians, but this is completely opaque to future readers. | `Regular_sublayer`, `Cylindrical_sublayer`, `Enclosed_leg`, `Regular_leg` (Table), `Regular_with_splat_leg` |
| 12 | **`Regular_sublayer` subtracts global `position` from additional-layer positions; `Cylindrical_sublayer` does not** — in `Regular_sublayer` the additional mesh position is `[attrs[3] - position[0], ..., attrs[5] - position[2]]`, but `Cylindrical_sublayer` uses `[attrs[3], attrs[4], attrs[5]]` without subtracting `position`. The two classes have different coordinate semantics for the same parameter. | `Regular_sublayer` line ~54, `Cylindrical_sublayer` line ~114 |
| 13 | **`Cuboidal_Leg` / Oven `Multilevel_Leg` — empty-concat crash** — if `num_legs[0]` is not 1, 2, 3, or 4, no branch fires and `vertices_list` is empty. | `Cuboidal_Leg`, `Multilevel_Leg` (Oven/Refrigerator) |

---

## Lid (1 class from Bottle)

| # | Issue | Where |
|---|---|---|
| 1 | **Opaque `middle_radius` formula** — `outer_size[1] * (1 - inner_size[2] / outer_size[2]) + outer_size[0] * inner_size[2] / outer_size[2]` is a linear interpolation between `outer_size[1]` (outer bottom radius) and `outer_size[0]` (outer top radius) by the fraction `inner_size[2] / outer_size[2]`, but there is no comment explaining the geometric intent. | `Cylindrical_Lid`, line ~37 |

---

## Lever (1 class from Clip)

| # | Issue | Where |
|---|---|---|
| 1 | **`level_` prefix throughout — likely `lever_` typo** — all parameters and mesh names use `level_` (`level_support_size`, `level_handle_rotation`, etc.) instead of the semantically correct `lever_`, inconsistent with `self.semantic = 'Lever'`. | `Regular_lever`, all param names |
| 2 | **Non-default global transform flags** — uses `rotation_order="YXZ", offset_first=True` with no comment explaining why this class differs from the library default. | `Regular_lever`, line ~79 |

---

## Layer (2 classes from Table)

| # | Issue | Where |
|---|---|---|
| 1 | **`self.mesh` / `self.additional_mesh` overwritten every iteration** — both loop bodies assign the same attribute name; only the last iteration's mesh survives on the instance. | Both classes |
| 2 | **Opaque radian-conversion one-liner** — same stride-9 magic-number comprehension as in Leg templates. | Both classes, `__init__` |
| 3 | **`Regular_sublayer` subtracts `position` from additional-layer coordinates; `Cylindrical_sublayer` does not** — same inconsistency as in Leg (`Regular_sublayer` line ~54 subtracts `position[0/1/2]`, `Cylindrical_sublayer` line ~114 does not). | `Regular_sublayer` vs `Cylindrical_sublayer` |
| 4 | **`number_of_additional_sublayers` float in `range()`** — `additional_sublayers_params[0]` is a float; `range(float)` raises `TypeError` in Python 3. | Both classes, second loop |
| 5 | **Empty-concat crash** — if `number_of_subs[0] == 0` and `number_of_additional_sublayers == 0`, both loops are skipped and `np.concatenate([])` crashes. | Both classes |

---

## Knob (1 class from Switch)

| # | Issue | Where |
|---|---|---|
| 1 | **Single-item `np.concatenate`** — one mesh, full list/concatenate boilerplate is unnecessary. | `Standard_Knob` |
| 2 | **`offset_first=True` undocumented** — global transform uses `apply_transformation(..., offset_first=True)`, the non-default flag, with no comment. Most other classes use the default. | `Standard_Knob`, line ~49 |

---

## Jaw (2 classes from Clip)

| # | Issue | Where |
|---|---|---|
| 1 | **`Regular_jaw` — position applied via constructor but rotation bypassed via direct vertex mutation** — `Cuboid` is constructed with `position=mesh_*_position`, correctly placing the mesh. Then `apply_transformation(mesh.vertices, [0,0,0], mesh_*_rotation)` applies only rotation around the global origin, not the mesh center. This is an intentional pivot-rotation design (jaw rotates around z=0) but uses the pre-transform anti-pattern without comment. | `Regular_jaw` |
| 2 | **Both classes — non-default global transform flags** — `rotation_order="YXZ", offset_first=True` with no explanation. | Both classes, line ~63 and ~115 |
| 3 | **`Curved_jaw` — mesh-level Rodrigues matrix application** — uses `get_rodrigues_matrix` directly with a manual matrix multiply `(vertices - pivot) @ R.T + pivot` to rotate around a specific pivot point. Justified for pivot rotation but makes the code much harder to follow. | `Curved_jaw`, lines ~95–97 |

---

## Hook (1 class from Foldingrack)

| # | Issue | Where |
|---|---|---|
| 1 | **Potential negative Ring inner radius** — `Ring` is constructed with inner radius `circle_radius[0] - middle_size[1]`. If `middle_size[1] >= circle_radius[0]` the inner radius is zero or negative. No guard or assertion. | `Regular_hook`, line ~61 |

---

## Hinge (1 class from Door)

| # | Issue | Where |
|---|---|---|
| 1 | **`existence_of_door` treated as integer by addition** — `range(existence_of_door[0] + existence_of_door[1])` adds two booleans to get 0, 1, or 2. Works in Python but is non-idiomatic; a filtered list would be clearer. | `Standard_Hinge`, line ~42 |
| 2 | **`self.tmp_mesh` overwritten every inner-loop iteration** — only the last hinge survives on the instance. | `Standard_Hinge` |
| 3 | **Empty-concat crash** — if both `existence_of_door` values are 0, the outer `range(0)` produces no iterations, `vertices_list` is empty and `np.concatenate([])` crashes. | `Standard_Hinge` |
| 4 | **`sum(separation[0:i])` — no bounds check on `separation`** — for `number_of_hinge[0] = n`, the inner loop accesses `separation[0]` through `separation[n-2]`. If `separation` has fewer than `n-1` elements, it silently returns a short sum or raises IndexError depending on implementation. | `Standard_Hinge`, line ~46 |

---

## Handle (65 classes from Microwave, Safe, Oven, Dishwasher, KitchenPot, Doorhandle, Kettle, Bucket, Window, Mug, Scissors, Refrigerator, Shaver, Pliers, Door, Knife)

| # | Issue | Where |
|---|---|---|
| 1 | **Massive silent class name overwrite** — the largest instance of the overwrite anti-pattern in the library. `Cuboidal_Handle` is defined ×7 (Microwave/Oven/Dishwasher/Refrigerator identical; Scissors/Window/Knife each distinct); `Trifold_Handle` ×8 (4 identical + Safe + Mug + Kettle + Bucket with at least 3 incompatible signatures); `Trifold_Curve_Handle` ×4 identical; `Curve_Handle` ×4 identical; `Curved_Handle` ×4 (all different); `Round_U_Handle` ×2; `Flat_U_Handle` ×2; `Cylindrical_Handle` ×3 (Kettle, Door complex multi-door logic, Knife trivial); `Ring_Handle` ×2. The last definition in file order wins — callers from earlier sources (especially the Door complex version of `Cylindrical_Handle`) are silently replaced by the simpler Knife version. | Multiple class definitions throughout file |
| 2 | **`Regular_Body` from Shaver has `self.semantic = 'Handle'`** — the class is named `Regular_Body` and belongs to the Shaver category but sets `self.semantic = 'Handle'`, causing it to be categorised into this template file under a misleading name. | `Regular_Body` (Shaver source, line ~3574) |
| 3 | **`Middle_Curved_Handle` — `exist_angle` used as list, not scalar, in curve-offset math** — `exist_angle` is converted to a radians list at the top of `__init__`, but lines ~3964–3967 and ~4039–4042 call `np.cos(exist_angle)` and `np.sin(exist_angle)` on the full list instead of `exist_angle[0]`. This produces array results for `curve_offset_x`/`curve_offset_z` instead of scalars, which then propagate into `middle_offset_x`/`z` and the position vectors, producing incorrect geometry. The `Ring` constructor call one block above correctly uses `exist_angle[0]`. | `Middle_Curved_Handle`, behind-left and behind-right blocks |
| 4 | **`Middle_Curved_Handle` — `curve_offset` block duplicated** — the four-line computation of `curve_offset_x`, `curve_offset_z`, `middle_offset_x`, `middle_offset_z` is copy-pasted verbatim for the behind-left block (~3964) and behind-right block (~4039). The results differ only in how they are signed in the final position vector; the computation itself should be done once before both blocks. | `Middle_Curved_Handle` |
| 5 | **Door handle classes: empty-concat crash** — `LShape_Handle`, `PiShape_Handle`, `Cylindrical_Handle` (Door), and `Spherical_Handle` all reach `np.concatenate(vertices_list)` unconditionally. If both `existence_of_door` elements and both `existence_of_handle` elements are False, `vertices_list` is empty and the concatenate raises `ValueError`. Same root cause as `Standard_Door` and `Fourfold_Cover`. | Lines ~4319, ~4437, ~4560, ~4680 |
| 6 | **Door handle classes: pre-transform on mesh vertices + `self.X_mesh` loop overwrite** — all four Door handle classes (`LShape_Handle`, `PiShape_Handle`, `Cylindrical_Handle`, `Spherical_Handle`) directly mutate `tmp_mesh.vertices` via `apply_transformation` inside the direction-settings loop. `self.base_mesh`, `self.middle_mesh`, `self.top_mesh`, and `self.main_mesh` are re-assigned on each loop iteration, so only the last door/handle direction survives on the instance. | All four Door handle classes |
| 7 | **`PiShape_Handle` — `handle_z_direction` sign convention inverted** — all other three Door handle classes set `handle_z_direction = 1` when `handle == 1` (front, z+). `PiShape_Handle` sets `handle_z_direction = -1` when `handle == 1`. The inversion is undocumented and breaks the consistent sign convention across sibling classes. | `PiShape_Handle`, lines ~4379–4383 |
| 8 | **Scissors source: identical `root_mesh` block copy-pasted 5 times** — `Ring_Handle`, `Half_Ring_Handle`, `Double_Curved_Handle`, `Triple_Curved_Handle`, and `Cuboidal_Handle` (Scissors) each begin with an identical ~15-line block constructing `self.root_mesh` from `root_size` and `root_seperation`. Extracting this into a shared helper would remove ~60 lines of duplication. | All five Scissors handle classes |
| 9 | **`Double_Curved_Handle` / `Triple_Curved_Handle` share identical signatures** — both accept the same 9 parameters; the distinction between "double" and "triple" segments is not visible in the constructor signature and presumably lives in the body. Without a comment or docstring the semantic difference is opaque. | `Double_Curved_Handle`, `Triple_Curved_Handle` |
| 10 | **Window `Cuboidal_Handle` uses a dict param (`windows_size`)** — uniquely across all 54 template files, this class accepts `windows_size` as a dictionary (e.g. `windows_size["size_0"][1]`), not a plain list. `self.handle_mesh`, `self.top_mesh`, `self.bottom_mesh`, and `self.main_mesh` are all overwritten in loops. | `Cuboidal_Handle` (Window source) |
| 11 | **Pliers classes — bilateral 4-segment copy-paste** — `Straight_Handle`, `Rear_Curved_Handle`, `Middle_Curved_Handle`, and `Asymmetric_Straight_Handle` each unroll front-left, behind-left, front-right, behind-right as four separate 15–30 line blocks. Only X-sign, Y-rotation sign, and offset direction differ per side. | All four Pliers handle classes |
| 12 | **`Multideck_Handle` — typo in parameter name** — `beside_seperation` should be `beside_separation`. Consistent within the class but inconsistent with `beside_separation` spelling in sibling classes. | `Multideck_Handle` (Knife source) |
| 13 | **Microwave/Oven/Dishwasher/Refrigerator groups — 4×4 = 16 identical class definitions** — `Cuboidal_Handle`, `Trifold_Handle`, `Trifold_Curve_Handle`, and `Curve_Handle` are defined four times each (once per appliance category) with byte-for-byte identical bodies. The last definition (Refrigerator) wins. 15 definitions are dead code. | Four classes × four categories |

---

## Guard (1 class from Knife)

| # | Issue | Where |
|---|---|---|
| 1 | **Single-item `np.concatenate`** — one mesh, full list/concatenate boilerplate is unnecessary. | `Standard_Guard` |
| 2 | **Cuboid constructed at origin with no position** — unlike nearly every other class, the mesh is built at `[0,0,0]` with no `position=` argument, relying entirely on the global `apply_transformation`. This is internally consistent but diverges from the library convention of centering each sub-mesh at its intended local position before the global transform. | `Standard_Guard` |

---

## Gripper (2 classes from Pliers)

| # | Issue | Where |
|---|---|---|
| 1 | **4-segment fully unrolled copy-paste in `Cusp_Gripper`** — left-front, left-behind, right-front, right-behind each repeat the same 3-step pattern (define local offset → `adjust_position_from_rotation` → `list_add` with separation offset). Only the X-sign and Y-rotation sign differ per segment. A loop over `[(+1, +rot), (+1, -rot), (-1, -rot), (-1, +rot)]` would eliminate ~80 lines. | `Cusp_Gripper` |
| 2 | **Position variable reused for two semantically different values** — e.g. `front_1_mesh_position_1` is first set to the pre-rotation local offset, then immediately reassigned to the rotation-adjusted result of `adjust_position_from_rotation`. The same name represents two different things on consecutive lines. | `Cusp_Gripper` |
| 3 | **`rotation_1 = [np.pi/2, 0, 0]` redeclared 4 times** — identical constant independently assigned for each of the four segments. Should be a single shared local variable. | `Cusp_Gripper` |
| 4 | **`gripper_rotation` converted before `rotation`** — both classes convert `gripper_rotation` to radians on line 25/165 before `rotation` on line 26/166. Every other class converts `rotation` first. Inconsistent ordering with no effect on correctness but breaks the established convention. | Both classes |
| 5 | **`rotation_order='ZYX'` for right mesh only in `Curved_Gripper`** — left mesh uses default rotation order; right mesh explicitly specifies `'ZYX'`. The asymmetric convention between the two mirrored halves is undocumented, making it hard to verify the geometry is correct. | `Curved_Gripper` |

---

## Glasses (4 classes from Eyeglasses)

| # | Issue | Where |
|---|---|---|
| 1 | **Sentinel vertex never removed from mesh** — an extra bookkeeping point is appended to each mesh's vertex array to track its center after rotation, then used to compute the final position offset. The sentinel vertex is never stripped out and gets baked into the final concatenated geometry, producing a spurious dangling vertex in every lens. | All 4 classes |
| 2 | **Pre-transformation on individual mesh vertices** — all classes call `apply_transformation` directly on `self.right/left_mesh.vertices` instead of passing `position=` to the constructor. Same pattern as Cap/Standard_Door/Regular_door. | All 4 classes |
| 3 | **Right/left mesh construction fully unrolled** — both lenses have identical geometry; only the rotation and position signs are negated for the left. The full construction is copy-pasted rather than shared with a `sign` parameter. | All 4 classes |
| 4 | **`right/left_meshes[0]` gets sentinel vertex appended twice in `TrapezoidalFrame_Glasses`** — line 178 appends the sentinel to `right_meshes[0]` before the loop at line 180 which appends it again to every mesh including index 0. Same double-append at lines 258/260 for `left_meshes[0]`. | `TrapezoidalFrame_Glasses` |
| 5 | **`left_meshes` is a byte-for-byte copy of `right_meshes`** — all 4 Cuboid constructions in `left_meshes` (lines 199–256) are identical to `right_meshes` (lines 119–176); the mirror comes only from the subsequent transformation loop. ~57 lines of pure duplication. | `TrapezoidalFrame_Glasses` |
| 6 | **Extremely long opaque inline geometry expressions** — formulas on lines 155, 157, 169, 171, 235, 237, 249, 251 each exceed 100 characters and chain multiple `size[i]`/`width[0]`/`top_offset[0]` terms without intermediate variables or comments. The geometric intent is unverifiable by inspection. | `TrapezoidalFrame_Glasses` |
| 7 | **Magic hardcoded vertex indices** — `Round_Glasses` uses `vertices[3]` and `vertices[259]`; `RoundFrame_Glasses` uses `vertices[1]` and `vertices[513]` to locate lens edge points. These depend entirely on the internal vertex ordering of `Cylinder`/`Ring`. Any change to primitive resolution silently corrupts lens positioning with no error. | `Round_Glasses`, `RoundFrame_Glasses` |
| 8 | **`position` passed as nested list `[[x, y, z]]`** — in `Round_Glasses` and `RoundFrame_Glasses` the second `apply_transformation` call wraps position in an extra list level (e.g. `position=[[-edge[1][0]+interval[0]/2, ...]]`). This is inconsistent with all other call sites where position is `[x, y, z]`. | `Round_Glasses`, `RoundFrame_Glasses` |

---

## Frame (1 class from Window)

| # | Issue | Where |
|---|---|---|
| 1 | **Class name / semantic mismatch** — the class is `Standard_Windowframe` but `self.semantic = 'Frame'`. The class is categorised under the Frame semantic type yet its name signals window-specific context, which will be confusing if Frame templates from other categories are ever added. | `Standard_Windowframe` |
| 2 | **Single-item `np.concatenate`** — one mesh, full list/concatenate boilerplate is unnecessary. | `Standard_Windowframe` |
| 3 | **Negated Y offset passed inline** — `[inner_outer_offset[0], -inner_outer_offset[1]]` negates the Y component silently at the call site with no comment. If a caller passes a positive Y offset intending upward shift, the sign flip is invisible. | `Standard_Windowframe` |

---

## Drawer (2 classes from StorageFurniture, Table)

| # | Issue | Where |
|---|---|---|
| 1 | **`Regular_drawer` defined ×2 with incompatible strides** — StorageFurniture uses stride-20 (no handle rotation), Table uses stride-21 (extra `handle_rotation` at index 14 with radian conversion). Table version wins; StorageFurniture callers get silently misaligned geometry. Same pattern as `Regular_door`. | StorageFurniture, Table |
| 2 | **Flat stride encoding** — same anti-pattern as `Regular_door`/`Regular_cabinet`: all per-drawer data packed into one flat `drawers_params` list, extracted via magic index arithmetic. | Both versions |
| 3 | **`self.mesh` overwritten every iteration** — assigned for each of the 6+ mesh parts per drawer; only the last survives on the instance. | Both versions |
| 4 | **`number_of_handle` used as float in `range()`** — `self.number_of_handle[drawer_idx]` is a raw element from the float `drawers_params` list, and `range(6 + float)` raises `TypeError` in Python 3. Requires either an `int()` cast or storing the value as integer. | Both versions, loop line |
| 5 | **Table version: `handle_offset[0]` used for Y position — likely bug** — line 196 computes handle Y as `drawer_offset[1] + handle_offset[drawer_idx][0]`, reusing the X component of `handle_offset` for the Y axis. StorageFurniture correctly uses `handle_offset[1]` for Y. | Table `Regular_drawer`, handle block |
| 6 | **`position_sign` condition asymmetry** — for sides (mesh_idx 0/1): `mesh_idx == 0` → -1. For front/back (mesh_idx 2/3): `mesh_idx == 3` → -1. The inverted condition (0 vs 3) across two analogous pairs is easy to misread. | Both versions |

---

## Doorframe (1 class from Door)

| # | Issue | Where |
|---|---|---|
| 1 | **`front_right_mesh_position` uses `front_left_size[0]` — likely bug** — line 139 places the right panel at `sub1_inner_size[0]/2 + front_left_size[0]/2` instead of `front_right_size[0]/2`. When `sub1_inner_outer_offset[0] != 0`, the two sizes differ and the right panel is both mispositioned and constructed with the wrong dimension. The equivalent `back_right_mesh_position` (line 191) correctly uses `back_right_size[0]`. | `Standard_Doorframe`, front frame block |
| 2 | **`existence_of_doorframe[0]` and `[1]` blocks are near-identical copy-paste** — both blocks compute `_top_size`, `_left_size`, `_right_size` and place 3 Cuboids; the only differences are parameter names (`sub1_*` vs `sub2_*`) and z-sign (`+main_outer_size[2]/2` vs `-main_outer_size[2]/2`). Should be a loop over the two layers. | `Standard_Doorframe` |
| 3 | **13-parameter flat signature with parallel `sub1`/`sub2` groups** — `sub1_outer_size`, `sub1_inner_size`, `sub1_inner_outer_offset`, `sub1_offset` and their `sub2` counterparts are structurally identical groups. Should be a list of sub-frame parameter structs. | `Standard_Doorframe.__init__` |
| 4 | **`main_offset` encodes [x, z] while `sub_offset` encodes [x, y]** — `main_offset[1]` is used as the Z component of positions; `sub1_offset[1]` / `sub2_offset[1]` are used as Y components. The same parameter name "offset" has different axis semantics between the main and sub frames, with no indication in the signature. | `Standard_Doorframe` |

---

## Door (17 classes from Microwave, Safe, Oven, Dishwasher, Washingmachine, Refrigerator, StorageFurniture, Table, Door)

| # | Issue | Where |
|---|---|---|
| 1 | **`Cuboidal_Door` defined ×6** — Microwave, Safe, Oven, Dishwasher, Refrigerator are byte-for-byte identical (position `z=size[2]/2`); Washingmachine differs (`y=size[1]/2, z=0`). Refrigerator's version (last) survives, Washingmachine's distinct convention is silently discarded. | All six sources |
| 2 | **`Sunken_Door` defined ×5** — Microwave, Safe, Oven, Dishwasher, Refrigerator are byte-for-byte identical. Refrigerator wins. Should exist exactly once. | All five sources |
| 3 | **`Regular_door` defined ×2 with incompatible strides** — StorageFurniture uses 12 params per door (rotation at index 8), Table uses 13 params per door (rotation at indices 6 and 9 with an extra `handle_rotation`). Table's version wins; any caller supplying 12-param data will silently receive misaligned geometry. | StorageFurniture, Table |
| 4 | **`self.mesh` overwritten every iteration in both `Regular_door` versions** — the nested loop over `door_idx` and `mesh_idx` reassigns `self.mesh`; only the last panel survives on the instance. | Both `Regular_door` |
| 5 | **Flat stride encoding in `Regular_door`** — same anti-pattern as `Regular_cabinet` and `Storagefurniture_body`; magic stride (12 or 13) and magic rotation indices selected by `i % stride in [...]`. | Both `Regular_door` |
| 6 | **`Standard_Door`: potential `np.concatenate([])` crash** — if both `existence_of_door[0]` and `existence_of_door[1]` are falsy, `vertices_list` stays empty and `np.concatenate([])` raises. | `Standard_Door` |
| 7 | **`Standard_Door`: pre-transformation on individual mesh vertices** — both door panels call `apply_transformation` directly on `self.left/right_mesh.vertices`, same inconsistent pattern as USB Cap classes. | `Standard_Door` |
| 8 | **`Standard_Door`: pivot position changes silently with door count** — when both doors exist the pivot offsets are `±size[0]`; when only one door exists the offset halves to `±size[0]/2`. The change is undocumented and makes the single-door geometry inconsistent with the double-door geometry. | `Standard_Door` |
| 9 | **Backslash line continuation in `Cuboidal_Door`** (Microwave, line 51) — `apply_transformation(...)\` uses a trailing backslash instead of parentheses for line continuation. Fragile: any accidental trailing space after the backslash causes a SyntaxError. | `Cuboidal_Door` (Microwave) |
| 10 | **`Roller_Door`: two rings share identical position/rotation computed separately** — `circle_mesh_position` and `middle_mesh_position` are both `[circle_size[0], 0, circle_size[2]/2]`; both rotations are also `[np.pi/2, 0, 0]`. Should be extracted to a shared variable. | `Roller_Door` |

---

## Dial (1 class from Safe)

| # | Issue | Where |
|---|---|---|
| 1 | **Asymmetric parameter structure** — `bottom_size` has 3 elements (top radius, bottom radius, length) allowing a tapered bottom cylinder, while `top_size` has only 2 elements (radius, length) with no taper option. The two parts cannot both be tapered without changing the API. | `Cylindrical_Dial` |
| 2 | **Duplicate hardcoded rotation** — both bottom and top meshes independently define `rotation = [-np.pi / 2, 0, 0]`. Could be one shared local variable. | `Cylindrical_Dial` |
| 3 | **Z-axis alignment via rotation trick is undocumented** — cylinders are rotated `-π/2` around X to lie along the Z-axis, and all positions are expressed in Z. No comment explains this coordinate choice. | `Cylindrical_Dial` |

---

## Cylinder (2 classes from Bucket, Mug)

| # | Issue | Where |
|---|---|---|
| 1 | **`Single_Cylinder` defined ×2 — byte-for-byte identical** — Bucket and Mug both define the exact same class with the same body. The second definition silently overwrites the first. Should exist exactly once. | Bucket, Mug |
| 2 | **Single-item `np.concatenate`** — one mesh, no need for the list/concatenate boilerplate. | Both definitions |

---

## Cover (19 classes from Box, Gluestick, Stapler, Dishwasher, KitchenPot, Kettle, Lighter, Trashcan)

| # | Issue | Where |
|---|---|---|
| 1 | **`Cylindrical_Cover` defined ×3** — Gluestick (2-part Ring+Cylinder), KitchenPot (single Cylinder), Trashcan (single Cylinder, same as KitchenPot). Three different implementations under the same name; Python silently keeps Trashcan's, discarding the more complex Gluestick version entirely. | Gluestick, KitchenPot, Trashcan |
| 2 | **`Regular_Cover` defined ×2** — Box and Lighter versions are structurally identical except the z-offset sign flips from `+outer_size[2]/2` to `-outer_size[2]/2`. Lighter's version silently overwrites Box's. | Box, Lighter |
| 3 | **`Carved_Cover` (Stapler) is structurally identical to `Regular_Cover` (Box)** — same two-part geometry (top Cuboid + bottom Rectangular_Ring), same formulas, same parameter names. Only the class name and z-offset differ. Should share an implementation. | `Carved_Cover`, `Regular_Cover` |
| 4 | **`Fourfold_Cover`: 4 explicit copy-paste `if` blocks instead of a loop** — front, back, left, right panels each get their own block with the same mesh construction; only the axis sign and rotation index change. A loop over `[(idx, axis_sign, rot_axis)]` would eliminate the duplication. | `Fourfold_Cover` |
| 5 | **`self.mesh` overwritten across all 4 conditionals in `Fourfold_Cover`** — all four panels assign to `self.mesh`; only the last enabled panel survives on the instance. | `Fourfold_Cover` |
| 6 | **Potential `np.concatenate([])` crash in `Fourfold_Cover`** — if all 4 `has_cover` flags are 0, `vertices_list` is empty and `np.concatenate([])` will raise. | `Fourfold_Cover` |
| 7 | **`Holed_Cuboidal_Cover`: front/behind blocks are copy-paste (z-sign flip only), left/right blocks are copy-paste (x-sign flip only)** — ~140 lines of near-identical code across 4 side panels. Should be a loop over 4 directions. | `Holed_Cuboidal_Cover` |
| 8 | **`self.mesh`, `self.mesh_1/2/3` overwritten in all 4 side blocks of `Holed_Cuboidal_Cover`** — all four sides assign to the same instance names; only the final set survives. | `Holed_Cuboidal_Cover` |
| 9 | **`locals()` hack + `self.knob_mesh` loop overwrite in `Standard_Cover`** — `knob_%d_size` lookup for up to 5 knobs; same anti-pattern as Burner/Button. `self.knob_mesh` also only retains the last knob. | `Standard_Cover` |
| 10 | **`height` parameter with mixed-semantics elements** — `Holed_Cylindrical_Cover` packs 3 distinct height values (cap, ring, side-panel) into one list; `Cuboidal_Cover` packs front and back heights. Neither is self-documenting. | `Holed_Cylindrical_Cover`, `Cuboidal_Cover` |
| 11 | **`self.mesh` loop overwrite in `Holed_Cylindrical_Cover`** — `num_sides` Ring panels all write to `self.mesh`. | `Holed_Cylindrical_Cover` |
| 12 | **Single-item `np.concatenate` in 4 trivial classes** — `Simplified_Cover`, `Cuboidal_Topcover`, `Cylindrical_Cover` (KitchenPot), `Cylindrical_Hollow_Cover` each have one mesh but use the full list/concatenate boilerplate. | Four single-mesh classes |

---

## Controller (1 class from Safe)

| # | Issue | Where |
|---|---|---|
| 1 | **Single-item `np.concatenate`** — only one mesh; list/concatenate boilerplate is unnecessary. | `Regular_Controller` |
| 2 | **`bottom_mesh` name for the only mesh** — there is no top/other mesh, so "bottom" is a misleading residual label. | `Regular_Controller` |

---

## Connector (8 classes from Safe, USB, Eyeglasses, Laptop)

| # | Issue | Where |
|---|---|---|
| 1 | **Typos in class names** — `Cylindrical_Connecter` (Safe, ×2: should be "Connector") and `Simplied_Connector` (USB, should be "Simplified"). Creates confusing naming alongside the correct `Cylindrical_Connector` from Laptop. | `Cylindrical_Connecter`, `T_Shaped_Connecter`, `Simplied_Connector` |
| 2 | **`self.back_mesh` loop variable overwrite** — both Laptop classes assign `self.back_mesh` inside a loop; only the last iteration survives on the instance. Should be a local variable. | `Cuboidal_Connector`, `Cylindrical_Connector` |
| 3 | **`sum(separation[0:i])` with no bounds check** — spacing accumulation silently uses however many elements `separation` contains; no validation that `len(separation) >= number_of_connector[0] - 1`. Under-supplied list gives wrong positions without error. | `Cuboidal_Connector`, `Cylindrical_Connector` |
| 4 | **Potential `np.concatenate([])` crash when `number_of_connector[0] == 0`** — same empty-list crash risk seen in `Board`. No guard on the loop. | `Cuboidal_Connector`, `Cylindrical_Connector` |
| 5 | **`connector_rotation` only uses index `[0]`** — X-axis rotation is applied but Y/Z elements are silently ignored even if provided. | `Cuboidal_Connector` |
| 6 | **Opaque inline offset arithmetic in `Regular_Connector`** — `Rectangular_Ring` is constructed with `size[1] / 2 - thickness[0]` and `[0, thickness[0] / 2 - size[1] / 4]` as inline magic expressions. No comments or intermediate variables explain the geometry derivation. | `Regular_Connector` |
| 7 | **`top_mesh` / `bottom_mesh` naming in `Dual_Connector` is misleading** — the two cuboids are positioned entirely by `offset_1` / `offset_2` and may not be vertically arranged. The names imply a fixed spatial relationship that isn't enforced. | `Dual_Connector` |
| 8 | **Single-item `np.concatenate` in 4 classes** — `Cylindrical_Connecter`, `Simplied_Connector`, `Regular_Connector`, `Standard_Connector` all use the list/concatenate boilerplate for a single mesh. | All four single-mesh classes |

---

## Clip (2 classes from Pen)

| # | Issue | Where |
|---|---|---|
| 1 | **`clip_offset` mixed-semantics list** — `clip_offset[0]` offsets the vertical arm in Y, `clip_offset[1]` offsets the tip in Y. The two elements control different structural parts; a single parameter name gives no indication of this. | `Trifold_Clip` |
| 2 | **Tip position formula is unreadable** — `y = -clip_vertical_size[1] - clip_offset[0] + clip_tip_size[1] / 2 - clip_offset[1]` combines four terms with no intermediate variable or comment explaining the coordinate derivation. | `Trifold_Clip` |
| 3 | **Single-item `np.concatenate`** — `Curved_Clip` appends one mesh to `vertices_list` / `faces_list` and then calls `np.concatenate`. The list/concatenate boilerplate adds no value here; `self.vertices = self.mesh.vertices` would be equivalent. | `Curved_Clip` |

---

## Cap (6 classes from Pen, USB, Shampoo)

| # | Issue | Where |
|---|---|---|
| 1 | **`SquareEnded_Cap` / `RoundEnded_Cap` near-identical duplication** — ~200 lines almost completely duplicated. Only differences: `RoundEnded_Cap` adds two semicircular end cylinders and adjusts the Cuboid depth by `size[0]/2`. Should be one class with an `is_round_ended` flag or subclassing. | `SquareEnded_Cap`, `RoundEnded_Cap` |
| 2 | **`self.rotation = rotation` stores already-converted radians** — both USB classes and `Regular_cap` set `self.rotation = rotation` after the degrees→radians conversion, shadowing the parent's attribute with radians instead of the original degrees. | `SquareEnded_Cap`, `RoundEnded_Cap`, `Regular_cap` |
| 3 | **`shaft_interval` used as raw scalar, not `shaft_interval[0]`** — both USB classes access `shaft_interval` directly (lines 196/207, 341/351) while all other parameters use `[0]` indexing. If `shaft_interval` is passed as a list this silently produces wrong position values. | `SquareEnded_Cap`, `RoundEnded_Cap` |
| 4 | **`c_mesh` pre-transformed via `apply_transformation` on vertices** — the arc ring mesh calls `apply_transformation(self.c_mesh.vertices, c_mesh_position, [0, cap_rotation[0], 0])` directly instead of passing `position=` to the constructor. Inconsistent with all other meshes in the same class. | `SquareEnded_Cap`, `RoundEnded_Cap` |
| 5 | **`self.nozzle_mesh` overwritten (Ring → Cylinder)** — first assignment builds the outer Ring annulus, second builds the inner solid Cylinder. The instance attribute holds only the final Cylinder; the Ring is accessible only through `vertices_list`. | `Cylindrical_cap` |
| 6 | **First Ring in `Cylindrical_cap` has no position** — the outer annulus Ring is placed at origin with no offset, while the inner Cylinder uses `position=[0, inner_size[2]/2, 0]`. These two geometries share no explicit alignment coordinate; geometric correctness depends on implicit centering conventions. | `Cylindrical_cap` |
| 7 | **`separation` parameter declared and stored but never used** — `Regular_cap` accepts `separation` and saves `self.separation = separation`, but the geometry construction only builds a single `Cylinder` without referencing it. Dead parameter. | `Regular_cap` |

---

## Cabinet (`Regular_cabinet`)

| # | Issue | Where |
|---|---|---|
| 1 | **Flat stride-56 encoding** — `cabinets_params` is a flat list with 56 values per cabinet, all extracted via index arithmetic in `__init__`. Same anti-pattern as `Storagefurniture_body` but at larger scale. Should be a list of structured per-cabinet objects. | `Regular_cabinet` |
| 2 | **Selective inline radian conversion on flat list** — `i % 56 in [22, 23, 24, 25, 41, 42, 43, 44]` selects rotation fields by magic position. Same pattern as `Storagefurniture_body`; magic indices are completely opaque without the stride map. | `Regular_cabinet` |
| 3 | **Top and beneath cabinet loops are near-identical copy-paste** — ~170 lines duplicated between `for cabinet_idx in range(self.number_of_top_cabinet)` and `for cabinet_idx in range(self.number_of_beneath_cabinet)`. Should be a single unified loop with an offset parameter. | `Regular_cabinet` |
| 4 | **Index inconsistency bug** — beneath cabinet `cabinet_doors_mesh` / `cabinet_drawers_mesh` use `self.type_of_spaces[cabinet_idx]` and `self.drawer_number_of_handles[cabinet_idx]` instead of `[actual_idx]`. Drawer/door counts for beneath cabinets silently use top-cabinet parameters. | Beneath cabinet loop |
| 5 | **Y-axis adjustment applied only to door handle, not door panel** — line 494's `self.mesh.vertices[:, 1] -= ...` is inside the `else` branch of `for mesh_idx in range(2)`, only adjusting mesh_idx == 1 (handle), not mesh_idx == 0 (door panel). Fragile indentation-dependent logic. | Beneath cabinet door loop |
| 6 | **`door_handles_size` indexed without `cabinet_idx`** — line 328 uses `self.door_handles_size[0]`, `[1]`, `[2]` (flat) while line 488 correctly uses `self.door_handles_size[cabinet_idx][0]` etc. Likely a bug causing wrong handle sizes in top cabinets. | Top cabinet door loop |
| 7 | **Magic constant `- 5`** — `_pos = self.cab_up_down_inner_sizes[...] + _height / 2 - 5` has unexplained hardcoded offset. | Top cabinet layer loop |
| 8 | **`actual_idx = cabinet_idx` in top loop is a no-op** — assigned but equals `cabinet_idx` throughout; serves no purpose in the top loop unlike in the beneath loop. | Top cabinet loop |
| 9 | **`self.mesh` overwritten in every nested loop iteration** — should always be a local variable. | Both loops |
| 10 | **`else: pass` dead branches** — two instances for unrecognized `type_of_spaces` values. | Both loops |
| 11 | **Inconsistent parameter unwrapping** — `number_of_top_cabinet[0]` and `number_of_beneath_cabinet[0]` are unwrapped to scalars on instance, but `number_of_layers` is left as a list and indexed differently. | `__init__` |

---

## Button (8 classes from Microwave, Oven, Pen, Washingmachine, Lighter, Knife)

| # | Issue | Where |
|---|---|---|
| 1 | **`Controller_With_Button` defined ×3** (Microwave, Oven, Washingmachine) — silent overwrite. | All three sources |
| 2 | **`locals()` hack in all 3 `Controller_With_Button` variants** — same anti-pattern confirmed library-wide. Microwave: up to 4 buttons (10 params); Oven: up to 10 buttons (22 params); Washingmachine: up to 8 buttons (18 params). | All three sources |
| 3 | **Oven and Washingmachine `Controller_With_Button` near-identical** — same tilted-panel base geometry and identical loop body; differ only in max button count. Should be one class with a variable-length `button_params` list. | Oven, Washingmachine |
| 4 | **Semantic mismatch** — `Controller_With_Button` is a composite controller panel, but `self.semantic = 'Button'`. Same pattern as `Top_With_Burner`/`'Burner'`. | All three `Controller_With_Button` |
| 5 | **`L_Shaped_Button` and `Double_Cambered_Button` share duplicated base** — identical `bottom_mesh` + `top_mesh` Cuboid construction copy-pasted; `Double_Cambered_Button` only adds the camber cylinders on top. | `L_Shaped_Button`, `Double_Cambered_Button` |
| 6 | **`bottom_cambered_mesh_rotation` and `top_cambered_mesh_rotation` are identical** — both `[0, np.pi, 0]`; could be a single named constant. | `Double_Cambered_Button` |
| 7 | **`beside_radius_z` mixed-semantics list** — `[0]` for bottom camber, `[1]` for top camber; not clearly named. | `Double_Cambered_Button` |
| 8 | **Unnecessary single-mesh list boilerplate** | `Cylindrical_Button`, `Regular_Button` |
| 9 | **Single-element lists as scalars** — `num_buttons[0]`, `top_bottom_offset[0]`, `beside_radius_z[0]`. | Multiple classes |

---

## Burner (`Top_With_Burner`)

| # | Issue | Where |
|---|---|---|
| 1 | **32-argument flat signature — worst in codebase** — 30 numbered params (`burner_1_size` … `burner_6_central_offset`) + `bottom_size` + `num_burners`. Should be `burner_params: list` of per-burner tuples/dicts. | `Top_With_Burner` |
| 2 | **`locals()` hack — 5 lookups per loop iteration** — `locals()['burner_%d_size'%(i+1)]` etc. Same anti-pattern as `Mutiple_Layer_Body`, but more pervasive here. | `Top_With_Burner` |
| 3 | **`self.mesh` and `self.center_mesh` overwritten in loop** — should be local variables. | `Top_With_Burner` |
| 4 | **Semantic mismatch** — class named `Top_With_Burner` (a composite top panel) but `self.semantic = 'Burner'`. The whole panel is classified as a burner part. | `Top_With_Burner` |
| 5 | **`bottom_size` misleading name** — refers to the oven's top surface panel; `top_panel_size` would be clearer. | `Top_With_Burner` |
| 6 | **`num_burners[0]`** — single-element list as scalar. | `Top_With_Burner` |

---

## Bracket (`Semi_Ring_Bracket`, `Tilted_Bracket`, `Enclosed_Bracket`)

| # | Issue | Where |
|---|---|---|
| 1 | **Top/bottom endpoint logic duplicated** — `has_top_endpoint` and `has_bottom_endpoint` blocks are structurally identical with only Y sign flipped; a `flag = ±1` loop would halve the code. | `Semi_Ring_Bracket` |
| 2 | **Boolean-as-integer flags** — `pivot_continuity[0] == 1`, `has_top_endpoint[0] == 1`, `has_bottom_endpoint[0] == 1`. | `Semi_Ring_Bracket` |
| 3 | **Typo: `pivot_seperation`** → `pivot_separation`. | `Semi_Ring_Bracket` |
| 4 | **`bracket_exist_angle` ambiguous naming** — same issue as `exist_angle` in Baffle/Kettle; `arc_angle` or `extent_angle` would be clearer. | `Semi_Ring_Bracket` |
| 5 | **`circle_thickness` mixed-semantics list** — `[0]` is radial thickness, `[1]` is height; name doesn't convey this. | `Tilted_Bracket` |
| 6 | **`self.bracket_mesh` overwritten in conditional** — optional second half-ring clobbers first on instance. | `Enclosed_Bracket` |
| 7 | **`half_circle_number[0] == 2` as count-based switch** — semantically a boolean `has_second_half`; same pattern as `number_of_box` in Base. | `Enclosed_Bracket` |
| 8 | **Two `Ring` calls differ only in rotation** — could be a loop over a list of rotations for `range(half_circle_number[0])`. | `Enclosed_Bracket` |
| 9 | **Single-element lists as scalars** — `pivot_seperation[0]`, `endpoint_radius[0]`, `bracket_offset[0]`, `circle_radius[0]`, etc. | All classes |

---

## Body (51 classes from Microwave, Safe, Box, Gluestick, Stapler, Oven, Dishwasher, StorageFurniture, Pen, USB, KitchenPot, Kettle, Bucket, Table, Mug, Switch, Washingmachine, Dispenser, Shampoo, Lighter, Refrigerator, Bottle, Trashcan)

| # | Issue | Where |
|---|---|---|
| 1 | **Identical duplicate class bodies** — `Cuboidal_Body` defined ×5 (Microwave, Safe, Gluestick, Oven, Dishwasher) with literally the same code; `Double_Layer_Body` ×2 (Oven, Dishwasher); `Cylindrical_Body` ×2 (Gluestick, KitchenPot). Silent last-definition-wins + wasted duplication across source files. | Multiple sources |
| 2 | **`locals()` hack for numbered parameters** — `Mutiple_Layer_Body` uses `locals()['sub_clapboard_%d_size'%(i+1)]` to dynamically retrieve 10 numbered positional params. Anti-pattern; should be two lists. | `Mutiple_Layer_Body` |
| 3 | **20-argument flat signature** — `sub_clapboard_1_size/offset` through `sub_clapboard_10_size/offset` as individual positional params. Should be `sub_clapboard_sizes: list`, `sub_clapboard_offsets: list`. | `Mutiple_Layer_Body` |
| 4 | **Flat stride encoding in `Storagefurniture_body`** — `storagefurniture_layers_params` (stride 5) and `additional_layers_params` (stride 9) are flat lists accessed via index arithmetic. Extremely brittle; should be structured objects. | `Storagefurniture_body` |
| 5 | **Selective inline radian conversion on flat list** — one-liner comprehension with `(i-1) % 9 in [6, 7, 8]` to convert specific stride-positions. Direct consequence of flat encoding. | `Storagefurniture_body` |
| 6 | **Naming inconsistency** — `Storagefurniture_body` uses lowercase `b`; all others use `TitleCase`. | `Storagefurniture_body` |
| 7 | **`elif ... else: pass` dead branch** | `Storagefurniture_body` |
| 8 | **`self.mesh` overwritten repeatedly across multiple loops** — loop variable stored on instance. | `Storagefurniture_body`, `Mutiple_Layer_Body`, `Standard_Body` shaft loop |
| 9 | **Left/right pair unrolled instead of `flag` loop** — shaft cylinders in `Standard_Body`. | `Standard_Body` |
| 10 | **Boolean-as-integer flags** — `has_shaft[0] == 1`, `has_lid[0] == 1`. | `Standard_Body`, `Storagefurniture_body` |
| 11 | **Typos** — "Mutiple" → "Multiple" (`Mutiple_Layer_Body`), "seperation" → "separation" (`beside_seperation` in `Standard_Body`). | Two classes |
| 12 | **Unnecessary single-mesh list boilerplate** | `Flat_Top`, `Cylindrical_Body` (Gluestick), `Toothpaste_Body`, `Cuboidal_Body` (Gluestick), `Cylindrical_Barrel` |
| 13 | **Single-element lists as scalars** — pervasive across all classes. | All classes |
| 14 | **`Cylindrical_Body` — 4 identical definitions** (KitchenPot, Bucket, Mug, Trashcan): same params, same `middle_radius` formula, same Cylinder + Ring construction. Pixel-perfect copies. | 4 sources |
| 15 | **`Prismatic_Body` — duplicate across Bucket and Mug**: identical code in both. | Bucket, Mug |
| 16 | **`Multilevel_Body` — `locals()` hack in 4 more classes** (Kettle, Mug, Dispenser, Bottle) + defined 4 times. Anti-pattern is even more widespread than `Mutiple_Layer_Body`. | Kettle, Mug, Dispenser, Bottle |
| 17 | **`L_type_desktop` — missing `super().__init__()` call**: parent `ConceptTemplate` never initialized; `self.position`/`self.rotation` manually assigned instead. | `L_type_desktop` |
| 18 | **`L_type_desktop` — `np.sqrt(vertical_size[0] ** 2)` is just `abs(vertical_size[0])`**: unnecessarily complex expression. | `L_type_desktop` |
| 19 | **`Front_Facing_Roller_Body` / `Upright_Roller_Body` — near-identical structure**: both build Cuboid + `Box_Cylinder_Ring`, differing only in axis orientation. Same pattern as `UShapedXZ/YZ_Base`. | Washingmachine |
| 20 | **`Standard_Base` (Switch) — `self.back_mesh` overwritten in conditional**: main mesh and optional second part both assigned to same attribute. | `Standard_Base` |
| 21 | **Shampoo naming inconsistency**: `Cylindrical_body`, `Cuboidal_body`, `Toothpaste_body` use lowercase `b`, inconsistent with rest of library. | Shampoo classes |
| 22 | **`Toothpaste_body` (Shampoo) uses magic constant `1e-2`**: `bottom_radius=1e-2` instead of `0` like Gluestick's `Toothpaste_Body`. Near-zero avoids degenerate geometry but is undocumented. | `Toothpaste_body` |
| 23 | **`Cylindrical_body` (Shampoo) — flat list stride encoding**: `all_sizes` restructured inline via stride-2 comprehension, same anti-pattern as `Storagefurniture_body`. | `Cylindrical_body` |
| 24 | **`Cambered_Body` (Lighter) — left/right half-cylinders unrolled**: only Z position sign differs, same flag-loop opportunity. | `Cambered_Body` |
| 25 | **`Separated_Cylindrical_Body` — unnecessarily complex position formula**: `clapboard_size[1]/2 - (outer_size[2]/2 - (outer_size[2] - inner_size[2]))` simplifies to `clapboard_size[1]/2 - inner_size[2]/2`. | `Separated_Cylindrical_Body` |
| 26 | **`exist_angle` ambiguous naming** reappears in `Semi_Spherical_Body` and `Spherical_Cylindrical_Body`. | Kettle classes |

---

## Board (`Regular_backboard`, `Regular_partition`)

| # | Issue | Where |
|---|---|---|
| 1 | **Unnecessary single-mesh list boilerplate** | `Regular_backboard` |
| 2 | **Redundant explicit zero rotation** — `mesh_rotation = [0, 0, 0]` passed to `Cuboid` when it's already the default. | `Regular_backboard` |
| 3 | **`self.mesh` overwritten across three conditional blocks** — only last active partition survives on the instance. Should be local or distinctly named. | `Regular_partition` |
| 4 | **Runtime crash if all `has_partition` flags are 0** — `np.concatenate([])` on an empty list raises `ValueError`. No guard exists. | `Regular_partition` |
| 5 | **Boolean flags as integers** — `has_partition[n] == 1` for all three checks. | `Regular_partition` |
| 6 | **Left/right panels unrolled into separate `if` blocks** — `has_partition[0]` and `[2]` produce identical geometry with only X sign flipped; a `flag` loop would be consistent and concise. | `Regular_partition` |
| 7 | **`has_partition` mixes two semantically different things** — indices 0/2 are symmetric side panels, index 1 is a geometrically distinct rear panel. Separate named booleans would be clearer. | `Regular_partition` |
| 8 | **Single-element list as scalar** — `left_right_separation[0]`. | `Regular_partition` |

---

## Blade (6 classes from Scissors, Shaver, Knife)

| # | Issue | Where |
|---|---|---|
| 1 | **Duplicate class names — silent overwrites** — `Cusp_Blade` ×2 (Scissors, Knife), `Curved_Blade` ×2 (Scissors, Knife). Scissors variants unreachable at import. | Scissors/Knife variants |
| 2 | **`tip_angle` declared but never used** — converted, stored on instance, never referenced in geometry. Dead parameter. | Knife `Curved_Blade` |
| 3 | **`blade_rotation` negated during conversion** — `[-x / 180 * np.pi ...]` instead of standard positive conversion. Unexplained sign flip; likely a bug or needs a comment. | `Regular_Blade` |
| 4 | **Pre-transform on individual meshes instead of `Cuboid` rotation param** — `apply_transformation` called on `.vertices` directly; local rotation could be passed to `Cuboid` constructor. | `Regular_Blade` |
| 5 | **Axis orientation conflict between same-named classes** — Scissors `Cusp_Blade` orients along X, Knife `Cusp_Blade` along Y, with mirrored `top_offset` indices. Confusing since they share a name. | `Cusp_Blade` (both sources) |
| 6 | **Unnecessary single-mesh list boilerplate** | `Cuboidal_Blade` |
| 7 | **Single-element lists as scalars** — `root_z_offset[0]`, `tip_length[0]`, `tip_z_offset[0]`, `blade_rotation[0]`. | Multiple classes |

---

## Armrest (`Solid_armrest`, `Office_armrest`)

| # | Issue | Where |
|---|---|---|
| 1 | **`self.mesh` as loop temp on instance** — overwritten each iteration, only last cuboid survives. Should be a local `mesh` variable. | Both classes |
| 2 | **No parameter documentation** — `size`, `armrest_separation`, etc. are index-based lists with no explanation of what each index means. | Both classes |
| 3 | **Unreadable inline math** — `Office_armrest` position calculation is a 7-line nested expression; intermediate named variables would clarify geometric intent. | `Office_armrest` |
| 4 | **`rotation_order` inconsistency** — `Solid_armrest` uses default `"XYZ"`, `Office_armrest` uses `"YXZ"`. Silently different behavior for users. | Both classes |
| 5 | **Magic loop ranges** — `range(2)` and `range(4)` lack comments explaining the structure (left/right, horizontal/vertical supports). | Both classes |

---

## Baffle (`Cuboidal_Baffle`, `Rectangular_Baffle`, `Curved_Baffle`)

| # | Issue | Where |
|---|---|---|
| 1 | **Unnecessary list boilerplate for single mesh** — `vertices_list`/`faces_list`/`total_num_vertices` overhead for one component. | `Cuboidal_Baffle` |
| 2 | **Missing `# Source:` comment + header mismatch** — file says "Contains 2 class(es)" but has 3; `Cuboidal_Baffle` has no source annotation, suggesting extraction script bug or untracked manual addition. | `Cuboidal_Baffle` |
| 3 | **Explicit unrolling of symmetric pair instead of loop** — left/right meshes are copy-pasted with manually flipped signs. Inconsistent with `Solid_armrest` which used a `flag` loop for the same pattern. | `Rectangular_Baffle`, `Curved_Baffle` |
| 4 | **Single-element lists used as scalars** — `baffle_separation[0]`, `baffle_rotation[0]`, `height[0]`, `exist_angle[0]`, `seperation_rotation[0]` all wrap scalars with no benefit. Consistent pattern across the library. | `Rectangular_Baffle`, `Curved_Baffle` |
| 5 | **Repeated angle computation** — `np.pi / 2 - seperation_rotation[0] / 2` written twice; should be a named variable. | `Curved_Baffle` |
| 6 | **Typo: `seperation_rotation`** → `separation_rotation`, propagates to stored instance attribute. | `Curved_Baffle` |
| 7 | **Ambiguous parameter name `exist_angle`** — likely means arc extent; `arc_angle` or `extent_angle` would be clearer. | `Curved_Baffle` |

---

## Base (16 classes from Globe, Display, Faucet, Laptop)

| # | Issue | Where |
|---|---|---|
| 1 | **[Critical] Duplicate class names — silent overwrites** — `Cuboidal_Base` defined ×3, `Cylindrical_Base` ×2, `Round_Base` ×2. Python's last-definition-wins means Globe and Display variants are unreachable dead code at import time. | Globe/Display/Faucet variants |
| 2 | **`base_rotation` not converted to radians** — used directly in `apply_transformation` while every other angle param is converted. Likely a bug if callers pass degrees. | `Curved_Base` |
| 3 | **`self.tmp_mesh` overwritten 5× as a loop variable on instance** — all five cylinder assignments should be local variables. Same for `self.back_mesh` being overwritten in Faucet `Cuboidal_Base` / `Cylindrical_Base`. | `UShapedXZ_Base`, `UShapedYZ_Base`, Faucet `Cuboidal_Base`, Faucet `Cylindrical_Base` |
| 4 | **`UShapedXZ_Base` and `UShapedYZ_Base` duplicate structure** — identical U-shape assembly logic, differing only in plane. Should share a helper or be merged with an axis parameter. | Both U-shaped classes |
| 5 | **`has_bottom_part[0] == 1` — boolean as integer** — should be a plain `bool` parameter. | `Table_Like_Base` |
| 6 | **`number_of_box`/`number_of_cylinder` as count-based switch** — value of 1 or 2 used to decide adding a second mesh; semantically this is a boolean flag. | Faucet `Cuboidal_Base`, Faucet `Cylindrical_Base` |
| 7 | **Single-element lists as scalars** — `num_legs[0]`, `R[0]`, `tilt_angle[0]`, `has_bottom_part[0]`, etc. Pervasive pattern across all classes. | Multiple classes |
| 8 | **Loop variable mesh refs stored on instance** — `self.claw_mesh`, `self.leg_mesh`, `self.bottom_mesh` overwritten each iteration. | `Star_Shaped_Base`, `Table_Like_Base` |
| 9 | **Unnecessary list boilerplate for single-mesh classes** — `Regular_Base`, `Round_Base` (Faucet), `Curved_Base`, `Cuboidal_Base` (Display) each hold one mesh but use full list machinery. | 4 single-mesh classes |
| 10 | **Typo: `leg_seperation`** → `leg_separation`. | `Table_Like_Base` |

---

## Back (`Solid_back`, `Ladder_back`, `Splat_back`, `Latice_back`, `Slat_back`)

| # | Issue | Where |
|---|---|---|
| 1 | **Massive code duplication across 4 classes** — `Ladder_back`, `Splat_back`, `Latice_back`, `Slat_back` all share the identical logic for building the two vertical side posts (i<2) and top horizontal rail (i==2). | All 4 framed classes |
| 2 | **Single loop handles structurally unrelated pieces** — vertical posts, top rail, and sub-pieces are mixed into one `if/elif/else` chain indexed by `i`. Splitting into separate named construction steps would be cleaner and easier to extend. | All 4 framed classes |
| 3 | **Magic index offsets `(i-3)` and `(i-4)` for sub-pieces** — these offsets arise from the mixed loop. Extracting sub-piece construction into its own loop `for j in range(number_of_subs[0])` would replace the magic with `j * interval`. | `Ladder_back`, `Latice_back`, `Slat_back` |
| 4 | **`self.mesh` loop temp on instance** — same issue as Armrest. | All 4 framed classes |
| 5 | **`number_of_subs` is a list but only `[0]` is accessed** — semantically this should be a plain `int`. | All 5 classes |
| 6 | **`rotation_order` inconsistency** — `Slat_back` uses `"ZYX"` for vertical posts but default `"XYZ"` for horizontal slats within the same class. | `Slat_back` |
| 7 | **Unnecessary list overhead in `Solid_back`** — `vertices_list`/`faces_list` are used for a single mesh; direct assignment would suffice. | `Solid_back` |
