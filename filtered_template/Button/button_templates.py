"""
Button Templates
Automatically extracted from concept_template.py files
Contains 8 class(es)
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
class Controller_With_Button(ConceptTemplate):
    def __init__(self, bottom_size, button_1_size, button_1_offset, button_2_size, button_2_offset, button_3_size, button_3_offset, button_4_size, button_4_offset, num_buttons, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.bottom_size = bottom_size
        self.button_1_size = button_1_size
        self.button_1_offset = button_1_offset
        self.button_2_size = button_2_size
        self.button_2_offset = button_2_offset
        self.button_3_size = button_3_size
        self.button_3_offset = button_3_offset
        self.button_4_size = button_4_size
        self.button_4_offset = button_4_offset
        self.num_buttons = num_buttons

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_position = [
            0,
            0,
            bottom_size[2] / 2
        ]
        self.mesh = Cuboid(bottom_size[1], bottom_size[0], bottom_size[2],
                           position = mesh_position)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        for i in range(num_buttons[0]):
            mesh_position = [
                locals()['button_%d_offset'%(i+1)][0], 
                locals()['button_%d_offset'%(i+1)][1], 
                bottom_size[2] + locals()['button_%d_size'%(i+1)][2] / 2
            ]
            self.mesh = Cuboid(locals()['button_%d_size'%(i+1)][1], locals()['button_%d_size'%(i+1)][0], locals()['button_%d_size'%(i+1)][2], 
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

        self.semantic = 'Button'


# Source: Oven/concept_template.py
class Controller_With_Button(ConceptTemplate):
    def __init__(self, bottom_size, button_1_size, button_1_offset, button_2_size, button_2_offset, button_3_size, button_3_offset, button_4_size, button_4_offset, button_5_size, button_5_offset, button_6_size, button_6_offset, button_7_size, button_7_offset, button_8_size, button_8_offset, button_9_size, button_9_offset, button_10_size, button_10_offset, num_buttons, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.bottom_size = bottom_size
        self.button_1_size = button_1_size
        self.button_1_offset = button_1_offset
        self.button_2_size = button_2_size
        self.button_2_offset = button_2_offset
        self.button_3_size = button_3_size
        self.button_3_offset = button_3_offset
        self.button_4_size = button_4_size
        self.button_4_offset = button_4_offset
        self.button_5_size = button_5_size
        self.button_5_offset = button_5_offset
        self.button_6_size = button_6_size
        self.button_6_offset = button_6_offset
        self.button_7_size = button_7_size
        self.button_7_offset = button_7_offset
        self.button_8_size = button_8_size
        self.button_8_offset = button_8_offset
        self.button_9_size = button_9_size
        self.button_9_offset = button_9_offset
        self.button_10_size = button_10_size
        self.button_10_offset = button_10_offset
        self.num_buttons = num_buttons

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_position = [
            0,
            0,
            bottom_size[3] / 2
        ]
        self.mesh = Cuboid(bottom_size[1], bottom_size[0], bottom_size[2],
                           bottom_width = bottom_size[3],
                           top_offset = [0, -(bottom_size[3] - bottom_size[2]) / 2],
                           position = mesh_position)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        button_rotation = np.arctan((bottom_size[3] - bottom_size[2]) / bottom_size[1])
        for i in range(num_buttons[0]):
            mesh_position = [
                locals()['button_%d_offset'%(i+1)][0], 
                locals()['button_%d_offset'%(i+1)][1] * np.cos(button_rotation) + locals()['button_%d_size'%(i+1)][2] / 2 * np.sin(button_rotation), 
                (bottom_size[2] + bottom_size[3]) / 2 + locals()['button_%d_size'%(i+1)][2] / 2 * np.cos(button_rotation) - locals()['button_%d_offset'%(i+1)][1] * np.sin(button_rotation)
            ]
            mesh_rotation = [-button_rotation, 0, 0]
            self.mesh = Cuboid(locals()['button_%d_size'%(i+1)][1], locals()['button_%d_size'%(i+1)][0], locals()['button_%d_size'%(i+1)][2], 
                               position = mesh_position,
                               rotation = mesh_rotation)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Button'


# Source: Pen/concept_template.py
class Cylindrical_Button(ConceptTemplate):
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
            size[2] / 2,
            0
        ]
        self.mesh = Cylinder(size[2], size[0], size[1],
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

        self.semantic = 'Button'


# Source: Pen/concept_template.py
class Bistratal_Button(ConceptTemplate):
    def __init__(self, bottom_size, top_size, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.bottom_size = bottom_size
        self.top_size = top_size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_position = [
            0,
            bottom_size[2] / 2,
            0
        ]
        self.mesh = Cylinder(bottom_size[2], bottom_size[0], bottom_size[1],
                             position = mesh_position)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        top_mesh_position = [
            0,
            bottom_size[2] + top_size[2] / 2,
            0
        ]
        self.top_mesh = Cylinder(top_size[2], top_size[0], top_size[1],
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

        self.semantic = 'Button'


# Source: Washingmachine/concept_template.py
class Controller_With_Button(ConceptTemplate):
    def __init__(self, bottom_size, button_1_size, button_1_offset, button_2_size, button_2_offset, button_3_size, button_3_offset, button_4_size, button_4_offset, button_5_size, button_5_offset, button_6_size, button_6_offset, button_7_size, button_7_offset, button_8_size, button_8_offset, num_buttons, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.bottom_size = bottom_size
        self.button_1_size = button_1_size
        self.button_1_offset = button_1_offset
        self.button_2_size = button_2_size
        self.button_2_offset = button_2_offset
        self.button_3_size = button_3_size
        self.button_3_offset = button_3_offset
        self.button_4_size = button_4_size
        self.button_4_offset = button_4_offset
        self.button_5_size = button_5_size
        self.button_5_offset = button_5_offset
        self.button_6_size = button_6_size
        self.button_6_offset = button_6_offset
        self.button_7_size = button_7_size
        self.button_7_offset = button_7_offset
        self.button_8_size = button_8_size
        self.button_8_offset = button_8_offset
        self.num_buttons = num_buttons

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_position = [
            0,
            0,
            bottom_size[3] / 2
        ]
        self.mesh = Cuboid(bottom_size[1], bottom_size[0], bottom_size[2],
                           bottom_width = bottom_size[3],
                           top_offset = [0, -(bottom_size[3] - bottom_size[2]) / 2],
                           position = mesh_position)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        button_rotation = np.arctan((bottom_size[3] - bottom_size[2]) / bottom_size[1])
        for i in range(num_buttons[0]):
            mesh_position = [
                locals()['button_%d_offset'%(i+1)][0], 
                locals()['button_%d_offset'%(i+1)][1] * np.cos(button_rotation) + locals()['button_%d_size'%(i+1)][2] / 2 * np.sin(button_rotation), 
                (bottom_size[2] + bottom_size[3]) / 2 + locals()['button_%d_size'%(i+1)][2] / 2 * np.cos(button_rotation) - locals()['button_%d_offset'%(i+1)][1] * np.sin(button_rotation)
            ]
            mesh_rotation = [-button_rotation, 0, 0]
            self.mesh = Cuboid(locals()['button_%d_size'%(i+1)][1], locals()['button_%d_size'%(i+1)][0], locals()['button_%d_size'%(i+1)][2], 
                               position = mesh_position,
                               rotation = mesh_rotation)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Button'


# Source: Lighter/concept_template.py
class L_Shaped_Button(ConceptTemplate):
    def __init__(self, top_size, bottom_size, top_bottom_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.top_size = top_size
        self.bottom_size = bottom_size
        self.top_bottom_offset = top_bottom_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0, 
            bottom_size[1] / 2,
            0
        ]
        self.bottom_mesh = Cuboid(bottom_size[1], bottom_size[0], bottom_size[2],
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        top_mesh_position = [
            0, 
            bottom_size[1] + top_size[1] / 2,
            top_bottom_offset[0]
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

        self.semantic = 'Button'


# Source: Lighter/concept_template.py
class Double_Cambered_Button(ConceptTemplate):
    def __init__(self, top_size, bottom_size, beside_radius_z, top_bottom_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.top_size = top_size
        self.bottom_size = bottom_size
        self.beside_radius_z = beside_radius_z
        self.top_bottom_offset = top_bottom_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0, 
            bottom_size[1] / 2,
            0
        ]
        self.bottom_mesh = Cuboid(bottom_size[1], bottom_size[0], bottom_size[2],
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        top_mesh_position = [
            0, 
            bottom_size[1] + top_size[1] / 2,
            top_bottom_offset[0]
        ]
        self.top_mesh = Cuboid(top_size[1], top_size[0], top_size[2],
                               position = top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_cambered_mesh_position = [
            0, 
            bottom_size[1] / 2,
            -bottom_size[2] / 2
        ]
        bottom_cambered_mesh_rotation = [0, np.pi, 0]
        self.bottom_cambered_mesh = Cylinder(bottom_size[1], bottom_size[0] / 2,
                                             top_radius_z = beside_radius_z[0],
                                             bottom_radius_z = beside_radius_z[0],
                                             is_half = True,
                                             position = bottom_cambered_mesh_position,
                                             rotation = bottom_cambered_mesh_rotation)
        vertices_list.append(self.bottom_cambered_mesh.vertices)
        faces_list.append(self.bottom_cambered_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_cambered_mesh.vertices)

        top_cambered_mesh_position = [
            0, 
            bottom_size[1] + top_size[1] / 2,
            -top_size[2] / 2 + top_bottom_offset[0]
        ]
        top_cambered_mesh_rotation = [0, np.pi, 0]
        self.top_cambered_mesh = Cylinder(top_size[1], top_size[0] / 2,
                                          top_radius_z = beside_radius_z[1],
                                          bottom_radius_z = beside_radius_z[1],
                                          is_half = True,
                                          position = top_cambered_mesh_position,
                                          rotation = top_cambered_mesh_rotation)
        vertices_list.append(self.top_cambered_mesh.vertices)
        faces_list.append(self.top_cambered_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_cambered_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Button'


# Source: Knife/concept_template.py
class Regular_Button(ConceptTemplate):
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

        self.semantic = 'Button'
