# End-to-End Pipeline Demo: The Laptop Category

This document walks through the full lifecycle of a category (using **Laptop** as the concrete example). It demonstrates how to transition from the original monolithic codebase to the clean geometric taxonomy, generate the training corpus, and run the 2-stage LLM inference.

---

## 1. Phase 1: Codebase Restructuring (The "Before" & "After")

### The "Before" State
Originally, part definitions were tightly coupled to the category. The file `code/Laptop/concept_template.py` contained hardcoded definitions for `Regular_Base`, `Hinged_Panel_Screen`, `Cuboidal_Connector`, etc., making them difficult for an LLM to reuse or learn from generically.

### The "After" State: `part_template/` Extraction
After Phase 1, the logic is broken out by **semantic parts**. We move them to `part_template/` and attach highly structured docstrings to help the LLM understand the geometry.

**`part_template/base.py`**
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
        # [Geometry logic omitted for brevity]
        pass
```

**`part_template/screen.py`**
```python
class Hinged_Panel_Screen(ConceptTemplate):
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
        # [Geometry logic omitted for brevity]
        pass
```

### The "After" State: Assembly Manifest
The original category file `code/Laptop/concept_template.py` is stripped down to act purely as an **assembly manifest**. It only contains imports from the shared `part_template/` library.

**`code/Laptop/concept_template.py`**
```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'part_template'))

from base import Regular_Base
from screen import Hinged_Panel_Screen
from connector import Cuboidal_Connector, Cylindrical_Connector
```

---

## 2. Phase 2: Training Data Construction

With the library decoupled, we translate the existing `.pkl` instantiation data into text-to-code training examples for our models.

### Stage 1 Training: Level 2 Examples (Part Templates)
Goal: Teach the LLM to read a geometric description and identify if an existing component fits, or if it needs to write a new one from primitives.

**Example 2A: Selecting an Existing Class**
```text
### Task: write_part_class
### Semantic type: Screen
### Description: a flat rectangular screen panel hinged at the back edge of the base, tilted open at an angle.
### Existing classes in screen.py:
#   Hinged_Panel_Screen — flat cuboid tilted at screen_rotation, offset from hinge
### Decision: use_existing: Hinged_Panel_Screen
### Instantiation (Demo):
Hinged_Panel_Screen(
    size=[0.32, 0.01, 0.22],
    offset=[0.12, 0.0],
    screen_rotation=[110],
    position=[0.0, 0.02, -0.01],
    rotation=[0.0, 0.0, 0.0]
)
```

**Example 2B: Writing a New Class**
```text
### Task: write_part_class
### Semantic type: Base
### Description: a tapered laptop base that is thicker at the back and extremely thin at the front.
### Existing classes in base.py:
#   Regular_Base — single flat cuboid block
### Decision: write_new: Tapered_Base
### Code:
class Tapered_Base(ConceptTemplate):
    def __init__(self, front_thickness, back_thickness, ...):
        ...
```

### Stage 2 Training: Level 3 Examples (Full Instance Assembly)
Goal: Teach the LLM to parse a full object description, decompose it, grab the necessary parts from the library, and wire them together.

*Note: 48 Laptop `.pkl` entries translate to 48 Level 3 training examples for this category.*

**Example 3A: Full Laptop Assembly**
```text
### Task: generate_concept_template
### Category: Laptop
### Description: a clamshell laptop with a standard rectangular base, a thin hinged screen, and two rectangular side ports.
### Output:
# Part decomposition:
#   Base:      Regular_Base
#   Screen:    Hinged_Panel_Screen
#   Connector: Cuboidal_Connector

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'part_template'))

from base import Regular_Base
from screen import Hinged_Panel_Screen
from connector import Cuboidal_Connector

base = Regular_Base(size=[0.32, 0.02, 0.22], position=[0.0, -0.01, 0.0], rotation=[0.0, 0.0, 0.0])
screen = Hinged_Panel_Screen(size=[0.30, 0.01, 0.21], offset=[0.11, 0.0], screen_rotation=[110], position=[0.0, 0.02, -0.01], rotation=[0.0, 0.0, 0.0])
ports = Cuboidal_Connector(number_of_connector=[2], size=[0.015, 0.008, 0.012], separation=[0.01], offset=[-0.02, -0.005, 0.08], connector_rotation=[0])
```

---

## 3. Phase 3: Live LLM Inference Walkthrough

Once the model is fine-tuned, here is how a live inference looks when the user provides an **unseen description**.

**Input Prompt:**
> "Create a bulky gaming laptop. It has a surprisingly thick, multi-level base for cooling, a heavy screen tilted back 100 degrees, and four cylindrical audio/power jacks stacked on the right side."

**1. Stage 1 LLM (Decomposition & Part Fetching)**
*   Analyzes components: `MultiLevel_Base`, `Hinged_Panel_Screen`, `Cylindrical_Connector`.
*   Checks `part_template/base.py` -> Doesn't find `MultiLevel_Base`.
*   **Result:** LLM autogenerates a new `MultiLevel_Base` class building upon generic primitives (Cuboid). LLM identifies `Hinged_Panel_Screen` and `Cylindrical_Connector` exist and flags them for import.

**2. Stage 2 LLM (Instance Assembly)**
*   Pulls the newly drafted `MultiLevel_Base` class definition.
*   Imports `Hinged_Panel_Screen` and `Cylindrical_Connector` from `part_template/`.
*   Generates instantiation code predicting numeric size relations (e.g., assigning a thicker `size` parameter to the base).

**3. Execution** 
*   Python interprets the output script.
*   Open3D renders the newly minted 3D mesh. If the generated mesh has non-degenerate topology errors, it is fed back into the inference loop for a 1-time parameter retry.