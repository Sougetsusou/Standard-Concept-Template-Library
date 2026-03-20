"""
Bracket Templates
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


# Source: Globe/concept_template.py
class Semi_Ring_Bracket(ConceptTemplate):
    def __init__(self, pivot_size, pivot_continuity, pivot_seperation, has_top_endpoint, has_bottom_endpoint, endpoint_radius, bracket_size, bracket_exist_angle, bracket_offset, bracket_rotation, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        bracket_exist_angle = [x / 180 * np.pi for x in bracket_exist_angle]
        bracket_rotation = [x / 180 * np.pi for x in bracket_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.pivot_size = pivot_size
        self.pivot_continuity = pivot_continuity
        self.pivot_seperation = pivot_seperation
        self.has_top_endpoint = has_top_endpoint
        self.has_bottom_endpoint = has_bottom_endpoint
        self.endpoint_radius = endpoint_radius
        self.bracket_size = bracket_size
        self.bracket_exist_angle = bracket_exist_angle
        self.bracket_offset = bracket_offset
        self.bracket_rotation = bracket_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        if pivot_continuity[0] == 1:
            self.pivot_mesh = Cylinder(pivot_size[1], pivot_size[0])
            vertices_list.append(self.pivot_mesh.vertices)
            faces_list.append(self.pivot_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.pivot_mesh.vertices)

        else:
            top_pivot_mesh_position = [
                0,
                pivot_seperation[0] / 2 + pivot_size[1] / 2,
                0
            ]
            self.top_pivot_mesh = Cylinder(pivot_size[1], pivot_size[0],
                                           position = top_pivot_mesh_position)
            vertices_list.append(self.top_pivot_mesh.vertices)
            faces_list.append(self.top_pivot_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.top_pivot_mesh.vertices)

            bottom_pivot_mesh_position = [
                0,
                -pivot_seperation[0] / 2 - pivot_size[1] / 2,
                0
            ]
            self.bottom_pivot_mesh = Cylinder(pivot_size[1], pivot_size[0],
                                              position = bottom_pivot_mesh_position)
            vertices_list.append(self.bottom_pivot_mesh.vertices)
            faces_list.append(self.bottom_pivot_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.bottom_pivot_mesh.vertices)

        if has_top_endpoint[0] == 1:
            if pivot_continuity[0] == 0:
                top_endpoint_mesh_position = [
                    0,
                    pivot_seperation[0] / 2 + pivot_size[1] + endpoint_radius[0],
                    0
                ]
            else:
                top_endpoint_mesh_position = [
                    0,
                    pivot_size[1] / 2 + endpoint_radius[0],
                    0
                ]
            self.top_endpoint_mesh = Sphere(endpoint_radius[0],
                                            position = top_endpoint_mesh_position)
            vertices_list.append(self.top_endpoint_mesh.vertices)
            faces_list.append(self.top_endpoint_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.top_endpoint_mesh.vertices)

        if has_bottom_endpoint[0] == 1:
            if pivot_continuity[0] == 0:
                bottom_endpoint_mesh_position = [
                    0,
                    -pivot_seperation[0] / 2 - pivot_size[1] - endpoint_radius[0],
                    0
                ]
            else:
                bottom_endpoint_mesh_position = [
                    0,
                    -pivot_size[1] / 2 - endpoint_radius[0],
                    0
                ]
            self.bottom_endpoint_mesh = Sphere(endpoint_radius[0],
                                               position = bottom_endpoint_mesh_position)
            vertices_list.append(self.bottom_endpoint_mesh.vertices)
            faces_list.append(self.bottom_endpoint_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.bottom_endpoint_mesh.vertices)

        bracket_mesh_position = [
            0,
            bracket_offset[0],
            0
        ]
        bracket_mesh_rotation = [
            0,
            -np.pi / 2 + bracket_exist_angle[0] / 2 - bracket_rotation[0],
            np.pi / 2
        ]
        self.bracket_mesh = Ring(bracket_size[2], bracket_size[0], bracket_size[1], bracket_exist_angle[0],
                                 position = bracket_mesh_position,
                                 rotation = bracket_mesh_rotation)
        vertices_list.append(self.bracket_mesh.vertices)
        faces_list.append(self.bracket_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bracket_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Bracket'


# Source: Globe/concept_template.py
class Tilted_Bracket(ConceptTemplate):
    def __init__(self, pivot_size, bracket_size, circle_thickness, circle_rotation, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        circle_rotation = [x / 180 * np.pi for x in circle_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.pivot_size = pivot_size
        self.bracket_size = bracket_size
        self.circle_thickness = circle_thickness
        self.circle_rotation = circle_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        pivot_mesh_rotation = [np.pi / 2, 0, 0]
        self.pivot_mesh = Cylinder(pivot_size[1], pivot_size[0],
                                   rotation = pivot_mesh_rotation)
        vertices_list.append(self.pivot_mesh.vertices)
        faces_list.append(self.pivot_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.pivot_mesh.vertices)

        bracket_mesh_rotation = [
            np.pi / 2,
            np.pi / 2,
            0
        ]
        self.bracket_mesh = Ring(bracket_size[2], bracket_size[0], bracket_size[1], np.pi,
                                 rotation = bracket_mesh_rotation)
        vertices_list.append(self.bracket_mesh.vertices)
        faces_list.append(self.bracket_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bracket_mesh.vertices)

        circle_mesh_rotation = [
            0,
            0,
            circle_rotation[0]
        ]
        self.circle_mesh = Ring(circle_thickness[1], bracket_size[1], bracket_size[1] - circle_thickness[0],
                                rotation = circle_mesh_rotation)
        vertices_list.append(self.circle_mesh.vertices)
        faces_list.append(self.circle_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.circle_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Bracket'


# Source: Globe/concept_template.py
class Enclosed_Bracket(ConceptTemplate):
    def __init__(self, bracket_size, circle_radius, circle_thickness, half_circle_number, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.bracket_size = bracket_size
        self.circle_radius = circle_radius
        self.circle_thickness = circle_thickness
        self.half_circle_number = half_circle_number

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bracket_mesh_rotation = [
            np.pi / 2,
            np.pi / 2,
            0
        ]
        self.bracket_mesh = Ring(bracket_size[2], bracket_size[0], bracket_size[1], np.pi, 
                                 rotation = bracket_mesh_rotation)
        vertices_list.append(self.bracket_mesh.vertices)
        faces_list.append(self.bracket_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bracket_mesh.vertices)

        if half_circle_number[0] == 2:
            bracket_mesh_rotation = [
                np.pi / 2,
                0,
                0
            ]
            self.bracket_mesh = Ring(bracket_size[2], bracket_size[0], bracket_size[1], np.pi, 
                                     rotation = bracket_mesh_rotation)
            vertices_list.append(self.bracket_mesh.vertices)
            faces_list.append(self.bracket_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.bracket_mesh.vertices)

        outer_radius = circle_radius[0] + circle_thickness[0] / 2
        inner_radius = circle_radius[0] - circle_thickness[0] / 2
        self.circle_mesh = Ring(circle_thickness[1], outer_radius, inner_radius)
        vertices_list.append(self.circle_mesh.vertices)
        faces_list.append(self.circle_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.circle_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Bracket'
