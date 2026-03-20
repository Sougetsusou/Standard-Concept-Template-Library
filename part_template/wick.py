import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Standard_Wick(ConceptTemplate):
    """
    Semantic: Wick
    Geometry: single upright cylinder
    Used by: Lighter
    Parameters:
      size [radius, height]: radius and height of the wick cylinder
    """
    def __init__(self, size, position=[0, 0, 0], rotation=[0, 0, 0]):
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)
        self.size = size

        radius, height = size[0], size[1]

        self.mesh = Cylinder(height, radius, position=[0, height / 2, 0])
        self.vertices = self.mesh.vertices
        self.faces = self.mesh.faces
        self.vertices = apply_transformation(self.vertices, position, rotation)
        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))
        self.semantic = 'Wick'
