"""
Baffle Templates
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

class Cuboidal_Baffle(ConceptTemplate):
    def __init__(self, size, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_position = [
            0,
            size[1] / 2,
            0
        ]
        self.mesh = Cuboid(size[1], size[0], size[2],
                             position = mesh_position)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Baffle'

# Source: Pliers/concept_template.py
class Rectangular_Baffle(ConceptTemplate):
    def __init__(self, size, baffle_separation, baffle_rotation, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        baffle_rotation = [x / 180 * np.pi for x in baffle_rotation]
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.baffle_separation = baffle_separation
        self.baffle_rotation = baffle_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        left_mesh_position = [
            baffle_separation[0] / 2, 
            0,
            0
        ]
        left_mesh_rotation = [0, baffle_rotation[0], 0]

        self.left_mesh = Cuboid(size[1], size[0], size[2],
                                position = left_mesh_position,
                                rotation = left_mesh_rotation)
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        right_mesh_position = [
            -baffle_separation[0] / 2, 
            0,
            0
        ]
        right_mesh_rotation = [0, -baffle_rotation[0], 0]

        self.right_mesh = Cuboid(size[1], size[0], size[2],
                                 position = right_mesh_position,
                                 rotation = right_mesh_rotation)
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Baffle'


# Source: Pliers/concept_template.py
class Curved_Baffle(ConceptTemplate):
    def __init__(self, radius, height, exist_angle, seperation_rotation, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        exist_angle = [x / 180 * np.pi for x in exist_angle]
        seperation_rotation = [x / 180 * np.pi for x in seperation_rotation]
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.radius = radius
        self.height = height
        self.exist_angle = exist_angle
        self.seperation_rotation = seperation_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        left_mesh_rotation = [
            0, 
            np.pi / 2 - seperation_rotation[0] / 2, 
            0
        ]

        self.left_mesh = Ring(height[0], radius[0], radius[1], exist_angle[0],
                              rotation = left_mesh_rotation)
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        right_mesh_rotation = [
            0, 
            np.pi / 2 - seperation_rotation[0] / 2, 
            np.pi
        ]

        self.right_mesh = Ring(height[0], radius[0], radius[1], exist_angle[0],
                               rotation = right_mesh_rotation)
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Baffle'
