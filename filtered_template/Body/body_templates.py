"""
Body Templates
Automatically extracted from concept_template.py files
Contains 51 class(es)
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


# Source: Microwave/concept_template.py
class Cuboidal_Body(ConceptTemplate):
    def __init__(self, size, thickness, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.thickness = thickness

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0,
            0,
            -(size[2] - thickness[4]) / 2
        ]
        self.bottom_mesh = Cuboid(size[1], size[0], thickness[4], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        inner_offset_y = (thickness[1] - thickness[0]) / 2
        inner_offset_x = (thickness[3] - thickness[2]) / 2
        top_mesh_position = [
            0,
            0,
            thickness[4] / 2
        ]
        top_mesh_rotation = [np.pi / 2, 0, 0]
        self.top_mesh = Rectangular_Ring(size[2] - thickness[4], size[0], size[1], 
                                         size[0] - thickness[2] - thickness[3],
                                         size[1] - thickness[0] - thickness[1],
                                         [inner_offset_x, -inner_offset_y],
                                         position = top_mesh_position,
                                         rotation = top_mesh_rotation)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Safe/concept_template.py
class Cuboidal_Body(ConceptTemplate):
    def __init__(self, size, thickness, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.thickness = thickness

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0,
            0,
            -(size[2] - thickness[4]) / 2
        ]
        self.bottom_mesh = Cuboid(size[1], size[0], thickness[4], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        inner_offset_y = (thickness[1] - thickness[0]) / 2
        inner_offset_x = (thickness[3] - thickness[2]) / 2
        top_mesh_position = [
            0,
            0,
            thickness[4] / 2
        ]
        top_mesh_rotation = [np.pi / 2, 0, 0]
        self.top_mesh = Rectangular_Ring(size[2] - thickness[4], size[0], size[1], 
                                         size[0] - thickness[2] - thickness[3],
                                         size[1] - thickness[0] - thickness[1],
                                         [inner_offset_x, -inner_offset_y],
                                         position = top_mesh_position,
                                         rotation = top_mesh_rotation)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Safe/concept_template.py
class Mutiple_Layer_Body(ConceptTemplate):
    def __init__(self, size, thickness, main_clapboard_size, main_clapboard_offset, num_of_sub_clapboards, sub_clapboard_1_size, sub_clapboard_1_offset, sub_clapboard_2_size, sub_clapboard_2_offset, sub_clapboard_3_size, sub_clapboard_3_offset, sub_clapboard_4_size, sub_clapboard_4_offset, sub_clapboard_5_size, sub_clapboard_5_offset, sub_clapboard_6_size, sub_clapboard_6_offset, sub_clapboard_7_size, sub_clapboard_7_offset, sub_clapboard_8_size, sub_clapboard_8_offset, sub_clapboard_9_size, sub_clapboard_9_offset, sub_clapboard_10_size, sub_clapboard_10_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.thickness = thickness
        self.main_clapboard_size = main_clapboard_size
        self.main_clapboard_offset = main_clapboard_offset
        self.num_of_sub_clapboards = num_of_sub_clapboards
        self.sub_clapboard_1_size = sub_clapboard_1_size
        self.sub_clapboard_1_offset = sub_clapboard_1_offset
        self.sub_clapboard_2_size = sub_clapboard_2_size
        self.sub_clapboard_2_offset = sub_clapboard_2_offset
        self.sub_clapboard_3_size = sub_clapboard_3_size
        self.sub_clapboard_3_offset = sub_clapboard_3_offset
        self.sub_clapboard_4_size = sub_clapboard_4_size
        self.sub_clapboard_4_offset = sub_clapboard_4_offset
        self.sub_clapboard_5_size = sub_clapboard_5_size
        self.sub_clapboard_5_offset = sub_clapboard_5_offset
        self.sub_clapboard_6_size = sub_clapboard_6_size
        self.sub_clapboard_6_offset = sub_clapboard_6_offset
        self.sub_clapboard_7_size = sub_clapboard_7_size
        self.sub_clapboard_7_offset = sub_clapboard_7_offset
        self.sub_clapboard_8_size = sub_clapboard_8_size
        self.sub_clapboard_8_offset = sub_clapboard_8_offset
        self.sub_clapboard_9_size = sub_clapboard_9_size
        self.sub_clapboard_9_offset = sub_clapboard_9_offset
        self.sub_clapboard_10_size = sub_clapboard_10_size
        self.sub_clapboard_10_offset = sub_clapboard_10_offset


        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0,
            0,
            -(size[2] - thickness[4]) / 2
        ]
        self.bottom_mesh = Cuboid(size[1], size[0], thickness[4], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        inner_offset_y = (thickness[1] - thickness[0]) / 2
        inner_offset_x = (thickness[3] - thickness[2]) / 2
        top_mesh_position = [
            0,
            0,
            thickness[4] / 2
        ]
        top_mesh_rotation = [np.pi / 2, 0, 0]
        self.top_mesh = Rectangular_Ring(size[2] - thickness[4], size[0], size[1], 
                                         size[0] - thickness[2] - thickness[3],
                                         size[1] - thickness[0] - thickness[1],
                                         [inner_offset_x, -inner_offset_y],
                                         position = top_mesh_position,
                                         rotation = top_mesh_rotation)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        board_mesh_position = [
            (thickness[3] - thickness[2]) / 2,
            (thickness[1] - thickness[0]) / 2 + main_clapboard_offset[0],
            thickness[4] / 2 - (size[2] - thickness[4] - main_clapboard_size[1]) / 2
        ]
        self.board_mesh = Cuboid(main_clapboard_size[0], size[0] - thickness[2] - thickness[3], main_clapboard_size[1],
                                 position = board_mesh_position)
        vertices_list.append(self.board_mesh.vertices)
        faces_list.append(self.board_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.board_mesh.vertices)

        for i in range(num_of_sub_clapboards[0]):
            board_mesh_position = [
                (thickness[3] - thickness[2]) / 2 + locals()['sub_clapboard_%d_offset'%(i+1)][0],
                (thickness[1] - thickness[0]) / 2 + locals()['sub_clapboard_%d_offset'%(i+1)][1],
                thickness[4] / 2 - (size[2] - thickness[4] - locals()['sub_clapboard_%d_size'%(i+1)][2]) / 2
            ]
            self.board_mesh = Cuboid(locals()['sub_clapboard_%d_size'%(i+1)][1], locals()['sub_clapboard_%d_size'%(i+1)][0], locals()['sub_clapboard_%d_size'%(i+1)][2],
                                     position = board_mesh_position)
            vertices_list.append(self.board_mesh.vertices)
            faces_list.append(self.board_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.board_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Box/concept_template.py
class Cuboidal_Body(ConceptTemplate):
    def __init__(self, top_size, bottom_size, height, top_bottom_offset, thickness, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.top_size = top_size
        self.bottom_size = bottom_size
        self.height = height
        self.top_bottom_offset = top_bottom_offset
        self.thickness = thickness

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        middle_x = top_size[0] * thickness[1] / height[0] + bottom_size[0] * (height[0] - thickness[1]) / height[0]
        middle_z = top_size[1] * thickness[1] / height[0] + bottom_size[1] * (height[0] - thickness[1]) / height[0]
        middle_offset_x = top_bottom_offset[0] * thickness[1] / height[0]
        middle_offset_z = top_bottom_offset[1] * thickness[1] / height[0]


        top_mesh_position = [
            middle_offset_x,
            thickness[1] / 2,
            middle_offset_z
        ]
        self.top_mesh = Rectangular_Ring(height[0] - thickness[1], top_size[0], top_size[1],
                                         top_size[0] - thickness[0] * 2, top_size[1] - thickness[2] * 2,
                                         [0, 0], middle_x, middle_z,
                                         middle_x - thickness[0] * 2, middle_z - thickness[2] * 2,
                                         top_bottom_offset = [top_bottom_offset[0] - middle_offset_x, top_bottom_offset[1] - middle_offset_z],
                                         position = top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [
            0, 
            -(height[0] - thickness[1]) / 2,
            0
        ]
        self.bottom_mesh = Cuboid(thickness[1], middle_x, middle_z,
                                  bottom_size[0], bottom_size[1],
                                  top_offset = [middle_offset_x, middle_offset_z],
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)


        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Gluestick/concept_template.py
class Cylindrical_Body(ConceptTemplate):
    def __init__(self, size, x_z_ratio, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.x_z_ratio = x_z_ratio

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.base_mesh = Cylinder(size[2], size[0], size[1],
                                  x_z_ratio[0] * size[0], x_z_ratio[0] * size[1])
        vertices_list.append(self.base_mesh.vertices)
        faces_list.append(self.base_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.base_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Gluestick/concept_template.py
class Toothpaste_Body(ConceptTemplate):
    def __init__(self, radius, bottom_length, height, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.radius = radius
        self.bottom_length = bottom_length
        self.height = height

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.base_mesh = Cylinder(height[0], radius[0],
                                  bottom_radius=0,
                                  bottom_radius_z=bottom_length[0] / 2)
        vertices_list.append(self.base_mesh.vertices)
        faces_list.append(self.base_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.base_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Gluestick/concept_template.py
class Cuboidal_Body(ConceptTemplate):
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

        self.base_mesh = Cuboid(size[2], size[0], size[1])
        vertices_list.append(self.base_mesh.vertices)
        faces_list.append(self.base_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.base_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Stapler/concept_template.py
class Standard_Body(ConceptTemplate):
    def __init__(self, base_size, beside_size, beside_seperation, beside_offset_z, has_shaft, shaft_central_size, shaft_beside_size, shaft_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.base_size = base_size
        self.beside_size = beside_size
        self.beside_seperation = beside_seperation
        self.beside_offset_z = beside_offset_z
        self.has_shaft = has_shaft
        self.shaft_central_size = shaft_central_size
        self.shaft_beside_size = shaft_beside_size
        self.shaft_offset = shaft_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.base_mesh = Cuboid(base_size[1], base_size[0], base_size[2])
        vertices_list.append(self.base_mesh.vertices)
        faces_list.append(self.base_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.base_mesh.vertices)

        left_mesh_position = [
            beside_seperation[0] / 2,
            (base_size[1] + beside_size[1]) / 2,
            -base_size[2] / 2 + beside_size[2] / 2 + beside_offset_z[0]
        ]
        self.left_mesh = Cuboid(beside_size[1], beside_size[0], beside_size[2],
                                position = left_mesh_position)
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        right_mesh_position = [
            -beside_seperation[0] / 2,
            (base_size[1] + beside_size[1]) / 2,
            -base_size[2] / 2 + beside_size[2] / 2 + beside_offset_z[0]
        ]
        self.right_mesh = Cuboid(beside_size[1], beside_size[0], beside_size[2],
                                 position = right_mesh_position)
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        if has_shaft[0] == 1:
            central_shaft_mesh_position = [
                0,
                (base_size[1] + beside_size[1]) / 2 + shaft_offset[0],
                -base_size[2] / 2 + beside_size[2] / 2 + beside_offset_z[0] + shaft_offset[1]
            ]
            central_shaft_mesh_rotation = [0, 0, np.pi / 2]
            self.central_shaft_mesh = Cylinder(shaft_central_size[1], shaft_central_size[0],
                                               position = central_shaft_mesh_position,
                                               rotation = central_shaft_mesh_rotation)
            vertices_list.append(self.central_shaft_mesh.vertices)
            faces_list.append(self.central_shaft_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.central_shaft_mesh.vertices)

            left_shaft_mesh_position = [
                (shaft_central_size[1] + shaft_beside_size[1]) / 2,
                (base_size[1] + beside_size[1]) / 2 + shaft_offset[0],
                -base_size[2] / 2 + beside_size[2] / 2 + beside_offset_z[0] + shaft_offset[1]
            ]
            left_shaft_mesh_rotation = [0, 0, np.pi / 2]
            self.left_shaft_mesh = Cylinder(shaft_beside_size[1], shaft_beside_size[0],
                                            position = left_shaft_mesh_position,
                                            rotation = left_shaft_mesh_rotation)
            vertices_list.append(self.left_shaft_mesh.vertices)
            faces_list.append(self.left_shaft_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.left_shaft_mesh.vertices)

            right_shaft_mesh_position = [
                -(shaft_central_size[1] + shaft_beside_size[1]) / 2,
                (base_size[1] + beside_size[1]) / 2 + shaft_offset[0],
                -base_size[2] / 2 + beside_size[2] / 2 + beside_offset_z[0] + shaft_offset[1]
            ]
            right_shaft_mesh_rotation = [0, 0, np.pi / 2]
            self.right_shaft_mesh = Cylinder(shaft_beside_size[1], shaft_beside_size[0],
                                             position = right_shaft_mesh_position,
                                             rotation = right_shaft_mesh_rotation)
            vertices_list.append(self.right_shaft_mesh.vertices)
            faces_list.append(self.right_shaft_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.right_shaft_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Oven/concept_template.py
class Cuboidal_Body(ConceptTemplate):
    def __init__(self, size, thickness, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.thickness = thickness

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0,
            0,
            -(size[2] - thickness[4]) / 2
        ]
        self.bottom_mesh = Cuboid(size[1], size[0], thickness[4], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        inner_offset_y = (thickness[1] - thickness[0]) / 2
        inner_offset_x = (thickness[3] - thickness[2]) / 2
        top_mesh_position = [
            0,
            0,
            thickness[4] / 2
        ]
        top_mesh_rotation = [np.pi / 2, 0, 0]
        self.top_mesh = Rectangular_Ring(size[2] - thickness[4], size[0], size[1], 
                                         size[0] - thickness[2] - thickness[3],
                                         size[1] - thickness[0] - thickness[1],
                                         [inner_offset_x, -inner_offset_y],
                                         position = top_mesh_position,
                                         rotation = top_mesh_rotation)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Oven/concept_template.py
class Double_Layer_Body(ConceptTemplate):
    def __init__(self, size, thickness, clapboard_size, clapboard_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.thickness = thickness
        self.clapboard_size = clapboard_size
        self.clapboard_offset = clapboard_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0,
            0,
            -(size[2] - thickness[4]) / 2
        ]
        self.bottom_mesh = Cuboid(size[1], size[0], thickness[4], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        inner_offset_y = (thickness[1] - thickness[0]) / 2
        inner_offset_x = (thickness[3] - thickness[2]) / 2
        top_mesh_position = [
            0,
            0,
            thickness[4] / 2
        ]
        top_mesh_rotation = [np.pi / 2, 0, 0]
        self.top_mesh = Rectangular_Ring(size[2] - thickness[4], size[0], size[1], 
                                         size[0] - thickness[2] - thickness[3],
                                         size[1] - thickness[0] - thickness[1],
                                         [inner_offset_x, -inner_offset_y],
                                         position = top_mesh_position,
                                         rotation = top_mesh_rotation)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        board_mesh_position = [
            (thickness[3] - thickness[2]) / 2,
            (thickness[1] - thickness[0]) / 2 + clapboard_offset[0],
            thickness[4] / 2 - (size[2] - thickness[4] - clapboard_size[1]) / 2
        ]
        self.board_mesh = Cuboid(clapboard_size[0], size[0] - thickness[2] - thickness[3], clapboard_size[1],
                                 position = board_mesh_position)
        vertices_list.append(self.board_mesh.vertices)
        faces_list.append(self.board_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.board_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Oven/concept_template.py
class Flat_Top(ConceptTemplate):
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

        self.semantic = 'Body'


# Source: Dishwasher/concept_template.py
class Cuboidal_Body(ConceptTemplate):
    def __init__(self, size, thickness, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.thickness = thickness

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0,
            0,
            -(size[2] - thickness[4]) / 2
        ]
        self.bottom_mesh = Cuboid(size[1], size[0], thickness[4], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        inner_offset_y = (thickness[1] - thickness[0]) / 2
        inner_offset_x = (thickness[3] - thickness[2]) / 2
        top_mesh_position = [
            0,
            0,
            thickness[4] / 2
        ]
        top_mesh_rotation = [np.pi / 2, 0, 0]
        self.top_mesh = Rectangular_Ring(size[2] - thickness[4], size[0], size[1], 
                                         size[0] - thickness[2] - thickness[3],
                                         size[1] - thickness[0] - thickness[1],
                                         [inner_offset_x, -inner_offset_y],
                                         position = top_mesh_position,
                                         rotation = top_mesh_rotation)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Dishwasher/concept_template.py
class Double_Layer_Body(ConceptTemplate):
    def __init__(self, size, thickness, clapboard_size, clapboard_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.thickness = thickness
        self.clapboard_size = clapboard_size
        self.clapboard_offset = clapboard_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0,
            0,
            -(size[2] - thickness[4]) / 2
        ]
        self.bottom_mesh = Cuboid(size[1], size[0], thickness[4], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        inner_offset_y = (thickness[1] - thickness[0]) / 2
        inner_offset_x = (thickness[3] - thickness[2]) / 2
        top_mesh_position = [
            0,
            0,
            thickness[4] / 2
        ]
        top_mesh_rotation = [np.pi / 2, 0, 0]
        self.top_mesh = Rectangular_Ring(size[2] - thickness[4], size[0], size[1], 
                                         size[0] - thickness[2] - thickness[3],
                                         size[1] - thickness[0] - thickness[1],
                                         [inner_offset_x, -inner_offset_y],
                                         position = top_mesh_position,
                                         rotation = top_mesh_rotation)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        board_mesh_position = [
            (thickness[3] - thickness[2]) / 2,
            (thickness[1] - thickness[0]) / 2 + clapboard_offset[0],
            thickness[4] / 2 - (size[2] - thickness[4] - clapboard_size[1]) / 2
        ]
        self.board_mesh = Cuboid(clapboard_size[0], size[0] - thickness[2] - thickness[3], clapboard_size[1],
                                 position = board_mesh_position)
        vertices_list.append(self.board_mesh.vertices)
        faces_list.append(self.board_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.board_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: StorageFurniture/concept_template.py
class Storagefurniture_body(ConceptTemplate):
    def __init__(self, size, back_size, left_right_inner_size, base_size, has_lid, lid_size, lid_offset,
                 WHOLE_number_of_layer, WHOLE_layer_sizes, WHOLE_layer_offset, WHOLE_interval_between_layers,
                 storagefurniture_layers_params, additional_layers_params, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        additional_layers_params = [x / 180 * np.pi if ((i > 1) and ((i - 1) % 9 in [6, 7, 8])) else x for i, x in enumerate(additional_layers_params)]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.back_size = back_size
        self.left_right_inner_size = left_right_inner_size
        self.base_size = base_size
        self.has_lid = has_lid
        self.lid_size = lid_size
        self.lid_offset = lid_offset
        self.WHOLE_number_of_layer = WHOLE_number_of_layer
        self.WHOLE_layer_sizes = WHOLE_layer_sizes
        self.WHOLE_layer_offset = WHOLE_layer_offset
        self.WHOLE_interval_between_layers = WHOLE_interval_between_layers
        self.EACH_number_of_layer = [storagefurniture_layers_params[i * 5] for i in range(WHOLE_number_of_layer[0] + 1)]
        self.EACH_layer_sizes = [storagefurniture_layers_params[i * 5 + 1: i * 5 + 3] for i in range(WHOLE_number_of_layer[0] + 1)]
        self.EACH_layer_offset = [storagefurniture_layers_params[i * 5 + 3] for i in range(WHOLE_number_of_layer[0] + 1)]
        self.EACH_interval_between_layers = [storagefurniture_layers_params[i * 5 + 4] for i in range(WHOLE_number_of_layer[0] + 1)]
        self.number_of_additional_layers = additional_layers_params[0]
        self.additional_layers_attributes = additional_layers_params[1:]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        body_mesh_number = 4
        lid_mesh_number = 1 if has_lid[0] == 1 else 0
        WHOLE_layer_mesh_number = WHOLE_number_of_layer[0]
        TOTAL_EACH_layer_mesh_number = sum(self.EACH_number_of_layer)
        TOTAL_mesh_list = [body_mesh_number, lid_mesh_number, WHOLE_layer_mesh_number, TOTAL_EACH_layer_mesh_number]
        record_layer_position = []

        for mesh_idx in range(sum(TOTAL_mesh_list[:3])):
            if mesh_idx < TOTAL_mesh_list[0]:
                if mesh_idx < 2:
                    position_sign = -1 if mesh_idx == 0 else 1
                    mesh_position = [position_sign * (size[0] - left_right_inner_size[0]) / 2, 0, 0]
                    self.mesh = Cuboid(size[1], left_right_inner_size[0], size[2], position=mesh_position)
                elif mesh_idx == 3:
                    mesh_position = [0, -(size[1] - base_size[0]) / 2, 0]
                    self.mesh = Cuboid(base_size[0], size[0] - 2 * left_right_inner_size[0], size[2], position=mesh_position)
                else:
                    mesh_position = [0, 0, (back_size[0] - size[2]) / 2]
                    self.mesh = Cuboid(size[1], size[0], back_size[0], position=mesh_position)
            elif mesh_idx < sum(TOTAL_mesh_list[:2]):
                if has_lid[0] == 1:
                    mesh_position = [lid_offset[0], lid_offset[1] + size[1] / 2 + lid_size[1] / 2, lid_offset[2] + back_size[0] / 2]
                    self.mesh = Cuboid(lid_size[1], lid_size[0], lid_size[2], position=mesh_position)
                else:
                    pass
            else:
                record_layer_position.append(WHOLE_layer_offset[0] + (mesh_idx - sum(TOTAL_mesh_list[:2])) * WHOLE_interval_between_layers[mesh_idx - sum(TOTAL_mesh_list[:2]) - 1])
                mesh_position = [0, size[1] / 2 - record_layer_position[mesh_idx - sum(TOTAL_mesh_list[:2])], 0]
                self.mesh = Cuboid(WHOLE_layer_sizes[0], size[0] - 2 * left_right_inner_size[0], size[2], position=mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        for space_idx in range(WHOLE_layer_mesh_number + 1):
            if WHOLE_layer_mesh_number == 0:
                _height = size[1] - base_size[0]
                _pos = base_size[0] / 2
            elif space_idx == 0:
                _height = WHOLE_layer_offset[0] - WHOLE_layer_sizes[0] / 2
                _pos = size[1] / 2 - WHOLE_layer_offset[0] + _height / 2 + WHOLE_layer_sizes[0] / 2
            elif space_idx == WHOLE_layer_mesh_number:
                _height = size[1] - record_layer_position[space_idx - 1] - WHOLE_layer_sizes[0] / 2 - base_size[0]
                _pos = -size[1] / 2 + _height / 2 + base_size[0]
            else:
                _height = WHOLE_interval_between_layers[space_idx - 1]
                _pos = size[1] / 2 - record_layer_position[space_idx] + _height / 2

            for mesh_idx in range(self.EACH_number_of_layer[space_idx]):
                mesh_position = [-size[0] / 2 + (self.EACH_layer_offset[space_idx] + mesh_idx * self.EACH_interval_between_layers[space_idx]) + left_right_inner_size[0], _pos, 0]
                self.mesh = Cuboid(_height, self.EACH_layer_sizes[space_idx][0], self.EACH_layer_sizes[space_idx][1], position=mesh_position)
                vertices_list.append(self.mesh.vertices)
                faces_list.append(self.mesh.faces + total_num_vertices)
                total_num_vertices += len(self.mesh.vertices)

        for additional_idx in range(self.number_of_additional_layers):
            mesh_position = [self.additional_layers_attributes[9 * additional_idx + 3] - position[0],
                             self.additional_layers_attributes[9 * additional_idx + 4] - position[1],
                             self.additional_layers_attributes[9 * additional_idx + 5] - position[2]]
            mesh_rotation = [self.additional_layers_attributes[9 * additional_idx + 6],
                             self.additional_layers_attributes[9 * additional_idx + 7],
                             self.additional_layers_attributes[9 * additional_idx + 8]]
            self.additional_mesh = Cuboid(self.additional_layers_attributes[9 * additional_idx + 1],
                                          self.additional_layers_attributes[9 * additional_idx],
                                          self.additional_layers_attributes[9 * additional_idx + 2],
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

        self.semantic = 'Body'


# Source: Pen/concept_template.py
class Cylindrical_Barrel(ConceptTemplate):
    def __init__(self, size, thickness, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.thickness = thickness

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.mesh = Ring(size[2], size[0], size[0] - thickness[0],
                         outer_bottom_radius = size[1],
                         inner_bottom_radius = size[1] - thickness[0])
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Pen/concept_template.py
class Double_Layer_Barrel(ConceptTemplate):
    def __init__(self, main_size, bottom_size, thickness, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.main_size = main_size
        self.bottom_size = bottom_size
        self.thickness = thickness

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.mesh = Ring(main_size[2], main_size[0], main_size[0] - thickness[0],
                         outer_bottom_radius = main_size[1],
                         inner_bottom_radius = main_size[1] - thickness[0])
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        bottom_mesh_position = [
            0,
            -(main_size[2] + bottom_size[1]) / 2,
            0
        ]
        self.bottom_mesh = Ring(bottom_size[1], main_size[1], main_size[1] - thickness[0],
                                outer_bottom_radius = bottom_size[0],
                                inner_bottom_radius = bottom_size[0] - thickness[0],
                                position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: USB/concept_template.py
class Regular_Body(ConceptTemplate):
    def __init__(self, size, has_back_part, has_side_part, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.has_back_part = has_back_part
        self.size = size
        self.has_side_part = has_side_part

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        main_mesh_position = [0, 0, -size[2] / 2]
        self.main_mesh = Cuboid(size[1], size[0], size[2],
                                position=main_mesh_position)
        vertices_list.append(self.main_mesh.vertices)
        faces_list.append(self.main_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.main_mesh.vertices)

        if has_back_part[0]:
            back_mesh_position = [0, 0, -size[2]]
            back_mesh_rotation = [0, np.pi, np.pi / 2]
            self.back_mesh = Cylinder(size[0], size[1] / 2, size[1] / 2, is_half=True,
                                      position=back_mesh_position,
                                      rotation=back_mesh_rotation)
            vertices_list.append(self.back_mesh.vertices)
            faces_list.append(self.back_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.back_mesh.vertices)

        if has_side_part[0]:
            left_mesh_position = [-size[0] / 2, 0, -size[2] / 2]
            left_mesh_rotation = [np.pi / 2, 0, -np.pi / 2]
            self.left_mesh = Cylinder(size[2], size[1] / 2, size[1] / 2, is_half=True,
                                      position=left_mesh_position,
                                      rotation=left_mesh_rotation)
            vertices_list.append(self.left_mesh.vertices)
            faces_list.append(self.left_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.left_mesh.vertices)

            right_mesh_position = [size[0] / 2, 0, -size[2] / 2]
            right_mesh_rotation = [np.pi / 2, 0, np.pi / 2]
            self.right_mesh = Cylinder(size[2], size[1] / 2, size[1] / 2, is_half=True,
                                       position=right_mesh_position,
                                       rotation=right_mesh_rotation)
            vertices_list.append(self.right_mesh.vertices)
            faces_list.append(self.right_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.right_mesh.vertices)

        if has_back_part[0] and has_side_part[0]:
            left_back_mesh_position = [-size[0] / 2, 0, -size[2]]
            left_back_mesh_rotation = [0, np.pi, 0]
            self.left_back_mesh = Sphere(radius=size[1] / 2, longitude_angle=np.pi / 2,
                                         position=left_back_mesh_position,
                                         rotation=left_back_mesh_rotation)
            vertices_list.append(self.left_back_mesh.vertices)
            faces_list.append(self.left_back_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.left_back_mesh.vertices)

            right_back_mesh_position = [size[0] / 2, 0, -size[2]]
            right_back_mesh_rotation = [0, np.pi / 2, 0]
            self.right_back_mesh = Sphere(radius=size[1] / 2, longitude_angle=np.pi / 2,
                                          position=right_back_mesh_position,
                                          rotation=right_back_mesh_rotation)
            vertices_list.append(self.right_back_mesh.vertices)
            faces_list.append(self.right_back_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.right_back_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: USB/concept_template.py
class RoundEnded_Body(ConceptTemplate):
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

        main_mesh_position = [0, 0, -size[2] / 2]
        self.main_mesh = Cuboid(size[1], size[0], size[2],
                                position=main_mesh_position)
        vertices_list.append(self.main_mesh.vertices)
        faces_list.append(self.main_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.main_mesh.vertices)

        back_mesh_position = [0, 0, -size[2]]
        back_mesh_rotation = [0, np.pi, 0]
        self.back_mesh = Cylinder(size[1], size[0] / 2, size[0] / 2, is_half=True,
                                  position=back_mesh_position,
                                  rotation=back_mesh_rotation)
        vertices_list.append(self.back_mesh.vertices)
        faces_list.append(self.back_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.back_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: KitchenPot/concept_template.py
class Cylindrical_Body(ConceptTemplate):
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

        middle_radius = outer_size[0] * (1 - inner_size[2] / outer_size[2]) + outer_size[1] * inner_size[2] / outer_size[2]
        bottom_height = outer_size[2] - inner_size[2]
        bottom_mesh_position = [0, -inner_size[2] / 2, 0]
        self.bottom_mesh = Cylinder(bottom_height, middle_radius, outer_size[1], 
                                    position=bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        top_mesh_position = [0, (outer_size[2] - inner_size[2]) / 2, 0]
        self.top_mesh = Ring(inner_size[2], outer_size[0], inner_size[0], 
                             outer_bottom_radius = middle_radius,
                             inner_bottom_radius = inner_size[1],
                             position=top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Kettle/concept_template.py
class Semi_Spherical_Body(ConceptTemplate):
    def __init__(self, horizontal_axis, vertical_axis, exist_angle, bottom_size, x_z_ratio, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        exist_angle = [x / 180 * np.pi for x in exist_angle]
        super().__init__(position, rotation)

        # Record Parameters
        self.horizontal_axis = horizontal_axis
        self.vertical_axis = vertical_axis
        self.exist_angle = exist_angle
        self.bottom_size = bottom_size
        self.x_z_ratio = x_z_ratio

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.top_mesh = Sphere(horizontal_axis[0] * x_z_ratio[0], np.pi / 2 - exist_angle[0], np.pi / 2,
                               radius_y = vertical_axis[0], 
                               radius_z = horizontal_axis[0])
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        middle_mesh_rotation = [np.pi, 0, 0]
        self.middle_mesh = Sphere(horizontal_axis[0] * x_z_ratio[0], np.pi / 2 - exist_angle[1], np.pi / 2,
                                  radius_y = vertical_axis[1], 
                                  radius_z = horizontal_axis[0],
                                  rotation = middle_mesh_rotation)
        vertices_list.append(self.middle_mesh.vertices)
        faces_list.append(self.middle_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.middle_mesh.vertices)

        bottom_radius = horizontal_axis[0] * np.cos(exist_angle[1])
        bottom_offset = horizontal_axis[0] * np.sin(exist_angle[1]) * vertical_axis[1] / horizontal_axis[0]
        bottom_mesh_position = [
            0, 
            -bottom_offset - bottom_size[1] / 2, 
            0
        ]
        self.bottom_mesh = Cylinder(bottom_size[1], bottom_radius * x_z_ratio[0], bottom_size[0] * x_z_ratio[0],
                                    top_radius_z = bottom_radius,
                                    bottom_radius_z = bottom_size[0],
                                    position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Kettle/concept_template.py
class Spherical_Cylindrical_Body(ConceptTemplate):
    def __init__(self, horizontal_axis, vertical_axis, exist_angle, bottom_size, x_z_ratio, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        exist_angle = [x / 180 * np.pi for x in exist_angle]
        super().__init__(position, rotation)

        # Record Parameters
        self.horizontal_axis = horizontal_axis
        self.vertical_axis = vertical_axis
        self.exist_angle = exist_angle
        self.bottom_size = bottom_size
        self.x_z_ratio = x_z_ratio

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.top_mesh = Sphere(horizontal_axis[0] * x_z_ratio[0], np.pi / 2 - exist_angle[0], np.pi / 2,
                               radius_y = vertical_axis[0], 
                               radius_z = horizontal_axis[0])
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [
            0, 
            -bottom_size[1] / 2, 
            0
        ]
        self.bottom_mesh = Cylinder(bottom_size[1], horizontal_axis[0] * x_z_ratio[0], bottom_size[0] * x_z_ratio[0],
                                    top_radius_z = horizontal_axis[0],
                                    bottom_radius_z = bottom_size[0],
                                    position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Kettle/concept_template.py
class Multilevel_Body(ConceptTemplate):
    def __init__(self, num_levels, level_1_bottom_radius, level_1_top_radius, level_1_height, level_2_top_radius=0, level_2_height=0, level_3_top_radius=0, level_3_height=0, level_4_top_radius=0, level_4_height=0, level_5_top_radius=0, level_5_height=0, x_z_ratio=1, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.num_levels = num_levels
        self.level_1_bottom_radius = level_1_bottom_radius
        self.level_1_top_radius = level_1_top_radius
        self.level_1_height = level_1_height
        self.level_2_top_radius = level_2_top_radius
        self.level_2_height = level_2_height
        self.level_3_top_radius = level_3_top_radius
        self.level_3_height = level_3_height
        self.level_4_top_radius = level_4_top_radius
        self.level_4_height = level_4_height
        self.level_5_top_radius = level_5_top_radius
        self.level_5_height = level_5_height
        self.x_z_ratio = x_z_ratio

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_1_top_radius = level_1_top_radius[0] * (1 - level_1_height[1] / level_1_height[0]) + level_1_bottom_radius[0] * level_1_height[1] / level_1_height[0]
        mesh_1_height = level_1_height[0] - level_1_height[1]
        bottom_mesh_position = [0, -level_1_height[1] / 2, 0]
        self.bottom_mesh = Cylinder(mesh_1_height, mesh_1_top_radius * x_z_ratio[0], level_1_bottom_radius[0] * x_z_ratio[0], 
                                    top_radius_z = mesh_1_top_radius,
                                    bottom_radius_z = level_1_bottom_radius[0],
                                    position=bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        top_mesh_position = [0, (level_1_height[0] - level_1_height[1]) / 2, 0]
        self.top_mesh = Ring(level_1_height[1], level_1_top_radius[0], level_1_top_radius[1], 
                             outer_bottom_radius = mesh_1_top_radius,
                             inner_bottom_radius = level_1_bottom_radius[1],
                             x_z_ratio = x_z_ratio[0],
                             position=top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        delta_height = level_1_height[0] / 2
        for i in range(num_levels[0] - 1):
            delta_height += locals()['level_'+ str(i+2) +'_height'][0] / 2
            top_mesh_position = [0, delta_height, 0]
            delta_height += locals()['level_'+ str(i+2) +'_height'][0] / 2
            self.top_mesh = Ring(locals()['level_'+ str(i+2) +'_height'][0], locals()['level_'+ str(i+2) +'_top_radius'][0], locals()['level_'+ str(i+2) +'_top_radius'][1], 
                                 outer_bottom_radius = locals()['level_'+ str(i+1) +'_top_radius'][0],
                                 inner_bottom_radius = locals()['level_'+ str(i+1) +'_top_radius'][1],
                                 x_z_ratio = x_z_ratio[0],
                                 position=top_mesh_position)
            vertices_list.append(self.top_mesh.vertices)
            faces_list.append(self.top_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.top_mesh.vertices)


        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Bucket/concept_template.py
class Cylindrical_Body(ConceptTemplate):
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

        middle_radius = outer_size[0] * (1 - inner_size[2] / outer_size[2]) + outer_size[1] * inner_size[2] / outer_size[2]
        bottom_height = outer_size[2] - inner_size[2]
        bottom_mesh_position = [0, -inner_size[2] / 2, 0]
        self.bottom_mesh = Cylinder(bottom_height, middle_radius, outer_size[1], 
                                    position=bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        top_mesh_position = [0, (outer_size[2] - inner_size[2]) / 2, 0]
        self.top_mesh = Ring(inner_size[2], outer_size[0], inner_size[0], 
                             outer_bottom_radius = middle_radius,
                             inner_bottom_radius = inner_size[1],
                             position=top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)


        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Bucket/concept_template.py
class Prismatic_Body(ConceptTemplate):
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

        middle_radius = outer_size[0] * (1 - inner_size[2] / outer_size[2]) + outer_size[1] * inner_size[2] / outer_size[2]
        bottom_height = outer_size[2] - inner_size[2]
        bottom_mesh_position = [0, -inner_size[2] / 2, 0]
        self.bottom_mesh = Cuboid(bottom_height, middle_radius * np.sqrt(2), middle_radius * np.sqrt(2), 
                                  outer_size[1] * np.sqrt(2), outer_size[1] * np.sqrt(2),
                                  position=bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        top_mesh_position = [0, (outer_size[2] - inner_size[2]) / 2, 0]
        self.top_mesh = Rectangular_Ring(inner_size[2], outer_size[0] * np.sqrt(2), outer_size[0] * np.sqrt(2), 
                                         inner_size[0] * np.sqrt(2), inner_size[0] * np.sqrt(2),
                                         outer_bottom_length = middle_radius * np.sqrt(2), outer_bottom_width = middle_radius * np.sqrt(2), 
                                         inner_bottom_length = inner_size[1] * np.sqrt(2), inner_bottom_width = inner_size[1] * np.sqrt(2), 
                                         position=top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)


        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Table/concept_template.py
class Regular_desktop(ConceptTemplate):
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

        self.desktop_mesh = Cuboid(self.size[1], self.size[0], self.size[2])
        vertices_list.append(self.desktop_mesh.vertices)
        faces_list.append(self.desktop_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.desktop_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Table/concept_template.py
class Cylindrical_desktop(ConceptTemplate):
    def __init__(self, size, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.radius = size[0]
        self.height = size[1]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.desktop_mesh = Cylinder(self.height, self.radius)
        vertices_list.append(self.desktop_mesh.vertices)
        faces_list.append(self.desktop_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.desktop_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Table/concept_template.py
class L_type_desktop(ConceptTemplate):
    def __init__(self, horizontal_size, vertical_size, desktop_angle, position=[0, 0, 0], rotation=[0, 0, 0]):
        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        desktop_angle = [x / 180 * np.pi for x in desktop_angle]

        # Record Parameters
        self.horizontal_size = horizontal_size
        self.vertical_size = vertical_size
        self.desktop_angle = desktop_angle
        self.position = position
        self.rotation = rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.base_mesh = Cuboid(self.horizontal_size[1], self.horizontal_size[0], self.horizontal_size[2])
        vertices_list.append(self.base_mesh.vertices)
        faces_list.append(self.base_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.base_mesh.vertices)

        other_mesh_rotation = [0, desktop_angle[0], 0]
        other_mesh_position = [-horizontal_size[0] / 2 - np.sqrt(vertical_size[0] ** 2) *
                               np.sin(desktop_angle[0]),
                               0,
                               -horizontal_size[1] / 2 - np.sqrt(vertical_size[0] ** 2) *
                               np.cos(desktop_angle[0])]
        self.other_mesh = Cuboid(self.horizontal_size[1], self.horizontal_size[0], self.horizontal_size[2],
                                 position=other_mesh_position, rotation=other_mesh_rotation)
        vertices_list.append(self.other_mesh.vertices)
        faces_list.append(self.other_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.other_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Mug/concept_template.py
class Cylindrical_Body(ConceptTemplate):
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

        middle_radius = outer_size[0] * (1 - inner_size[2] / outer_size[2]) + outer_size[1] * inner_size[2] / outer_size[2]
        bottom_height = outer_size[2] - inner_size[2]
        bottom_mesh_position = [0, -inner_size[2] / 2, 0]
        self.bottom_mesh = Cylinder(bottom_height, middle_radius, outer_size[1], 
                                    position=bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        top_mesh_position = [0, (outer_size[2] - inner_size[2]) / 2, 0]
        self.top_mesh = Ring(inner_size[2], outer_size[0], inner_size[0], 
                             outer_bottom_radius = middle_radius,
                             inner_bottom_radius = inner_size[1],
                             position=top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Mug/concept_template.py
class Prismatic_Body(ConceptTemplate):
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

        middle_radius = outer_size[0] * (1 - inner_size[2] / outer_size[2]) + outer_size[1] * inner_size[2] / outer_size[2]
        bottom_height = outer_size[2] - inner_size[2]
        bottom_mesh_position = [0, -inner_size[2] / 2, 0]
        self.bottom_mesh = Cuboid(bottom_height, middle_radius * np.sqrt(2), middle_radius * np.sqrt(2), 
                                  outer_size[1] * np.sqrt(2), outer_size[1] * np.sqrt(2),
                                  position=bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        top_mesh_position = [0, (outer_size[2] - inner_size[2]) / 2, 0]
        self.top_mesh = Rectangular_Ring(inner_size[2], outer_size[0] * np.sqrt(2), outer_size[0] * np.sqrt(2), 
                                         inner_size[0] * np.sqrt(2), inner_size[0] * np.sqrt(2),
                                         outer_bottom_length = middle_radius * np.sqrt(2), outer_bottom_width = middle_radius * np.sqrt(2), 
                                         inner_bottom_length = inner_size[1] * np.sqrt(2), inner_bottom_width = inner_size[1] * np.sqrt(2), 
                                         position=top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Mug/concept_template.py
class Multilevel_Body(ConceptTemplate):
    def __init__(self, num_levels, level_1_bottom_radius, level_1_top_radius, level_1_height, level_2_top_radius=0, level_2_height=0, level_3_top_radius=0, level_3_height=0, level_4_top_radius=0, level_4_height=0, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.num_levels = num_levels
        self.level_1_bottom_radius = level_1_bottom_radius
        self.level_1_top_radius = level_1_top_radius
        self.level_1_height = level_1_height
        self.level_2_top_radius = level_2_top_radius
        self.level_2_height = level_2_height
        self.level_3_top_radius = level_3_top_radius
        self.level_3_height = level_3_height
        self.level_4_top_radius = level_4_top_radius
        self.level_4_height = level_4_height

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_1_top_radius = level_1_top_radius[0] * (1 - level_1_height[1] / level_1_height[0]) + level_1_bottom_radius[0] * level_1_height[1] / level_1_height[0]
        mesh_1_height = level_1_height[0] - level_1_height[1]
        bottom_mesh_position = [0, -level_1_height[1] / 2, 0]
        self.bottom_mesh = Cylinder(mesh_1_height, mesh_1_top_radius, level_1_bottom_radius[0], 
                                    position=bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        top_mesh_position = [0, (level_1_height[0] - level_1_height[1]) / 2, 0]
        self.top_mesh = Ring(level_1_height[1], level_1_top_radius[0], level_1_top_radius[1], 
                             outer_bottom_radius = mesh_1_top_radius,
                             inner_bottom_radius = level_1_bottom_radius[1],
                             position=top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        delta_height = level_1_height[0] / 2
        for i in range(num_levels[0] - 1):
            delta_height += locals()['level_'+ str(i+2) +'_height'][0] / 2
            top_mesh_position = [0, delta_height, 0]
            delta_height += locals()['level_'+ str(i+2) +'_height'][0] / 2
            self.top_mesh = Ring(locals()['level_'+ str(i+2) +'_height'][0], locals()['level_'+ str(i+2) +'_top_radius'][0], locals()['level_'+ str(i+2) +'_top_radius'][1], 
                                 outer_bottom_radius = locals()['level_'+ str(i+1) +'_top_radius'][0],
                                 inner_bottom_radius = locals()['level_'+ str(i+1) +'_top_radius'][1],
                                 position=top_mesh_position)
            vertices_list.append(self.top_mesh.vertices)
            faces_list.append(self.top_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.top_mesh.vertices)


        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Switch/concept_template.py
class Standard_Base(ConceptTemplate):
    def __init__(self, size, has_back_part, back_part_size, back_part_offset, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.has_back_part = has_back_part
        self.size = size
        self.back_part_size = back_part_size
        self.back_part_offset = back_part_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        back_mesh_position = [0, 0, -size[2] / 2]
        self.back_mesh = Cuboid(size[1], size[0], size[2],
                                position=back_mesh_position)
        vertices_list.append(self.back_mesh.vertices)
        faces_list.append(self.back_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.back_mesh.vertices)

        if has_back_part[0]:
            back_mesh_position = [
                back_part_offset[0], 
                back_part_offset[1], 
                -size[2] - back_part_size[2] / 2
            ]
            self.back_mesh = Cuboid(back_part_size[1], back_part_size[0], back_part_size[2],
                                    position=back_mesh_position)
            vertices_list.append(self.back_mesh.vertices)
            faces_list.append(self.back_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.back_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Switch/concept_template.py
class Frame_Base(ConceptTemplate):
    def __init__(self, size, inner_size, inner_outer_offset, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.inner_size = inner_size
        self.inner_outer_offset = inner_outer_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        back_mesh_rotation = [np.pi / 2, 0, 0]
        self.back_mesh = Rectangular_Ring(size[2], size[0], size[1],
                                          inner_size[0], inner_size[1],
                                          [inner_outer_offset[0], -inner_outer_offset[1]],
                                          rotation=back_mesh_rotation)
        vertices_list.append(self.back_mesh.vertices)
        faces_list.append(self.back_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.back_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Switch/concept_template.py
class Parallel_Base(ConceptTemplate):
    def __init__(self, size, sub_offset, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.sub_offset = sub_offset
        self.size = size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        left_mesh_position = [
            -size[0] / 2, 
            0, 
            -size[4] / 2
        ]
        self.left_mesh = Cuboid(size[2], size[0], size[4],
                                position=left_mesh_position)
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        right_mesh_position = [
            size[1] / 2, 
            sub_offset[0], 
            -size[4] / 2
        ]
        self.right_mesh = Cuboid(size[3], size[1], size[4],
                                 position=right_mesh_position)
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Washingmachine/concept_template.py
class Front_Facing_Roller_Body(ConceptTemplate):
    def __init__(self, outer_size, inner_size, inner_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.outer_size = outer_size
        self.inner_size = inner_size
        self.inner_offset = inner_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0,
            0,
            -inner_size[1] / 2
        ]
        self.bottom_mesh = Cuboid(outer_size[1], outer_size[0], outer_size[2] - inner_size[1], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        top_mesh_position = [
            0,
            0,
            (outer_size[2] - inner_size[1]) / 2
        ]
        self.top_mesh = Box_Cylinder_Ring(outer_size[1], outer_size[0], inner_size[1], inner_size[0], 
                                          inner_cylinder_offset = [inner_offset[0], inner_offset[1]],
                                          position = top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Washingmachine/concept_template.py
class Upright_Roller_Body(ConceptTemplate):
    def __init__(self, outer_size, inner_size, inner_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.outer_size = outer_size
        self.inner_size = inner_size
        self.inner_offset = inner_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0,
            -inner_size[1] / 2,
            0
        ]
        self.bottom_mesh = Cuboid(outer_size[1] - inner_size[1], outer_size[0], outer_size[2], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        top_mesh_position = [
            0,
            (outer_size[1] - inner_size[1]) / 2,
            0
        ]
        top_mesh_rotation = [-np.pi / 2, 0, 0]
        self.top_mesh = Box_Cylinder_Ring(outer_size[2], outer_size[0], inner_size[1], inner_size[0], 
                                          inner_cylinder_offset = [inner_offset[0], -inner_offset[1]],
                                          position = top_mesh_position,
                                          rotation = top_mesh_rotation)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Washingmachine/concept_template.py
class Cuboidal_Body(ConceptTemplate):
    def __init__(self, outer_size, thickness, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.outer_size = outer_size
        self.thickness = thickness

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0,
            -(outer_size[1] - thickness[2]) / 2,
            0
        ]
        self.bottom_mesh = Cuboid(thickness[2], outer_size[0], outer_size[2], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        top_mesh_position = [
            0,
            thickness[2] / 2,
            0
        ]
        self.top_mesh = Rectangular_Ring(outer_size[1] - thickness[2], outer_size[0], outer_size[2], 
                                         outer_size[0] - thickness[1] * 2,
                                         outer_size[2] - thickness[0] * 2,
                                         position = top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Dispenser/concept_template.py
class Multilevel_Body(ConceptTemplate):
    def __init__(self, num_levels, level_1_size, level_2_size, level_3_size, level_4_size, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.num_levels = num_levels
        self.level_1_size = level_1_size
        self.level_2_size = level_2_size
        self.level_3_size = level_3_size
        self.level_4_size = level_4_size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.bottom_mesh = Cylinder(level_1_size[1], level_1_size[0], level_1_size[2])
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        delta_height = level_1_size[1] / 2
        for i in range(num_levels[0] - 1):
            delta_height += locals()['level_'+ str(i+2) +'_size'][1] / 2
            mesh_position = [0, delta_height, 0]
            delta_height += locals()['level_'+ str(i+2) +'_size'][1] / 2
            self.mesh = Cylinder(locals()['level_'+ str(i+2) +'_size'][1], locals()['level_'+ str(i+2) +'_size'][0], locals()['level_'+ str(i+1) +'_size'][0], 
                                 position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order='YXZ')

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Dispenser/concept_template.py
class Cuboidal_Body(ConceptTemplate):
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

        self.mesh = Cuboid(size[1], size[0], size[2])
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order='YXZ')

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Shampoo/concept_template.py
class Cylindrical_body(ConceptTemplate):
    def __init__(self, num_of_part, all_sizes, x_z_ratio, position=[0, 0, 0], rotation=[0, 0, 0]):
        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.num_of_part = num_of_part
        self.all_sizes = [all_sizes[0:3]] + [[all_sizes[i], all_sizes[i + 1]] for i in range(3, len(all_sizes), 2)]
        self.x_z_ratio = x_z_ratio

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        top_radius, bottom_radius, height = self.all_sizes[0][0], self.all_sizes[0][2], self.all_sizes[0][1]
        self.mesh_1 = Cylinder(height=height, top_radius=top_radius, bottom_radius=bottom_radius, top_radius_z=top_radius * x_z_ratio[0],
                               bottom_radius_z=bottom_radius * x_z_ratio[0])
        vertices_list.append(self.mesh_1.vertices)
        faces_list.append(self.mesh_1.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_1.vertices)

        delta_height = self.all_sizes[0][1] / 2
        for part_idx in range(1, num_of_part[0]):
            top_radius, bottom_radius, height = self.all_sizes[part_idx][0], self.all_sizes[part_idx - 1][0], self.all_sizes[part_idx][1]
            delta_height += height
            part_mesh_position = [0, delta_height - height / 2, 0]
            self.part_mesh = Cylinder(height=height, top_radius=top_radius, bottom_radius=bottom_radius, top_radius_z=top_radius * x_z_ratio[0],
                                      bottom_radius_z=bottom_radius * x_z_ratio[0],
                                      position=part_mesh_position)
            vertices_list.append(self.part_mesh.vertices)
            faces_list.append(self.part_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.part_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Shampoo/concept_template.py
class Cuboidal_body(ConceptTemplate):
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

        self.mesh_1 = Cuboid(size[1], size[0], size[2])
        vertices_list.append(self.mesh_1.vertices)
        faces_list.append(self.mesh_1.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_1.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Shampoo/concept_template.py
class Toothpaste_body(ConceptTemplate):
    def __init__(self, radius, bottom_length, height, position=[0, 0, 0], rotation=[0, 0, 0]):
        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.radius = radius
        self.bottom_length = bottom_length
        self.height = height

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.base_mesh = Cylinder(height[0], radius[0],
                                  bottom_radius=1e-2,
                                  bottom_radius_z=bottom_length[0] / 2)
        vertices_list.append(self.base_mesh.vertices)
        faces_list.append(self.base_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.base_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Lighter/concept_template.py
class Cuboidal_Body(ConceptTemplate):
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

        self.mesh = Cuboid(size[1], size[0], size[2])
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Lighter/concept_template.py
class Cambered_Body(ConceptTemplate):
    def __init__(self, size, beside_radius_z, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.beside_radius_z = beside_radius_z

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.mesh = Cuboid(size[1], size[0], size[2])
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        left_mesh_position = [
            0, 
            0,
            -size[2] / 2
        ]
        left_mesh_rotation = [0, np.pi, 0]
        self.left_mesh = Cylinder(size[1], size[0] / 2,
                                  top_radius_z = beside_radius_z[0],
                                  bottom_radius_z = beside_radius_z[0],
                                  is_half = True,
                                  position = left_mesh_position,
                                  rotation = left_mesh_rotation)
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        right_mesh_position = [
            0, 
            0,
            size[2] / 2
        ]
        self.right_mesh = Cylinder(size[1], size[0] / 2,
                                   top_radius_z = beside_radius_z[0],
                                   bottom_radius_z = beside_radius_z[0],
                                   is_half = True,
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

        self.semantic = 'Body'


# Source: Lighter/concept_template.py
class Double_Layer_Body(ConceptTemplate):
    def __init__(self, main_size, top_size, top_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.main_size = main_size
        self.top_size = top_size
        self.top_offset = top_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.mesh = Cuboid(main_size[1], main_size[0], main_size[2])
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        top_mesh_position = [
            top_offset[0], 
            (main_size[1] + top_size[1]) / 2,
            top_offset[1]
        ]
        self.top_mesh = Cuboid(top_size[1], top_size[0], top_size[2],
                               position = top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Refrigerator/concept_template.py
class Cuboidal_Body(ConceptTemplate):
    def __init__(self, size, thickness, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.thickness = thickness

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0,
            0,
            -(size[2] - thickness[4]) / 2
        ]
        self.bottom_mesh = Cuboid(size[1], size[0], thickness[4], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        inner_offset_y = (thickness[1] - thickness[0]) / 2
        inner_offset_x = (thickness[3] - thickness[2]) / 2
        top_mesh_position = [
            0,
            0,
            thickness[4] / 2
        ]
        top_mesh_rotation = [np.pi / 2, 0, 0]
        self.top_mesh = Rectangular_Ring(size[2] - thickness[4], size[0], size[1], 
                                         size[0] - thickness[2] - thickness[3],
                                         size[1] - thickness[0] - thickness[1],
                                         [inner_offset_x, -inner_offset_y],
                                         position = top_mesh_position,
                                         rotation = top_mesh_rotation)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Refrigerator/concept_template.py
class Double_Layer_Body(ConceptTemplate):
    def __init__(self, size, thickness, clapboard_size, clapboard_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.thickness = thickness
        self.clapboard_size = clapboard_size
        self.clapboard_offset = clapboard_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0,
            0,
            -(size[2] - thickness[4]) / 2
        ]
        self.bottom_mesh = Cuboid(size[1], size[0], thickness[4], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        inner_offset_y = (thickness[1] - thickness[0]) / 2
        inner_offset_x = (thickness[3] - thickness[2]) / 2
        top_mesh_position = [
            0,
            0,
            thickness[4] / 2
        ]
        top_mesh_rotation = [np.pi / 2, 0, 0]
        self.top_mesh = Rectangular_Ring(size[2] - thickness[4], size[0], size[1], 
                                         size[0] - thickness[2] - thickness[3],
                                         size[1] - thickness[0] - thickness[1],
                                         [inner_offset_x, -inner_offset_y],
                                         position = top_mesh_position,
                                         rotation = top_mesh_rotation)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        board_mesh_position = [
            (thickness[3] - thickness[2]) / 2,
            (thickness[1] - thickness[0]) / 2 + clapboard_offset[0],
            thickness[4] / 2 - (size[2] - thickness[4] - clapboard_size[1]) / 2
        ]
        self.board_mesh = Cuboid(clapboard_size[0], size[0] - thickness[2] - thickness[3], clapboard_size[1],
                                 position = board_mesh_position)
        vertices_list.append(self.board_mesh.vertices)
        faces_list.append(self.board_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.board_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Refrigerator/concept_template.py
class Left_Right_Double_Layer_Body(ConceptTemplate):
    def __init__(self, size, thickness, clapboard_size, clapboard_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.thickness = thickness
        self.clapboard_size = clapboard_size
        self.clapboard_offset = clapboard_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0,
            0,
            -(size[2] - thickness[4]) / 2
        ]
        self.bottom_mesh = Cuboid(size[1], size[0], thickness[4], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        inner_offset_y = (thickness[1] - thickness[0]) / 2
        inner_offset_x = (thickness[3] - thickness[2]) / 2
        top_mesh_position = [
            0,
            0,
            thickness[4] / 2
        ]
        top_mesh_rotation = [np.pi / 2, 0, 0]
        self.top_mesh = Rectangular_Ring(size[2] - thickness[4], size[0], size[1], 
                                         size[0] - thickness[2] - thickness[3],
                                         size[1] - thickness[0] - thickness[1],
                                         [inner_offset_x, -inner_offset_y],
                                         position = top_mesh_position,
                                         rotation = top_mesh_rotation)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        board_mesh_position = [
            (thickness[3] - thickness[2]) / 2 + clapboard_offset[0],
            (thickness[1] - thickness[0]) / 2,
            thickness[4] / 2 - (size[2] - thickness[4] - clapboard_size[1]) / 2
        ]
        self.board_mesh = Cuboid(size[1] - thickness[0] - thickness[1], clapboard_size[0], clapboard_size[1],
                                 position = board_mesh_position)
        vertices_list.append(self.board_mesh.vertices)
        faces_list.append(self.board_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.board_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Bottle/concept_template.py
class Multilevel_Body(ConceptTemplate):
    def __init__(self, num_levels, level_1_size, level_2_size, level_3_size, level_4_size, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.num_levels = num_levels
        self.level_1_size = level_1_size
        self.level_2_size = level_2_size
        self.level_3_size = level_3_size
        self.level_4_size = level_4_size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.bottom_mesh = Cylinder(level_1_size[1], level_1_size[0], level_1_size[2])
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        delta_height = level_1_size[1] / 2
        for i in range(num_levels[0] - 1):
            delta_height += locals()['level_'+ str(i+2) +'_size'][1] / 2
            mesh_position = [0, delta_height, 0]
            delta_height += locals()['level_'+ str(i+2) +'_size'][1] / 2
            self.mesh = Cylinder(locals()['level_'+ str(i+2) +'_size'][1], locals()['level_'+ str(i+2) +'_size'][0], locals()['level_'+ str(i+1) +'_size'][0], 
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

        self.semantic = 'Body'


# Source: Trashcan/concept_template.py
class Cylindrical_Body(ConceptTemplate):
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

        middle_radius = outer_size[0] * (1 - inner_size[2] / outer_size[2]) + outer_size[1] * inner_size[2] / outer_size[2]
        bottom_height = outer_size[2] - inner_size[2]
        bottom_mesh_position = [0, -inner_size[2] / 2, 0]
        self.bottom_mesh = Cylinder(bottom_height, middle_radius, outer_size[1], 
                                    position=bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        top_mesh_position = [0, (outer_size[2] - inner_size[2]) / 2, 0]
        self.top_mesh = Ring(inner_size[2], outer_size[0], inner_size[0], 
                             outer_bottom_radius = middle_radius,
                             inner_bottom_radius = inner_size[1],
                             position=top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Trashcan/concept_template.py
class Prismatic_Body(ConceptTemplate):
    def __init__(self, top_size, bottom_size, height, top_offset, thickness, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.top_size = top_size
        self.bottom_size = bottom_size
        self.height = height
        self.top_offset = top_offset
        self.thickness = thickness

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_position = [
            0, 
            -(height[1] - height[0]) / 2, 
            0
        ]
        self.mesh = Rectangular_Ring(height[0], top_size[0], top_size[1], 
                                    top_size[0] - thickness[0] * 2, top_size[1] - thickness[1] * 2, 
                                    outer_bottom_length = bottom_size[0], outer_bottom_width = bottom_size[1],
                                    inner_bottom_length = bottom_size[0] - thickness[0] * 2, inner_bottom_width = bottom_size[1] - thickness[1] * 2,
                                    back_height = height[1],
                                    top_bottom_offset = [top_offset[0], top_offset[1]],
                                    position = mesh_position)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        middle_x = (top_size[0] - thickness[0] * 2) * thickness[2] / height[0] + (bottom_size[0] - thickness[0] * 2) * (height[0] - thickness[2]) / height[0]
        middle_z = (top_size[1] - thickness[1] * 2) * thickness[2] / height[0] + (bottom_size[1] - thickness[1] * 2) * (height[0] - thickness[2]) / height[0]
        middle_offset_x = top_offset[0] * thickness[2] / height[0]
        middle_offset_z = top_offset[1] * thickness[2] / height[0]
        bottom_mesh_position = [
            0, 
            -(height[1] - thickness[2]) / 2, 
            0
        ]
        self.bottom_mesh = Cuboid(thickness[2], middle_x, middle_z, 
                                  bottom_length = bottom_size[0] - thickness[0] * 2, bottom_width = bottom_size[1] - thickness[1] * 2,
                                  top_offset = [middle_offset_x, middle_offset_z],
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


# Source: Trashcan/concept_template.py
class Separated_Cylindrical_Body(ConceptTemplate):
    def __init__(self, outer_size, inner_size, clapboard_size, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.outer_size = outer_size
        self.inner_size = inner_size
        self.clapboard_size = clapboard_size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        middle_radius = outer_size[0] * (1 - inner_size[2] / outer_size[2]) + outer_size[1] * inner_size[2] / outer_size[2]
        bottom_height = outer_size[2] - inner_size[2]
        bottom_mesh_position = [0, -inner_size[2] / 2, 0]
        self.bottom_mesh = Cylinder(bottom_height, middle_radius, outer_size[1], 
                                    position=bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        top_mesh_position = [0, (outer_size[2] - inner_size[2]) / 2, 0]
        self.top_mesh = Ring(inner_size[2], outer_size[0], inner_size[0], 
                             outer_bottom_radius = middle_radius,
                             inner_bottom_radius = inner_size[1],
                             position=top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        clapboard_mesh_position = [
            0, 
            clapboard_size[1] / 2 - (outer_size[2] / 2 - (outer_size[2] - inner_size[2])), 
            0
        ]
        self.clapboard_mesh = Cuboid(clapboard_size[1], clapboard_size[0], clapboard_size[2], 
                                     position = clapboard_mesh_position)
        vertices_list.append(self.clapboard_mesh.vertices)
        faces_list.append(self.clapboard_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.clapboard_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'
