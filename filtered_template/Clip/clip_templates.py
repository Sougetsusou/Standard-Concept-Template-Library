"""
Clip Templates
Automatically extracted from concept_template.py files
Contains 2 class(es)
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


# Source: Pen/concept_template.py
class Trifold_Clip(ConceptTemplate):
    def __init__(self, clip_root_size, clip_vertical_size, clip_tip_size, clip_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.clip_root_size = clip_root_size
        self.clip_vertical_size = clip_vertical_size
        self.clip_tip_size = clip_tip_size
        self.clip_offset = clip_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_position = [
            0,
            -clip_root_size[1] / 2,
            clip_root_size[2] / 2
        ]
        self.mesh = Cuboid(clip_root_size[1], clip_root_size[0], clip_root_size[2],
                           position = mesh_position)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        middle_mesh_position = [
            0,
            -clip_vertical_size[1] / 2 - clip_offset[0],
            clip_root_size[2] + clip_vertical_size[2] / 2
        ]
        self.middle_mesh = Cuboid(clip_vertical_size[1], clip_vertical_size[0], clip_vertical_size[2],
                                  position = middle_mesh_position)
        vertices_list.append(self.middle_mesh.vertices)
        faces_list.append(self.middle_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.middle_mesh.vertices)

        tip_mesh_position = [
            0,
            -clip_vertical_size[1] - clip_offset[0] + clip_tip_size[1] / 2 - clip_offset[1],
            clip_root_size[2] - clip_tip_size[2] / 2
        ]
        self.tip_mesh = Cuboid(clip_tip_size[1], clip_tip_size[0], clip_tip_size[2],
                               position = tip_mesh_position)
        vertices_list.append(self.tip_mesh.vertices)
        faces_list.append(self.tip_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.tip_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Clip'


# Source: Pen/concept_template.py
class Curved_Clip(ConceptTemplate):
    def __init__(self, clip_curve_size, clip_curve_exist_angle, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        clip_curve_exist_angle = [x / 180 * np.pi for x in clip_curve_exist_angle]
        super().__init__(position, rotation)

        # Record Parameters
        self.clip_curve_size = clip_curve_size
        self.clip_curve_exist_angle = clip_curve_exist_angle

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_position = [
            0, 
            -clip_curve_size[0] * np.sin(clip_curve_exist_angle[0] / 2), 
            -clip_curve_size[0] * np.cos(clip_curve_exist_angle[0] / 2)
        ]
        mesh_rotation = [
            0,
            -np.pi / 2 + clip_curve_exist_angle[0] / 2,
            np.pi / 2
        ]
        self.mesh = Ring(clip_curve_size[2], clip_curve_size[0], clip_curve_size[1], clip_curve_exist_angle[0],
                         position = mesh_position,
                         rotation = mesh_rotation)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Clip'
