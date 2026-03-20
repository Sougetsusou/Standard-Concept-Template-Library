"""
Shaft Templates
Automatically extracted from concept_template.py files
Contains 6 class(es)
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


# Source: Ruler/concept_template.py
class Regular_shaft(ConceptTemplate):
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

        mesh_rotation = [np.pi / 2, 0, 0]
        self.mesh = Cylinder(size[1], size[0], rotation=mesh_rotation)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Shaft'


# Source: Scissors/concept_template.py
class Cuboidal_Shaft(ConceptTemplate):
    def __init__(self, size, layer_offset, shaft_rotation, up_down_relationship, has_central_shaft, central_shaft_size, central_shaft_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        shaft_rotation = [x / 180 * np.pi for x in shaft_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.layer_offset = layer_offset
        self.shaft_rotation = shaft_rotation
        self.up_down_relationship = up_down_relationship
        self.has_central_shaft = has_central_shaft
        self.central_shaft_size = central_shaft_size
        self.central_shaft_offset = central_shaft_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        if up_down_relationship[0] == 0:
            left_mesh_position = [
                0, 
                size[1] / 2,
                layer_offset[0]
            ]
        elif up_down_relationship[0] == 1:
            left_mesh_position = [
                0, 
                -size[1] / 2,
                layer_offset[0]
            ]
        left_mesh_rotation = [0, shaft_rotation[0], 0]
        self.left_mesh = Cuboid(size[1], size[0], size[2],
                                position = left_mesh_position,
                                rotation = left_mesh_rotation)
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        if up_down_relationship[0] == 0:
            right_mesh_position = [
                0, 
                -size[1] / 2,
                -layer_offset[0]
            ]
        elif up_down_relationship[0] == 1:
            right_mesh_position = [
                0, 
                size[1] / 2,
                -layer_offset[0]
            ]
        right_mesh_rotation = [0, -shaft_rotation[0], 0]
        self.right_mesh = Cuboid(size[1], size[0], size[2],
                                 position = right_mesh_position,
                                 rotation = right_mesh_rotation)
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        if has_central_shaft[0] == 1:
            mesh_position = [
                central_shaft_offset[0],
                central_shaft_offset[1],
                central_shaft_offset[2]
            ]
            self.mesh = Cylinder(central_shaft_size[1], central_shaft_size[0],
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

        self.semantic = 'Shaft'


# Source: Scissors/concept_template.py
class Double_Cuboidal_Shaft(ConceptTemplate):
    def __init__(self, size, front_size, front_offset, layer_offset, shaft_rotation, up_down_relationship, has_central_shaft, central_shaft_size, central_shaft_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        shaft_rotation = [x / 180 * np.pi for x in shaft_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.front_size = front_size
        self.front_offset = front_offset
        self.layer_offset = layer_offset
        self.shaft_rotation = shaft_rotation
        self.up_down_relationship = up_down_relationship
        self.has_central_shaft = has_central_shaft
        self.central_shaft_size = central_shaft_size
        self.central_shaft_offset = central_shaft_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # left
        if up_down_relationship[0] == 0:
            left_mesh_position = [
                0, 
                size[1] / 2,
                layer_offset[0]
            ]
        elif up_down_relationship[0] == 1:
            left_mesh_position = [
                0, 
                -size[1] / 2,
                layer_offset[0]
            ]
        left_mesh_rotation = [0, shaft_rotation[0], 0]
        self.left_mesh = Cuboid(size[1], size[0], size[2],
                                position = left_mesh_position,
                                rotation = left_mesh_rotation)
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        # left front
        left_front_mesh_position_1 = [
            (size[0] + front_size[0]) / 2, 
            0,
            front_offset[0]
        ]
        left_front_mesh_rotation = [0, shaft_rotation[0], 0]
        left_front_mesh_position_1 = adjust_position_from_rotation(left_front_mesh_position_1, left_front_mesh_rotation)

        if up_down_relationship[0] == 0:
            left_front_mesh_position_2 = [
                0, 
                size[1] / 2,
                layer_offset[0]
            ]
            left_front_mesh_position = list_add(left_front_mesh_position_1, left_front_mesh_position_2)
        elif up_down_relationship[0] == 1:
            left_front_mesh_position_2 = [
                0, 
                -size[1] / 2,
                layer_offset[0]
            ]
            left_front_mesh_position = list_add(left_front_mesh_position_1, left_front_mesh_position_2)

        self.left_front_mesh = Cuboid(size[1], front_size[0], front_size[1],
                                      position = left_front_mesh_position,
                                      rotation = left_front_mesh_rotation)
        vertices_list.append(self.left_front_mesh.vertices)
        faces_list.append(self.left_front_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_front_mesh.vertices)

        # right
        if up_down_relationship[0] == 0:
            right_mesh_position = [
                0, 
                -size[1] / 2,
                -layer_offset[0]
            ]
        elif up_down_relationship[0] == 1:
            right_mesh_position = [
                0, 
                size[1] / 2,
                -layer_offset[0]
            ]
        right_mesh_rotation = [0, -shaft_rotation[0], 0]
        self.right_mesh = Cuboid(size[1], size[0], size[2],
                                 position = right_mesh_position,
                                 rotation = right_mesh_rotation)
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        # right front
        right_front_mesh_position_1 = [
            (size[0] + front_size[0]) / 2, 
            0,
            -front_offset[0]
        ]
        right_front_mesh_rotation = [0, -shaft_rotation[0], 0]
        right_front_mesh_position_1 = adjust_position_from_rotation(right_front_mesh_position_1, right_front_mesh_rotation)

        if up_down_relationship[0] == 0:
            right_front_mesh_position_2 = [
                0, 
                -size[1] / 2,
                -layer_offset[0]
            ]
            right_front_mesh_position = list_add(right_front_mesh_position_1, right_front_mesh_position_2)
        elif up_down_relationship[0] == 1:
            right_front_mesh_position_2 = [
                0, 
                size[1] / 2,
                -layer_offset[0]
            ]
            right_front_mesh_position = list_add(right_front_mesh_position_1, right_front_mesh_position_2)

        self.right_front_mesh = Cuboid(size[1], front_size[0], front_size[1],
                                       position = right_front_mesh_position,
                                       rotation = right_front_mesh_rotation)
        vertices_list.append(self.right_front_mesh.vertices)
        faces_list.append(self.right_front_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_front_mesh.vertices)

        if has_central_shaft[0] == 1:
            mesh_position = [
                central_shaft_offset[0],
                central_shaft_offset[1],
                central_shaft_offset[2]
            ]
            self.mesh = Cylinder(central_shaft_size[1], central_shaft_size[0],
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

        self.semantic = 'Shaft'


# Source: Scissors/concept_template.py
class Cylindrical_Shaft(ConceptTemplate):
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

        left_mesh_position = [
            0, 
            size[1] / 4,
            0
        ]
        self.left_mesh = Cylinder(size[1] / 2, size[0], 
                                  position = left_mesh_position)
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        right_mesh_position = [
            0, 
            -size[1] / 4,
            0
        ]
        self.right_mesh = Cylinder(size[1] / 2, size[0], 
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

        self.semantic = 'Shaft'


# Source: Pliers/concept_template.py
class Round_Shaft(ConceptTemplate):
    def __init__(self, size, has_central_shaft, central_shaft_size, central_shaft_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.has_central_shaft = has_central_shaft
        self.central_shaft_size = central_shaft_size
        self.central_shaft_offset = central_shaft_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.mesh = Cylinder(size[1], size[0])
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        if has_central_shaft[0] == 1:
            mesh_position = [
                central_shaft_offset[0],
                central_shaft_offset[1],
                central_shaft_offset[2]
            ]
            self.mesh = Cylinder(central_shaft_size[1], central_shaft_size[0],
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

        self.semantic = 'Shaft'


# Source: Pliers/concept_template.py
class Rectangular_Shaft(ConceptTemplate):
    def __init__(self, num_layers, layer_1_size, layer_2_size, layer_2_offset, layer_3_size, layer_3_offset, layer_rotation, has_central_shaft, central_shaft_size, central_shaft_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        layer_rotation = [x / 180 * np.pi for x in layer_rotation]
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.num_layers = num_layers
        self.layer_1_size = layer_1_size
        self.layer_2_size = layer_2_size
        self.layer_2_offset = layer_2_offset
        self.layer_3_size = layer_3_size
        self.layer_3_offset = layer_3_offset
        self.layer_rotation = layer_rotation
        self.has_central_shaft = has_central_shaft
        self.central_shaft_size = central_shaft_size
        self.central_shaft_offset = central_shaft_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        layer_1_mesh_position = [
            0, 
            -layer_1_size[1] / 2,
            0
        ]
        layer_1_mesh_rotation = [0, layer_rotation[0], 0]
        self.layer_1_mesh = Cuboid(layer_1_size[1], layer_1_size[0], layer_1_size[2],
                                   position = layer_1_mesh_position,
                                   rotation = layer_1_mesh_rotation)
        vertices_list.append(self.layer_1_mesh.vertices)
        faces_list.append(self.layer_1_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.layer_1_mesh.vertices)

        if num_layers[0] >= 2:
            layer_2_mesh_position = [
                layer_2_offset[0], 
                layer_2_size[1] / 2,
                layer_2_offset[1]
            ]
            layer_2_mesh_rotation = [0, layer_rotation[1], 0]
            self.layer_2_mesh = Cuboid(layer_2_size[1], layer_2_size[0], layer_2_size[2],
                                       position = layer_2_mesh_position,
                                       rotation = layer_2_mesh_rotation)
            vertices_list.append(self.layer_2_mesh.vertices)
            faces_list.append(self.layer_2_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.layer_2_mesh.vertices)

        if num_layers[0] >= 3:
            layer_3_mesh_position = [
                layer_3_offset[0], 
                layer_2_size[1] + layer_3_size[1] / 2,
                layer_3_offset[1]
            ]
            layer_3_mesh_rotation = [0, layer_rotation[2], 0]
            self.layer_3_mesh = Cuboid(layer_3_size[1], layer_3_size[0], layer_3_size[2],
                                       position = layer_3_mesh_position,
                                       rotation = layer_3_mesh_rotation)
            vertices_list.append(self.layer_3_mesh.vertices)
            faces_list.append(self.layer_3_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.layer_3_mesh.vertices)

        if has_central_shaft[0] == 1:
            mesh_position = [
                central_shaft_offset[0],
                central_shaft_offset[1],
                central_shaft_offset[2]
            ]
            self.mesh = Cylinder(central_shaft_size[1], central_shaft_size[0],
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

        self.semantic = 'Shaft'
