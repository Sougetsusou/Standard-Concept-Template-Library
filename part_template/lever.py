import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Regular_Lever(ConceptTemplate):
    """
    Semantic: Lever
    Geometry: two symmetric support cuboids + two angled handle cuboids forming a clip lever
    Used by: Clip
    Parameters:
      lever_support_size [w, h, d]: size of each support arm
      lever_support_separation [gap]: X-axis half-gap between the two support arms
      lever_handle_size [w, h, d]: size of each handle piece
      lever_handle_offset [y]: Y offset of handle attachment from support center
      lever_handle_rotation [rx]: tilt angle of handle pieces in degrees
    """
    def __init__(self, lever_support_size, lever_support_separation,
                 lever_handle_size, lever_handle_offset, lever_handle_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):
        rotation = [x / 180 * np.pi for x in rotation]
        lever_handle_rotation = [x / 180 * np.pi for x in lever_handle_rotation]
        super().__init__(position, rotation)
        self.lever_support_size = lever_support_size
        self.lever_support_separation = lever_support_separation
        self.lever_handle_size = lever_handle_size
        self.lever_handle_offset = lever_handle_offset
        self.lever_handle_rotation = lever_handle_rotation

        sw, sh, sd = lever_support_size
        gap = lever_support_separation[0]
        hw, hh, hd = lever_handle_size
        hoy = lever_handle_offset[0]
        rx = lever_handle_rotation[0]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for sign in [1, -1]:
            tmp_mesh = Cuboid(sh, sw, sd, position=[sign * (gap + sw / 2), 0, 0])
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

        for sign in [1, -1]:
            tmp_mesh = Cuboid(hh, hw, hd,
                              position=[0,
                                        hoy * np.cos(rx),
                                        sign * (sd + hd) / 2 - sign * hoy * np.sin(rx)],
                              rotation=[-sign * rx, 0, 0])
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)
        # YXZ + offset_first: required by clip pivot geometry
        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)
        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))
        self.semantic = 'Lever'
