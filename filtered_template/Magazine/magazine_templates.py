"""
Magazine Templates
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


# Source: Stapler/concept_template.py
class Carved_Magazine(ConceptTemplate):
    def __init__(self, outer_size, inner_size, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.outer_size = outer_size
        self.inner_size = inner_size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        top_mesh_position = [
            0,
            (outer_size[1] + inner_size[1]) / 2,
            outer_size[2] / 2
        ]
        top_mesh_rotation = [0, 0, np.pi]
        self.top_mesh = Cuboid(outer_size[1] - inner_size[1], outer_size[0], outer_size[2],
                               position = top_mesh_position,
                               rotation = top_mesh_rotation)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [
            0, 
            inner_size[1] / 2,
            outer_size[2] / 2
        ]
        bottom_mesh_rotation = [0, 0, np.pi]
        self.bottom_mesh = Rectangular_Ring(inner_size[1], outer_size[0], outer_size[2], inner_size[0], inner_size[2],
                                            position = bottom_mesh_position,
                                            rotation = bottom_mesh_rotation)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Magazine'


# Source: Stapler/concept_template.py
class Complex_Magazine(ConceptTemplate):
    def __init__(self, size, thickness, front_height, beside_length, beside_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.thickness = thickness
        self.front_height = front_height
        self.beside_length = beside_length
        self.beside_offset = beside_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0,
            thickness[0] / 2,
            size[2] / 2
        ]
        self.bottom_mesh = Cuboid(thickness[0], size[0], size[2],
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        behind_mesh_position = [
            0,
            size[1] / 2,
            thickness[0] / 2
        ]
        self.behind_mesh = Cuboid(size[1], size[0], thickness[0],
                                  position = bottom_mesh_position)
        vertices_list.append(self.behind_mesh.vertices)
        faces_list.append(self.behind_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.behind_mesh.vertices)

        front_mesh_position = [
            0,
            front_height[0] / 2,
            size[2] - thickness[0] / 2
        ]
        self.front_mesh = Cuboid(front_height[0], size[0], thickness[0],
                                  position = front_mesh_position)
        vertices_list.append(self.front_mesh.vertices)
        faces_list.append(self.front_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.front_mesh.vertices)

        left_mesh_position = [
            size[0] / 2 - thickness[0] / 2,
            size[1] / 2,
            size[2] / 2 + beside_offset[0]
        ]
        self.left_mesh = Cuboid(size[1], thickness[0], beside_length[0],
                                position = left_mesh_position)
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        right_mesh_position = [
            -size[0] / 2 + thickness[0] / 2,
            size[1] / 2,
            size[2] / 2 + beside_offset[0]
        ]
        self.right_mesh = Cuboid(size[1], thickness[0], beside_length[0],
                                position = right_mesh_position)
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Magazine'
