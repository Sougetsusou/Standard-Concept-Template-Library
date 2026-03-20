import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Standard_Knob(ConceptTemplate):
    """
    Semantic: Knob
    Geometry: single flat cylinder protruding along Z axis
    Used by: Switch
    Parameters:
      size [radius, height]: radius and height of the knob cylinder
    """
    def __init__(self, size, position=[0, 0, 0], rotation=[0, 0, 0]):
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)
        self.size = size

        radius, height = size[0], size[1]

        self.base_mesh = Cylinder(height, radius, radius,
                                  position=[0, 0, height / 2],
                                  rotation=[np.pi / 2, 0, 0])

        self.vertices = self.base_mesh.vertices
        self.faces = self.base_mesh.faces

        # offset_first=True: translation applied before rotation (knob sits on a rotated surface)
        self.vertices = apply_transformation(self.vertices, position, rotation, offset_first=True)
        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))
        self.semantic = 'Knob'
