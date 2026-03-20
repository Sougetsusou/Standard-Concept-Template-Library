import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation
from knowledge_utils import *


class Regular_Seat(ConceptTemplate):
    """
    Semantic: Seat
    Geometry: flat rectangular cuboid seat surface
    Used by: Chair
    Parameters:
      size [w, h, d]: width, height (thickness), depth of the seat
      position, rotation: global transform
    """
    def __init__(self, size, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.size = size

        width, height, depth = size

        self.mesh = Cuboid(height, width, depth)
        self.vertices = self.mesh.vertices
        self.faces = self.mesh.faces

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Seat'


class Round_Seat(ConceptTemplate):
    """
    Semantic: Seat
    Geometry: circular cylindrical seat surface
    Used by: Chair
    Parameters:
      size [radius, height]: radius and thickness of the seat disc
      position, rotation: global transform
    """
    def __init__(self, size, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.size = size

        radius, height = size[0], size[1]

        self.mesh = Cylinder(height, radius)
        self.vertices = self.mesh.vertices
        self.faces = self.mesh.faces

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Seat'
