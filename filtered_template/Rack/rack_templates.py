"""
Rack Templates
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


# Source: Foldingrack/concept_template.py
class Regular_rack(ConceptTemplate):
    def __init__(self, size, horizontal_rotation, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        horizontal_rotation = [x / 180 * np.pi for x in horizontal_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.horizontal_rotation = horizontal_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_1_rotation = [0, 0, horizontal_rotation[0]]
        mesh_1_position = apply_transformation([size[0] / 2, -size[1] / 2, 0], position=[0, 0, 0], rotation=mesh_1_rotation)
        self.mesh_1 = Cuboid(size[1], size[0], size[2], position=mesh_1_position, rotation=mesh_1_rotation)
        vertices_list.append(self.mesh_1.vertices)
        faces_list.append(self.mesh_1.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_1.vertices)

        mesh_2_rotation = [0, 0, -horizontal_rotation[0]]
        mesh_2_position = apply_transformation([size[0] / 2, size[1] / 2, 0], position=[0, 0, 0], rotation=mesh_2_rotation)
        self.mesh_2 = Cuboid(size[1], size[0], size[2], position=mesh_2_position, rotation=mesh_2_rotation)
        vertices_list.append(self.mesh_2.vertices)
        faces_list.append(self.mesh_2.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_2.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Rack'


# Source: Foldingrack/concept_template.py
class Curved_rack(ConceptTemplate):
    def __init__(self, size, edge_radius, edge_exist_rotation, horizontal_rotation, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        edge_exist_rotation = [x / 180 * np.pi for x in edge_exist_rotation]
        horizontal_rotation = [x / 180 * np.pi for x in horizontal_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.edge_radius = edge_radius
        self.edge_exist_rotation = edge_exist_rotation
        self.horizontal_rotation = horizontal_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_1_rotation = [0, 0, horizontal_rotation[0]]
        mesh_1_position = apply_transformation([size[0] / 2, -size[1] / 2, 0], position=[0, 0, 0],
                                               rotation=mesh_1_rotation)
        self.mesh_1 = Cuboid(size[1], size[0], size[2], position=mesh_1_position, rotation=mesh_1_rotation)
        vertices_list.append(self.mesh_1.vertices)
        faces_list.append(self.mesh_1.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_1.vertices)

        mesh_2_rotation = [0, 0, -horizontal_rotation[0]]
        mesh_2_position = apply_transformation([size[0] / 2, size[1] / 2, 0], position=[0, 0, 0],
                                               rotation=mesh_2_rotation)
        self.mesh_2 = Cuboid(size[1], size[0], size[2], position=mesh_2_position, rotation=mesh_2_rotation)
        vertices_list.append(self.mesh_2.vertices)
        faces_list.append(self.mesh_2.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_2.vertices)

        mesh_3_rotation = [np.pi / 2, 0, np.pi - horizontal_rotation[0]]
        mesh_3_position = [edge_radius[0] * np.cos(horizontal_rotation[0]) + size[1] * np.sin(horizontal_rotation[0]),
                           size[1] * np.cos(horizontal_rotation[0]) - edge_radius[0] * np.sin(horizontal_rotation[0]),
                           0]
        self.mesh_3 = Ring(size[2], edge_radius[0], edge_radius[0] - size[0], edge_exist_rotation[0], position=mesh_3_position, rotation=mesh_3_rotation)
        vertices_list.append(self.mesh_3.vertices)
        faces_list.append(self.mesh_3.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_3.vertices)

        mesh_4_rotation = [-np.pi / 2, 0, np.pi + horizontal_rotation[0]]
        mesh_4_position = [edge_radius[0] * np.cos(horizontal_rotation[0]) + size[1] * np.sin(horizontal_rotation[0]),
                           -size[1] * np.cos(horizontal_rotation[0]) + edge_radius[0] * np.sin(horizontal_rotation[0]),
                           0]
        self.mesh_4 = Ring(size[2], edge_radius[0], edge_radius[0] - size[0], edge_exist_rotation[0], position=mesh_4_position, rotation=mesh_4_rotation)
        vertices_list.append(self.mesh_4.vertices)
        faces_list.append(self.mesh_4.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_4.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Rack'
