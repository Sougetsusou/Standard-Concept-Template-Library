"""
Window Templates
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


# Source: Window/concept_template.py
class Symmetrical_Window(ConceptTemplate):
    def __init__(self, outside_frame_inner_size, outside_frame_inner_outer_offset, number_of_window, size_0, glass_size_0, glass_offset_0, size_1, glass_size_1, glass_offset_1, size_2, glass_size_2, glass_offset_2, offset_x, offset_z, symmetryOrNot, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.outside_frame_inner_size = outside_frame_inner_size
        self.outside_frame_inner_outer_offset = outside_frame_inner_outer_offset
        self.number_of_window = number_of_window
        self.size_0 = size_0
        self.glass_size_0 = glass_size_0
        self.glass_offset_0 = glass_offset_0
        self.size_1 = size_1
        self.glass_size_1 = glass_size_1
        self.glass_offset_1 = glass_offset_1
        self.size_2 = size_2
        self.glass_size_2 = glass_size_2
        self.glass_offset_2 = glass_offset_2
        self.offset_x = offset_x
        self.offset_z = offset_z
        self.symmetryOrNot = symmetryOrNot

        vertices_list = []
        faces_list = []
        self.meshes = []
        total_num_vertices = 0

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # set z position of three layers
        layer_z_position = [
            -size_0[1] / 2 - size_0[1] / 2 + offset_z[0],
            offset_z[0],
            size_0[1] / 2 + size_1[1] / 2 + offset_z[0],
        ]

        # set asymmetry flag (-1 when glass need flipped)
        asymmetryFlag = 1
        if symmetryOrNot:
            asymmetryFlag = -1
        window_configurations = []

        # window configuration information setting
        window_size = [
            {
                "frame_size": size_0,
                "glass_size": glass_size_0,
                "glass_offset": glass_offset_0,
            },
            {
                "frame_size": size_1,
                "glass_size": glass_size_1,
                "glass_offset": glass_offset_1,
            },
            {
                "frame_size": size_2,
                "glass_size": glass_size_2,
                "glass_offset": glass_offset_2,
            },
        ]
        for size in window_size:
            size["frame_size"] = [
                size["frame_size"][0],
                outside_frame_inner_size[1],
                size["frame_size"][1],
            ]
        if number_of_window[0] > 0:
            if number_of_window[0] == 1:
                window_configurations = [
                    {
                        "window_size": window_size[0],
                        "position": [offset_x[0], 0, layer_z_position[1]],
                        "asymmetryFlag": 1,
                    },
                ]
            elif number_of_window[0] == 2:
                window_configurations = [
                    {
                        "window_size": window_size[0],
                        "position": [offset_x[0], 0, layer_z_position[1]],
                        "asymmetryFlag": 1,
                    },
                    {
                        "window_size": window_size[0],
                        "position": [offset_x[1], 0, layer_z_position[1]],
                        "asymmetryFlag": asymmetryFlag,
                    },
                ]
            elif number_of_window[0] == 3:
                window_configurations = [
                    {
                        "window_size": window_size[0],
                        "position": [offset_x[0], 0, layer_z_position[1]],
                        "asymmetryFlag": 1,
                    },
                    {
                        "window_size": window_size[1],
                        "position": [offset_x[1], 0, layer_z_position[2]],
                        "asymmetryFlag": 1,
                    },
                    {
                        "window_size": window_size[0],
                        "position": [offset_x[2], 0, layer_z_position[1]],
                        "asymmetryFlag": asymmetryFlag,
                    },
                ]
            elif number_of_window[0] == 4:
                window_configurations = [
                    {
                        "window_size": window_size[0],
                        "position": [offset_x[0], 0, layer_z_position[1]],
                        "asymmetryFlag": 1,
                    },
                    {
                        "window_size": window_size[1],
                        "position": [offset_x[1], 0, layer_z_position[2]],
                        "asymmetryFlag": 1,
                    },
                    {
                        "window_size": window_size[1],
                        "position": [offset_x[2], 0, layer_z_position[2]],
                        "asymmetryFlag": asymmetryFlag,
                    },
                    {
                        "window_size": window_size[0],
                        "position": [offset_x[3], 0, layer_z_position[1]],
                        "asymmetryFlag": asymmetryFlag,
                    },
                ]
            elif number_of_window[0] == 5:
                window_configurations = [
                    {
                        "window_size": window_size[2],
                        "position": [offset_x[0], 0, layer_z_position[0]],
                        "asymmetryFlag": 1,
                    },
                    {
                        "window_size": window_size[0],
                        "position": [offset_x[1], 0, layer_z_position[1]],
                        "asymmetryFlag": 1,
                    },
                    {
                        "window_size": window_size[1],
                        "position": [offset_x[2], 0, layer_z_position[2]],
                        "asymmetryFlag": 1,
                    },
                    {
                        "window_size": window_size[0],
                        "position": [offset_x[3], 0, layer_z_position[1]],
                        "asymmetryFlag": asymmetryFlag,
                    },
                    {
                        "window_size": window_size[2],
                        "position": [offset_x[4], 0, layer_z_position[0]],
                        "asymmetryFlag": asymmetryFlag,
                    },
                ]
            elif number_of_window[0] == 6:
                window_configurations = [
                    {
                        "window_size": window_size[2],
                        "position": [offset_x[0], 0, layer_z_position[0]],
                        "asymmetryFlag": 1,
                    },
                    {
                        "window_size": window_size[0],
                        "position": [offset_x[1], 0, layer_z_position[1]],
                        "asymmetryFlag": 1,
                    },
                    {
                        "window_size": window_size[1],
                        "position": [offset_x[2], 0, layer_z_position[2]],
                        "asymmetryFlag": 1,
                    },
                    {
                        "window_size": window_size[1],
                        "position": [offset_x[3], 0, layer_z_position[2]],
                        "asymmetryFlag": asymmetryFlag,
                    },
                    {
                        "window_size": window_size[0],
                        "position": [offset_x[4], 0, layer_z_position[1]],
                        "asymmetryFlag": asymmetryFlag,
                    },
                    {
                        "window_size": window_size[2],
                        "position": [offset_x[5], 0, layer_z_position[0]],
                        "asymmetryFlag": asymmetryFlag,
                    },
                ]

        # flip the glass offset x when symmetry , add offset from the outside frame to window position
        for configuration in window_configurations:
            configuration["window_size"]["glass_offset"][0] = (configuration["window_size"]["glass_offset"][0] * configuration["asymmetryFlag"])
            configuration["position"][1] = (configuration["position"][1] + outside_frame_inner_outer_offset[1])

        self.window_configurations = window_configurations
        
        # meshes definition
        for configuration in window_configurations:
            self.frame_mesh = Rectangular_Ring(
                configuration["window_size"]["frame_size"][2],
                configuration["window_size"]["frame_size"][0],
                configuration["window_size"]["frame_size"][1],
                configuration["window_size"]["glass_size"][0],
                configuration["window_size"]["glass_size"][1],
                [
                    configuration["window_size"]["glass_offset"][0],
                    -configuration["window_size"]["glass_offset"][1],
                ],
                position=configuration["position"],
                rotation=[np.pi / 2, 0, 0],
            )
            vertices_list.append(self.frame_mesh.vertices)
            faces_list.append(self.frame_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.frame_mesh.vertices)

            glass_mesh_position = []
            for i in range(3):
                glass_mesh_position.append(configuration["position"][i] + configuration["window_size"]["glass_offset"][i])

            self.glass_mesh = Cuboid(
                configuration["window_size"]["glass_size"][1],
                configuration["window_size"]["glass_size"][0],
                configuration["window_size"]["glass_size"][2],
                position=glass_mesh_position,
            )
            vertices_list.append(self.glass_mesh.vertices)
            faces_list.append(self.glass_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.glass_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Window'


# Source: Window/concept_template.py
class Asymmetrical_Window(ConceptTemplate):
    def __init__(self, outside_frame_inner_size, outside_frame_inner_outer_offset, number_of_window, size_0, glass_size_0, glass_offset_0, size_1, glass_size_1, glass_offset_1, size_2, glass_size_2, glass_offset_2, size_3, glass_size_3, glass_offset_3, offset_x, offset_z, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.outside_frame_inner_size = outside_frame_inner_size
        self.outside_frame_inner_outer_offset = outside_frame_inner_outer_offset
        self.number_of_window = number_of_window
        self.size_0 = size_0
        self.glass_size_0 = glass_size_0
        self.glass_offset_0 = glass_offset_0
        self.size_1 = size_1
        self.glass_size_1 = glass_size_1
        self.glass_offset_1 = glass_offset_1
        self.size_2 = size_2
        self.glass_size_2 = glass_size_2
        self.glass_offset_2 = glass_offset_2
        self.size_3 = size_3
        self.glass_size_3 = glass_size_3
        self.glass_offset_3 = glass_offset_3
        self.offset_x = offset_x
        self.offset_z = offset_z

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # set z position of three layers
        layer_z_position = [
            offset_z[0],
            size_0[1] / 2 + size_1[1] / 2 + offset_z[0],
            size_0[1] / 2 + size_1[1] + size_2[1] / 2 + offset_z[0],
            size_0[1] / 2 + size_1[1] + size_2[1] + size_3[1] / 2 + offset_z[0],
        ]
        # window configuration information setting
        window_size = [
            {
                "frame_size": size_0,
                "glass_size": glass_size_0,
                "glass_offset": glass_offset_0,
            },
            {
                "frame_size": size_1,
                "glass_size": glass_size_1,
                "glass_offset": glass_offset_1,
            },
            {
                "frame_size": size_2,
                "glass_size": glass_size_2,
                "glass_offset": glass_offset_2,
            },
            {
                "frame_size": size_3,
                "glass_size": glass_size_3,
                "glass_offset": glass_offset_3,
            },
        ]
        for size in window_size:
            size["frame_size"] = [
                size["frame_size"][0],
                outside_frame_inner_size[1],
                size["frame_size"][1],
            ]
        # set window configurations
        window_configurations = []
        for i in range(number_of_window[0]):
            window_configurations.append(
                {
                    "window_size": window_size[i],
                    "position": [
                        offset_x[i],
                        outside_frame_inner_outer_offset[1],
                        layer_z_position[i],
                    ],
                }
            )
        self.window_configurations = window_configurations

        # meshes definition
        for configuration in window_configurations:
            self.frame_mesh = Rectangular_Ring(
                configuration["window_size"]["frame_size"][2],
                configuration["window_size"]["frame_size"][0],
                configuration["window_size"]["frame_size"][1],
                configuration["window_size"]["glass_size"][0],
                configuration["window_size"]["glass_size"][1],
                [
                    configuration["window_size"]["glass_offset"][0],
                    -configuration["window_size"]["glass_offset"][1],
                ],
                position=configuration["position"],
                rotation=[np.pi / 2, 0, 0],
            )
            vertices_list.append(self.frame_mesh.vertices)
            faces_list.append(self.frame_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.frame_mesh.vertices)

            glass_mesh_position = []
            for i in range(3):
                glass_mesh_position.append(configuration["position"][i] + configuration["window_size"]["glass_offset"][i])

            self.glass_mesh = Cuboid(
                configuration["window_size"]["glass_size"][1],
                configuration["window_size"]["glass_size"][0],
                configuration["window_size"]["glass_size"][2],
                position=glass_mesh_position,
            )
            vertices_list.append(self.glass_mesh.vertices)
            faces_list.append(self.glass_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.glass_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Window'


# Source: Window/concept_template.py
class VerticalSlid_Window(ConceptTemplate):
    def __init__(self, outside_frame_inner_size, outside_frame_inner_outer_offset, number_of_window, size_0, glass_size_0, glass_offset_0, size_1, glass_size_1, glass_offset_1, offset_y, offset_z, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.outside_frame_inner_size = outside_frame_inner_size
        self.outside_frame_inner_outer_offset = outside_frame_inner_outer_offset
        self.number_of_window = number_of_window
        self.size_0 = size_0
        self.glass_size_0 = glass_size_0
        self.glass_offset_0 = glass_offset_0
        self.size_1 = size_1
        self.glass_size_1 = glass_size_1
        self.glass_offset_1 = glass_offset_1
        self.offset_y = offset_y
        self.offset_z = offset_z

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # set z position of three layers
        layer_z_position = [
            offset_z[0],
            size_0[1] / 2 + size_1[1] / 2 + offset_z[0],
        ]

        # window configuration information setting
        window_size = [
            {
                "frame_size": size_0,
                "glass_size": glass_size_0,
                "glass_offset": glass_offset_0,
            },
            {
                "frame_size": size_1,
                "glass_size": glass_size_1,
                "glass_offset": glass_offset_1,
            },
        ]
        for size in window_size:
            size["frame_size"] = [
                outside_frame_inner_size[0],
                size["frame_size"][0],
                size["frame_size"][1],
            ]

        # set window configurations
        window_configurations = []
        for i in range(number_of_window[0]):
            window_configurations.append(
                {
                    "window_size": window_size[i],
                    "position": [
                        outside_frame_inner_outer_offset[0],
                        offset_y[i],
                        layer_z_position[i],
                    ],
                }
            )
        self.window_configurations = window_configurations

        # meshes definition
        for configuration in window_configurations:
            self.frame_mesh = Rectangular_Ring(
                configuration["window_size"]["frame_size"][2],
                configuration["window_size"]["frame_size"][0],
                configuration["window_size"]["frame_size"][1],
                configuration["window_size"]["glass_size"][0],
                configuration["window_size"]["glass_size"][1],
                [
                    configuration["window_size"]["glass_offset"][0],
                    -configuration["window_size"]["glass_offset"][1],
                ],
                position=configuration["position"],
                rotation=[np.pi / 2, 0, 0],
            )
            vertices_list.append(self.frame_mesh.vertices)
            faces_list.append(self.frame_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.frame_mesh.vertices)

            glass_mesh_position = []
            for i in range(3):
                glass_mesh_position.append(configuration["position"][i] + configuration["window_size"]["glass_offset"][i])

            self.glass_mesh = Cuboid(
                configuration["window_size"]["glass_size"][1],
                configuration["window_size"]["glass_size"][0],
                configuration["window_size"]["glass_size"][2],
                position=glass_mesh_position,
            )
            vertices_list.append(self.glass_mesh.vertices)
            faces_list.append(self.glass_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.glass_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Window'
