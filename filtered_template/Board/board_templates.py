"""
Board Templates
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


# Source: Table/concept_template.py
class Regular_backboard(ConceptTemplate):
    def __init__(self, size, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_rotation = [0, 0, 0]
        mesh_position = [0, -size[1] / 2, 0]
        self.mesh = Cuboid(size[1], size[0], size[2], position=mesh_position, rotation=mesh_rotation)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Board'


# Source: Table/concept_template.py
class Regular_partition(ConceptTemplate):
    def __init__(self, has_partition, left_right_size, rear_size, left_right_separation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.has_partition = has_partition
        self.left_right_size = left_right_size
        self.rear_size = rear_size
        self.left_right_separation = left_right_separation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        if has_partition[0] == 1:
            mesh_position = [left_right_separation[0] / 2 + left_right_size[0] / 2, left_right_size[1] / 2, 0]
            self.mesh = Cuboid(left_right_size[1], left_right_size[0], left_right_size[2],
                               position=mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        if has_partition[1] == 1:
            mesh_position = [0, rear_size[0] / 2, -left_right_size[2] / 2 - rear_size[1] / 2]
            self.mesh = Cuboid(rear_size[0], left_right_separation[0] + 2 * left_right_size[0], rear_size[1],
                               position=mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        if has_partition[2] == 1:
            mesh_position = [-left_right_separation[0] / 2 - left_right_size[0] / 2, left_right_size[1] / 2, 0]
            self.mesh = Cuboid(left_right_size[1], left_right_size[0], left_right_size[2],
                               position=mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Board'
