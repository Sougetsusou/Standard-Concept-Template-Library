"""
Leg Templates
Automatically extracted from concept_template.py files
Contains 21 class(es)
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


# Source: Safe/concept_template.py
class Cuboidal_Leg(ConceptTemplate):
    def __init__(self, front_legs_size, rear_legs_size, legs_separation, num_legs, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.front_legs_size = front_legs_size
        self.rear_legs_size = rear_legs_size
        self.legs_separation = legs_separation
        self.num_legs = num_legs

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        if (num_legs[0] == 1):
            mesh_position = [
                0,
                -front_legs_size[1] / 2,
                0
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        elif (num_legs[0] == 2):
            mesh_position = [
                legs_separation[0] / 2, 
                -front_legs_size[1] / 2,
                0
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                -legs_separation[0] / 2,
                -front_legs_size[1] / 2,
                0
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        elif (num_legs[0] == 3):
            mesh_position = [
                legs_separation[0] / 2,
                -front_legs_size[1] / 2,
                legs_separation[2] / 2
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                -legs_separation[0] / 2,
                -front_legs_size[1] / 2,
                legs_separation[2] / 2
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                0,
                -rear_legs_size[1] / 2,
                -legs_separation[2] / 2
            ]
            self.mesh = Cuboid(rear_legs_size[1], rear_legs_size[0], rear_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        elif (num_legs[0] == 4):
            mesh_position = [
                legs_separation[0] / 2,
                -front_legs_size[1] / 2,
                legs_separation[2] / 2
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                -legs_separation[0] / 2,
                -front_legs_size[1] / 2,
                legs_separation[2] / 2
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                legs_separation[1] / 2,
                -rear_legs_size[1] / 2,
                -legs_separation[2] / 2
            ]
            self.mesh = Cuboid(rear_legs_size[1], rear_legs_size[0], rear_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                -legs_separation[1] / 2,
                -rear_legs_size[1] / 2,
                -legs_separation[2] / 2
            ]
            self.mesh = Cuboid(rear_legs_size[1], rear_legs_size[0], rear_legs_size[2],
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

        self.semantic = 'Leg'


# Source: Box/concept_template.py
class Cuboidal_Leg(ConceptTemplate):
    def __init__(self, front_legs_size, rear_legs_size, legs_separation, num_legs, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.front_legs_size = front_legs_size
        self.rear_legs_size = rear_legs_size
        self.legs_separation = legs_separation
        self.num_legs = num_legs

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        if (num_legs[0] == 1):
            mesh_position = [
                0,
                -front_legs_size[1] / 2,
                0
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        elif (num_legs[0] == 2):
            mesh_position = [
                legs_separation[0] / 2, 
                -front_legs_size[1] / 2,
                0
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                -legs_separation[0] / 2,
                -front_legs_size[1] / 2,
                0
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        elif (num_legs[0] == 3):
            mesh_position = [
                legs_separation[0] / 2,
                -front_legs_size[1] / 2,
                legs_separation[2] / 2
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                -legs_separation[0] / 2,
                -front_legs_size[1] / 2,
                legs_separation[2] / 2
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                0,
                -rear_legs_size[1] / 2,
                -legs_separation[2] / 2
            ]
            self.mesh = Cuboid(rear_legs_size[1], rear_legs_size[0], rear_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        elif (num_legs[0] == 4):
            mesh_position = [
                legs_separation[0] / 2,
                -front_legs_size[1] / 2,
                legs_separation[2] / 2
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                -legs_separation[0] / 2,
                -front_legs_size[1] / 2,
                legs_separation[2] / 2
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                legs_separation[1] / 2,
                -rear_legs_size[1] / 2,
                -legs_separation[2] / 2
            ]
            self.mesh = Cuboid(rear_legs_size[1], rear_legs_size[0], rear_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                -legs_separation[1] / 2,
                -rear_legs_size[1] / 2,
                -legs_separation[2] / 2
            ]
            self.mesh = Cuboid(rear_legs_size[1], rear_legs_size[0], rear_legs_size[2],
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

        self.semantic = 'Leg'


# Source: Oven/concept_template.py
class Multilevel_Leg(ConceptTemplate):
    def __init__(self, front_legs_size, rear_legs_size, legs_separation, num_legs, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.front_legs_size = front_legs_size
        self.rear_legs_size = rear_legs_size
        self.legs_separation = legs_separation
        self.num_legs = num_legs

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        if (num_legs[0] == 1):
            mesh_position = [
                0,
                -front_legs_size[1] / 2,
                0
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        elif (num_legs[0] == 2):
            mesh_position = [
                legs_separation[0] / 2, 
                -front_legs_size[1] / 2,
                0
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                -legs_separation[0] / 2,
                -front_legs_size[1] / 2,
                0
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        elif (num_legs[0] == 3):
            mesh_position = [
                legs_separation[0] / 2,
                -front_legs_size[1] / 2,
                legs_separation[2] / 2
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                -legs_separation[0] / 2,
                -front_legs_size[1] / 2,
                legs_separation[2] / 2
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                0,
                -rear_legs_size[1] / 2,
                -legs_separation[2] / 2
            ]
            self.mesh = Cuboid(rear_legs_size[1], rear_legs_size[0], rear_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        elif (num_legs[0] == 4):
            mesh_position = [
                legs_separation[0] / 2,
                -front_legs_size[1] / 2,
                legs_separation[2] / 2
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                -legs_separation[0] / 2,
                -front_legs_size[1] / 2,
                legs_separation[2] / 2
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                legs_separation[1] / 2,
                -rear_legs_size[1] / 2,
                -legs_separation[2] / 2
            ]
            self.mesh = Cuboid(rear_legs_size[1], rear_legs_size[0], rear_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                -legs_separation[1] / 2,
                -rear_legs_size[1] / 2,
                -legs_separation[2] / 2
            ]
            self.mesh = Cuboid(rear_legs_size[1], rear_legs_size[0], rear_legs_size[2],
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

        self.semantic = 'Leg'


# Source: Chair/concept_template.py
class Regular_leg(ConceptTemplate):
    def __init__(self, number_of_legs, legs_separation, central_rotation,
                 symmetry_mode, front_legs_size, front_rotation, rear_legs_size, rear_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):
        
        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        central_rotation = [x / 180 * np.pi for x in central_rotation]
        front_rotation = [x / 180 * np.pi for x in front_rotation]
        rear_rotation = [x / 180 * np.pi for x in rear_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.number_of_legs = number_of_legs
        self.legs_separation = legs_separation
        self.central_rotation = central_rotation
        self.symmetry_mode = symmetry_mode
        self.front_legs_size = front_legs_size
        self.front_rotation = front_rotation
        self.rear_legs_size = rear_legs_size
        self.rear_rotation = rear_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(number_of_legs[0]):
            rotation_sign = 1 if (i % 2 == 0 or self.symmetry_mode[0] == 0) else -1
            position_sign = 1 if (i % 2 == 1) else -1
            if number_of_legs[0] == 1:
                mesh_rotation = [front_rotation[0], central_rotation[0], 0]
                mesh_position = [0, -front_legs_size[1] / 2 * np.cos(front_rotation[0]), 0]
                self.mesh = Cuboid(self.front_legs_size[1], self.front_legs_size[0], self.front_legs_size[2],
                                   position=mesh_position, rotation=mesh_rotation)
            if number_of_legs[0] == 2:
                mesh_rotation = [front_rotation[0], central_rotation[0], rotation_sign * front_rotation[1]]
                mesh_position = [position_sign * legs_separation[0] / 2 * np.cos(central_rotation[0]),
                                 -front_legs_size[1] / 2 * np.cos(front_rotation[0]) * np.cos(front_rotation[1]),
                                 position_sign * legs_separation[0] / 2 * np.sin(central_rotation[0])]
                self.mesh = Cuboid(self.front_legs_size[1], self.front_legs_size[0], self.front_legs_size[2],
                                   position=mesh_position, rotation=mesh_rotation, rotation_order="XZY")
            if number_of_legs[0] == 3:
                if i < 2:
                    mesh_rotation = [front_rotation[0], central_rotation[0], rotation_sign * front_rotation[1]]
                    mesh_position = [
                        position_sign * legs_separation[0] / 2 * np.cos(central_rotation[0]) + legs_separation[
                            2] / 2 * np.sin(central_rotation[0]),
                        -front_legs_size[1] / 2 * np.cos(front_rotation[0]) * np.cos(front_rotation[1]),
                        -position_sign * legs_separation[0] / 2 * np.sin(central_rotation[0]) + legs_separation[
                            2] / 2 * np.cos(central_rotation[0])]
                    self.mesh = Cuboid(self.front_legs_size[1], self.front_legs_size[0], self.front_legs_size[2],
                                       position=mesh_position, rotation=mesh_rotation, rotation_order="XZY")
                else:
                    mesh_rotation = [rear_rotation[0], central_rotation[0], rear_rotation[1]]
                    mesh_position = [position_sign * legs_separation[2] / 2 * np.sin(central_rotation[0]),
                                     -rear_legs_size[1] / 2 * np.cos(rear_rotation[0]) * np.cos(rear_rotation[1]),
                                     position_sign * legs_separation[2] / 2 * np.cos(central_rotation[0])]
                    self.mesh = Cuboid(self.rear_legs_size[1], self.rear_legs_size[0], self.rear_legs_size[2],
                                       position=mesh_position, rotation=mesh_rotation, rotation_order="XZY")
            if number_of_legs[0] == 4:
                if i < 2:
                    mesh_rotation = [front_rotation[0], central_rotation[0], rotation_sign * front_rotation[1]]
                    mesh_position = [
                        position_sign * legs_separation[0] / 2 * np.cos(central_rotation[0]) + legs_separation[
                            2] / 2 * np.sin(central_rotation[0]),
                        -front_legs_size[1] / 2 * np.cos(front_rotation[0]) * np.cos(front_rotation[1]),
                        -position_sign * legs_separation[0] / 2 * np.sin(central_rotation[0]) + legs_separation[
                            2] / 2 * np.cos(central_rotation[0])]
                    self.mesh = Cuboid(self.front_legs_size[1], self.front_legs_size[0], self.front_legs_size[2],
                                       position=mesh_position, rotation=mesh_rotation, rotation_order="XZY")
                else:
                    mesh_rotation = [rear_rotation[0], central_rotation[0], rotation_sign * rear_rotation[1]]
                    mesh_position = [
                        position_sign * legs_separation[1] / 2 * np.cos(central_rotation[0]) - legs_separation[
                            2] / 2 * np.sin(central_rotation[0]),
                        -rear_legs_size[1] / 2 * np.cos(rear_rotation[0]) * np.cos(rear_rotation[1]),
                        -position_sign * legs_separation[1] / 2 * np.sin(central_rotation[0]) - legs_separation[
                            2] / 2 * np.cos(central_rotation[0])]
                    self.mesh = Cuboid(self.rear_legs_size[1], self.rear_legs_size[0], self.rear_legs_size[2],
                                       position=mesh_position, rotation=mesh_rotation, rotation_order="XZY")

            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Leg'


# Source: Chair/concept_template.py
class C_shaped_office_leg(ConceptTemplate):
    def __init__(self, vertical_leg_size, horizontal_z_leg_size, horizontal_x_leg_size,
                 vertical_leg_separation, vertical_leg_rotation, horizontal_leg_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        vertical_leg_rotation = [x / 180 * np.pi for x in vertical_leg_rotation]
        horizontal_leg_rotation = [x / 180 * np.pi for x in horizontal_leg_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.vertical_leg_size = vertical_leg_size
        self.horizontal_z_leg_size = horizontal_z_leg_size
        self.horizontal_x_leg_size = horizontal_x_leg_size
        self.vertical_leg_separation = vertical_leg_separation
        self.vertical_leg_rotation = vertical_leg_rotation
        self.horizontal_leg_rotation = horizontal_leg_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(5):
            rotation_sign = -1 if (i % 2 == 1) else 1
            position_sign = -1 if (i % 2 == 1) else 1
            if i < 2:
                mesh_rotation = [vertical_leg_rotation[0], 0, rotation_sign * vertical_leg_rotation[1]]
                mesh_position = [position_sign * vertical_leg_separation[0] / 2,
                                 -vertical_leg_size[1] / 2 * np.cos(vertical_leg_rotation[0]) * np.cos(
                                     vertical_leg_rotation[1]), 0]
                self.mesh = Cuboid(self.vertical_leg_size[1], self.vertical_leg_size[0], self.vertical_leg_size[2],
                                   position=mesh_position, rotation=mesh_rotation, rotation_order="ZXY")
            elif i < 4:
                mesh_rotation = [horizontal_leg_rotation[0], rotation_sign * horizontal_leg_rotation[1], 0]
                mesh_position = [position_sign * (vertical_leg_separation[0] / 2 + vertical_leg_size[1] / 2 * np.sin(
                    vertical_leg_rotation[1]) - horizontal_z_leg_size[1] / 2 * np.sin(horizontal_leg_rotation[1])),
                                 -(vertical_leg_size[1] - horizontal_z_leg_size[0] / 2) * np.cos(
                                     vertical_leg_rotation[0]) * np.cos(
                                     vertical_leg_rotation[1]) + (
                                         horizontal_z_leg_size[1] + horizontal_z_leg_size[0]) / 2 * np.sin(
                                     horizontal_leg_rotation[0]),
                                 -vertical_leg_size[1] / 2 * np.cos(vertical_leg_rotation[1]) * np.sin(
                                     vertical_leg_rotation[0]) - (
                                         vertical_leg_size[2] + horizontal_z_leg_size[1]) / 2 * np.cos(
                                     horizontal_leg_rotation[1]) * np.cos(horizontal_leg_rotation[0])]
                self.mesh = Cuboid(self.horizontal_z_leg_size[0], self.vertical_leg_size[0],
                                   self.horizontal_z_leg_size[1],
                                   position=mesh_position, rotation=mesh_rotation, rotation_order="YXZ")
            else:
                mesh_rotation = [horizontal_leg_rotation[0], 0, 0]
                mesh_position = [0,
                                 -(vertical_leg_size[1] - horizontal_z_leg_size[0] / 2) * np.cos(
                                     vertical_leg_rotation[0]) * np.cos(
                                     vertical_leg_rotation[1]) + (
                                         horizontal_z_leg_size[1] * 2 + horizontal_z_leg_size[0] +
                                         horizontal_x_leg_size[0]) / 2 * np.sin(horizontal_leg_rotation[0]),
                                 -vertical_leg_size[1] / 2 * np.cos(vertical_leg_rotation[1]) * np.sin(
                                     vertical_leg_rotation[0]) - (vertical_leg_size[2] + horizontal_z_leg_size[1] * 2 +
                                                                  horizontal_x_leg_size[0]) / 2 * np.cos(
                                     horizontal_leg_rotation[1]) * np.cos(horizontal_leg_rotation[0])]
                self.mesh = Cuboid(self.horizontal_z_leg_size[0],
                                   vertical_leg_separation[0] + vertical_leg_size[0] + vertical_leg_size[1] * np.sin(
                                       vertical_leg_rotation[1]) - 2 * (
                                           horizontal_z_leg_size[1] + vertical_leg_size[2] / 2 +
                                           horizontal_x_leg_size[0] / 2) * np.sin(horizontal_leg_rotation[1]),
                                   self.horizontal_x_leg_size[0],
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

        self.semantic = 'Leg'


# Source: Chair/concept_template.py
class Star_leg(ConceptTemplate):
    def __init__(self, vertical_sizes, sub_sizes, sub_central_offset,
                 tilt_angle, central_rotation, horizontal_rotation, number_of_sub_legs,
                 position=[0, 0, 0], rotation=[0, 0, 0]):
        
        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        tilt_angle = [x / 180 * np.pi for x in tilt_angle]
        central_rotation = [x / 180 * np.pi for x in central_rotation]
        horizontal_rotation = [x / 180 * np.pi for x in horizontal_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.vertical_sizes = vertical_sizes
        self.sub_sizes = sub_sizes
        self.sub_central_offset = sub_central_offset
        self.tilt_angle = tilt_angle
        self.central_rotation = central_rotation
        self.horizontal_rotation = horizontal_rotation
        self.number_of_sub_legs = number_of_sub_legs

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(1 + number_of_sub_legs[0]):
            if i == 0:
                mesh_rotation = [horizontal_rotation[0], central_rotation[0], 0]
                mesh_position = [0, 0, 0]
                self.mesh = Cylinder(vertical_sizes[1], vertical_sizes[0], position=mesh_position,
                                     rotation=mesh_rotation)
            else:
                sub_rotation = np.pi / number_of_sub_legs[0] * (i - 1) * 2
                mesh_position = [
                    -(sub_sizes[2] / 2 * np.cos(tilt_angle[0]) * np.sin(sub_rotation)) * np.cos(central_rotation[0]) + (
                            sub_sizes[2] / 2 * np.cos(tilt_angle[0]) * np.cos(sub_rotation)) * np.sin(
                        central_rotation[0]),
                    (-vertical_sizes[1] / 2 + sub_sizes[1] / 2 + sub_central_offset[0]) * np.cos(horizontal_rotation[0]) - (
                            (sub_sizes[2] / 2 * np.cos(tilt_angle[0]) * np.cos(sub_rotation)) * np.cos(
                        central_rotation[0]) + (
                                    sub_sizes[2] / 2 * np.cos(tilt_angle[0]) * np.sin(sub_rotation)) * np.sin(
                        central_rotation[0])) * np.sin(horizontal_rotation[0]),
                    ((sub_sizes[2] / 2 * np.cos(tilt_angle[0]) * np.cos(sub_rotation)) * np.cos(central_rotation[0]) + (
                            sub_sizes[2] / 2 * np.cos(tilt_angle[0]) * np.sin(sub_rotation)) * np.sin(
                        central_rotation[0])) * np.cos(horizontal_rotation[0]) + (
                            -vertical_sizes[1] + sub_sizes[1] / 2 + sub_central_offset[0]) * np.sin(
                        horizontal_rotation[0]) + vertical_sizes[1] / 2 * np.sin(horizontal_rotation[0])]
                self.mesh = Cuboid(sub_sizes[1], sub_sizes[0], sub_sizes[2])

                tilt_mat = np.array(get_rodrigues_matrix([1, 0, 0], tilt_angle[0]))
                self.mesh.vertices = np.matmul(self.mesh.vertices, tilt_mat.T)
                sub_mat = np.array(get_rodrigues_matrix([0, 1, 0], -sub_rotation))
                self.mesh.vertices = np.matmul(self.mesh.vertices, sub_mat.T)

                cen_mat4 = np.array(get_rodrigues_matrix([0, 1, 0], central_rotation[0]))
                self.mesh.vertices = np.matmul(self.mesh.vertices, cen_mat4.T)

                h_mat4 = np.array(get_rodrigues_matrix([1, 0, 0], horizontal_rotation[0]))
                self.mesh.vertices = np.matmul(self.mesh.vertices, h_mat4.T)

                self.mesh.vertices = apply_transformation(self.mesh.vertices, mesh_position, [0, 0, 0])


            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Leg'


# Source: Chair/concept_template.py
class Regular_leg_with_splat(ConceptTemplate):
    def __init__(self, front_legs_size, rear_legs_size, legs_separation,
                 central_rotation, front_rotation, rear_rotation,
                 front_rear_bridging_bars_sizes, left_right_bridging_bars_sizes, front_rear_bridging_bars_offset,
                 left_right_bridging_bars_offset, bridging_bars_existance, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        central_rotation = [x / 180 * np.pi for x in central_rotation]
        front_rotation = [x / 180 * np.pi for x in front_rotation]
        rear_rotation = [x / 180 * np.pi for x in rear_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.front_legs_size = front_legs_size
        self.rear_legs_size = rear_legs_size
        self.legs_separation = legs_separation
        self.central_rotation = central_rotation
        self.front_rotation = front_rotation
        self.rear_rotation = rear_rotation
        self.front_rear_bridging_bars_sizes = front_rear_bridging_bars_sizes
        self.left_right_bridging_bars_sizes = left_right_bridging_bars_sizes
        self.front_rear_bridging_bars_offset = front_rear_bridging_bars_offset
        self.left_right_bridging_bars_offset = left_right_bridging_bars_offset
        self.bridging_bars_existance = bridging_bars_existance

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(4):
            rotation_sign = -1 if (i % 2 == 1) else 1
            position_sign = -1 if (i % 2 == 0) else 1
            if i < 2:
                mesh_rotation = [front_rotation[0], central_rotation[0], rotation_sign * front_rotation[1]]
                mesh_position = [
                    position_sign * legs_separation[0] / 2 * np.cos(central_rotation[0]) + legs_separation[
                        2] / 2 * np.sin(central_rotation[0]),
                    -front_legs_size[1] / 2 * np.cos(front_rotation[0]) * np.cos(front_rotation[1]),
                    -position_sign * legs_separation[0] / 2 * np.sin(central_rotation[0]) + legs_separation[
                        2] / 2 * np.cos(central_rotation[0])]
                self.mesh = Cuboid(self.front_legs_size[1], self.front_legs_size[0], self.front_legs_size[2],
                                   position=mesh_position, rotation=mesh_rotation, rotation_order="XZY")
            else:
                mesh_rotation = [rear_rotation[0], central_rotation[0], rotation_sign * rear_rotation[1]]
                mesh_position = [
                        position_sign * legs_separation[1] / 2 * np.cos(central_rotation[0]) - legs_separation[
                            2] / 2 * np.sin(central_rotation[0]),
                        -rear_legs_size[1] / 2 * np.cos(rear_rotation[0]) * np.cos(rear_rotation[1]),
                        -position_sign * legs_separation[1] / 2 * np.sin(central_rotation[0]) - legs_separation[
                            2] / 2 * np.cos(central_rotation[0])]
                self.mesh = Cuboid(self.rear_legs_size[1], self.rear_legs_size[0], self.rear_legs_size[2],
                                   position=mesh_position, rotation=mesh_rotation, rotation_order="XZY")

            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        if bridging_bars_existance[0] == 1:
            mesh_rotation = [front_rotation[0], central_rotation[0], 0]
            mesh_position = [
                (legs_separation[2] / 2 + front_rear_bridging_bars_offset[0] * np.sin(front_rotation[0])) * np.sin(
                    central_rotation[0]),
                -(front_legs_size[1] / 2 - front_rear_bridging_bars_offset[0]) * np.cos(front_rotation[0]) * np.cos(
                    front_rotation[1]),
                (legs_separation[2] / 2 + front_rear_bridging_bars_offset[0] * np.sin(front_rotation[0])) * np.cos(
                    central_rotation[0])]
            self.mesh = Cuboid(front_rear_bridging_bars_sizes[0],
                               legs_separation[0] - front_legs_size[0] + front_rear_bridging_bars_offset[0] * np.sin(
                                   front_rotation[1]) * 2,
                               front_rear_bridging_bars_sizes[1],
                               position=mesh_position, rotation=mesh_rotation, rotation_order="XZY")
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        if bridging_bars_existance[1] == 1:
            mesh_rotation = [rear_rotation[0], central_rotation[0], 0]
            mesh_position = [
                (-legs_separation[2] / 2 + front_rear_bridging_bars_offset[1] * np.sin(rear_rotation[0])) * np.sin(
                    central_rotation[0]),
                -(rear_legs_size[1] / 2 - front_rear_bridging_bars_offset[1]) * np.cos(rear_rotation[0]) * np.cos(
                    rear_rotation[1]),
                (-legs_separation[2] / 2 + front_rear_bridging_bars_offset[1] * np.sin(rear_rotation[0])) * np.cos(
                    central_rotation[0])]
            self.mesh = Cuboid(front_rear_bridging_bars_sizes[0],
                               legs_separation[1] - rear_legs_size[0] + front_rear_bridging_bars_offset[1] * np.sin(
                                   front_rotation[1]) * 2,
                               front_rear_bridging_bars_sizes[1],
                               position=mesh_position, rotation=mesh_rotation, rotation_order="XZY")
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        if bridging_bars_existance[2] == 1:

            fr_an_x = - legs_separation[0] / 2 - left_right_bridging_bars_offset[0] * np.cos(
                front_rotation[0]) * np.sin(front_rotation[1])
            fr_an_y = -(front_legs_size[1] / 2 - left_right_bridging_bars_offset[0]) * np.cos(
                front_rotation[0]) * np.cos(front_rotation[1])
            fr_an_z = legs_separation[2] / 2 + left_right_bridging_bars_offset[0] * np.sin(
                front_rotation[0])

            re_an_x = - legs_separation[1] / 2 - left_right_bridging_bars_offset[1] * np.cos(
                rear_rotation[0]) * np.sin(rear_rotation[1])
            re_an_y = -(rear_legs_size[1] / 2 - left_right_bridging_bars_offset[1]) * np.cos(
                rear_rotation[0]) * np.cos(rear_rotation[1])
            re_an_z = - legs_separation[2] / 2 + left_right_bridging_bars_offset[1] * np.sin(
                rear_rotation[0])

            diff_x, diff_y, diff_z = fr_an_x - re_an_x, fr_an_y - re_an_y, fr_an_z - re_an_z
            diff_norm = np.sqrt(diff_x ** 2 + diff_y ** 2 + diff_z ** 2)

            if diff_norm > 0:
                mesh_rotation = [-np.arcsin(diff_y / diff_norm), np.arctan(diff_x / np.sign(diff_z) / (np.abs(diff_z) + 1e-7)) + central_rotation[0], 0]
                mesh_position = [
                    (fr_an_x + re_an_x) / 2 * np.cos(central_rotation[0]) + (fr_an_z + re_an_z) / 2 * np.sin(
                        central_rotation[0]),
                    (fr_an_y + re_an_y) / 2,
                    (fr_an_z + re_an_z) / 2 * np.cos(central_rotation[0]) - (fr_an_x + re_an_x) / 2 * np.sin(
                        central_rotation[0])
                ]

                self.mesh = Cuboid(
                    left_right_bridging_bars_sizes[1],
                    left_right_bridging_bars_sizes[0],
                    diff_norm - (front_legs_size[2] + rear_legs_size[2]) / 2,
                    position=mesh_position,
                    rotation=mesh_rotation, rotation_order="XZY"
                )
                vertices_list.append(self.mesh.vertices)
                faces_list.append(self.mesh.faces + total_num_vertices)
                total_num_vertices += len(self.mesh.vertices)

        if bridging_bars_existance[3] == 1:

            fr_an_x = legs_separation[0] / 2 + left_right_bridging_bars_offset[0] * np.cos(
                front_rotation[0]) * np.sin(front_rotation[1])
            fr_an_y = -(front_legs_size[1] / 2 - left_right_bridging_bars_offset[0]) * np.cos(
                front_rotation[0]) * np.cos(front_rotation[1])
            fr_an_z = legs_separation[2] / 2 + left_right_bridging_bars_offset[0] * np.sin(
                front_rotation[0])

            re_an_x = legs_separation[1] / 2 + left_right_bridging_bars_offset[1] * np.cos(
                rear_rotation[0]) * np.sin(rear_rotation[1])
            re_an_y = -(front_legs_size[1] / 2 - left_right_bridging_bars_offset[1]) * np.cos(
                rear_rotation[0]) * np.cos(rear_rotation[1])
            re_an_z = - legs_separation[2] / 2 + left_right_bridging_bars_offset[1] * np.sin(
                rear_rotation[0])

            diff_x, diff_y, diff_z = fr_an_x - re_an_x, fr_an_y - re_an_y, fr_an_z - re_an_z
            diff_norm = np.sqrt(diff_x ** 2 + diff_y ** 2 + diff_z ** 2)

            if diff_norm > 0:

                mesh_rotation = [-np.arcsin(diff_y / diff_norm), np.arctan(diff_x / np.sign(diff_z) / (np.abs(diff_z) + 1e-7)) + central_rotation[0], 0]
                mesh_position = [
                    (fr_an_x + re_an_x) / 2 * np.cos(central_rotation[0]) + (fr_an_z + re_an_z) / 2 * np.sin(
                        central_rotation[0]),
                    (fr_an_y + re_an_y) / 2,
                    (fr_an_z + re_an_z) / 2 * np.cos(central_rotation[0]) - (fr_an_x + re_an_x) / 2 * np.sin(
                        central_rotation[0])
                ]

                self.mesh = Cuboid(
                    left_right_bridging_bars_sizes[1],
                    left_right_bridging_bars_sizes[0],
                    diff_norm - (front_legs_size[2] + rear_legs_size[2]) / 2,
                    position=mesh_position,
                    rotation=mesh_rotation, rotation_order="XZY"
                )
                vertices_list.append(self.mesh.vertices)
                faces_list.append(self.mesh.faces + total_num_vertices)
                total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Leg'


# Source: Chair/concept_template.py
class Barstool_leg(ConceptTemplate):
    def __init__(self, vertical_sizes, bottom_sizes, horizontal_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):
        
        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        horizontal_rotation = [x / 180 * np.pi for x in horizontal_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.vertical_sizes = vertical_sizes
        self.bottom_sizes = bottom_sizes
        self.horizontal_rotation = horizontal_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_rotation = [horizontal_rotation[0], 0, 0]
        mesh_position = [0, -vertical_sizes[1] / 2 * np.cos(horizontal_rotation[0]), 0]
        self.support_mesh = Cylinder(vertical_sizes[1], vertical_sizes[0], position=mesh_position,
                                     rotation=mesh_rotation)
        vertices_list.append(self.support_mesh.vertices)
        faces_list.append(self.support_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.support_mesh.vertices)

        mesh_rotation = [horizontal_rotation[0], 0, 0]
        mesh_position = [0, (-vertical_sizes[1] - bottom_sizes[1] / 2) * np.cos(horizontal_rotation[0]),
                         (vertical_sizes[1] - bottom_sizes[1]) / 2 * np.sin(horizontal_rotation[0])]
        self.bottom_mesh = Cylinder(bottom_sizes[1], bottom_sizes[0], position=mesh_position,
                                    rotation=mesh_rotation)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Leg'


# Source: Dishwasher/concept_template.py
class Single_Leg(ConceptTemplate):
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
            -size[1] / 2,
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

        self.semantic = 'Leg'


# Source: Dishwasher/concept_template.py
class Multilevel_Leg(ConceptTemplate):
    def __init__(self, has_top_part, top_size, top_bottom_offset, front_legs_size, rear_legs_size, legs_separation, num_legs, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.has_top_part = has_top_part
        self.top_size = top_size
        self.top_bottom_offset = top_bottom_offset
        self.front_legs_size = front_legs_size
        self.rear_legs_size = rear_legs_size
        self.legs_separation = legs_separation
        self.num_legs = num_legs

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        top_offset = 0
        if (has_top_part[0] == 1):
            mesh_position = [
                0,
                -top_size[1] / 2,
                0
            ]
            self.mesh = Cuboid(top_size[1], top_size[0], top_size[2],
                                 position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)
            top_offset = top_size[1]

        if (num_legs[0] == 1):
            mesh_position = [
                top_bottom_offset[0],
                -top_offset - front_legs_size[1] / 2,
                top_bottom_offset[1]
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        elif (num_legs[0] == 2):
            mesh_position = [
                legs_separation[0] / 2 + top_bottom_offset[0], 
                -top_offset - front_legs_size[1] / 2,
                top_bottom_offset[1]
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                -legs_separation[0] / 2 + top_bottom_offset[0],
                -top_offset - front_legs_size[1] / 2,
                top_bottom_offset[1]
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        elif (num_legs[0] == 3):
            mesh_position = [
                legs_separation[0] / 2 + top_bottom_offset[0],
                -top_offset - front_legs_size[1] / 2,
                legs_separation[2] / 2 + top_bottom_offset[1]
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                -legs_separation[0] / 2 + top_bottom_offset[0],
                -top_offset - front_legs_size[1] / 2,
                legs_separation[2] / 2 + top_bottom_offset[1]
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                top_bottom_offset[0],
                -top_offset - rear_legs_size[1] / 2,
                -legs_separation[2] / 2 + top_bottom_offset[1]
            ]
            self.mesh = Cuboid(rear_legs_size[1], rear_legs_size[0], rear_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        elif (num_legs[0] == 4):
            mesh_position = [
                legs_separation[0] / 2 + top_bottom_offset[0],
                -top_offset - front_legs_size[1] / 2,
                legs_separation[2] / 2 + top_bottom_offset[1]
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                -legs_separation[0] / 2 + top_bottom_offset[0],
                -top_offset - front_legs_size[1] / 2,
                legs_separation[2] / 2 + top_bottom_offset[1]
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                legs_separation[1] / 2 + top_bottom_offset[0],
                -top_offset - rear_legs_size[1] / 2,
                -legs_separation[2] / 2 + top_bottom_offset[1]
            ]
            self.mesh = Cuboid(rear_legs_size[1], rear_legs_size[0], rear_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                -legs_separation[1] / 2 + top_bottom_offset[0],
                -top_offset - rear_legs_size[1] / 2,
                -legs_separation[2] / 2 + top_bottom_offset[1]
            ]
            self.mesh = Cuboid(rear_legs_size[1], rear_legs_size[0], rear_legs_size[2],
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

        self.semantic = 'Leg'


# Source: StorageFurniture/concept_template.py
class Enclosed_leg(ConceptTemplate):
    def __init__(self, size, inner_sizes, additional_legs_params, position=[0, 0, 0], rotation=[0, 0, 0]):
        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        additional_legs_params = [additional_legs_params[0]] + [x / 180 * np.pi if (i - 1) % 9 in [6, 7, 8] else x for i, x in enumerate(additional_legs_params[1:], start=1)]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.inner_sizes = inner_sizes
        self.number_of_additional_legs = additional_legs_params[0]
        self.additional_legs_attributes = additional_legs_params[1:]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for mesh_idx in range(4):
            if size[0] <= 0.01 and size[2] <= 0.01:
                break
            position_sign = -1 if mesh_idx % 2 == 0 else 1
            if mesh_idx < 2:
                mesh_position = [position_sign * (size[0] - inner_sizes[0]) / 2, 0, 0]
                self.mesh = Cuboid(size[1], inner_sizes[0], size[2], position=mesh_position)
            else:
                mesh_position = [0, 0, position_sign * (size[2] - inner_sizes[1]) / 2]
                self.mesh = Cuboid(size[1], size[0], inner_sizes[1], position=mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        for i in range(self.number_of_additional_legs):
            mesh_position = [self.additional_legs_attributes[9 * i + 3],
                             self.additional_legs_attributes[9 * i + 4],
                             self.additional_legs_attributes[9 * i + 5]]
            mesh_rotation = [self.additional_legs_attributes[9 * i + 6],
                             self.additional_legs_attributes[9 * i + 7],
                             self.additional_legs_attributes[9 * i + 8]]
            self.additional_mesh = Cuboid(self.additional_legs_attributes[9 * i + 1],
                                          self.additional_legs_attributes[9 * i],
                                          self.additional_legs_attributes[9 * i + 2],
                                          position=mesh_position, rotation=mesh_rotation)
            vertices_list.append(self.additional_mesh.vertices)
            faces_list.append(self.additional_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.additional_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Leg'


# Source: Table/concept_template.py
class Regular_leg(ConceptTemplate):
    def __init__(self, front_legs_size, rear_legs_size, number_of_legs, legs_separation,
                 central_rotation, front_rotation, rear_rotation, symmetry_mode, additional_legs_params,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        central_rotation = [x / 180 * np.pi for x in central_rotation]
        front_rotation = [x / 180 * np.pi for x in front_rotation]
        rear_rotation = [x / 180 * np.pi for x in rear_rotation]
        additional_legs_params = [x / 180 * np.pi if ((i > 1) and ((i - 1) % 9 in [6, 7, 8])) else x for i, x in
                                  enumerate(additional_legs_params)]
        super().__init__(position, rotation)

        # Record Parameters
        self.front_legs_size = front_legs_size
        self.rear_legs_size = rear_legs_size
        self.number_of_legs = number_of_legs
        self.legs_separation = legs_separation
        self.central_rotation = central_rotation
        self.front_rotation = front_rotation
        self.rear_rotation = rear_rotation
        self.symmetry_mode = symmetry_mode
        self.number_of_additional_legs = additional_legs_params[0]
        self.additional_legs_attributes = additional_legs_params[1:]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(number_of_legs[0]):
            if number_of_legs[0] == 1:
                mesh_rotation = [front_rotation[0], central_rotation[0], 0]
                mesh_position = [0, -front_legs_size[1] * np.cos(front_rotation[0]) / 2, 0]
                self.mesh = Cuboid(self.front_legs_size[1], self.front_legs_size[0],
                                   self.front_legs_size[2],
                                   position=mesh_position, rotation=mesh_rotation)

            if number_of_legs[0] == 2:
                rotation_sign = 1 if (i == 0 or self.symmetry_mode == 0) else -1
                position_sign = 1 if i == 1 else -1
                mesh_rotation = [front_rotation[0], central_rotation[0], rotation_sign * front_rotation[1]]
                mesh_position = [position_sign * legs_separation[0] / 2 * np.cos(central_rotation[0]),
                                 -front_legs_size[1] / 2 * np.cos(front_rotation[0]),
                                 position_sign * legs_separation[0] / 2 * np.sin(central_rotation[0])]
                self.mesh = Cuboid(self.front_legs_size[1], self.front_legs_size[0],
                                   self.front_legs_size[2],
                                   position=mesh_position, rotation=mesh_rotation)

            if number_of_legs[0] == 3:
                rotation_sign = 1 if (i == 0 or self.symmetry_mode == 0) else -1
                position_sign = 1 if i == 1 else -1
                if i < 2:
                    mesh_rotation = [front_rotation[0], central_rotation[0], rotation_sign * front_rotation[1]]
                    mesh_position = [
                        position_sign * legs_separation[0] / 2 * np.cos(central_rotation[0]) + legs_separation[
                            2] / 2 * np.sin(central_rotation[0]),
                        -front_legs_size[1] / 2 * np.cos(front_rotation[0]) * np.cos(front_rotation[1]),
                        -position_sign * legs_separation[0] / 2 * np.sin(central_rotation[0]) + legs_separation[
                            2] / 2 * np.cos(central_rotation[0])]
                    size = front_legs_size
                else:
                    mesh_rotation = [rear_rotation[0], central_rotation[0], rear_rotation[1]]
                    mesh_position = [-legs_separation[2] / 2 * np.sin(central_rotation[0]),
                                     -rear_legs_size[1] / 2 * np.cos(rear_rotation[0]) * np.cos(rear_rotation[1]),
                                     -legs_separation[2] / 2 * np.cos(central_rotation[0])]
                    size = rear_legs_size
                self.mesh = Cuboid(size[1], size[0], size[2],
                                   position=mesh_position, rotation=mesh_rotation)

            if number_of_legs[0] == 4:
                rotation_sign = -1 if (i % 2 == 1 and symmetry_mode[0] == 1) else 1
                position_sign = 1 if (i % 2 == 1) else -1
                if i < 2:
                    mesh_rotation = [front_rotation[0], central_rotation[0], rotation_sign * front_rotation[1]]
                    mesh_position = [
                        position_sign * legs_separation[0] / 2 * np.cos(central_rotation[0]) + legs_separation[
                            2] / 2 * np.sin(central_rotation[0]),
                        -front_legs_size[1] / 2 * np.cos(front_rotation[0]) * np.cos(front_rotation[1]),
                        -position_sign * legs_separation[0] / 2 * np.sin(central_rotation[0]) + legs_separation[
                            2] / 2 * np.cos(central_rotation[0])]
                    size = front_legs_size
                else:
                    mesh_rotation = [rear_rotation[0], central_rotation[0], rotation_sign * rear_rotation[1]]
                    mesh_position = [
                        position_sign * legs_separation[1] / 2 * np.cos(central_rotation[0]) - legs_separation[
                            2] / 2 * np.sin(central_rotation[0]),
                        -front_legs_size[1] / 2 * np.cos(rear_rotation[0]) * np.cos(rear_rotation[1]),
                        -position_sign * legs_separation[1] / 2 * np.sin(central_rotation[0]) - legs_separation[
                            2] / 2 * np.cos(central_rotation[0])]
                    size = rear_legs_size
                self.mesh = Cuboid(size[1], size[0], size[2],
                                   position=mesh_position, rotation=mesh_rotation)

            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        for i in range(self.number_of_additional_legs):
            mesh_position = [self.additional_legs_attributes[9 * i + 3] - position[0],
                             self.additional_legs_attributes[9 * i + 4] -
                             self.additional_legs_attributes[9 * i + 1] * np.cos(self.additional_legs_attributes[9 * i + 6]) * np.cos(
                                 self.additional_legs_attributes[9 * i + 8]) / 2,
                             self.additional_legs_attributes[9 * i + 5] - position[2]]
            mesh_rotation = [self.additional_legs_attributes[9 * i + 6],
                             self.additional_legs_attributes[9 * i + 7],
                             self.additional_legs_attributes[9 * i + 8]]
            self.additional_mesh = Cuboid(self.additional_legs_attributes[9 * i + 1],
                                          self.additional_legs_attributes[9 * i],
                                          self.additional_legs_attributes[9 * i + 2],
                                          position=mesh_position, rotation=mesh_rotation)
            vertices_list.append(self.additional_mesh.vertices)
            faces_list.append(self.additional_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.additional_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Leg'


# Source: Table/concept_template.py
class Regular_with_splat_leg(ConceptTemplate):
    def __init__(self, front_legs_size, rear_legs_size, legs_separation,
                 central_rotation, front_rotation, rear_rotation,
                 front_rear_bridging_bars_sizes, left_right_bridging_bars_sizes,
                 front_rear_bridging_bars_offset, left_right_bridging_bars_offset, bridging_bars_existance,
                 additional_legs_params, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        central_rotation = [x / 180 * np.pi for x in central_rotation]
        front_rotation = [x / 180 * np.pi for x in front_rotation]
        rear_rotation = [x / 180 * np.pi for x in rear_rotation]
        additional_legs_params = [x / 180 * np.pi if ((i > 1) and ((i - 1) % 9 in [6, 7, 8])) else x for i, x in
                                  enumerate(additional_legs_params)]
        super().__init__(position, rotation)

        # Record Parameters
        self.front_legs_size = front_legs_size
        self.rear_legs_size = rear_legs_size
        self.legs_separation = legs_separation
        self.central_rotation = central_rotation
        self.front_rotation = front_rotation
        self.rear_rotation = rear_rotation
        self.front_rear_bridging_bars_sizes = front_rear_bridging_bars_sizes
        self.left_right_bridging_bars_sizes = left_right_bridging_bars_sizes
        self.front_rear_bridging_bars_offset = front_rear_bridging_bars_offset
        self.left_right_bridging_bars_offset = left_right_bridging_bars_offset
        self.bridging_bars_existance = bridging_bars_existance
        self.number_of_additional_legs = additional_legs_params[0]
        self.additional_legs_attributes = additional_legs_params[1:]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(4):
            rotation_sign = -1 if (i % 2 == 1) else 1
            position_sign = -1 if (i % 2 == 0) else 1
            if i < 2:
                mesh_rotation = [front_rotation[0], central_rotation[0], rotation_sign * front_rotation[1]]
                mesh_position = [
                    position_sign * legs_separation[0] / 2 * np.cos(central_rotation[0]) + legs_separation[
                        2] / 2 * np.sin(central_rotation[0]),
                    -front_legs_size[1] / 2 * np.cos(front_rotation[0]) * np.cos(front_rotation[1]),
                    -position_sign * legs_separation[0] / 2 * np.sin(central_rotation[0]) + legs_separation[
                        2] / 2 * np.cos(central_rotation[0])]
                self.mesh = Cuboid(self.front_legs_size[1], self.front_legs_size[0], self.front_legs_size[2],
                                   position=mesh_position, rotation=mesh_rotation)
            else:
                mesh_rotation = [rear_rotation[0], central_rotation[0], rotation_sign * rear_rotation[1]]
                mesh_position = [
                    position_sign * legs_separation[1] / 2 * np.cos(central_rotation[0]) - legs_separation[
                        2] / 2 * np.sin(central_rotation[0]),
                    -front_legs_size[1] / 2 * np.cos(front_rotation[0]) * np.cos(front_rotation[1]),
                    -position_sign * legs_separation[1] / 2 * np.sin(central_rotation[0]) - legs_separation[
                        2] / 2 * np.cos(central_rotation[0])]
                self.mesh = Cuboid(self.rear_legs_size[1], self.rear_legs_size[0], self.rear_legs_size[2],
                                   position=mesh_position, rotation=mesh_rotation)

            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        if bridging_bars_existance[0] == 1:
            mesh_rotation = [front_rotation[0], central_rotation[0], 0]
            mesh_position = [
                (legs_separation[2] / 2 + front_rear_bridging_bars_offset[0] * np.sin(front_rotation[0])) * np.sin(
                    central_rotation[0]),
                -(front_legs_size[1] / 2 - front_rear_bridging_bars_offset[0]) * np.cos(front_rotation[0]) * np.cos(
                    front_rotation[1]),
                (legs_separation[2] / 2 + front_rear_bridging_bars_offset[0] * np.sin(front_rotation[0])) * np.cos(
                    central_rotation[0])]
            self.mesh = Cuboid(front_rear_bridging_bars_sizes[0],
                               legs_separation[0] - front_legs_size[0] + front_rear_bridging_bars_offset[0] * np.sin(
                                   front_rotation[1]) * 2,
                               front_rear_bridging_bars_sizes[1],
                               position=mesh_position, rotation=mesh_rotation)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        if bridging_bars_existance[1] == 1:
            mesh_rotation = [rear_rotation[0], central_rotation[0], 0]
            mesh_position = [
                (-legs_separation[2] / 2 + front_rear_bridging_bars_offset[1] * np.sin(rear_rotation[0])) * np.sin(
                    central_rotation[0]),
                -(rear_legs_size[1] / 2 - front_rear_bridging_bars_offset[1]) * np.cos(rear_rotation[0]) * np.cos(
                    rear_rotation[1]),
                (-legs_separation[2] / 2 + front_rear_bridging_bars_offset[1] * np.sin(rear_rotation[0])) * np.cos(
                    central_rotation[0])]
            self.mesh = Cuboid(front_rear_bridging_bars_sizes[0],
                               legs_separation[1] - rear_legs_size[0] + front_rear_bridging_bars_offset[1] * np.sin(
                                   front_rotation[1]) * 2,
                               front_rear_bridging_bars_sizes[1],
                               position=mesh_position, rotation=mesh_rotation)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        if bridging_bars_existance[2] == 1:

            fr_an_x = - legs_separation[0] / 2 - left_right_bridging_bars_offset[0] * np.cos(
                front_rotation[0]) * np.sin(front_rotation[1])
            fr_an_y = -(front_legs_size[1] / 2 - left_right_bridging_bars_offset[0]) * np.cos(
                front_rotation[0]) * np.cos(front_rotation[1])
            fr_an_z = legs_separation[2] / 2 + left_right_bridging_bars_offset[0] * np.sin(
                front_rotation[0])

            re_an_x = - legs_separation[1] / 2 - left_right_bridging_bars_offset[1] * np.cos(
                rear_rotation[0]) * np.sin(rear_rotation[1])
            re_an_y = -(rear_legs_size[1] / 2 - left_right_bridging_bars_offset[1]) * np.cos(
                rear_rotation[0]) * np.cos(rear_rotation[1])
            re_an_z = - legs_separation[2] / 2 + left_right_bridging_bars_offset[1] * np.sin(
                rear_rotation[0])

            diff_x, diff_y, diff_z = fr_an_x - re_an_x, fr_an_y - re_an_y, fr_an_z - re_an_z
            diff_norm = np.sqrt(diff_x ** 2 + diff_y ** 2 + diff_z ** 2)

            if diff_norm > 0:
                mesh_rotation = [-np.arcsin(diff_y / diff_norm),
                                 np.arctan(diff_x / np.sign(diff_z) / (np.abs(diff_z) + 1e-7)) + central_rotation[0], 0]
                mesh_position = [
                    (fr_an_x + re_an_x) / 2 * np.cos(central_rotation[0]) + (fr_an_z + re_an_z) / 2 * np.sin(
                        central_rotation[0]),
                    (fr_an_y + re_an_y) / 2,
                    (fr_an_z + re_an_z) / 2 * np.cos(central_rotation[0]) - (fr_an_x + re_an_x) / 2 * np.sin(
                        central_rotation[0])
                ]

                self.mesh = Cuboid(
                    left_right_bridging_bars_sizes[1],
                    left_right_bridging_bars_sizes[0],
                    diff_norm - (front_legs_size[2] + rear_legs_size[2]) / 2,
                    position=mesh_position,
                    rotation=mesh_rotation
                )
                vertices_list.append(self.mesh.vertices)
                faces_list.append(self.mesh.faces + total_num_vertices)
                total_num_vertices += len(self.mesh.vertices)

        if bridging_bars_existance[3] == 1:

            fr_an_x = legs_separation[0] / 2 + left_right_bridging_bars_offset[0] * np.cos(
                front_rotation[0]) * np.sin(front_rotation[1])
            fr_an_y = -(front_legs_size[1] / 2 - left_right_bridging_bars_offset[0]) * np.cos(
                front_rotation[0]) * np.cos(front_rotation[1])
            fr_an_z = legs_separation[2] / 2 + left_right_bridging_bars_offset[0] * np.sin(
                front_rotation[0])

            re_an_x = legs_separation[1] / 2 + left_right_bridging_bars_offset[1] * np.cos(
                rear_rotation[0]) * np.sin(rear_rotation[1])
            re_an_y = -(front_legs_size[1] / 2 - left_right_bridging_bars_offset[1]) * np.cos(
                rear_rotation[0]) * np.cos(rear_rotation[1])
            re_an_z = - legs_separation[2] / 2 + left_right_bridging_bars_offset[1] * np.sin(
                rear_rotation[0])

            diff_x, diff_y, diff_z = fr_an_x - re_an_x, fr_an_y - re_an_y, fr_an_z - re_an_z
            diff_norm = np.sqrt(diff_x ** 2 + diff_y ** 2 + diff_z ** 2)

            if diff_norm > 0:
                mesh_rotation = [-np.arcsin(diff_y / diff_norm),
                                 np.arctan(diff_x / np.sign(diff_z) / (np.abs(diff_z) + 1e-7)) + central_rotation[0], 0]
                mesh_position = [
                    (fr_an_x + re_an_x) / 2 * np.cos(central_rotation[0]) + (fr_an_z + re_an_z) / 2 * np.sin(
                        central_rotation[0]),
                    (fr_an_y + re_an_y) / 2,
                    (fr_an_z + re_an_z) / 2 * np.cos(central_rotation[0]) - (fr_an_x + re_an_x) / 2 * np.sin(
                        central_rotation[0])
                ]

                self.mesh = Cuboid(
                    left_right_bridging_bars_sizes[1],
                    left_right_bridging_bars_sizes[0],
                    diff_norm - (front_legs_size[2] + rear_legs_size[2]) / 2,
                    position=mesh_position,
                    rotation=mesh_rotation
                )
                vertices_list.append(self.mesh.vertices)
                faces_list.append(self.mesh.faces + total_num_vertices)
                total_num_vertices += len(self.mesh.vertices)

        for i in range(self.number_of_additional_legs):
            mesh_position = [self.additional_legs_attributes[9 * i + 3] - position[0],
                             self.additional_legs_attributes[9 * i + 4] -
                             self.additional_legs_attributes[9 * i + 1] * np.cos(self.additional_legs_attributes[9 * i + 6]) * np.cos(
                                 self.additional_legs_attributes[9 * i + 8]) / 2,
                             self.additional_legs_attributes[9 * i + 5] - position[2]]
            mesh_rotation = [self.additional_legs_attributes[9 * i + 6],
                             self.additional_legs_attributes[9 * i + 7],
                             self.additional_legs_attributes[9 * i + 8]]
            self.additional_mesh = Cuboid(self.additional_legs_attributes[9 * i + 1],
                                          self.additional_legs_attributes[9 * i],
                                          self.additional_legs_attributes[9 * i + 2],
                                          position=mesh_position, rotation=mesh_rotation)
            vertices_list.append(self.additional_mesh.vertices)
            faces_list.append(self.additional_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.additional_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Leg'


# Source: Table/concept_template.py
class Cable_stayed_leg(ConceptTemplate):
    def __init__(self, front_legs_size, rear_legs_size, number_of_legs,
                 connections_size, connections_offset, legs_separation, central_rotation,
                 other_rotation, additional_legs_params, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        central_rotation = [x / 180 * np.pi for x in central_rotation]
        other_rotation = [x / 180 * np.pi for x in other_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.front_legs_size = front_legs_size
        self.rear_legs_size = rear_legs_size
        self.number_of_legs = number_of_legs
        self.connections_size = connections_size
        self.connections_offset = connections_offset
        self.legs_separation = legs_separation
        self.central_rotation = central_rotation[0]
        self.other_rotation = other_rotation
        self.number_of_additional_legs = additional_legs_params[0]
        self.additional_legs_attributes = additional_legs_params[1:]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        if self.number_of_legs[0] == 1:
            mesh_position = [0, -front_legs_size[1] / 2 * np.cos(other_rotation[0]), 0]
            mesh_rotation = [other_rotation[0], central_rotation[0], other_rotation[1]]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position=mesh_position, rotation=mesh_rotation)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        if self.number_of_legs[0] == 4:
            front_position, rear_position = None, None
            for i in range(number_of_legs[0]):
                rotation_sign = 1 if (i == 0) else -1
                position_sign = 1 if (i % 2 == 1) else -1
                if i < 2:
                    mesh_rotation = [other_rotation[0], central_rotation[0], rotation_sign * other_rotation[1]]
                    mesh_position = [
                        position_sign * legs_separation[0] / 2 * np.cos(central_rotation[0]) + legs_separation[
                            2] / 2 * np.sin(central_rotation[0]),
                        -front_legs_size[1] / 2 * np.cos(other_rotation[0]) * np.cos(other_rotation[1]),
                        -position_sign * legs_separation[0] / 2 * np.sin(central_rotation[0]) + legs_separation[
                            2] / 2 * np.cos(central_rotation[0])]
                    if i == 0:
                        front_position = mesh_position
                    size = front_legs_size
                else:
                    mesh_rotation = [-other_rotation[0], central_rotation[0], rotation_sign * other_rotation[1]]
                    mesh_position = [
                        position_sign * legs_separation[1] / 2 * np.cos(central_rotation[0]) - legs_separation[
                            2] / 2 * np.sin(central_rotation[0]),
                        -front_legs_size[1] / 2 * np.cos(-other_rotation[0]) * np.cos(other_rotation[1]),
                        -position_sign * legs_separation[1] / 2 * np.sin(central_rotation[0]) - legs_separation[
                            2] / 2 * np.cos(central_rotation[0])]
                    if i == 3:
                        rear_position = mesh_position
                    size = rear_legs_size
                self.mesh = Cuboid(size[1], size[0], size[2],
                                   position=mesh_position, rotation=mesh_rotation)
                vertices_list.append(self.mesh.vertices)
                faces_list.append(self.mesh.faces + total_num_vertices)
                total_num_vertices += len(self.mesh.vertices)
            
            for i in range(2):
                rot_mult = 1 if i == 0 else -1
                length = np.sqrt((front_position[0] - rear_position[0]) ** 2 + (front_position[1] - rear_position[1]) ** 2 + (front_position[2] - rear_position[2]) ** 2)
                direction_vector = np.array([front_position[0] - rear_position[0], front_position[2] - rear_position[2]])
                rotation_angle = np.arctan2(direction_vector[1], direction_vector[0])
                mesh_rotation = [0, central_rotation[0] + rot_mult * rotation_angle, 0]
                mesh_position = [0, -connections_size[1] / 2, 0]
                self.mesh = Cuboid(connections_size[0], length, connections_size[1],
                                   position=mesh_position, rotation=mesh_rotation)
                vertices_list.append(self.mesh.vertices)
                faces_list.append(self.mesh.faces + total_num_vertices)
                total_num_vertices += len(self.mesh.vertices)

        for i in range(self.number_of_additional_legs):
            mesh_position = [self.additional_legs_attributes[9 * i + 3] - position[0],
                             self.additional_legs_attributes[9 * i + 4] -
                             self.additional_legs_attributes[9 * i + 1] * np.cos(self.additional_legs_attributes[9 * i + 6]) * np.cos(
                                 self.additional_legs_attributes[9 * i + 8]) / 2,
                             self.additional_legs_attributes[9 * i + 5] - position[2]]
            mesh_rotation = [self.additional_legs_attributes[9 * i + 6],
                             self.additional_legs_attributes[9 * i + 7],
                             self.additional_legs_attributes[9 * i + 8]]
            self.additional_mesh = Cuboid(self.additional_legs_attributes[9 * i + 1],
                                          self.additional_legs_attributes[9 * i],
                                          self.additional_legs_attributes[9 * i + 2],
                                          position=mesh_position, rotation=mesh_rotation)
            vertices_list.append(self.additional_mesh.vertices)
            faces_list.append(self.additional_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.additional_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Leg'


# Source: Table/concept_template.py
class Star_leg(ConceptTemplate):
    def __init__(self, vertical_size, sub_size, sub_central_offset,
                 tilt_angle, central_rotation, horizontal_rotation, number_of_sub_legs,
                 additional_legs_params, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        tilt_angle = [x / 180 * np.pi for x in tilt_angle]
        central_rotation = [x / 180 * np.pi for x in central_rotation]
        horizontal_rotation = [x / 180 * np.pi for x in horizontal_rotation]
        additional_legs_params = [x / 180 * np.pi if ((i > 1) and ((i - 1) % 9 in [6, 7, 8])) else x for i, x in
                                  enumerate(additional_legs_params)]
        super().__init__(position, rotation)

        # Record Parameters
        self.vertical_size = vertical_size
        self.sub_size = sub_size
        self.sub_central_offset = sub_central_offset
        self.tilt_angle = tilt_angle
        self.central_rotation = central_rotation
        self.horizontal_rotation = horizontal_rotation
        self.number_of_sub_legs = number_of_sub_legs
        self.number_of_additional_legs = additional_legs_params[0]
        self.additional_legs_attributes = additional_legs_params[1:]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(1 + number_of_sub_legs[0]):
            if i == 0:
                mesh_rotation = [horizontal_rotation[0], central_rotation[0], 0]
                mesh_position = [0, -vertical_size[1] / 2 * np.cos(horizontal_rotation[0]), 0]
                self.mesh = Cylinder(vertical_size[1], vertical_size[0], position=mesh_position,
                                     rotation=mesh_rotation)
            else:
                sub_rotation = np.pi / number_of_sub_legs[0] * (i - 1) * 2
                mesh_rotation = [tilt_angle[0] + horizontal_rotation[0], central_rotation[0] - sub_rotation, 0]
                mesh_position = [
                    -(sub_size[2] / 2 * np.cos(tilt_angle[0]) * np.sin(sub_rotation)) * np.cos(central_rotation[0]) + (
                            sub_size[2] / 2 * np.cos(tilt_angle[0]) * np.cos(sub_rotation)) * np.sin(
                        central_rotation[0]),
                    (-vertical_size[1] + sub_size[1] / 2 + sub_central_offset[0]) * np.cos(horizontal_rotation[0]) - (
                            (sub_size[2] / 2 * np.cos(tilt_angle[0]) * np.cos(sub_rotation)) * np.cos(
                        central_rotation[0]) + (
                                    sub_size[2] / 2 * np.cos(tilt_angle[0]) * np.sin(sub_rotation)) * np.sin(
                        central_rotation[0])) * np.sin(horizontal_rotation[0]),
                    ((sub_size[2] / 2 * np.cos(tilt_angle[0]) * np.cos(sub_rotation)) * np.cos(central_rotation[0]) + (
                            sub_size[2] / 2 * np.cos(tilt_angle[0]) * np.sin(sub_rotation)) * np.sin(
                        central_rotation[0])) * np.cos(horizontal_rotation[0]) + (
                            -vertical_size[1] + sub_size[1] / 2 + sub_central_offset[0]) * np.sin(
                        horizontal_rotation[0]) + vertical_size[1] / 2 * np.sin(horizontal_rotation[0])]
                self.mesh = Cuboid(sub_size[1], sub_size[0], sub_size[2], position=mesh_position,
                                   rotation=mesh_rotation)

            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        for i in range(self.number_of_additional_legs):
            mesh_position = [self.additional_legs_attributes[9 * i + 3] - position[0],
                             self.additional_legs_attributes[9 * i + 4] -
                             self.additional_legs_attributes[9 * i + 1] * np.cos(self.additional_legs_attributes[9 * i + 6]) * np.cos(
                                 self.additional_legs_attributes[9 * i + 8]) / 2,
                             self.additional_legs_attributes[9 * i + 5] - position[2]]
            mesh_rotation = [self.additional_legs_attributes[9 * i + 6],
                             self.additional_legs_attributes[9 * i + 7],
                             self.additional_legs_attributes[9 * i + 8]]
            self.additional_mesh = Cuboid(self.additional_legs_attributes[9 * i + 1],
                                          self.additional_legs_attributes[9 * i],
                                          self.additional_legs_attributes[9 * i + 2],
                                          position=mesh_position, rotation=mesh_rotation)
            vertices_list.append(self.additional_mesh.vertices)
            faces_list.append(self.additional_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.additional_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Leg'


# Source: Table/concept_template.py
class Bar_cylindrical_leg(ConceptTemplate):
    def __init__(self, vertical_size, bottom_size, horizontal_rotation,
                 additional_legs_params, position=[0, 0, 0], rotation=[0, 0, 0]):
        
        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        horizontal_rotation = [x / 180 * np.pi for x in horizontal_rotation]
        additional_legs_params = [x / 180 * np.pi if ((i > 1) and ((i - 1) % 9 in [6, 7, 8])) else x for i, x in
                                  enumerate(additional_legs_params)]
        super().__init__(position, rotation)

        # Record Parameters
        self.vertical_size = vertical_size
        self.bottom_size = bottom_size
        self.horizontal_rotation = horizontal_rotation
        self.number_of_additional_legs = additional_legs_params[0]
        self.additional_legs_attributes = additional_legs_params[1:]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_rotation = [horizontal_rotation[0], 0, 0]
        mesh_position = [0, -vertical_size[1] / 2 * np.cos(horizontal_rotation[0]), 0]
        self.support_mesh = Cylinder(vertical_size[1], vertical_size[0], position=mesh_position,
                                     rotation=mesh_rotation)
        vertices_list.append(self.support_mesh.vertices)
        faces_list.append(self.support_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.support_mesh.vertices)

        mesh_rotation = [horizontal_rotation[0], 0, 0]
        mesh_position = [0, (-vertical_size[1] - bottom_size[1] / 2) * np.cos(horizontal_rotation[0]),
                         (vertical_size[1] - bottom_size[1]) / 2 * np.sin(horizontal_rotation[0])]
        self.bottom_mesh = Cylinder(bottom_size[1], bottom_size[0], position=mesh_position,
                                    rotation=mesh_rotation)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        for i in range(self.number_of_additional_legs):
            mesh_position = [self.additional_legs_attributes[9 * i + 3] - position[0],
                             self.additional_legs_attributes[9 * i + 4] -
                             self.additional_legs_attributes[9 * i + 1] * np.cos(self.additional_legs_attributes[9 * i + 6]) * np.cos(
                                 self.additional_legs_attributes[9 * i + 8]) / 2,
                             self.additional_legs_attributes[9 * i + 5] - position[2]]
            mesh_rotation = [self.additional_legs_attributes[9 * i + 6],
                             self.additional_legs_attributes[9 * i + 7],
                             self.additional_legs_attributes[9 * i + 8]]
            self.additional_mesh = Cuboid(self.additional_legs_attributes[9 * i + 1],
                                          self.additional_legs_attributes[9 * i],
                                          self.additional_legs_attributes[9 * i + 2],
                                          position=mesh_position, rotation=mesh_rotation)
            vertices_list.append(self.additional_mesh.vertices)
            faces_list.append(self.additional_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.additional_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)
        
        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Leg'


# Source: Table/concept_template.py
class Bar_cuboid_leg(ConceptTemplate):
    def __init__(self, vertical_size, bottom_size, bottom_rotation, horizontal_rotation,
                 additional_legs_params, position=[0, 0, 0], rotation=[0, 0, 0]):
        
        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        bottom_rotation = [x / 180 * np.pi for x in bottom_rotation]
        horizontal_rotation = [x / 180 * np.pi for x in horizontal_rotation]
        additional_legs_params = [x / 180 * np.pi if ((i > 1) and ((i - 1) % 9 in [6, 7, 8])) else x for i, x in
                                  enumerate(additional_legs_params)]
        super().__init__(position, rotation)

        # Record Parameters
        self.vertical_size = vertical_size
        self.bottom_size = bottom_size
        self.bottom_rotation = bottom_rotation
        self.horizontal_rotation = horizontal_rotation
        self.number_of_additional_legs = additional_legs_params[0]
        self.additional_legs_attributes = additional_legs_params[1:]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_rotation = [horizontal_rotation[0], 0, 0]
        mesh_position = [0, -vertical_size[1] / 2 * np.cos(horizontal_rotation[0]), 0]
        self.support_mesh = Cuboid(vertical_size[1], vertical_size[0], vertical_size[2],
                                   position=mesh_position,
                                   rotation=mesh_rotation)
        vertices_list.append(self.support_mesh.vertices)
        faces_list.append(self.support_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.support_mesh.vertices)

        mesh_rotation = [horizontal_rotation[0], bottom_rotation[0], 0]
        mesh_position = [0, (-vertical_size[1] - bottom_size[1] / 2) * np.cos(horizontal_rotation[0]),
                         (vertical_size[1] - bottom_size[1]) / 2 * np.sin(horizontal_rotation[0])]
        self.bottom_mesh = Cuboid(bottom_size[1], bottom_size[0], bottom_size[2],
                                  position=mesh_position,
                                  rotation=mesh_rotation)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        for i in range(self.number_of_additional_legs):
            mesh_position = [self.additional_legs_attributes[9 * i + 3] - position[0],
                             self.additional_legs_attributes[9 * i + 4] -
                             self.additional_legs_attributes[9 * i + 1] * np.cos(self.additional_legs_attributes[9 * i + 6]) * np.cos(
                                 self.additional_legs_attributes[9 * i + 8]) / 2,
                             self.additional_legs_attributes[9 * i + 5] - position[2]]
            mesh_rotation = [self.additional_legs_attributes[9 * i + 6],
                             self.additional_legs_attributes[9 * i + 7],
                             self.additional_legs_attributes[9 * i + 8]]
            self.additional_mesh = Cuboid(self.additional_legs_attributes[9 * i + 1],
                                          self.additional_legs_attributes[9 * i],
                                          self.additional_legs_attributes[9 * i + 2],
                                          position=mesh_position, rotation=mesh_rotation)
            vertices_list.append(self.additional_mesh.vertices)
            faces_list.append(self.additional_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.additional_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Leg'


# Source: Table/concept_template.py
class Desk_type_leg(ConceptTemplate):
    def __init__(self, vertical_size, horizontal_size, vertical_separation,
                 vertical_rotation, horizontal_rotation, connections_size,
                 number_of_connections, connections_offset, interval_between_connections,
                 additional_legs_params, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        vertical_rotation = [x / 180 * np.pi for x in vertical_rotation]
        horizontal_rotation = [x / 180 * np.pi for x in horizontal_rotation]
        additional_legs_params = [x / 180 * np.pi if ((i > 1) and ((i - 1) % 9 in [6, 7, 8])) else x for i, x in
                                  enumerate(additional_legs_params)]
        super().__init__(position, rotation)

        # Record Parameters
        self.vertical_size = vertical_size
        self.horizontal_size = horizontal_size
        self.vertical_separation = vertical_separation
        self.vertical_rotation = vertical_rotation
        self.horizontal_rotation = horizontal_rotation
        self.connections_size = connections_size
        self.number_of_connections = number_of_connections
        self.connections_offset = connections_offset
        self.interval_between_connections = interval_between_connections
        self.number_of_additional_legs = additional_legs_params[0]
        self.additional_legs_attributes = additional_legs_params[1:]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(4 + number_of_connections[0]):
            rotation_sign = 1 if i == 0 else -1
            position_sign = -1 if (i % 2 == 0) else 1
            pose = apply_transformation([0, -vertical_size[1] / 2, 0], [0, 0, 0],
                                        [vertical_rotation[0], 0, vertical_rotation[1]])
            if i < 2:
                mesh_rotation = [vertical_rotation[0], 0, rotation_sign * vertical_rotation[1]]
                mesh_position = [position_sign * vertical_separation[0] / 2, pose[1], 0]
                self.mesh = Cuboid(vertical_size[1], vertical_size[0], vertical_size[2],
                                   position=mesh_position, rotation=mesh_rotation)
            elif i < 4:
                mesh_rotation = [horizontal_rotation[0], 0, 0]
                mesh_position = [position_sign * (vertical_separation[0] / 2 - pose[0]), 2 * pose[1],
                                 -vertical_size[1] / 2 * np.sin(vertical_rotation[0])]
                self.mesh = Cuboid(horizontal_size[1], horizontal_size[0], horizontal_size[2], position=mesh_position,
                                   rotation=mesh_rotation)
            else:

                mesh_rotation = [vertical_rotation[0], 0, 0]
                mesh_position = [0,
                                 -(vertical_size[1] / 2 - (
                                         (i - 4) * interval_between_connections[0] + connections_offset[
                                     0]) * np.cos(vertical_rotation[0]) * np.cos(vertical_rotation[1])),
                                 ((i - 4) * interval_between_connections[0] + connections_offset[0]) * np.sin(
                                     vertical_rotation[0])]
                self.mesh = Cuboid(connections_size[0],
                                   vertical_separation[0] - vertical_size[0] + 2 * (
                                           connections_offset[0] + (i - 4) * interval_between_connections[0]) * np.sin(
                                       vertical_rotation[1]),
                                   connections_size[1],
                                   position=mesh_position, rotation=mesh_rotation)

            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        for i in range(self.number_of_additional_legs):
            mesh_position = [self.additional_legs_attributes[9 * i + 3] - position[0],
                             self.additional_legs_attributes[9 * i + 4] -
                             self.additional_legs_attributes[9 * i + 1] * np.cos(self.additional_legs_attributes[9 * i + 6]) * np.cos(
                                 self.additional_legs_attributes[9 * i + 8]) / 2,
                             self.additional_legs_attributes[9 * i + 5] - position[2]]
            mesh_rotation = [self.additional_legs_attributes[9 * i + 6],
                             self.additional_legs_attributes[9 * i + 7],
                             self.additional_legs_attributes[9 * i + 8]]
            self.additional_mesh = Cuboid(self.additional_legs_attributes[9 * i + 1],
                                          self.additional_legs_attributes[9 * i],
                                          self.additional_legs_attributes[9 * i + 2],
                                          position=mesh_position, rotation=mesh_rotation)
            vertices_list.append(self.additional_mesh.vertices)
            faces_list.append(self.additional_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.additional_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Leg'


# Source: Eyeglasses/concept_template.py
class Regular_Leg(ConceptTemplate):
    def __init__(self, glass_interval, size1, size2, rotation_1, rotation_2, offset_x, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        rotation_1 = [x / 180 * np.pi for x in rotation_1]
        rotation_2 = [x / 180 * np.pi for x in rotation_2]
        super().__init__(position, rotation)

        # Record Parameters
        self.size1 = size1
        self.size2 = size2
        self.glass_interval = glass_interval
        self.rotation_1 = rotation_1
        self.rotation_2 = rotation_2
        self.offset_x = offset_x

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        leg_interval = offset_x[0] * 2 + glass_interval[0]

        for direction in [-1, 1]:
            tmp_meshes = []

            top_mesh_position = [
                -direction * size2[0] / 2, 
                -size2[1] / 2, 
                -size2[2] / 2
            ]
            top_mesh = Cuboid(size2[1], size2[0], size2[2],
                              position=top_mesh_position)
            tmp_meshes.append(top_mesh)

            top_mesh.vertices = apply_transformation(
                top_mesh.vertices,
                position=[0, 0, -size1[2]],
                rotation=[-rotation_2[0], -direction * rotation_2[1], 0],
                rotation_order="YXZ",
            )
            middle_mesh_position = [
                -direction * size1[0] / 2, 
                -size1[1] / 2, 
                -size1[2] / 2
            ]
            middle_mesh = Cuboid(size1[1], size1[0], size1[2],
                                 position=middle_mesh_position)
            tmp_meshes.append(middle_mesh)

            for mesh in tmp_meshes:
                mesh.vertices = apply_transformation(
                    mesh.vertices,
                    position=[
                        direction * leg_interval / 2,
                        0,
                        0,
                    ],
                    rotation=[-rotation_1[0], -direction * rotation_1[1], 0],
                    rotation_order="YXZ",
                )
                vertices_list.append(mesh.vertices)
                faces_list.append(mesh.faces + total_num_vertices)
                total_num_vertices += len(mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Leg'


# Source: Eyeglasses/concept_template.py
class Trifold_Leg(ConceptTemplate):
    def __init__(self, glass_interval, size1, size2, rotation_1, rotation_2, connector_size, offset_x, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        rotation_1 = [x / 180 * np.pi for x in rotation_1]
        rotation_2 = [x / 180 * np.pi for x in rotation_2]
        super().__init__(position, rotation)

        # Record Parameters
        self.size1 = size1
        self.size2 = size2
        self.glass_interval = glass_interval
        self.rotation_1 = rotation_1
        self.rotation_2 = rotation_2
        self.offset_x = offset_x
        self.connector_size = connector_size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        leg_interval = offset_x[0] * 2 + glass_interval[0]

        for direction in [-1, 1]:
            tmp_meshes = []

            top_mesh_position = [
                -direction * size2[0] / 2, 
                -size2[1] / 2, 
                -size2[2] / 2
            ]
            top_mesh = Cuboid(size2[1], size2[0], size2[2],
                              position=top_mesh_position)
            tmp_meshes.append(top_mesh)

            top_mesh.vertices = apply_transformation(
                top_mesh.vertices,
                position=[0, 0, -size1[2]],
                rotation=[-rotation_2[0], -direction * rotation_2[1], 0],
                rotation_order="XYZ",
            )

            middle_mesh_position = [
                -direction * size1[0] / 2, 
                -size1[1] / 2, 
                -size1[2] / 2
            ]
            middle_mesh = Cuboid(size1[1], size1[0], size1[2],
                                 position=middle_mesh_position)
            tmp_meshes.append(middle_mesh)

            for mesh in tmp_meshes:
                mesh.vertices = apply_transformation(
                    mesh.vertices,
                    position=[0, 0, 0],
                    rotation=[-rotation_1[0], -direction * rotation_1[1], 0],
                    rotation_order="XYZ",
                )

            bottom_mesh_position = [
                -direction * connector_size[0] / 2,
                -connector_size[1] / 2,
                connector_size[2] / 2,
            ]
            bottom_mesh = Cuboid(connector_size[1], connector_size[0], connector_size[2],
                                 position=bottom_mesh_position)
            tmp_meshes.append(bottom_mesh)

            for mesh in tmp_meshes:
                mesh.vertices = apply_transformation(
                    mesh.vertices,
                    position=[
                        direction * leg_interval / 2 + offset_x[0] + direction * connector_size[0],
                        connector_size[1] / 2,
                        0,
                    ],
                    rotation=[0, 0, 0],
                )
                vertices_list.append(mesh.vertices)
                faces_list.append(mesh.faces + total_num_vertices)
                total_num_vertices += len(mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Leg'


# Source: Refrigerator/concept_template.py
class Multilevel_Leg(ConceptTemplate):
    def __init__(self, front_legs_size, rear_legs_size, legs_separation, num_legs, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.front_legs_size = front_legs_size
        self.rear_legs_size = rear_legs_size
        self.legs_separation = legs_separation
        self.num_legs = num_legs

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        if (num_legs[0] == 1):
            mesh_position = [
                0,
                -front_legs_size[1] / 2,
                0
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        elif (num_legs[0] == 2):
            mesh_position = [
                legs_separation[0] / 2, 
                -front_legs_size[1] / 2,
                0
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                -legs_separation[0] / 2,
                -front_legs_size[1] / 2,
                0
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        elif (num_legs[0] == 3):
            mesh_position = [
                legs_separation[0] / 2,
                -front_legs_size[1] / 2,
                legs_separation[2] / 2
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                -legs_separation[0] / 2,
                -front_legs_size[1] / 2,
                legs_separation[2] / 2
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                0,
                -rear_legs_size[1] / 2,
                -legs_separation[2] / 2
            ]
            self.mesh = Cuboid(rear_legs_size[1], rear_legs_size[0], rear_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        elif (num_legs[0] == 4):
            mesh_position = [
                legs_separation[0] / 2,
                -front_legs_size[1] / 2,
                legs_separation[2] / 2
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                -legs_separation[0] / 2,
                -front_legs_size[1] / 2,
                legs_separation[2] / 2
            ]
            self.mesh = Cuboid(front_legs_size[1], front_legs_size[0], front_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                legs_separation[1] / 2,
                -rear_legs_size[1] / 2,
                -legs_separation[2] / 2
            ]
            self.mesh = Cuboid(rear_legs_size[1], rear_legs_size[0], rear_legs_size[2],
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            mesh_position = [
                -legs_separation[1] / 2,
                -rear_legs_size[1] / 2,
                -legs_separation[2] / 2
            ]
            self.mesh = Cuboid(rear_legs_size[1], rear_legs_size[0], rear_legs_size[2],
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

        self.semantic = 'Leg'
