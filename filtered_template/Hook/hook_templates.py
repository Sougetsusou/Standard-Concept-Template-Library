"""
Hook Templates
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


# Source: Foldingrack/concept_template.py
class Regular_hook(ConceptTemplate):
    def __init__(self, base_size, middle_size, middle_offset,
                 middle_rotation, circle_radius, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        middle_rotation = [x / 180 * np.pi for x in middle_rotation]
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.base_size = base_size
        self.middle_size = middle_size
        self.middle_offset = middle_offset
        self.middle_rotation = middle_rotation
        self.circle_radius = circle_radius

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_1_position = [-base_size[0] / 2, 0, 0]
        self.mesh_1 = Cuboid(base_size[1], base_size[0], base_size[2], position=mesh_1_position)
        vertices_list.append(self.mesh_1.vertices)
        faces_list.append(self.mesh_1.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_1.vertices)

        mesh_2_rotation = [0, 0, -middle_rotation[0]]
        mesh_2_position = [-base_size[0] - middle_size[0] / 2 * np.cos(middle_rotation[0]),
                           middle_size[0] / 2 * np.sin(middle_rotation[0]) + middle_offset[0],
                           middle_offset[1]]
        self.mesh_2 = Cuboid(middle_size[1], middle_size[0], middle_size[2], position=mesh_2_position, rotation=mesh_2_rotation)
        vertices_list.append(self.mesh_2.vertices)
        faces_list.append(self.mesh_2.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_2.vertices)

        mesh_3_rotation = [np.pi / 2, 0, -np.pi / 2]
        mesh_3_position = [-base_size[0] - middle_size[0] * np.cos(middle_rotation[0]) + middle_size[1] / 2 * np.sin(middle_rotation[0]),
                           middle_size[0] * np.sin(middle_rotation[0]) + middle_offset[0] - circle_radius[0] + middle_size[1] / 2 * np.cos(middle_rotation[0]),
                           middle_offset[1]]
        self.mesh_3 = Ring(middle_size[2], circle_radius[0], circle_radius[0] - middle_size[1], np.pi, position=mesh_3_position, rotation=mesh_3_rotation)
        vertices_list.append(self.mesh_3.vertices)
        faces_list.append(self.mesh_3.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_3.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Hook'
