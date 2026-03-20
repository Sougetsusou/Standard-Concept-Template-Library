"""
Lever Templates
Automatically extracted from concept_template.py files
Contains 1 class(es)
"""

from base_template import ConceptTemplate
from geometry_template import *
from knowledge_utils import *
from math import degrees, atan2, sqrt
from utils import apply_transformation
from utils import apply_transformation, adjust_position_from_rotation, list_add
from utils import apply_transformation, get_rodrigues_matrix
import copy
import numpy as np
import open3d as o3d
import trimesh


# Source: Clip/concept_template.py
class Regular_lever(ConceptTemplate):
    def __init__(self, level_support_size, level_support_seperation, level_handle_size, level_handle_offset, level_handle_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):
        
        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        level_handle_rotation = [x / 180 * np.pi for x in level_handle_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.level_support_size = level_support_size
        self.level_support_seperation = level_support_seperation
        self.level_handle_size = level_handle_size
        self.level_handle_offset = level_handle_offset
        self.level_handle_rotation = level_handle_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        level_support_1_position = [-level_support_seperation[0] - level_support_size[0] / 2, 0, 0]
        self.level_support_mesh_1 = Cuboid(level_support_size[1], level_support_size[0], level_support_size[2],
                                           position=level_support_1_position)
        vertices_list.append(self.level_support_mesh_1.vertices)
        faces_list.append(self.level_support_mesh_1.faces + total_num_vertices)
        total_num_vertices += len(self.level_support_mesh_1.vertices)

        level_support_2_position = [level_support_seperation[0] + level_support_size[0] / 2, 0, 0]
        self.level_support_mesh_2 = Cuboid(level_support_size[1], level_support_size[0], level_support_size[2],
                                           position=level_support_2_position)
        vertices_list.append(self.level_support_mesh_2.vertices)
        faces_list.append(self.level_support_mesh_2.faces + total_num_vertices)
        total_num_vertices += len(self.level_support_mesh_2.vertices)

        level_handle_3_rotation = [-level_handle_rotation[0], 0, 0]
        level_handle_3_position = [0, level_handle_offset[0] * np.cos(level_handle_rotation[0]),
                                   (level_support_size[2] + level_handle_size[2]) / 2 - level_handle_offset[0] * np.sin(level_handle_rotation[0])]
        self.level_handle_mesh_3 = Cuboid(level_handle_size[1], level_handle_size[0], level_handle_size[2],
                                          position=level_handle_3_position,
                                          rotation=level_handle_3_rotation)
        vertices_list.append(self.level_handle_mesh_3.vertices)
        faces_list.append(self.level_handle_mesh_3.faces + total_num_vertices)
        total_num_vertices += len(self.level_handle_mesh_3.vertices)

        level_handle_4_rotation = [level_handle_rotation[0], 0, 0]
        level_handle_4_position = [0, level_handle_offset[0] * np.cos(level_handle_rotation[0]),
                                   -(level_support_size[2] + level_handle_size[2]) / 2 + level_handle_offset[0] * np.sin(level_handle_rotation[0])]
        self.level_handle_mesh_4 = Cuboid(level_handle_size[1], level_handle_size[0], level_handle_size[2],
                                          position=level_handle_4_position,
                                          rotation=level_handle_4_rotation)
        vertices_list.append(self.level_handle_mesh_4.vertices)
        faces_list.append(self.level_handle_mesh_4.faces + total_num_vertices)
        total_num_vertices += len(self.level_handle_mesh_4.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Lever'
