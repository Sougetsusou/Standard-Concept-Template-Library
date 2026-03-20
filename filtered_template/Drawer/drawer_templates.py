"""
Drawer Templates
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


# Source: StorageFurniture/concept_template.py
class Regular_drawer(ConceptTemplate):
    def __init__(self, number_of_drawer, drawers_params, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.number_of_drawer = number_of_drawer
        self.drawer_size = [drawers_params[i * 20: i * 20 + 3] for i in range(number_of_drawer[0])]
        self.bottom_size = [drawers_params[i * 20 + 3] for i in range(number_of_drawer[0])]
        self.front_size = [drawers_params[i * 20 + 4: i * 20 + 7] for i in range(number_of_drawer[0])]
        self.front_offset = [drawers_params[i * 20 + 7] for i in range(number_of_drawer[0])]
        self.left_right_inner_size = [drawers_params[i * 20 + 8] for i in range(number_of_drawer[0])]
        self.rear_front_inner_size = [drawers_params[i * 20 + 9] for i in range(number_of_drawer[0])]
        self.number_of_handle = [drawers_params[i * 20 + 10] for i in range(number_of_drawer[0])]
        self.handle_sizes = [drawers_params[i * 20 + 11: i * 20 + 14] for i in range(number_of_drawer[0])]
        self.handle_offset = [drawers_params[i * 20 + 14: i * 20 + 16] for i in range(number_of_drawer[0])]
        self.handle_separation = [drawers_params[i * 20 + 16] for i in range(number_of_drawer[0])]
        self.drawer_offset = [drawers_params[i * 20 + 17: i * 20 + 20] for i in range(number_of_drawer[0])]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for drawer_idx in range(number_of_drawer[0]):
            for mesh_idx in range(6 + self.number_of_handle[drawer_idx]):
                if mesh_idx < 2:
                    position_sign = -1 if mesh_idx == 0 else 1
                    mesh_position = [position_sign * (
                            self.drawer_size[drawer_idx][0] - self.left_right_inner_size[drawer_idx]) / 2 +
                                     self.drawer_offset[drawer_idx][0],
                                     self.drawer_offset[drawer_idx][1],
                                     self.drawer_offset[drawer_idx][2]]
                    self.mesh = Cuboid(self.drawer_size[drawer_idx][1],
                                       self.left_right_inner_size[drawer_idx],
                                       self.drawer_size[drawer_idx][2],
                                       position=mesh_position)
                elif mesh_idx < 4:
                    position_sign = -1 if mesh_idx == 3 else 1
                    mesh_position = [self.drawer_offset[drawer_idx][0],
                                     self.drawer_offset[drawer_idx][1],
                                     position_sign * (
                                             self.drawer_size[drawer_idx][2] - self.rear_front_inner_size[drawer_idx]) / 2 + self.drawer_offset[drawer_idx][2]]
                    self.mesh = Cuboid(self.drawer_size[drawer_idx][1],
                                       self.drawer_size[drawer_idx][0] - 2 * self.left_right_inner_size[drawer_idx],
                                       self.rear_front_inner_size[drawer_idx],
                                       position=mesh_position)
                elif mesh_idx == 4:
                    mesh_position = [self.drawer_offset[drawer_idx][0],
                                     -self.drawer_size[drawer_idx][1] / 2 + self.drawer_offset[drawer_idx][1] -
                                     self.bottom_size[drawer_idx] / 2,
                                     self.drawer_offset[drawer_idx][2]]
                    self.mesh = Cuboid(self.bottom_size[drawer_idx],
                                       self.drawer_size[drawer_idx][0],
                                       self.drawer_size[drawer_idx][2],
                                       position=mesh_position)
                elif mesh_idx == 5:
                    mesh_position = [self.drawer_offset[drawer_idx][0],
                                     self.drawer_offset[drawer_idx][1] +
                                     self.front_offset[drawer_idx],
                                     self.drawer_offset[drawer_idx][2] + self.drawer_size[drawer_idx][2] / 2 +
                                     self.front_size[drawer_idx][2] / 2]
                    self.mesh = Cuboid(self.front_size[drawer_idx][1],
                                       self.front_size[drawer_idx][0],
                                       self.front_size[drawer_idx][2],
                                       position=mesh_position)
                else:
                    if self.number_of_handle[drawer_idx] == 2:
                        position_sign = 1 if mesh_idx == 6 else -1
                    else:
                        position_sign = 0
                    mesh_position = [self.drawer_offset[drawer_idx][0] + self.handle_offset[drawer_idx][0] +
                                     position_sign * self.handle_separation[drawer_idx] / 2,
                                     self.drawer_offset[drawer_idx][1] + self.handle_offset[drawer_idx][1],
                                     self.drawer_offset[drawer_idx][2] + self.drawer_size[drawer_idx][2] / 2 +
                                     self.front_size[drawer_idx][2] + self.front_size[drawer_idx][2] / 2]
                    self.mesh = Cuboid(self.handle_sizes[drawer_idx][1], self.handle_sizes[drawer_idx][0], self.handle_sizes[drawer_idx][2],
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

        self.semantic = 'Drawer'


# Source: Table/concept_template.py
class Regular_drawer(ConceptTemplate):
    def __init__(self, number_of_drawer, drawers_params, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        drawers_params = [x / 180 * np.pi if i % 21 in [14] else x for i, x in enumerate(drawers_params)]
        super().__init__(position, rotation)

        # Record Parameters
        self.number_of_drawer = number_of_drawer
        self.drawer_size = [drawers_params[i * 21: i * 21 + 3] for i in range(number_of_drawer[0])]
        self.bottom_size = [drawers_params[i * 21 + 3] for i in range(number_of_drawer[0])]
        self.front_size = [drawers_params[i * 21 + 4: i * 21 + 7] for i in range(number_of_drawer[0])]
        self.front_offset = [drawers_params[i * 21 + 7] for i in range(number_of_drawer[0])]
        self.left_right_inner_size = [drawers_params[i * 21 + 8] for i in range(number_of_drawer[0])]
        self.rear_front_inner_size = [drawers_params[i * 21 + 9] for i in range(number_of_drawer[0])]
        self.number_of_handle = [drawers_params[i * 21 + 10] for i in range(number_of_drawer[0])]
        self.handle_sizes = [drawers_params[i * 21 + 11: i * 21 + 14] for i in range(number_of_drawer[0])]
        self.handle_rotation = [drawers_params[i * 21 + 14] for i in range(number_of_drawer[0])]
        self.handle_offset = [drawers_params[i * 21 + 15: i * 21 + 17] for i in range(number_of_drawer[0])]
        self.handle_separation = [drawers_params[i * 21 + 17] for i in range(number_of_drawer[0])]
        self.drawer_offset = [drawers_params[i * 21 + 18: i * 21 + 21] for i in range(number_of_drawer[0])]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for drawer_idx in range(number_of_drawer[0]):
            for mesh_idx in range(6 + self.number_of_handle[drawer_idx]):
                if mesh_idx < 2:
                    position_sign = -1 if mesh_idx == 0 else 1
                    mesh_position = [position_sign * (
                            self.drawer_size[drawer_idx][0] - self.left_right_inner_size[drawer_idx]) / 2 +
                                     self.drawer_offset[drawer_idx][0],
                                     -self.drawer_size[drawer_idx][1] / 2 + self.drawer_offset[drawer_idx][1],
                                     self.drawer_offset[drawer_idx][2]]
                    self.mesh = Cuboid(self.drawer_size[drawer_idx][1],
                                       self.left_right_inner_size[drawer_idx],
                                       self.drawer_size[drawer_idx][2],
                                       position=mesh_position)
                elif mesh_idx < 4:
                    position_sign = -1 if mesh_idx == 3 else 1
                    mesh_position = [self.drawer_offset[drawer_idx][0],
                                     -self.drawer_size[drawer_idx][1] / 2 + self.drawer_offset[drawer_idx][1],
                                     position_sign * (
                                             self.drawer_size[drawer_idx][2] - self.rear_front_inner_size[drawer_idx]) / 2 + self.drawer_offset[drawer_idx][2]]
                    self.mesh = Cuboid(self.drawer_size[drawer_idx][1],
                                       self.drawer_size[drawer_idx][0] - 2 * self.left_right_inner_size[drawer_idx],
                                       self.rear_front_inner_size[drawer_idx],
                                       position=mesh_position)
                elif mesh_idx == 4:
                    mesh_position = [self.drawer_offset[drawer_idx][0],
                                     -self.drawer_size[drawer_idx][1] + self.drawer_offset[drawer_idx][1] - self.bottom_size[drawer_idx] / 2,
                                     self.drawer_offset[drawer_idx][2]]
                    self.mesh = Cuboid(self.bottom_size[drawer_idx],
                                       self.drawer_size[drawer_idx][0],
                                       self.drawer_size[drawer_idx][2],
                                       position=mesh_position)
                elif mesh_idx == 5:
                    mesh_position = [self.drawer_offset[drawer_idx][0],
                                     -self.drawer_size[drawer_idx][1] / 2 + self.drawer_offset[drawer_idx][1] +
                                     self.front_offset[drawer_idx],
                                     self.drawer_offset[drawer_idx][2] + self.drawer_size[drawer_idx][2] / 2 +
                                     self.front_size[drawer_idx][2] / 2]
                    self.mesh = Cuboid(self.front_size[drawer_idx][1],
                                       self.front_size[drawer_idx][0],
                                       self.front_size[drawer_idx][2],
                                       position=mesh_position)
                else:
                    if self.number_of_handle[drawer_idx] == 2:
                        position_sign = 1 if mesh_idx == 6 else -1
                    else:
                        position_sign = 0
                    mesh_rotation = [0, 0, self.handle_rotation[drawer_idx]]
                    mesh_position = [self.drawer_offset[drawer_idx][0] + self.handle_offset[drawer_idx][0] +
                                     position_sign * self.handle_separation[drawer_idx] / 2,
                                     -self.drawer_size[drawer_idx][1] / 2 + self.drawer_offset[drawer_idx][1] +
                                     self.handle_offset[drawer_idx][0],
                                     self.drawer_offset[drawer_idx][2] + self.drawer_size[drawer_idx][2] / 2 +
                                     self.front_size[drawer_idx][2] + self.front_size[drawer_idx][2] / 2]
                    self.mesh = Cuboid(self.handle_sizes[drawer_idx][1], self.handle_sizes[drawer_idx][0], self.handle_sizes[drawer_idx][2],
                                       position=mesh_position, rotation=mesh_rotation)
                vertices_list.append(self.mesh.vertices)
                faces_list.append(self.mesh.faces + total_num_vertices)
                total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Drawer'
