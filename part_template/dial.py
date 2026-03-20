import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Cylindrical_Dial(ConceptTemplate):
    """
    Semantic: Dial
    Geometry: tapered base cylinder + smaller top cylinder, both along Z axis
    Used by: Safe
    Parameters:
      bottom_size [top_r, bottom_r, height]: top radius, bottom radius, height of base cylinder
      top_size [radius, height]: radius and height of top cylinder
    """
    def __init__(self, bottom_size, top_size, position=[0, 0, 0], rotation=[0, 0, 0]):
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)
        self.bottom_size = bottom_size
        self.top_size = top_size

        bot_top_r, bot_bot_r, bot_h = bottom_size
        top_r, top_h = top_size[0], top_size[1]
        mesh_rotation = [-np.pi / 2, 0, 0]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        tmp_mesh = Cylinder(bot_h, bot_top_r, bot_bot_r,
                            position=[0, 0, bot_h / 2],
                            rotation=mesh_rotation)
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        tmp_mesh = Cylinder(top_h, top_r,
                            position=[0, 0, bot_h + top_h / 2],
                            rotation=mesh_rotation)
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)
        self.vertices = apply_transformation(self.vertices, position, rotation)
        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))
        self.semantic = 'Dial'
