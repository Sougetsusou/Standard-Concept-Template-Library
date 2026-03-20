"""
Gripper Templates
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


# Source: Pliers/concept_template.py
class Cusp_Gripper(ConceptTemplate):
    def __init__(self, behind_size, front_size, gripper_separation, gripper_rotation, position = [0, 0, 0], rotation = [0, 0, 0]):
        
        # Process rotation param
        gripper_rotation = [x / 180 * np.pi for x in gripper_rotation]
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.behind_size = behind_size
        self.front_size = front_size
        self.gripper_separation = gripper_separation
        self.gripper_rotation = gripper_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # front_left
        front_1_mesh_rotation_1 = [np.pi / 2, 0, 0]
        front_1_mesh_position_1 = [
            front_size[0] / 2, 
            0,
            behind_size[3] + front_size[3] / 2
        ]
        front_1_mesh_rotation_2 = [0, gripper_rotation[0], 0]
        front_1_mesh_position_1 = adjust_position_from_rotation(front_1_mesh_position_1, front_1_mesh_rotation_2)

        front_1_mesh_position_2 = [
            gripper_separation[0] / 2, 
            0,
            0
        ]
        front_1_mesh_position = list_add(front_1_mesh_position_1, front_1_mesh_position_2)
        front_1_mesh_rotation = list_add(front_1_mesh_rotation_1, front_1_mesh_rotation_2)

        self.front_1_mesh = Cuboid(front_size[3], front_size[1], front_size[2],
                                   front_size[0], front_size[2],
                                   top_offset = [(front_size[1] - front_size[0]) / 2, 0],
                                   position = front_1_mesh_position,
                                   rotation = front_1_mesh_rotation)
        vertices_list.append(self.front_1_mesh.vertices)
        faces_list.append(self.front_1_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.front_1_mesh.vertices)

        # behind_left
        behind_1_mesh_rotation_1 = [np.pi / 2, 0, 0]
        behind_1_mesh_position_1 = [
            behind_size[0] / 2, 
            0,
            behind_size[3] / 2
        ]
        behind_1_mesh_rotation_2 = [0, gripper_rotation[0], 0]
        behind_1_mesh_position_1 = adjust_position_from_rotation(behind_1_mesh_position_1, behind_1_mesh_rotation_2)

        behind_1_mesh_position_2 = [
            gripper_separation[0] / 2, 
            0,
            0
        ]
        behind_1_mesh_position = list_add(behind_1_mesh_position_1, behind_1_mesh_position_2)
        behind_1_mesh_rotation = list_add(behind_1_mesh_rotation_1, behind_1_mesh_rotation_2)

        self.behind_1_mesh = Cuboid(behind_size[3], behind_size[1], behind_size[2],
                                    behind_size[0], behind_size[2],
                                    top_offset = [-(behind_size[1] - behind_size[0]) / 2, 0],
                                    position = behind_1_mesh_position,
                                    rotation = behind_1_mesh_rotation)
        vertices_list.append(self.behind_1_mesh.vertices)
        faces_list.append(self.behind_1_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.behind_1_mesh.vertices)

        # front_right
        front_2_mesh_rotation_1 = [np.pi / 2, 0, 0]
        front_2_mesh_position_1 = [
            -front_size[0] / 2, 
            0,
            behind_size[3] + front_size[3] / 2
        ]
        front_2_mesh_rotation_2 = [0, -gripper_rotation[0], 0]
        front_2_mesh_position_1 = adjust_position_from_rotation(front_2_mesh_position_1, front_2_mesh_rotation_2)

        front_2_mesh_position_2 = [
            -gripper_separation[0] / 2, 
            0,
            0
        ]
        front_2_mesh_position = list_add(front_2_mesh_position_1, front_2_mesh_position_2)
        front_2_mesh_rotation = list_add(front_2_mesh_rotation_1, front_2_mesh_rotation_2)

        self.front_2_mesh = Cuboid(front_size[3], front_size[1], front_size[2],
                                   front_size[0], front_size[2],
                                   top_offset = [-(front_size[1] - front_size[0]) / 2, 0],
                                   position = front_2_mesh_position,
                                   rotation = front_2_mesh_rotation)
        vertices_list.append(self.front_2_mesh.vertices)
        faces_list.append(self.front_2_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.front_2_mesh.vertices)

        # behind_right
        behind_2_mesh_rotation_1 = [np.pi / 2, 0, 0]
        behind_2_mesh_position_1 = [
            -behind_size[0] / 2, 
            0,
            behind_size[3] / 2
        ]
        behind_2_mesh_rotation_2 = [0, -gripper_rotation[0], 0]
        behind_2_mesh_position_1 = adjust_position_from_rotation(behind_2_mesh_position_1, behind_2_mesh_rotation_2)

        behind_2_mesh_position_2 = [
            -gripper_separation[0] / 2, 
            0,
            0
        ]
        behind_2_mesh_position = list_add(behind_2_mesh_position_1, behind_2_mesh_position_2)
        behind_2_mesh_rotation = list_add(behind_2_mesh_rotation_1, behind_2_mesh_rotation_2)

        self.behind_2_mesh = Cuboid(behind_size[3], behind_size[1], behind_size[2],
                                    behind_size[0], behind_size[2],
                                    top_offset = [(behind_size[1] - behind_size[0]) / 2, 0],
                                    position = behind_2_mesh_position,
                                    rotation = behind_2_mesh_rotation)
        vertices_list.append(self.behind_2_mesh.vertices)
        faces_list.append(self.behind_2_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.behind_2_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Gripper'


# Source: Pliers/concept_template.py
class Curved_Gripper(ConceptTemplate):
    def __init__(self, radius, thickness, gripper_separation, gripper_rotation, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        gripper_rotation = [x / 180 * np.pi for x in gripper_rotation]
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.radius = radius
        self.thickness = thickness
        self.gripper_separation = gripper_separation
        self.gripper_rotation = gripper_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        left_mesh_position = [
            gripper_separation[0] / 2, 
            0,
            0
        ]
        left_mesh_rotation = [0, gripper_rotation[0], 0]

        self.left_mesh = Cylinder(thickness[0], radius[0], radius[0],
                                  top_radius_z = radius[1], bottom_radius_z = radius[1],
                                  is_quarter = True,
                                  position = left_mesh_position,
                                  rotation = left_mesh_rotation)
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        right_mesh_position = [
            -gripper_separation[0] / 2, 
            0,
            0
        ]
        right_mesh_rotation = [0, -gripper_rotation[0], np.pi]

        self.right_mesh = Cylinder(thickness[0], radius[0], radius[0],
                                   top_radius_z = radius[1], bottom_radius_z = radius[1],
                                   is_quarter = True,
                                   position = right_mesh_position,
                                   rotation = right_mesh_rotation,
                                   rotation_order = 'ZYX')
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Gripper'
