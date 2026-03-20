"""
Armrest Templates
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


# Source: Chair/concept_template.py
class Solid_armrest(ConceptTemplate):
    def __init__(self, size, armrest_separation, armrest_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        armrest_rotation = [x / 180 * np.pi for x in armrest_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.armrest_separation = armrest_separation
        self.armrest_rotation = armrest_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(2):
            flag = 1 if i == 0 else -1
            mesh_rotation = [armrest_rotation[0], 0, flag * armrest_rotation[1]]
            mesh_position = [-flag * armrest_separation[0] / 2,
                             size[1] / 2 * np.cos(armrest_rotation[1]) * np.cos(armrest_rotation[0]) - size[
                                 2] / 2 * np.sin(armrest_rotation[0]), 0]
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

        self.semantic = 'Armrest'


# Source: Chair/concept_template.py
class Office_armrest(ConceptTemplate):
    def __init__(self, horizontal_support_sizes, vertical_support_sizes, supports_contact_offset,
                 vertical_support_rotation, horizontal_support_rotation, armrest_separation, armrest_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        vertical_support_rotation = [x / 180 * np.pi for x in vertical_support_rotation]
        horizontal_support_rotation = [x / 180 * np.pi for x in horizontal_support_rotation]
        armrest_rotation = [x / 180 * np.pi for x in armrest_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.horizontal_support_sizes = horizontal_support_sizes
        self.vertical_support_sizes = vertical_support_sizes
        self.supports_contact_offset = supports_contact_offset
        self.vertical_support_rotation = vertical_support_rotation
        self.horizontal_support_rotation = horizontal_support_rotation
        self.armrest_separation = armrest_separation
        self.armrest_rotation = armrest_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(4):
            flag = 1 if (i % 2 == 0) else -1
            if i < 2:
                mesh_rotation = [horizontal_support_rotation[0], 0, flag * armrest_rotation[0]]
                mesh_position = [-flag * (armrest_separation[0] / 2 + (
                        vertical_support_sizes[1] * np.cos(vertical_support_rotation[0]) +
                        horizontal_support_sizes[1]) / 2 * np.sin(armrest_rotation[0])),
                                 (vertical_support_sizes[1] * np.cos(vertical_support_rotation[0]) * 2 +
                                  horizontal_support_sizes[1]) / 2 * np.cos(armrest_rotation[0]) + (
                                         supports_contact_offset[0] - vertical_support_sizes[1] / 2 * np.sin(
                                     vertical_support_rotation[0])) * np.tan(horizontal_support_rotation[0]),
                                 0]
                self.mesh = Cuboid(horizontal_support_sizes[1], horizontal_support_sizes[0],
                                   horizontal_support_sizes[2],
                                   position=mesh_position, rotation=mesh_rotation, rotation_order="YXZ")
            else:
                mesh_rotation = [vertical_support_rotation[0], 0, flag * armrest_rotation[0]]
                mesh_position = [-flag * armrest_separation[0] / 2,
                                 vertical_support_sizes[1] / 2 * np.cos(vertical_support_rotation[0]) * np.cos(
                                     armrest_rotation[0]),
                                 supports_contact_offset[0]]
                self.mesh = Cuboid(vertical_support_sizes[1], vertical_support_sizes[0],
                                   vertical_support_sizes[2],
                                   position=mesh_position, rotation=mesh_rotation, rotation_order="YXZ")

            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Armrest'
