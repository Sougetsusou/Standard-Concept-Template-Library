"""
Screen Templates
Automatically extracted from concept_template.py files
Contains 3 class(es)
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


# Source: Display/concept_template.py
class Frustum_Screen(ConceptTemplate):
    def __init__(self, has_additional_layer, additional_layer_size, size, back_part_offset, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.has_additional_layer = has_additional_layer
        self.additional_layer_size = additional_layer_size
        self.size = size
        self.back_part_offset = back_part_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        back_mesh_position = [0, 0, -size[2] / 2]
        back_mesh_rotation = [-np.pi / 2, 0, 0]
        self.back_mesh = Cuboid(size[2], size[0], size[1],
                                additional_layer_size[0], additional_layer_size[1],
                                [back_part_offset[0], back_part_offset[1]],
                                position=back_mesh_position,
                                rotation=back_mesh_rotation)
        vertices_list.append(self.back_mesh.vertices)
        faces_list.append(self.back_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.back_mesh.vertices)

        if has_additional_layer[0]:
            front_mesh_position = [0, 0, additional_layer_size[2] / 2]
            self.front_mesh = Cuboid(additional_layer_size[1], additional_layer_size[0], additional_layer_size[2],
                                     position=front_mesh_position)
            vertices_list.append(self.front_mesh.vertices)
            faces_list.append(self.front_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.front_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Screen'


# Source: Display/concept_template.py
class Standard_Screen(ConceptTemplate):
    def __init__(self, has_additional_layer, size, additional_layer_size, additional_layer_offset, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.has_additional_layer = has_additional_layer
        self.size = size
        self.additional_layer_size = additional_layer_size
        self.additional_layer_offset = additional_layer_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.front_mesh = Cuboid(size[1], size[0], size[2])
        vertices_list.append(self.front_mesh.vertices)
        faces_list.append(self.front_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.front_mesh.vertices)

        if has_additional_layer[0]:
            back_mesh_position = [
                additional_layer_offset[0],
                additional_layer_offset[1],
                -size[2] / 2 - additional_layer_size[2] / 2,
            ]
            self.back_mesh = Cuboid(additional_layer_size[1], additional_layer_size[0], additional_layer_size[2],
                                    position=back_mesh_position)
            vertices_list.append(self.back_mesh.vertices)
            faces_list.append(self.back_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.back_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Screen'


# Source: Laptop/concept_template.py
class Regular_Screen(ConceptTemplate):
    def __init__(self, size, offset, screen_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):
        
        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        screen_rotation = [x / 180 * np.pi for x in screen_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.offset = offset
        self.screen_rotation = screen_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0
        
        back_mesh_position = [
            0, 
            offset[0] + size[1] * np.cos(screen_rotation[0]) / 2,
            offset[1]
        ]
        back_mesh_rotation = [screen_rotation[0], 0, 0]
        self.back_mesh = Cuboid(size[1], size[0], size[2],
                                position=back_mesh_position,
                                rotation=back_mesh_rotation)
        vertices_list.append(self.back_mesh.vertices)
        faces_list.append(self.back_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.back_mesh.vertices)
        
        self.vertices=np.concatenate(vertices_list)
        self.faces=np.concatenate(faces_list)

        # Global Transformation
        self.vertices=apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Screen'
