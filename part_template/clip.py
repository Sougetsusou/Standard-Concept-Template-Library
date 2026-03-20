import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation
from knowledge_utils import *


class Regular_Lever(ConceptTemplate):
    """
    Semantic: Lever
    Geometry: two side support cuboids flanking a centre gap, plus two angled handle cuboids
              that tilt toward each other over the supports
    Used by: Clip
    Parameters:
      level_support_size [w, h, d]: dimensions of each side support
      level_support_seperation [gap]: X distance from centre to inner edge of each support
      level_handle_size [w, h, d]: dimensions of each handle piece
      level_handle_offset [y_lift]: Y lift of the handle above the support top
      level_handle_rotation [angle_deg]: tilt angle of each handle about the X axis
      position, rotation: global transform
    """
    def __init__(self, level_support_size, level_support_seperation,
                 level_handle_size, level_handle_offset, level_handle_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        level_handle_rotation = [x / 180 * np.pi for x in level_handle_rotation]
        super().__init__(position, rotation)

        self.level_support_size = level_support_size
        self.level_support_seperation = level_support_seperation
        self.level_handle_size = level_handle_size
        self.level_handle_offset = level_handle_offset
        self.level_handle_rotation = level_handle_rotation

        sw, sh, sd = level_support_size
        gap = level_support_seperation[0]
        hw, hh, hd = level_handle_size
        y_lift = level_handle_offset[0]
        angle = level_handle_rotation[0]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # left support
        self.mesh_support_1 = Cuboid(sh, sw, sd,
                                     position=[-gap - sw / 2, 0, 0])
        vertices_list.append(self.mesh_support_1.vertices)
        faces_list.append(self.mesh_support_1.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_support_1.vertices)

        # right support
        self.mesh_support_2 = Cuboid(sh, sw, sd,
                                     position=[gap + sw / 2, 0, 0])
        vertices_list.append(self.mesh_support_2.vertices)
        faces_list.append(self.mesh_support_2.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_support_2.vertices)

        # front handle — tilts backward (-angle), sits above the front edge of the supports
        mesh_handle_3_rotation = [-angle, 0, 0]
        mesh_handle_3_position = [
            0,
            y_lift * np.cos(angle),
            (sd + hd) / 2 - y_lift * np.sin(angle)
        ]
        self.mesh_handle_3 = Cuboid(hh, hw, hd,
                                    position=mesh_handle_3_position,
                                    rotation=mesh_handle_3_rotation)
        vertices_list.append(self.mesh_handle_3.vertices)
        faces_list.append(self.mesh_handle_3.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_handle_3.vertices)

        # rear handle — tilts forward (+angle), mirror of front handle
        mesh_handle_4_rotation = [angle, 0, 0]
        mesh_handle_4_position = [
            0,
            y_lift * np.cos(angle),
            -(sd + hd) / 2 + y_lift * np.sin(angle)
        ]
        self.mesh_handle_4 = Cuboid(hh, hw, hd,
                                    position=mesh_handle_4_position,
                                    rotation=mesh_handle_4_rotation)
        vertices_list.append(self.mesh_handle_4.vertices)
        faces_list.append(self.mesh_handle_4.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_handle_4.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # offset_first=True: global translation applied before rotation
        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Lever'
