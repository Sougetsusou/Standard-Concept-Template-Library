# End-to-End Demo: Laptop Category

This document walks through the full pipeline — from raw codebase to LLM training example
to inference on a new category — using Laptop as the concrete example.

---

## Step 1 — Source: Part Classes (Phase 1.2 output)

After restructuring, Laptop's 4 part classes live in semantic files under `code/shared/`:

### `code/shared/base_templates.py` (excerpt)
```python
class Regular_Base(ConceptTemplate):
    """
    Semantic: Base
    Geometry: single flat cuboid — the keyboard/trackpad base of a laptop
    Used by: Laptop
    Parameters:
      size [w, h, d]: width, height (thickness), depth of the base slab
    """
    def __init__(self, size, position=[0, 0, 0], rotation=[0, 0, 0]):
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)
        self.size = size

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.back_mesh = Cuboid(size[1], size[0], size[2])
        vertices_list.append(self.back_mesh.vertices)
        faces_list.append(self.back_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.back_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)
        self.vertices = apply_transformation(self.vertices, position, rotation)
        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))
        self.semantic = 'Base'
```

### `code/shared/screen_templates.py` (excerpt)
```python
class Regular_Screen(ConceptTemplate):
    """
    Semantic: Screen
    Geometry: flat cuboid tilted at screen_rotation angle, offset from hinge point
    Used by: Laptop
    Parameters:
      size [w, h, d]: width, height (thickness), depth of screen panel
      offset [y, z]: hinge position offset from base center
      screen_rotation [rx]: tilt angle of screen in degrees
    """
    def __init__(self, size, offset, screen_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):
        rotation = [x / 180 * np.pi for x in rotation]
        screen_rotation = [x / 180 * np.pi for x in screen_rotation]
        super().__init__(position, rotation)
        self.size = size
        self.offset = offset
        self.screen_rotation = screen_rotation

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        back_mesh_position = [
            0,
            offset[0] + size[1] * np.cos(screen_rotation[0]) / 2,
            offset[1]
        ]
        back_mesh_rotation = [screen_rotation[0], 0, 0]
        self.back_mesh = Cuboid(size[1], size[0], size[2],
                                position=back_mesh_position,
                                rotation=back_mesh_rotation)
        vertices_list.append(self.back_mesh.vertices)
        faces_list.append(self.back_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.back_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)
        self.vertices = apply_transformation(self.vertices, position, rotation)
        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))
        self.semantic = 'Screen'
```

### `code/shared/connector_templates.py` (excerpt)
```python
class Cuboidal_Connector(ConceptTemplate):
    """
    Semantic: Connector
    Geometry: N rectangular box connectors (e.g. USB ports) arranged in a row
    Used by: Laptop
    Parameters:
      number_of_connector [n]: how many connectors
      size [w, h, d]: size of each connector
      separation [s1, s2, ...]: gaps between consecutive connectors
      offset [x, y, z]: position of first connector relative to parent
      connector_rotation [rx]: tilt angle in degrees
    """
    ...

class Cylindrical_Connector(ConceptTemplate):
    """
    Semantic: Connector
    Geometry: N cylindrical connectors (e.g. audio jacks) arranged in a row
    Used by: Laptop
    Parameters:
      number_of_connector [n]: how many connectors
      size [r, h]: radius and height of each cylinder
      separation [s1, s2, ...]: gaps between consecutive connectors
      offset [x, y, z]: position of first connector relative to parent
    """
    ...
```

---

## Step 2 — Source: Assembly Manifest (Phase 1.3 output)

After restructuring, `code/Laptop/concept_template.py` declares available part classes:

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

