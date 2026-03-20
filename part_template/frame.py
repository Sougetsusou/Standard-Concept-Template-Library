import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Standard_Windowframe(ConceptTemplate):
    """
    Semantic: Frame
    Geometry: single Rectangular_Ring window frame
    Used by: Window
    Parameters:
      outside_frame_size [w, h, d]: outer dimensions of the frame
      outside_frame_inner_size [w, h]: inner opening dimensions
      outside_frame_inner_outer_offset [x, y]: XY offset of inner opening within frame
      position, rotation: global transform
    """
    def __init__(self, outside_frame_size, outside_frame_inner_size,
                 outside_frame_inner_outer_offset,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.outside_frame_size = outside_frame_size
        self.outside_frame_inner_size = outside_frame_inner_size
        self.outside_frame_inner_outer_offset = outside_frame_inner_outer_offset

        self.mesh = Rectangular_Ring(outside_frame_size[2],
                                     outside_frame_size[0],
                                     outside_frame_size[1],
                                     outside_frame_inner_size[0],
                                     outside_frame_inner_size[1],
                                     outside_frame_inner_outer_offset,
                                     rotation=[np.pi / 2, 0, 0])

        self.vertices = self.mesh.vertices
        self.faces = self.mesh.faces

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Frame'
