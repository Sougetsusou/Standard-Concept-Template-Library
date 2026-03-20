import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Simplied_Connector(ConceptTemplate):
    """
    Semantic: Connector
    Geometry: single solid cuboid connector block
    Used by: USB
    Parameters:
      size [w, h, d]: width, height, depth of the connector
      position, rotation: global transform
    """
    def __init__(self, size, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.size = size

        w, h, d = size[0], size[1], size[2]

        self.main_mesh = Cuboid(h, w, d, position=[0, 0, d / 2])

        self.vertices = self.main_mesh.vertices
        self.faces = self.main_mesh.faces

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Connector'


class Regular_Connector(ConceptTemplate):
    """
    Semantic: Connector
    Geometry: hollow Rectangular_Ring connector shell (USB port opening)
    Used by: USB
    Parameters:
      size [w, h, d]: outer width, height, depth of the connector
      thickness [t]: wall thickness
      position, rotation: global transform
    """
    def __init__(self, size, thickness, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.size = size
        self.thickness = thickness

        width, height, depth = size[0], size[1], size[2]
        t = thickness[0]
        inner_w = width - t * 2
        inner_h = height / 2 - t

        self.main_mesh = Rectangular_Ring(depth, width, height,
                                          inner_w, inner_h,
                                          [0, t / 2 - height / 4],
                                          rotation=[np.pi / 2, 0, 0],
                                          position=[0, 0, depth / 2])

        self.vertices = self.main_mesh.vertices
        self.faces = self.main_mesh.faces

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Connector'