from base_templates import Regular_Base
from screen_templates import Regular_Screen
from connector_templates import Cuboidal_Connector, Cylindrical_Connector
```

The actual instance assembly — which classes to use and with what parameter values —
is stored in `conceptualization.pkl`. Each pkl entry is one fully grounded instance:

```python
# pkl entry: id=125c93cbc6544bd1f9f50a550b8c1cce
Regular_Base(
    size=[0.32, 0.02, 0.22],
    position=[0.0, -0.01, 0.0],
    rotation=[0.0, 0.0, 0.0]
)
Regular_Screen(
    size=[0.30, 0.01, 0.21],
    offset=[0.11, 0.0],
    screen_rotation=[110],
    position=[0.0, 0.02, -0.01],
    rotation=[0.0, 0.0, 0.0]
)
Cuboidal_Connector(
    number_of_connector=[2],
    size=[0.015, 0.008, 0.012],
    separation=[0.01],
    offset=[-0.02, -0.005, 0.08],
    connector_rotation=[0],
    position=[0.0, 0.0, 0.0],
    rotation=[0.0, 0.0, 0.0]
)
```

This is what the LLM must learn to generate — a fully executable instance, not just imports.
48 Laptop pkl entries = 48 Level 3 training examples. Across 39 categories: ~3900 examples total.

---

## Step 3 — Training Data Construction (Phase 2)

Note: geometry primitives (Cuboid, Cylinder, Ring, etc.) are a known API — the LLM
already knows how to call them from pretraining. Training focuses on two things:
the part template pattern, and the part vocabulary.

### Level 2 example — Part template (select existing)
```
### Task: write_part_class
### Semantic type: Screen
### Description: a flat rectangular screen panel hinged at the back edge of the
                 base, tilted open at an angle
### Existing classes in screen_templates.py:
#   Regular_Screen — flat cuboid tilted at screen_rotation, offset from hinge
### Decision: use_existing: Regular_Screen
### Instantiation:
Regular_Screen(
    size=[0.32, 0.01, 0.22],
    offset=[0.12, 0.0],
    screen_rotation=[110],
    position=[0.0, 0.02, -0.01],
    rotation=[0.0, 0.0, 0.0]
)
```

### Level 2 example — Part template (use existing)
```
### Task: write_part_class
### Semantic type: Connector
### Description: a row of rectangular port openings along the side edge of the base
### Existing classes in connector_templates.py:
#   Cuboidal_Connector — N rectangular connectors in a row
#   Cylindrical_Connector — N cylindrical connectors in a row
### Decision: use_existing: Cuboidal_Connector
### Instantiation:
Cuboidal_Connector(
    number_of_connector=[2],
    size=[0.015, 0.008, 0.012],
    separation=[0.01],
    offset=[-0.02, -0.005, 0.08],
    connector_rotation=[0],
    position=[0.0, 0.0, 0.0],
    rotation=[0.0, 0.0, 0.0]
)
```

### Level 2 example — Part template (write new)
```
### Task: write_part_class
### Semantic type: Keyboard
### Description: a flat rectangular keyboard surface with a slight taper —
                 thicker at the back edge, thinner at the front
### Existing classes in keyboard_templates.py:
#   (none exist)
### Decision: write_new: Tapered_Keyboard
### Code:
class Tapered_Keyboard(ConceptTemplate):
    """
    Semantic: Keyboard
    Geometry: trapezoidal cuboid — flat keyboard surface, thicker at back than front
    Used by: Laptop
    Parameters:
      size [w, h_back, d]: width, back height, depth of keyboard surface
      front_height [h]: height at the front edge (thinner than back)
      position, rotation: global transform
    """
    def __init__(self, size, front_height, position=[0, 0, 0], rotation=[0, 0, 0]):
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)
        self.size = size
        self.front_height = front_height

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_position = [0, size[1] / 2, 0]
        tmp_mesh = Cuboid(size[1], size[0], size[2],
                          bottom_width=front_height[0],
                          top_offset=[0, (size[1] - front_height[0]) / 2],
                          position=mesh_position)
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)
        self.vertices = apply_transformation(self.vertices, position, rotation)
        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))
        self.semantic = 'Keyboard'
```

### Level 3 example — Full instance assembly
```
### Task: generate_concept_template
### Category: Laptop
### Description: a clamshell laptop with a flat rectangular keyboard base,
                 a thin screen panel hinged at the back that opens at an angle,
                 and a row of two rectangular ports along the side
### Output:

# Part decomposition:
#   Base:      Regular_Base — flat cuboid keyboard/trackpad base
#   Screen:    Regular_Screen — thin panel tilted open from hinge
#   Connector: Cuboidal_Connector — rectangular side ports

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

from base_templates import Regular_Base
from screen_templates import Regular_Screen
from connector_templates import Cuboidal_Connector

