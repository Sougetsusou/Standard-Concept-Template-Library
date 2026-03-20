import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Regular_Controller(ConceptTemplate):
    """
    Semantic: Controller
    Geometry: single flat cuboid control panel
    Used by: Safe
    Parameters:
      size [w, h, d]: width, height, depth of the controller panel
    """
    def __init__(self, size, position=[0, 0, 0], rotation=[0, 0, 0]):
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)
        self.size = size

        width, height, depth = size

        self.mesh = Cuboid(height, width, depth, position=[0, 0, depth / 2])
        self.vertices = self.mesh.vertices
        self.faces = self.mesh.faces
        self.vertices = apply_transformation(self.vertices, position, rotation)
        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))
        self.semantic = 'Controller'
