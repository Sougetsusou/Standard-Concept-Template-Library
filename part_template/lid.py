import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Cylindrical_Lid(ConceptTemplate):
    """
    Semantic: Lid
    Geometry: tapered cylindrical lid — hollow ring bottom (thread section) + solid cylinder top
    Used by: Bottle
    Parameters:
      outer_size [top_r, bottom_r, height]: outer top radius, outer bottom radius, total height
      inner_size [top_r, bottom_r, height]: inner top radius, inner bottom radius, thread height
    """
    def __init__(self, outer_size, inner_size, position=[0, 0, 0], rotation=[0, 0, 0]):
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)
        self.outer_size = outer_size
        self.inner_size = inner_size

        outer_top_r, outer_bot_r, outer_h = outer_size
        inner_top_r, inner_bot_r, inner_h = inner_size
        top_h = outer_h - inner_h

        # middle_radius: linear interpolation of outer radius at the thread/cap boundary height
        middle_r = outer_bot_r * (1 - inner_h / outer_h) + outer_top_r * inner_h / outer_h

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        tmp_mesh = Ring(inner_h, middle_r, inner_top_r,
                        outer_bottom_radius=outer_bot_r,
                        inner_bottom_radius=inner_bot_r,
                        position=[0, -(outer_h - inner_h) / 2, 0])
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        tmp_mesh = Cylinder(top_h, outer_top_r, middle_r,
                            position=[0, inner_h / 2, 0])
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)
        self.vertices = apply_transformation(self.vertices, position, rotation)
        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))
        self.semantic = 'Lid'