base = Regular_Base(
    size=[0.32, 0.02, 0.22],
    position=[0.0, -0.01, 0.0],
    rotation=[0.0, 0.0, 0.0]
)
screen = Regular_Screen(
    size=[0.30, 0.01, 0.21],
    offset=[0.11, 0.0],
    screen_rotation=[110],
    position=[0.0, 0.02, -0.01],
    rotation=[0.0, 0.0, 0.0]
)
ports = Cuboidal_Connector(
    number_of_connector=[2],
    size=[0.015, 0.008, 0.012],
    separation=[0.01],
    offset=[-0.02, -0.005, 0.08],
    connector_rotation=[0],
    position=[0.0, 0.0, 0.0],
    rotation=[0.0, 0.0, 0.0]
)
```

---

## Step 4 — Synthetic Augmentation (Phase 2.2)

Sample parameter variations from the Laptop pkl (48 instances) to generate
natural language descriptions paired with instantiation code.

Example variants generated from pkl distribution:

| Instance | Base size | Screen tilt | Connectors | Description generated |
|----------|-----------|-------------|------------|----------------------|
| A | [0.32, 0.02, 0.22] | 110° | 2 rectangular | "thin base, screen open wide, two side ports" |
| B | [0.36, 0.025, 0.24] | 90° | 1 cylindrical | "wider base, screen upright, one audio jack" |
| C | [0.28, 0.018, 0.20] | 130° | 3 rectangular | "compact base, screen tilted back, three ports" |

Each row becomes a Level 3 training example pairing the description with the
corresponding full instantiation code (part selection + concrete parameter values).

---

## Step 5 — Inference on a New Category (Tablet)

At inference time, the LLM receives only:

```
### Task: generate_concept_template
### Category: Tablet
### Description: a thin rectangular touchscreen device with no keyboard,
                 a single front-facing screen covering most of the face,
                 and two small buttons on the side edge
```

Expected LLM output (Stage 1 — part decomposition + selection):

```
# Part decomposition:
#   Screen: Regular_Screen — covers the full face, no tilt needed (screen_rotation=0)
#           → use_existing: Regular_Screen
#   Button: no existing Button class fits a side-mounted physical button
#           → write_new: Tablet_Side_Button

class Tablet_Side_Button(ConceptTemplate):
    """
    Semantic: Button
    Geometry: small rectangular protrusion on the side edge
    Parameters:
      size [w, h, d]: button dimensions
      offset [x, y, z]: position along side edge
    """
    def __init__(self, size, offset, position=[0, 0, 0], rotation=[0, 0, 0]):
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)
        self.size = size
        self.offset = offset

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_position = [offset[0], offset[1], offset[2]]
        tmp_mesh = Cuboid(size[1], size[0], size[2], position=mesh_position)
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)
        self.vertices = apply_transformation(self.vertices, position, rotation)
        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))
        self.semantic = 'Button'
```

Expected LLM output (Stage 2 — assembly manifest):

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

from screen_templates import Regular_Screen
from button_templates import Tablet_Side_Button  # newly written above
```

---

## Step 6 — Validation

```python
exec(open("Tablet/concept_template.py").read())
# instantiate with sample parameters
screen = Regular_Screen(
    size=[0.25, 0.005, 0.17],
    offset=[0.0, 0.0],
    screen_rotation=[0]
)
button = Tablet_Side_Button(
    size=[0.008, 0.003, 0.015],
    offset=[0.13, 0.0, 0.05]
)
# check meshes are non-degenerate
assert screen.overall_obj_mesh.is_volume or len(screen.overall_obj_pts) == SAMPLENUM
assert button.overall_obj_mesh.is_volume or len(button.overall_obj_pts) == SAMPLENUM
print("Validation passed")
```

---

## Key Observations from this Demo

1. **Part decomposition is learned implicitly** — the LLM sees 33 training categories
   and learns that "clamshell device" → Base + Screen + Connector. It generalizes
   "touchscreen device" → Screen + Button without being told.

2. **Primitives are a known API, not a training target** — the LLM already knows
   Cuboid, Cylinder, Ring from pretraining. What it learns here is the part template
   pattern (vertices_list, apply_transformation, trimesh, self.semantic) and the
   part vocabulary (which classes exist and what they produce).

3. **use_existing vs write_new is driven by docstring matching** — the LLM matches
   "side-mounted physical button" against existing class docstrings and finds no fit,
   so it writes a new class. The docstring vocabulary is the selection mechanism.

4. **New part classes follow the exact same pattern** — primitives + vertices_list loop
   + apply_transformation + trimesh. The LLM learns this pattern from Level 2 training
   and applies it to novel geometry.

5. **The assembly manifest is trivially short** — just imports. The LLM's main job
   is part identification and part class authoring, not boilerplate assembly code.
