"""
Handle Templates
Automatically extracted from concept_template.py files
Contains 65 class(es)
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
class Cuboidal_Handle(ConceptTemplate):
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
            0,
            size[2] / 2
        ]
        self.mesh = Cuboid(size[1], size[0], size[2],
                             position = mesh_position)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="ZXY")

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Microwave/concept_template.py
class Trifold_Handle(ConceptTemplate):
    def __init__(self, mounting_size, mounting_seperation, grip_size, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.mounting_size = mounting_size
        self.mounting_seperation = mounting_seperation
        self.grip_size = grip_size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        top_mesh_position = [
            0, 
            mounting_seperation[0] / 2, 
            mounting_size[2] / 2
        ]
        self.top_mesh = Cuboid(mounting_size[1], mounting_size[0], mounting_size[2], 
                               position = top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [
            0, 
            -mounting_seperation[0] / 2, 
            mounting_size[2] / 2
        ]
        self.bottom_mesh = Cuboid(mounting_size[1], mounting_size[0], mounting_size[2], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        vertical_mesh_position = [
            0, 
            0,
            mounting_size[2] + grip_size[2] / 2
        ]
        self.vertical_mesh = Cuboid(grip_size[1], grip_size[0], grip_size[2], 
                                    position = vertical_mesh_position)
        vertices_list.append(self.vertical_mesh.vertices)
        faces_list.append(self.vertical_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.vertical_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="ZXY")

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Microwave/concept_template.py
class Trifold_Curve_Handle(ConceptTemplate):
    def __init__(self, mounting_size, mounting_seperation, curve_size, curve_exist_angle, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        curve_exist_angle = [x / 180 * np.pi for x in curve_exist_angle]
        super().__init__(position, rotation)

        # Record Parameters
        self.mounting_size = mounting_size
        self.mounting_seperation = mounting_seperation
        self.curve_size = curve_size
        self.curve_exist_angle = curve_exist_angle

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        top_mesh_position = [
            0, 
            mounting_seperation[0] / 2, 
            mounting_size[2] / 2
        ]
        self.top_mesh = Cuboid(mounting_size[1], mounting_size[0], mounting_size[2], 
                               position = top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [
            0, 
            -mounting_seperation[0] / 2, 
            mounting_size[2] / 2
        ]
        self.bottom_mesh = Cuboid(mounting_size[1], mounting_size[0], mounting_size[2], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        curve_z_offset = mounting_size[2] - np.sqrt(curve_size[1] * curve_size[1] - (mounting_seperation[0] / 2) * (mounting_seperation[0] / 2))
        vertical_mesh_position = [
            0, 
            0,
            curve_z_offset
        ]
        vertical_mesh_rotation = [
            0, 
            -np.pi / 2 + curve_exist_angle[0] / 2,
            np.pi / 2
        ]
        self.vertical_mesh = Ring(curve_size[2], curve_size[0], curve_size[1], curve_exist_angle[0],
                                  position = vertical_mesh_position,
                                  rotation = vertical_mesh_rotation)
        vertices_list.append(self.vertical_mesh.vertices)
        faces_list.append(self.vertical_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.vertical_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="ZXY")

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Microwave/concept_template.py
class Curve_Handle(ConceptTemplate):
    def __init__(self, curve_size, curve_exist_angle, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        curve_exist_angle = [x / 180 * np.pi for x in curve_exist_angle]
        super().__init__(position, rotation)

        # Record Parameters
        self.curve_size = curve_size
        self.curve_exist_angle = curve_exist_angle

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        vertical_mesh_position = [
            0, 
            0,
            -curve_size[0] * np.cos(curve_exist_angle[0] / 2)
        ]
        vertical_mesh_rotation = [
            0, 
            -np.pi / 2 + curve_exist_angle[0] / 2,
            np.pi / 2
        ]
        self.vertical_mesh = Ring(curve_size[2], curve_size[0], curve_size[1], curve_exist_angle[0],
                                  position = vertical_mesh_position,
                                  rotation = vertical_mesh_rotation)
        vertices_list.append(self.vertical_mesh.vertices)
        faces_list.append(self.vertical_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.vertical_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="ZXY")

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Safe/concept_template.py
class Trifold_Handle(ConceptTemplate):
    def __init__(self, bottom_size, bottom_seperation, top_size, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.bottom_size = bottom_size
        self.bottom_seperation = bottom_seperation
        self.top_size = top_size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        top_mesh_position = [
            0, 
            bottom_seperation[0] / 2, 
            bottom_size[2] / 2
        ]
        self.top_mesh = Cuboid(bottom_size[1], bottom_size[0], bottom_size[2], 
                               position = top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [
            0, 
            -bottom_seperation[0] / 2, 
            bottom_size[2] / 2
        ]
        self.bottom_mesh = Cuboid(bottom_size[1], bottom_size[0], bottom_size[2], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        vertical_mesh_position = [
            0, 
            0,
            bottom_size[2] + top_size[2] / 2
        ]
        self.vertical_mesh = Cuboid(top_size[1], top_size[0], top_size[2], 
                                    position = vertical_mesh_position)
        vertices_list.append(self.vertical_mesh.vertices)
        faces_list.append(self.vertical_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.vertical_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="ZXY")

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Safe/concept_template.py
class Claw_Handle(ConceptTemplate):
    def __init__(self, bottom_size, fork_size, fork_offset, fork_tilt_rotation, num_forks, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        fork_tilt_rotation = [x / 180 * np.pi for x in fork_tilt_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.bottom_size = bottom_size
        self.fork_size = fork_size
        self.fork_offset = fork_offset
        self.fork_tilt_rotation = fork_tilt_rotation
        self.num_forks = num_forks

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0, 
            0, 
            bottom_size[1] / 2
        ]
        bottom_mesh_rotation = [np.pi / 2, 0, 0]
        self.bottom_mesh = Cylinder(bottom_size[1], bottom_size[0],
                                    position = bottom_mesh_position,
                                    rotation = bottom_mesh_rotation)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        for i in range(num_forks[0]):
            rotation_tmp = np.pi * 2 / num_forks[0] * i
            rotate_length = bottom_size[0] + fork_size[0] / 2 * np.cos(fork_tilt_rotation[0])
            
            mesh_position = [
                rotate_length * np.cos(rotation_tmp), 
                rotate_length * np.sin(rotation_tmp), 
                -fork_size[2] / 2 + bottom_size[1] + fork_size[0] / 2 * np.sin(fork_tilt_rotation[0]) - fork_offset[0]
            ]
            mesh_rotation = [
                0, 
                -fork_tilt_rotation[0], 
                rotation_tmp
            ]
            self.mesh = Cuboid(fork_size[1], fork_size[0], fork_size[2],
                               position = mesh_position,
                               rotation = mesh_rotation)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="ZXY")

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Safe/concept_template.py
class Round_Handle(ConceptTemplate):
    def __init__(self, bottom_size, fork_size, fork_offset, fork_tilt_rotation, circle_size, num_forks, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        fork_tilt_rotation = [x / 180 * np.pi for x in fork_tilt_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.bottom_size = bottom_size
        self.fork_size = fork_size
        self.fork_offset = fork_offset
        self.fork_tilt_rotation = fork_tilt_rotation
        self.circle_size = circle_size
        self.num_forks = num_forks

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0, 
            0, 
            bottom_size[1] / 2
        ]
        bottom_mesh_rotation = [np.pi / 2, 0, 0]
        self.bottom_mesh = Cylinder(bottom_size[1], bottom_size[0],
                                    position = bottom_mesh_position,
                                    rotation = bottom_mesh_rotation)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        for i in range(num_forks[0]):
            rotation_tmp = np.pi * 2 / num_forks[0] * i
            rotate_length = bottom_size[0] + fork_size[0] / 2 * np.cos(fork_tilt_rotation[0])
            
            mesh_position = [
                rotate_length * np.cos(rotation_tmp), 
                rotate_length * np.sin(rotation_tmp), 
                -fork_size[2] / 2 + bottom_size[1] + fork_size[0] / 2 * np.sin(fork_tilt_rotation[0]) - fork_offset[0]
            ]
            mesh_rotation = [
                0, 
                -fork_tilt_rotation[0], 
                rotation_tmp
            ]
            self.mesh = Cuboid(fork_size[1], fork_size[0], fork_size[2],
                               position = mesh_position,
                               rotation = mesh_rotation)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        outer_radius = circle_size[0]
        inner_radius = bottom_size[0] + fork_size[0] * np.cos(fork_tilt_rotation[0])
        circle_mesh_position = [
            0, 
            0, 
            bottom_size[1] - fork_size[2] / 2 + fork_size[0] * np.sin(fork_tilt_rotation[0]) - fork_offset[0]
        ]
        circle_mesh_rotation = [np.pi / 2, 0, 0]
        self.circle_mesh = Ring(circle_size[1], outer_radius, inner_radius, 
                                position = circle_mesh_position,
                                rotation = circle_mesh_rotation)
        vertices_list.append(self.circle_mesh.vertices)
        faces_list.append(self.circle_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.circle_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="ZXY")

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Oven/concept_template.py
class Cuboidal_Handle(ConceptTemplate):
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
            0,
            size[2] / 2
        ]
        self.mesh = Cuboid(size[1], size[0], size[2],
                             position = mesh_position)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="ZXY")

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Oven/concept_template.py
class Trifold_Handle(ConceptTemplate):
    def __init__(self, mounting_size, mounting_seperation, grip_size, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.mounting_size = mounting_size
        self.mounting_seperation = mounting_seperation
        self.grip_size = grip_size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        top_mesh_position = [
            0, 
            mounting_seperation[0] / 2, 
            mounting_size[2] / 2
        ]
        self.top_mesh = Cuboid(mounting_size[1], mounting_size[0], mounting_size[2], 
                               position = top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [
            0, 
            -mounting_seperation[0] / 2, 
            mounting_size[2] / 2
        ]
        self.bottom_mesh = Cuboid(mounting_size[1], mounting_size[0], mounting_size[2], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        vertical_mesh_position = [
            0, 
            0,
            mounting_size[2] + grip_size[2] / 2
        ]
        self.vertical_mesh = Cuboid(grip_size[1], grip_size[0], grip_size[2], 
                                    position = vertical_mesh_position)
        vertices_list.append(self.vertical_mesh.vertices)
        faces_list.append(self.vertical_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.vertical_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="ZXY")

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Oven/concept_template.py
class Trifold_Curve_Handle(ConceptTemplate):
    def __init__(self, mounting_size, mounting_seperation, curve_size, curve_exist_angle, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        curve_exist_angle = [x / 180 * np.pi for x in curve_exist_angle]
        super().__init__(position, rotation)

        # Record Parameters
        self.mounting_size = mounting_size
        self.mounting_seperation = mounting_seperation
        self.curve_size = curve_size
        self.curve_exist_angle = curve_exist_angle

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        top_mesh_position = [
            0, 
            mounting_seperation[0] / 2, 
            mounting_size[2] / 2
        ]
        self.top_mesh = Cuboid(mounting_size[1], mounting_size[0], mounting_size[2], 
                               position = top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [
            0, 
            -mounting_seperation[0] / 2, 
            mounting_size[2] / 2
        ]
        self.bottom_mesh = Cuboid(mounting_size[1], mounting_size[0], mounting_size[2], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        curve_z_offset = mounting_size[2] - np.sqrt(curve_size[1] * curve_size[1] - (mounting_seperation[0] / 2) * (mounting_seperation[0] / 2))
        vertical_mesh_position = [
            0, 
            0,
            curve_z_offset
        ]
        vertical_mesh_rotation = [
            0, 
            -np.pi / 2 + curve_exist_angle[0] / 2,
            np.pi / 2
        ]
        self.vertical_mesh = Ring(curve_size[2], curve_size[0], curve_size[1], curve_exist_angle[0],
                                  position = vertical_mesh_position,
                                  rotation = vertical_mesh_rotation)
        vertices_list.append(self.vertical_mesh.vertices)
        faces_list.append(self.vertical_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.vertical_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="ZXY")

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Oven/concept_template.py
class Curve_Handle(ConceptTemplate):
    def __init__(self, curve_size, curve_exist_angle, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        curve_exist_angle = [x / 180 * np.pi for x in curve_exist_angle]
        super().__init__(position, rotation)

        # Record Parameters
        self.curve_size = curve_size
        self.curve_exist_angle = curve_exist_angle

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        vertical_mesh_position = [
            0, 
            0,
            -curve_size[0] * np.cos(curve_exist_angle[0] / 2)
        ]
        vertical_mesh_rotation = [
            0, 
            -np.pi / 2 + curve_exist_angle[0] / 2,
            np.pi / 2
        ]
        self.vertical_mesh = Ring(curve_size[2], curve_size[0], curve_size[1], curve_exist_angle[0],
                                  position = vertical_mesh_position,
                                  rotation = vertical_mesh_rotation)
        vertices_list.append(self.vertical_mesh.vertices)
        faces_list.append(self.vertical_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.vertical_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="ZXY")

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Dishwasher/concept_template.py
class Cuboidal_Handle(ConceptTemplate):
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
            0,
            size[2] / 2
        ]
        self.mesh = Cuboid(size[1], size[0], size[2],
                             position = mesh_position)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="ZXY")

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Dishwasher/concept_template.py
class Trifold_Handle(ConceptTemplate):
    def __init__(self, mounting_size, mounting_seperation, grip_size, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.mounting_size = mounting_size
        self.mounting_seperation = mounting_seperation
        self.grip_size = grip_size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        top_mesh_position = [
            0, 
            mounting_seperation[0] / 2, 
            mounting_size[2] / 2
        ]
        self.top_mesh = Cuboid(mounting_size[1], mounting_size[0], mounting_size[2], 
                               position = top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [
            0, 
            -mounting_seperation[0] / 2, 
            mounting_size[2] / 2
        ]
        self.bottom_mesh = Cuboid(mounting_size[1], mounting_size[0], mounting_size[2], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        vertical_mesh_position = [
            0, 
            0,
            mounting_size[2] + grip_size[2] / 2
        ]
        self.vertical_mesh = Cuboid(grip_size[1], grip_size[0], grip_size[2], 
                                    position = vertical_mesh_position)
        vertices_list.append(self.vertical_mesh.vertices)
        faces_list.append(self.vertical_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.vertical_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="ZXY")

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Dishwasher/concept_template.py
class Trifold_Curve_Handle(ConceptTemplate):
    def __init__(self, mounting_size, mounting_seperation, curve_size, curve_exist_angle, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        curve_exist_angle = [x / 180 * np.pi for x in curve_exist_angle]
        super().__init__(position, rotation)

        # Record Parameters
        self.mounting_size = mounting_size
        self.mounting_seperation = mounting_seperation
        self.curve_size = curve_size
        self.curve_exist_angle = curve_exist_angle

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        top_mesh_position = [
            0, 
            mounting_seperation[0] / 2, 
            mounting_size[2] / 2
        ]
        self.top_mesh = Cuboid(mounting_size[1], mounting_size[0], mounting_size[2], 
                               position = top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [
            0, 
            -mounting_seperation[0] / 2, 
            mounting_size[2] / 2
        ]
        self.bottom_mesh = Cuboid(mounting_size[1], mounting_size[0], mounting_size[2], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        curve_z_offset = mounting_size[2] - np.sqrt(curve_size[1] * curve_size[1] - (mounting_seperation[0] / 2) * (mounting_seperation[0] / 2))
        vertical_mesh_position = [
            0, 
            0,
            curve_z_offset
        ]
        vertical_mesh_rotation = [
            0, 
            -np.pi / 2 + curve_exist_angle[0] / 2,
            np.pi / 2
        ]
        self.vertical_mesh = Ring(curve_size[2], curve_size[0], curve_size[1], curve_exist_angle[0],
                                  position = vertical_mesh_position,
                                  rotation = vertical_mesh_rotation)
        vertices_list.append(self.vertical_mesh.vertices)
        faces_list.append(self.vertical_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.vertical_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="ZXY")

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Dishwasher/concept_template.py
class Curve_Handle(ConceptTemplate):
    def __init__(self, curve_size, curve_exist_angle, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        curve_exist_angle = [x / 180 * np.pi for x in curve_exist_angle]
        super().__init__(position, rotation)

        # Record Parameters
        self.curve_size = curve_size
        self.curve_exist_angle = curve_exist_angle

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        vertical_mesh_position = [
            0, 
            0,
            -curve_size[0] * np.cos(curve_exist_angle[0] / 2)
        ]
        vertical_mesh_rotation = [
            0, 
            -np.pi / 2 + curve_exist_angle[0] / 2,
            np.pi / 2
        ]
        self.vertical_mesh = Ring(curve_size[2], curve_size[0], curve_size[1], curve_exist_angle[0],
                                  position = vertical_mesh_position,
                                  rotation = vertical_mesh_rotation)
        vertices_list.append(self.vertical_mesh.vertices)
        faces_list.append(self.vertical_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.vertical_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="ZXY")

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: KitchenPot/concept_template.py
class Cuboidal_Tophandle(ConceptTemplate):
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

        self.semantic = 'Handle'


# Source: KitchenPot/concept_template.py
class Trifold_Tophandle(ConceptTemplate):
    def __init__(self, mounting_size, mounting_seperation, grip_size, mounting_rotation, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        mounting_rotation = [x / 180 * np.pi for x in mounting_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.mounting_size = mounting_size
        self.mounting_seperation = mounting_seperation
        self.grip_size = grip_size
        self.mounting_rotation = mounting_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        left_mesh_position = [
            mounting_seperation[0] / 2 + mounting_size[1] * np.sin(mounting_rotation[0]) / 2, 
            mounting_size[1] * np.cos(mounting_rotation[0]) / 2, 
            0
        ]
        left_mesh_rotation = [0, 0, -mounting_rotation[0]]
        self.left_mesh = Cuboid(mounting_size[1], mounting_size[0], mounting_size[2], 
                                position = left_mesh_position,
                                rotation = left_mesh_rotation)
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        right_mesh_position = [
            -mounting_seperation[0] / 2 - mounting_size[1] * np.sin(mounting_rotation[0]) / 2, 
            mounting_size[1] * np.cos(mounting_rotation[0]) / 2, 
            0
        ]
        right_mesh_rotation = [0, 0, mounting_rotation[0]]
        self.right_mesh = Cuboid(mounting_size[1], mounting_size[0], mounting_size[2], 
                                 position = right_mesh_position,
                                 rotation = right_mesh_rotation)
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        top_mesh_position = [
            0, 
            mounting_size[1] * np.cos(mounting_rotation[0]) + grip_size[1] / 2, 
            0
        ]
        self.top_mesh = Cuboid(grip_size[1], grip_size[0], grip_size[2], 
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

        self.semantic = 'Handle'


# Source: KitchenPot/concept_template.py
class Semi_Ring_Tophandle(ConceptTemplate):
    def __init__(self, curve_size, curve_exist_angle, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        curve_exist_angle = [x / 180 * np.pi for x in curve_exist_angle]
        super().__init__(position, rotation)

        # Record Parameters
        self.curve_size = curve_size
        self.curve_exist_angle = curve_exist_angle

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_position = [
            0,
            -curve_size[0] * np.cos(curve_exist_angle[0] / 2),
            0
        ]
        mesh_rotation = [
            -np.pi / 2,
            -np.pi / 2 + curve_exist_angle[0] / 2,
            0
        ]
        self.mesh = Ring(curve_size[2], curve_size[0], curve_size[1], curve_exist_angle[0],
                         position = mesh_position,
                         rotation = mesh_rotation,
                         rotation_order = "YXZ")
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: KitchenPot/concept_template.py
class Multilevel_Tophandle(ConceptTemplate):
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

        delta_height = 0
        for i in range(num_levels[0]):
            delta_height += locals()['level_'+ str(i+1) +'_size'][2] / 2
            mesh_position = [0, delta_height, 0]
            delta_height += locals()['level_'+ str(i+1) +'_size'][2] / 2
            self.mesh = Cylinder(locals()['level_'+ str(i+1) +'_size'][2], locals()['level_'+ str(i+1) +'_size'][0], locals()['level_'+ str(i+1) +'_size'][1], 
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

        self.semantic = 'Handle'


# Source: KitchenPot/concept_template.py
class Trifold_Sidehandle(ConceptTemplate):
    def __init__(self, mounting_size, mounting_seperation, grip_size, mounting_rotation, handle_seperation, whole_rotation, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        mounting_rotation = [x / 180 * np.pi for x in mounting_rotation]
        whole_rotation = [x / 180 * np.pi for x in whole_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.mounting_size = mounting_size
        self.mounting_seperation = mounting_seperation
        self.grip_size = grip_size
        self.mounting_rotation = mounting_rotation
        self.handle_seperation = handle_seperation
        self.whole_rotation = whole_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # level_1
        level_1_position = [handle_seperation[0] / 2, 0, 0]
        level_1_rotation = [0, 0, whole_rotation[0]]

        left_1_mesh_position = [
            mounting_size[0] * np.cos(mounting_rotation[0]) / 2, 
            0,
            mounting_seperation[0] / 2 + mounting_size[0] * np.sin(mounting_rotation[0]) / 2
        ]
        left_1_mesh_rotation = [0, -mounting_rotation[0], 0]

        left_1_mesh_position = adjust_position_from_rotation(left_1_mesh_position, level_1_rotation)
        left_1_mesh_position = list_add(left_1_mesh_position, level_1_position)
        left_1_mesh_rotation = list_add(left_1_mesh_rotation, level_1_rotation)

        self.left_1_mesh = Cuboid(mounting_size[1], mounting_size[0], mounting_size[2], 
                                  position = left_1_mesh_position,
                                  rotation = left_1_mesh_rotation)
        vertices_list.append(self.left_1_mesh.vertices)
        faces_list.append(self.left_1_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_1_mesh.vertices)

        right_1_mesh_position = [
            mounting_size[0] * np.cos(mounting_rotation[0]) / 2, 
            0, 
            -mounting_seperation[0] / 2 - mounting_size[0] * np.sin(mounting_rotation[0]) / 2, 
        ]
        right_1_mesh_rotation = [0, mounting_rotation[0], 0]

        right_1_mesh_position = adjust_position_from_rotation(right_1_mesh_position, level_1_rotation)
        right_1_mesh_position = list_add(right_1_mesh_position, level_1_position)
        right_1_mesh_rotation = list_add(right_1_mesh_rotation, level_1_rotation)

        self.right_1_mesh = Cuboid(mounting_size[1], mounting_size[0], mounting_size[2], 
                                 position = right_1_mesh_position,
                                 rotation = right_1_mesh_rotation)
        vertices_list.append(self.right_1_mesh.vertices)
        faces_list.append(self.right_1_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_1_mesh.vertices)

        top_1_mesh_position = [
            mounting_size[0] * np.cos(mounting_rotation[0]) + grip_size[0] / 2, 
            0, 
            0
        ]
        top_1_mesh_rotation = [0, 0, 0]

        top_1_mesh_position = adjust_position_from_rotation(top_1_mesh_position, level_1_rotation)
        top_1_mesh_position = list_add(top_1_mesh_position, level_1_position)
        top_1_mesh_rotation = list_add(top_1_mesh_rotation, level_1_rotation)

        self.top_1_mesh = Cuboid(grip_size[1], grip_size[0], grip_size[2], 
                                 position = top_1_mesh_position,
                                 rotation = top_1_mesh_rotation)
        vertices_list.append(self.top_1_mesh.vertices)
        faces_list.append(self.top_1_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_1_mesh.vertices)

        # level_2
        level_2_position = [-handle_seperation[0] / 2, 0, 0]
        level_2_rotation = [0, 0, -whole_rotation[0]]

        left_2_mesh_position = [
            -mounting_size[0] * np.cos(mounting_rotation[0]) / 2, 
            0,
            mounting_seperation[0] / 2 + mounting_size[0] * np.sin(mounting_rotation[0]) / 2
        ]
        left_2_mesh_rotation = [0, mounting_rotation[0], 0]

        left_2_mesh_position = adjust_position_from_rotation(left_2_mesh_position, level_2_rotation)
        left_2_mesh_position = list_add(left_2_mesh_position, level_2_position)
        left_2_mesh_rotation = list_add(left_2_mesh_rotation, level_2_rotation)

        self.left_2_mesh = Cuboid(mounting_size[1], mounting_size[0], mounting_size[2], 
                                  position = left_2_mesh_position,
                                  rotation = left_2_mesh_rotation)
        vertices_list.append(self.left_2_mesh.vertices)
        faces_list.append(self.left_2_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_2_mesh.vertices)

        right_2_mesh_position = [
            -mounting_size[0] * np.cos(mounting_rotation[0]) / 2, 
            0, 
            -mounting_seperation[0] / 2 - mounting_size[0] * np.sin(mounting_rotation[0]) / 2, 
        ]
        right_2_mesh_rotation = [0, -mounting_rotation[0], 0]

        right_2_mesh_position = adjust_position_from_rotation(right_2_mesh_position, level_2_rotation)
        right_2_mesh_position = list_add(right_2_mesh_position, level_2_position)
        right_2_mesh_rotation = list_add(right_2_mesh_rotation, level_2_rotation)

        self.right_2_mesh = Cuboid(mounting_size[1], mounting_size[0], mounting_size[2], 
                                 position = right_2_mesh_position,
                                 rotation = right_2_mesh_rotation)
        vertices_list.append(self.right_2_mesh.vertices)
        faces_list.append(self.right_2_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_2_mesh.vertices)

        top_2_mesh_position = [
            -mounting_size[0] * np.cos(mounting_rotation[0]) - grip_size[0] / 2, 
            0, 
            0
        ]
        top_2_mesh_rotation = [0, 0, 0]

        top_2_mesh_position = adjust_position_from_rotation(top_2_mesh_position, level_2_rotation)
        top_2_mesh_position = list_add(top_2_mesh_position, level_2_position)
        top_2_mesh_rotation = list_add(top_2_mesh_rotation, level_2_rotation)

        self.top_2_mesh = Cuboid(grip_size[1], grip_size[0], grip_size[2], 
                                 position = top_2_mesh_position,
                                 rotation = top_2_mesh_rotation)
        vertices_list.append(self.top_2_mesh.vertices)
        faces_list.append(self.top_2_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_2_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: KitchenPot/concept_template.py
class L_Shaped_Sidehandle(ConceptTemplate):
    def __init__(self, bottom_size, top_size, handle_seperation, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.bottom_size = bottom_size
        self.top_size = top_size
        self.handle_seperation = handle_seperation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # level_1
        bottom_1_mesh_position = [
            handle_seperation[0] / 2 + bottom_size[0] / 2, 
            0,
            0
        ]
        self.bottom_1_mesh = Cuboid(bottom_size[1], bottom_size[0], bottom_size[2], 
                                    position = bottom_1_mesh_position)
        vertices_list.append(self.bottom_1_mesh.vertices)
        faces_list.append(self.bottom_1_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_1_mesh.vertices)

        top_1_mesh_position = [
            handle_seperation[0] / 2 + top_size[0] / 2, 
            (bottom_size[1] + top_size[1]) / 2,
            0
        ]

        self.top_1_mesh = Cuboid(top_size[1], top_size[0], top_size[2], 
                                 position = top_1_mesh_position)
        vertices_list.append(self.top_1_mesh.vertices)
        faces_list.append(self.top_1_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_1_mesh.vertices)

        # level_2
        bottom_2_mesh_position = [
            -handle_seperation[0] / 2 - bottom_size[0] / 2, 
            0,
            0
        ]
        self.bottom_2_mesh = Cuboid(bottom_size[1], bottom_size[0], bottom_size[2], 
                                    position = bottom_2_mesh_position)
        vertices_list.append(self.bottom_2_mesh.vertices)
        faces_list.append(self.bottom_2_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_2_mesh.vertices)

        top_2_mesh_position = [
            -handle_seperation[0] / 2 - top_size[0] / 2, 
            (bottom_size[1] + top_size[1]) / 2,
            0
        ]

        self.top_2_mesh = Cuboid(top_size[1], top_size[0], top_size[2], 
                                 position = top_2_mesh_position)
        vertices_list.append(self.top_2_mesh.vertices)
        faces_list.append(self.top_2_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_2_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: KitchenPot/concept_template.py
class Cuboidal_Sidehandle(ConceptTemplate):
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
            0,
            -size[2] / 2
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

        self.semantic = 'Handle'


# Source: Doorhandle/concept_template.py
class Regular_handle(ConceptTemplate):
    def __init__(self, fixed_part_size, vertical_movable_size, horizontal_movable_size, interpiece_offset_1, interpiece_offset_2, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.fixed_part_size = fixed_part_size
        self.vertical_movable_size = vertical_movable_size
        self.horizontal_movable_size = horizontal_movable_size
        self.interpiece_offset_1 = interpiece_offset_1
        self.interpiece_offset_2 = interpiece_offset_2

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        base_mesh_position = [0, 0, fixed_part_size[2] / 2]
        self.base_mesh = Cuboid(fixed_part_size[1], fixed_part_size[0], fixed_part_size[2],
                                position=base_mesh_position)
        vertices_list.append(self.base_mesh.vertices)
        faces_list.append(self.base_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.base_mesh.vertices)

        middle_mesh_position = [
            interpiece_offset_1[0],
            interpiece_offset_1[1],
            fixed_part_size[2] + vertical_movable_size[2] / 2,
        ]
        self.middle_mesh = Cuboid(vertical_movable_size[1], vertical_movable_size[0], vertical_movable_size[2],
                                  position=middle_mesh_position)
        vertices_list.append(self.middle_mesh.vertices)
        faces_list.append(self.middle_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.middle_mesh.vertices)

        main_mesh_position = [
            interpiece_offset_1[0] + interpiece_offset_2[0],
            interpiece_offset_1[1] + interpiece_offset_2[1],
            fixed_part_size[2] + vertical_movable_size[2] + horizontal_movable_size[2] / 2,
        ]
        self.main_mesh = Cuboid(horizontal_movable_size[1], horizontal_movable_size[0], horizontal_movable_size[2],
                                position=main_mesh_position)
        vertices_list.append(self.main_mesh.vertices)
        faces_list.append(self.main_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.main_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Doorhandle/concept_template.py
class Knob_handle(ConceptTemplate):
    def __init__(self, fixed_part_size, sub_size, main_size, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.fixed_part_size = fixed_part_size
        self.sub_size = sub_size
        self.main_size = main_size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        base_mesh_position = [0, 0, fixed_part_size[1] / 2]
        base_mesh_rotation = [np.pi / 2, 0, 0]
        self.base_mesh = Cylinder(fixed_part_size[1], fixed_part_size[0], fixed_part_size[0],
                                  position=base_mesh_position,
                                  rotation=base_mesh_rotation)
        vertices_list.append(self.base_mesh.vertices)
        faces_list.append(self.base_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.base_mesh.vertices)

        middle_mesh_position = [0, 0, fixed_part_size[1] + sub_size[1] / 2]
        middle_mesh_rotation = [np.pi / 2, 0, 0]
        self.middle_mesh = Cylinder(sub_size[1], sub_size[0], sub_size[0],
                                    position=middle_mesh_position,
                                    rotation=middle_mesh_rotation)
        vertices_list.append(self.middle_mesh.vertices)
        faces_list.append(self.middle_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.middle_mesh.vertices)

        main_mesh_position = [0, 0, fixed_part_size[1] + sub_size[1] + main_size[1] / 2]
        main_mesh_rotation = [np.pi / 2, 0, 0]
        self.main_mesh = Cylinder(main_size[1], main_size[0], main_size[0],
                                  position=main_mesh_position,
                                  rotation=main_mesh_rotation)
        vertices_list.append(self.main_mesh.vertices)
        faces_list.append(self.main_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.main_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Doorhandle/concept_template.py
class TShaped_handle(ConceptTemplate):
    def __init__(self, sub_size, main_size, interpiece_offset, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.sub_size = sub_size
        self.main_size = main_size
        self.interpiece_offset = interpiece_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        sub_mesh_position = [0, 0, sub_size[1] / 2]
        sub_mesh_rotation = [np.pi / 2, 0, 0]
        self.sub_mesh = Cylinder(sub_size[1], sub_size[0] / 2, sub_size[0] / 2,
                                 rotation=sub_mesh_rotation,
                                 position=sub_mesh_position)
        vertices_list.append(self.sub_mesh.vertices)
        faces_list.append(self.sub_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.sub_mesh.vertices)

        main_mesh_position = [
            interpiece_offset[0],
            interpiece_offset[1],
            sub_size[1] + main_size[2] / 2,
        ]
        self.main_mesh = Cuboid(main_size[1], main_size[0], main_size[2],
                                position=main_mesh_position)
        vertices_list.append(self.main_mesh.vertices)
        faces_list.append(self.main_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.main_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Kettle/concept_template.py
class Trifold_Handle(ConceptTemplate):
    def __init__(self, horizontal_thickness, horizontal_length, vertical_thickness, horizontal_rotation, horizontal_separation, mounting_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        horizontal_rotation = [x / 180 * np.pi for x in horizontal_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.horizontal_thickness = horizontal_thickness
        self.horizontal_length = horizontal_length
        self.vertical_thickness = vertical_thickness
        self.horizontal_rotation = horizontal_rotation
        self.horizontal_separation = horizontal_separation
        self.mounting_offset = mounting_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        top_mesh_position = [
            0, 
            horizontal_separation[0] / 2 - horizontal_length[0] * np.sin(horizontal_rotation[0]) / 2, 
            -mounting_offset[0] - horizontal_length[0] * np.cos(horizontal_rotation[0]) / 2
            ]
        top_mesh_rotation = [-horizontal_rotation[0], 0, 0]
        self.top_mesh = Cuboid(horizontal_thickness[1], horizontal_thickness[0], horizontal_length[0], 
                               position=top_mesh_position,
                               rotation=top_mesh_rotation)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [
            0, 
            -horizontal_separation[0] / 2 - horizontal_length[1] * np.sin(horizontal_rotation[1]) / 2, 
            -horizontal_length[1] * np.cos(horizontal_rotation[1]) / 2
            ]
        bottom_mesh_rotation = [-horizontal_rotation[1], 0, 0]
        self.bottom_mesh = Cuboid(horizontal_thickness[1], horizontal_thickness[0], horizontal_length[1], 
                                  position=bottom_mesh_position,
                                  rotation=bottom_mesh_rotation)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        delta_y = horizontal_separation[0] - horizontal_length[0] * np.sin(horizontal_rotation[0]) + horizontal_length[1] * np.sin(horizontal_rotation[1])
        delta_z = mounting_offset[0] - horizontal_length[1] * np.cos(horizontal_rotation[1]) + horizontal_length[0] * np.cos(horizontal_rotation[0])
        vertical_length = np.sqrt(delta_y * delta_y + delta_z * delta_z) + horizontal_thickness[1]
        vertical_rotation = np.arctan(delta_z / delta_y)
        vertical_y_offset = (-horizontal_length[0] * np.sin(horizontal_rotation[0]) - horizontal_length[1] * np.sin(horizontal_rotation[1])) / 2
        vertical_z_offset = (horizontal_length[1] * np.cos(horizontal_rotation[1]) + mounting_offset[0] + horizontal_length[0] * np.cos(horizontal_rotation[0])) / 2
        vertical_mesh_position = [
            0, 
            vertical_y_offset, 
            -vertical_z_offset - vertical_thickness[1] / 2
            ]
        vertical_mesh_rotation = [-vertical_rotation, 0, 0]
        self.vertical_mesh = Cuboid(vertical_length, vertical_thickness[0], vertical_thickness[1], 
                                    position=vertical_mesh_position,
                                    rotation=vertical_mesh_rotation)
        vertices_list.append(self.vertical_mesh.vertices)
        faces_list.append(self.vertical_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.vertical_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Kettle/concept_template.py
class Curved_Handle(ConceptTemplate):
    def __init__(self, radius, exist_angle, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        exist_angle = [x / 180 * np.pi for x in exist_angle]
        super().__init__(position, rotation)

        # Record Parameters
        self.radius = radius
        self.exist_angle = exist_angle

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_rotation = [np.pi, 0, -np.pi / 2]
        self.mesh = Torus(radius[0], radius[1], exist_angle[0],
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

        self.semantic = 'Handle'


# Source: Kettle/concept_template.py
class Ring_Handle(ConceptTemplate):
    def __init__(self, size, exist_angle, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        exist_angle = [x / 180 * np.pi for x in exist_angle]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.exist_angle = exist_angle

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_rotation = [np.pi, 0, -np.pi / 2]
        self.mesh = Ring(size[2], size[0], size[1], exist_angle[0],
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

        self.semantic = 'Handle'


# Source: Kettle/concept_template.py
class Cylindrical_Handle(ConceptTemplate):
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

        mesh_position = [0, 0, -size[2] / 2]
        mesh_rotation = [-np.pi / 2, 0, 0]
        self.mesh = Cylinder(size[2], size[0], size[1],
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

        self.semantic = 'Handle'


# Source: Kettle/concept_template.py
class Round_U_Handle(ConceptTemplate):
    def __init__(self, mounting_radius, vertical_separation, vertical_length, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.mounting_radius = mounting_radius
        self.vertical_separation = vertical_separation
        self.vertical_length = vertical_length

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        left_mesh_position = [
            0, 
            vertical_length[0] / 2, 
            vertical_separation[0] / 2
            ]
        self.left_mesh = Cylinder(vertical_length[0], mounting_radius[0],
                                  position=left_mesh_position)
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        right_mesh_position = [
            0, 
            vertical_length[0] / 2, 
            -vertical_separation[0] / 2
            ]
        self.right_mesh = Cylinder(vertical_length[0], mounting_radius[0],
                                  position=right_mesh_position)
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        curve_mesh_position = [
            0, 
            vertical_length[0], 
            0
        ]
        curve_mesh_rotation = [-np.pi / 2, np.pi / 2, 0]
        self.curve_mesh = Torus(vertical_separation[0] / 2, mounting_radius[0], np.pi,
                                position=curve_mesh_position,
                                rotation=curve_mesh_rotation)
        vertices_list.append(self.curve_mesh.vertices)
        faces_list.append(self.curve_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.curve_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Kettle/concept_template.py
class Flat_U_Handle(ConceptTemplate):
    def __init__(self, vertical_size, vertical_separation, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.vertical_size = vertical_size
        self.vertical_separation = vertical_separation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        left_mesh_position = [
            0, 
            vertical_size[1] / 2, 
            vertical_separation[0] / 2
            ]
        self.left_mesh = Cuboid(vertical_size[1], vertical_size[0], vertical_size[2], 
                                position=left_mesh_position)
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        right_mesh_position = [
            0, 
            vertical_size[1] / 2, 
            -vertical_separation[0] / 2
            ]
        self.right_mesh = Cuboid(vertical_size[1], vertical_size[0], vertical_size[2], 
                                position=right_mesh_position)
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        outer_radius = (vertical_separation[0] + vertical_size[2]) / 2
        mounting_radius = (vertical_separation[0] - vertical_size[2]) / 2
        curve_mesh_position = [
            0, 
            vertical_size[1], 
            0
            ]
        curve_mesh_rotation = [-np.pi / 2, np.pi / 2, 0]
        self.curve_mesh = Ring(vertical_size[0], outer_radius, mounting_radius, np.pi,
                               position=curve_mesh_position,
                               rotation=curve_mesh_rotation)
        vertices_list.append(self.curve_mesh.vertices)
        faces_list.append(self.curve_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.curve_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Bucket/concept_template.py
class Trifold_Handle(ConceptTemplate):
    def __init__(self, vertical_thickness, vertical_length, horizontal_thickness, vertical_rotation, vertical_separation, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        vertical_rotation = [x / 180 * np.pi for x in vertical_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.vertical_thickness = vertical_thickness
        self.vertical_length = vertical_length
        self.horizontal_thickness = horizontal_thickness
        self.vertical_rotation = vertical_rotation
        self.vertical_separation = vertical_separation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        top_mesh_position = [
            vertical_separation[0] / 2 - vertical_length[0] * np.sin(vertical_rotation[0]) / 2, 
            vertical_length[0] * np.cos(vertical_rotation[0]) / 2, 
            0
            ]
        top_mesh_rotation = [0, 0, vertical_rotation[0]]
        self.top_mesh = Cuboid(vertical_length[0], vertical_thickness[0], vertical_thickness[1], 
                               position=top_mesh_position,
                               rotation=top_mesh_rotation)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [
            -vertical_separation[0] / 2 - vertical_length[1] * np.sin(vertical_rotation[1]) / 2, 
            vertical_length[1] * np.cos(vertical_rotation[1]) / 2, 
            0
            ]
        bottom_mesh_rotation = [0, 0, vertical_rotation[1]]
        self.bottom_mesh = Cuboid(vertical_length[1], vertical_thickness[0], vertical_thickness[1], 
                                  position=bottom_mesh_position,
                                  rotation=bottom_mesh_rotation)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        delta_x = vertical_separation[0] - vertical_length[0] * np.sin(vertical_rotation[0]) + vertical_length[1] * np.sin(vertical_rotation[1])
        delta_y = vertical_length[0] * np.cos(vertical_rotation[0]) - vertical_length[1] * np.cos(vertical_rotation[1])
        horizontal_length = np.sqrt(delta_y * delta_y + delta_x * delta_x) + vertical_thickness[0]
        horizontal_rotation = np.arctan(delta_y / delta_x)
        vertical_x_offset = (-vertical_length[0] * np.sin(vertical_rotation[0]) - vertical_length[1] * np.sin(vertical_rotation[1])) / 2
        vertical_y_offset = (vertical_length[1] * np.cos(vertical_rotation[1]) + vertical_length[0] * np.cos(vertical_rotation[0])) / 2
        vertical_mesh_position = [
            vertical_x_offset, 
            vertical_y_offset + horizontal_thickness[0] / 2, 
            0
            ]
        vertical_mesh_rotation = [0, 0, horizontal_rotation]
        self.vertical_mesh = Cuboid(horizontal_thickness[0], horizontal_length, horizontal_thickness[1], 
                                    position=vertical_mesh_position,
                                    rotation=vertical_mesh_rotation)
        vertices_list.append(self.vertical_mesh.vertices)
        faces_list.append(self.vertical_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.vertical_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)


        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Bucket/concept_template.py
class Curved_Handle(ConceptTemplate):
    def __init__(self, radius, exist_angle, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        exist_angle = [x / 180 * np.pi for x in exist_angle]
        super().__init__(position, rotation)

        # Record Parameters
        self.radius = radius
        self.exist_angle = exist_angle

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_rotation = [-np.pi / 2, 0, 0]
        self.mesh = Torus(radius[0], radius[1], exist_angle[0],
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

        self.semantic = 'Handle'


# Source: Bucket/concept_template.py
class Round_U_Handle(ConceptTemplate):
    def __init__(self, inner_radius, vertical_separation, vertical_length, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.inner_radius = inner_radius
        self.vertical_separation = vertical_separation
        self.vertical_length = vertical_length

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        left_mesh_position = [
            vertical_separation[0] / 2, 
            vertical_length[0] / 2, 
            0
            ]
        self.left_mesh = Cylinder(vertical_length[0], inner_radius[0],
                                  position=left_mesh_position)
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        right_mesh_position = [
            -vertical_separation[0] / 2, 
            vertical_length[0] / 2, 
            0
            ]
        self.right_mesh = Cylinder(vertical_length[0], inner_radius[0],
                                  position=right_mesh_position)
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        curve_mesh_position = [
            0, 
            vertical_length[0], 
            0
            ]
        curve_mesh_rotation = [-np.pi / 2, 0, 0]
        self.curve_mesh = Torus(vertical_separation[0] / 2, inner_radius[0], np.pi,
                                position=curve_mesh_position,
                                rotation=curve_mesh_rotation)
        vertices_list.append(self.curve_mesh.vertices)
        faces_list.append(self.curve_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.curve_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Bucket/concept_template.py
class Flat_U_Handle(ConceptTemplate):
    def __init__(self, vertical_size, vertical_separation, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.vertical_size = vertical_size
        self.vertical_separation = vertical_separation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        left_mesh_position = [
            vertical_separation[0] / 2, 
            vertical_size[1] / 2, 
            0
            ]
        self.left_mesh = Cuboid(vertical_size[1], vertical_size[0], vertical_size[2], 
                                position=left_mesh_position)
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        right_mesh_position = [
            -vertical_separation[0] / 2, 
            vertical_size[1] / 2, 
            0
            ]
        self.right_mesh = Cuboid(vertical_size[1], vertical_size[0], vertical_size[2], 
                                position=right_mesh_position)
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        outer_radius = (vertical_separation[0] + vertical_size[0]) / 2
        inner_radius = (vertical_separation[0] - vertical_size[0]) / 2
        curve_mesh_position = [
            0, 
            vertical_size[1], 
            0
            ]
        curve_mesh_rotation = [-np.pi / 2, 0, 0]
        self.curve_mesh = Ring(vertical_size[2], outer_radius, inner_radius, np.pi,
                               position=curve_mesh_position,
                               rotation=curve_mesh_rotation)
        vertices_list.append(self.curve_mesh.vertices)
        faces_list.append(self.curve_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.curve_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Window/concept_template.py
class Cuboidal_Handle(ConceptTemplate):
    def __init__(self, handle_z_position, window_type, windows_size, num_of_handle, size, offset_x, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.handle_z_position = handle_z_position
        self.window_type = window_type
        self.windows_size = windows_size
        self.num_of_handle = num_of_handle
        self.size = size
        self.offset_x = offset_x

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(num_of_handle[0]):
            position_z = 0
            z_layer_position = handle_z_position[i]
            if window_type == 0:
                if z_layer_position == -1:
                    position_z -= windows_size["size_0"][1] / 2
                if z_layer_position >= 0:
                    position_z += windows_size["size_0"][1] / 2
                if z_layer_position >= 1:
                    position_z += windows_size["size_1"][1]
            elif window_type == 1:
                if z_layer_position >= 0:
                    position_z += windows_size["size_0"][1] / 2
                if z_layer_position >= 1:
                    position_z += windows_size["size_1"][1]
                if z_layer_position >= 2:
                    position_z += windows_size["size_2"][1]
                if z_layer_position == 3:
                    position_z += windows_size["size_3"][1]

            handle_mesh_position = [offset_x[i], 0, position_z + size[2] / 2]
            self.handle_mesh = Cuboid(size[1], size[0], size[2],
                                 position=handle_mesh_position)
            vertices_list.append(self.handle_mesh.vertices)
            faces_list.append(self.handle_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.handle_mesh.vertices)

        for i in range(num_of_handle[1]):
            position_z = 0
            z_layer_position = handle_z_position[i]
            if window_type == 0:
                if z_layer_position == -1:
                    position_z -= (
                        windows_size["size_0"][1] / 2 + windows_size["size_2"][1]
                    )
                if z_layer_position >= 0:
                    position_z += windows_size["size_0"][1] / 2
                if z_layer_position >= 1:
                    position_z += windows_size["size_0"][1]
            elif window_type == 1:
                if z_layer_position >= 0:
                    position_z -= windows_size["size_0"][1] / 2
                if z_layer_position >= 1:
                    position_z += windows_size["size_0"][1]
                if z_layer_position >= 2:
                    position_z += windows_size["size_1"][1]
                if z_layer_position == 3:
                    position_z += windows_size["size_2"][1]

            handle_mesh_position = [offset_x[i + 2], 0, position_z - size[2] / 2]
            self.handle_mesh = Cuboid(size[1], size[0], size[2],
                                 position=handle_mesh_position)
            vertices_list.append(self.handle_mesh.vertices)
            faces_list.append(self.handle_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.handle_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Window/concept_template.py
class Arched_Handle(ConceptTemplate):
    def __init__(self, handle_z_position, window_type, windows_size, num_of_handle, outer_size, bottom_size, offset_x, seperation, thinner_handle, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.handle_z_position = handle_z_position
        self.window_type = window_type
        self.windows_size = windows_size
        self.num_of_handle = num_of_handle
        self.outer_size = outer_size
        self.bottom_size = bottom_size
        self.offset_x = offset_x
        self.seperation = seperation
        self.thinner_handle = thinner_handle

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        central_angle = (np.arcsin((seperation[0] / 2 + bottom_size[1]) / outer_size[0]) * 2)
        arch_offset_z = bottom_size[2] - np.cos(central_angle / 2) * outer_size[0]

        for i in range(num_of_handle[0]):
            position_z = 0
            z_layer_position = handle_z_position[i]
            if window_type == 0:
                if z_layer_position == -1:
                    position_z -= windows_size["size_0"][1] / 2
                if z_layer_position >= 0:
                    position_z += windows_size["size_0"][1] / 2
                if z_layer_position >= 1:
                    position_z += windows_size["size_1"][1]
            elif window_type == 1:
                if z_layer_position >= 0:
                    position_z += windows_size["size_0"][1] / 2
                if z_layer_position >= 1:
                    position_z += windows_size["size_1"][1]
                if z_layer_position >= 2:
                    position_z += windows_size["size_2"][1]
                if z_layer_position == 3:
                    position_z += windows_size["size_3"][1]

            top_mesh_position = [
                offset_x[i],
                seperation[0] / 2 + bottom_size[1] / 2,
                position_z + bottom_size[2] / 2,
            ]   
            self.top_mesh = Cuboid(bottom_size[1], bottom_size[0], bottom_size[2],
                                   position=top_mesh_position)
            vertices_list.append(self.top_mesh.vertices)
            faces_list.append(self.top_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.top_mesh.vertices)

            bottom_mesh_position = [
                offset_x[i],
                -seperation[0] / 2 - bottom_size[1] / 2,
                position_z + bottom_size[2] / 2,
            ]
            self.bottom_mesh = Cuboid(bottom_size[1], bottom_size[0], bottom_size[2],
                                      position=bottom_mesh_position)
            vertices_list.append(self.bottom_mesh.vertices)
            faces_list.append(self.bottom_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.bottom_mesh.vertices)

            main_mesh_position = [
                offset_x[i],
                0,
                position_z + +arch_offset_z,
            ]
            main_mesh_rotation = [0, -np.pi / 2 + central_angle / 2, np.pi / 2]
            self.main_mesh = Ring(bottom_size[0], outer_size[0],
                                  seperation[0] / 2 / np.sin(central_angle / 2) + thinner_handle[0],
                                  exist_angle=central_angle,
                                  position=main_mesh_position,
                                  rotation=main_mesh_rotation)
            vertices_list.append(self.main_mesh.vertices)
            faces_list.append(self.main_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.main_mesh.vertices)

        for i in range(num_of_handle[1]):
            position_z = 0
            z_layer_position = handle_z_position[i]
            if window_type == 0:
                if z_layer_position == -1:
                    position_z -= (
                        windows_size["size_0"][1] / 2 + windows_size["size_2"][1]
                    )
                if z_layer_position >= 0:
                    position_z -= windows_size["size_0"][1] / 2
                if z_layer_position >= 1:
                    position_z += windows_size["size_0"][1]
            elif window_type == 1:
                if z_layer_position >= 0:
                    position_z -= windows_size["size_0"][1] / 2
                if z_layer_position >= 1:
                    position_z += windows_size["size_0"][1]
                if z_layer_position >= 2:
                    position_z += windows_size["size_1"][1]
                if z_layer_position == 3:
                    position_z += windows_size["size_2"][1]

            top_mesh_position = [
                offset_x[i+2],
                seperation[0] / 2 + bottom_size[1] / 2,
                position_z - bottom_size[2] / 2,
            ]   
            self.top_mesh = Cuboid(bottom_size[1], bottom_size[0], bottom_size[2],
                              position=top_mesh_position)
            vertices_list.append(self.top_mesh.vertices)
            faces_list.append(self.top_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.top_mesh.vertices)

            bottom_mesh_position = [
                offset_x[i+2],
                -seperation[0] / 2 - bottom_size[1] / 2,
                position_z - bottom_size[2] / 2,
            ]
            self.bottom_mesh = Cuboid(bottom_size[1], bottom_size[0], bottom_size[2],
                                 position=bottom_mesh_position)
            vertices_list.append(self.bottom_mesh.vertices)
            faces_list.append(self.bottom_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.bottom_mesh.vertices)

            main_mesh_position = [
                offset_x[i+2],
                0,
                position_z - arch_offset_z,
            ]
            main_mesh_rotation = [0, np.pi / 2 + central_angle / 2, np.pi / 2]
            self.main_mesh = Ring(bottom_size[0], outer_size[0],
                                  seperation[0] / 2 / np.sin(central_angle / 2) + thinner_handle[0],
                                  exist_angle=central_angle,
                                  position=main_mesh_position,
                                  rotation=main_mesh_rotation)
            vertices_list.append(self.main_mesh.vertices)
            faces_list.append(self.main_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.main_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Window/concept_template.py
class LShaped_Handle(ConceptTemplate):
    def __init__(self, handle_z_position, window_type, windows_size, num_of_handle, size_bottom, size_middle, size_top, offset_middle_y, offset_top_y, offset_x, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.handle_z_position = handle_z_position
        self.window_type = window_type
        self.windows_size = windows_size
        self.num_of_handle = num_of_handle
        self.size_bottom = size_bottom
        self.size_middle = size_middle
        self.size_top = size_top
        self.offset_middle_y = offset_middle_y
        self.offset_top_y = offset_top_y
        self.offset_x = offset_x

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(num_of_handle[0]):
            position_z = 0
            z_layer_position = handle_z_position[i]
            if window_type == 0:
                if z_layer_position == -1:
                    position_z -= windows_size["size_0"][1] / 2
                if z_layer_position >= 0:
                    position_z += windows_size["size_0"][1] / 2
                if z_layer_position >= 1:
                    position_z += windows_size["size_1"][1]
            elif window_type == 1:
                if z_layer_position >= 0:
                    position_z += windows_size["size_0"][1] / 2
                if z_layer_position >= 1:
                    position_z += windows_size["size_1"][1]
                if z_layer_position >= 2:
                    position_z += windows_size["size_2"][1]
                if z_layer_position == 3:
                    position_z += windows_size["size_3"][1]

            bottom_mesh_position = [
                offset_x[i],
                0,
                position_z + size_bottom[2] / 2,
            ]
            self.bottom_mesh = Cuboid(size_bottom[1], size_bottom[0], size_bottom[2],
                                      position=bottom_mesh_position)
            vertices_list.append(self.bottom_mesh.vertices)
            faces_list.append(self.bottom_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.bottom_mesh.vertices)

            middle_mesh_position = [
                offset_x[i],
                offset_middle_y[0],
                position_z + size_bottom[2] + size_middle[2] / 2,
            ]
            self.middle_mesh = Cuboid(size_middle[1], size_middle[0], size_middle[2],
                                      position=middle_mesh_position)
            vertices_list.append(self.middle_mesh.vertices)
            faces_list.append(self.middle_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.middle_mesh.vertices)

            top_mesh_position = [
                offset_x[i],
                offset_middle_y[0] + offset_top_y[0],
                position_z + size_bottom[2] + size_middle[2] + size_top[2] / 2,
            ]
            self.top_mesh = Cuboid(size_top[1], size_top[0], size_top[2],
                                   position=top_mesh_position)
            vertices_list.append(self.top_mesh.vertices)
            faces_list.append(self.top_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.top_mesh.vertices)

        for i in range(num_of_handle[1]):
            position_z = 0
            z_layer_position = handle_z_position[i]
            if window_type == 0:
                if z_layer_position == -1:
                    position_z -= (
                        windows_size["size_0"][1] / 2 + windows_size["size_2"][1]
                    )
                if z_layer_position >= 0:
                    position_z += windows_size["size_0"][1] / 2
                if z_layer_position >= 1:
                    position_z += windows_size["size_0"][1]
            elif window_type == 1:
                if z_layer_position >= 0:
                    position_z -= windows_size["size_0"][1] / 2
                if z_layer_position >= 1:
                    position_z += windows_size["size_0"][1]
                if z_layer_position >= 2:
                    position_z += windows_size["size_1"][1]
                if z_layer_position == 3:
                    position_z += windows_size["size_2"][1]

            bottom_mesh_position = [
                offset_x[i+2],
                0,
                position_z - size_bottom[2] / 2,
            ]  
            self.bottom_mesh = Cuboid(size_bottom[1], size_bottom[0], size_bottom[2],
                                      position=bottom_mesh_position)
            vertices_list.append(self.bottom_mesh.vertices)
            faces_list.append(self.bottom_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.bottom_mesh.vertices)

            middle_mesh_position = [
                offset_x[i+2],
                offset_middle_y[0],
                position_z - size_bottom[2] - size_middle[2] / 2,
            ]
            self.middle_mesh = Cuboid(size_middle[1], size_middle[0], size_middle[2],
                                      position=middle_mesh_position)
            vertices_list.append(self.middle_mesh.vertices)
            faces_list.append(self.middle_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.middle_mesh.vertices)

            top_mesh_position = [
                offset_x[i+2],
                offset_middle_y[0] + offset_top_y[0],
                position_z - size_bottom[2] - size_middle[2] - size_top[2] / 2,
            ]
            self.top_mesh = Cuboid(size_top[1], size_top[0], size_top[2],
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

        self.semantic = 'Handle'


# Source: Mug/concept_template.py
class Trifold_Handle(ConceptTemplate):
    def __init__(self, horizontal_thickness, horizontal_length, vertical_thickness, horizontal_rotation, horizontal_separation, mounting_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        horizontal_rotation = [x / 180 * np.pi for x in horizontal_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.horizontal_thickness = horizontal_thickness
        self.horizontal_length = horizontal_length
        self.vertical_thickness = vertical_thickness
        self.horizontal_rotation = horizontal_rotation
        self.horizontal_separation = horizontal_separation
        self.mounting_offset = mounting_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        top_mesh_position = [
            0, 
            horizontal_separation[0] / 2 - horizontal_length[0] * np.sin(horizontal_rotation[0]) / 2, 
            mounting_offset[0] + horizontal_length[0] * np.cos(horizontal_rotation[0]) / 2
            ]
        top_mesh_rotation = [horizontal_rotation[0], 0, 0]
        self.top_mesh = Cuboid(horizontal_thickness[1], horizontal_thickness[0], horizontal_length[0], 
                               position=top_mesh_position,
                               rotation=top_mesh_rotation)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [
            0, 
            -horizontal_separation[0] / 2 - horizontal_length[1] * np.sin(horizontal_rotation[1]) / 2, 
            horizontal_length[1] * np.cos(horizontal_rotation[1]) / 2
            ]
        bottom_mesh_rotation = [horizontal_rotation[1], 0, 0]
        self.bottom_mesh = Cuboid(horizontal_thickness[1], horizontal_thickness[0], horizontal_length[1], 
                                  position=bottom_mesh_position,
                                  rotation=bottom_mesh_rotation)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        delta_y = horizontal_separation[0] - horizontal_length[0] * np.sin(horizontal_rotation[0]) + horizontal_length[1] * np.sin(horizontal_rotation[1])
        delta_z = mounting_offset[0] - horizontal_length[1] * np.cos(horizontal_rotation[1]) + horizontal_length[0] * np.cos(horizontal_rotation[0])
        vertical_length = np.sqrt(delta_y * delta_y + delta_z * delta_z) + horizontal_thickness[1]
        vertical_rotation = np.arctan(delta_z / delta_y)
        vertical_y_offset = (-horizontal_length[0] * np.sin(horizontal_rotation[0]) - horizontal_length[1] * np.sin(horizontal_rotation[1])) / 2
        vertical_z_offset = (horizontal_length[1] * np.cos(horizontal_rotation[1]) + mounting_offset[0] + horizontal_length[0] * np.cos(horizontal_rotation[0])) / 2
        vertical_mesh_position = [
            0, 
            vertical_y_offset, 
            vertical_z_offset + vertical_thickness[1] / 2
            ]
        vertical_mesh_rotation = [vertical_rotation, 0, 0]
        self.vertical_mesh = Cuboid(vertical_length, vertical_thickness[0], vertical_thickness[1], 
                                  position=vertical_mesh_position,
                                  rotation=vertical_mesh_rotation)
        vertices_list.append(self.vertical_mesh.vertices)
        faces_list.append(self.vertical_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.vertical_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Mug/concept_template.py
class Curved_Handle(ConceptTemplate):
    def __init__(self, radius, central_angle, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        central_angle = [x / 180 * np.pi for x in central_angle]
        super().__init__(position, rotation)

        # Record Parameters
        self.radius = radius
        self.central_angle = central_angle

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_rotation = [0, 0, np.pi / 2]
        self.mesh = Torus(radius[0], radius[1], central_angle[0],
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

        self.semantic = 'Handle'


# Source: Scissors/concept_template.py
class Ring_Handle(ConceptTemplate):
    def __init__(self, root_size, root_rotation, arm_radius, arm_thickness, arm_offset, arm_rotation, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        root_rotation = [x / 180 * np.pi for x in root_rotation]
        arm_rotation = [x / 180 * np.pi for x in arm_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.root_size = root_size
        self.root_rotation = root_rotation
        self.arm_radius = arm_radius
        self.arm_thickness = arm_thickness
        self.arm_offset = arm_offset
        self.arm_rotation = arm_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # root
        root_mesh_position_1 = [
            root_size[0] / 2, 
            0,
            0
        ]
        root_mesh_rotation_1 = [0, -root_rotation[0], 0]
        root_mesh_position = adjust_position_from_rotation(root_mesh_position_1, root_mesh_rotation_1)

        root_mesh_rotation_2 = [np.pi / 2, np.pi / 2, 0]
        root_mesh_rotation = list_add(root_mesh_rotation_1, root_mesh_rotation_2)

        self.root_mesh = Cuboid(root_size[0], root_size[3], root_size[1],
                                root_size[2], root_size[1],
                                position = root_mesh_position,
                                rotation = root_mesh_rotation)
        vertices_list.append(self.root_mesh.vertices)
        faces_list.append(self.root_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.root_mesh.vertices)

        # arm
        arm_mesh_position_1 = [
            arm_radius[0], 
            0,
            0
        ]
        arm_mesh_rotation = [0, -arm_rotation[0], 0]
        arm_mesh_position_1 = adjust_position_from_rotation(arm_mesh_position_1, arm_mesh_rotation)

        arm_mesh_position_2 = [
            root_size[0] * np.cos(root_rotation[0]) - arm_offset[0] * np.tan(root_rotation[0]), 
            0,
            root_size[0] * np.sin(root_rotation[0]) + arm_offset[0]
        ]
        arm_mesh_position = list_add(arm_mesh_position_1, arm_mesh_position_2)

        self.arm_mesh = Ring(arm_thickness[0], arm_radius[1], arm_radius[3],
                             x_z_ratio = arm_radius[0] / arm_radius[1],
                             inner_x_z_ratio = arm_radius[2] / arm_radius[3],
                             position = arm_mesh_position,
                             rotation = arm_mesh_rotation)
        vertices_list.append(self.arm_mesh.vertices)
        faces_list.append(self.arm_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.arm_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Scissors/concept_template.py
class Half_Ring_Handle(ConceptTemplate):
    def __init__(self, root_size, root_rotation, arm_radius, arm_thickness, arm_horizontal_thickness, arm_offset, arm_rotation, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        root_rotation = [x / 180 * np.pi for x in root_rotation]
        arm_rotation = [x / 180 * np.pi for x in arm_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.root_size = root_size
        self.root_rotation = root_rotation
        self.arm_radius = arm_radius
        self.arm_thickness = arm_thickness
        self.arm_horizontal_thickness = arm_horizontal_thickness
        self.arm_offset = arm_offset
        self.arm_rotation = arm_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # root
        root_mesh_position_1 = [
            root_size[0] / 2, 
            0,
            0
        ]
        root_mesh_rotation_1 = [0, -root_rotation[0], 0]
        root_mesh_position = adjust_position_from_rotation(root_mesh_position_1, root_mesh_rotation_1)

        root_mesh_rotation_2 = [np.pi / 2, np.pi / 2, 0]
        root_mesh_rotation = list_add(root_mesh_rotation_1, root_mesh_rotation_2)

        self.root_mesh = Cuboid(root_size[0], root_size[3], root_size[1],
                                root_size[2], root_size[1],
                                position = root_mesh_position,
                                rotation = root_mesh_rotation)
        vertices_list.append(self.root_mesh.vertices)
        faces_list.append(self.root_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.root_mesh.vertices)

        # arm ring
        ring_mesh_position_1 = [
            arm_radius[0], 
            0,
            0
        ]
        ring_mesh_rotation = [0, -arm_rotation[0], 0]
        ring_mesh_position_1 = adjust_position_from_rotation(ring_mesh_position_1, ring_mesh_rotation)

        ring_mesh_position_2 = [
            root_size[0] * np.cos(root_rotation[0]) - arm_offset[0] * np.tan(root_rotation[0]), 
            0,
            root_size[0] * np.sin(root_rotation[0]) + arm_offset[0]
        ]
        ring_mesh_position = list_add(ring_mesh_position_1, ring_mesh_position_2)

        self.ring_mesh = Ring(arm_thickness[0], arm_radius[1], arm_radius[3], np.pi, 
                             x_z_ratio = arm_radius[0] / arm_radius[1],
                             inner_x_z_ratio = arm_radius[2] / arm_radius[3],
                             position = ring_mesh_position,
                             rotation = ring_mesh_rotation)
        vertices_list.append(self.ring_mesh.vertices)
        faces_list.append(self.ring_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.ring_mesh.vertices)

        # arm horizontal
        horizontal_mesh_position_1 = [
            arm_radius[0], 
            0,
            -arm_horizontal_thickness[0] / 2
        ]
        horizontal_mesh_rotation = [0, -arm_rotation[0], 0]
        horizontal_mesh_position_1 = adjust_position_from_rotation(horizontal_mesh_position_1, horizontal_mesh_rotation)

        horizontal_mesh_position_2 = [
            root_size[0] * np.cos(root_rotation[0]) - arm_offset[0] * np.tan(root_rotation[0]), 
            0,
            root_size[0] * np.sin(root_rotation[0]) + arm_offset[0]
        ]
        horizontal_mesh_position = list_add(horizontal_mesh_position_1, horizontal_mesh_position_2)

        self.horizontal_mesh = Cuboid(arm_thickness[0], arm_radius[0] * 2, arm_horizontal_thickness[0], 
                                      position = horizontal_mesh_position,
                                      rotation = horizontal_mesh_rotation)
        vertices_list.append(self.horizontal_mesh.vertices)
        faces_list.append(self.horizontal_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.horizontal_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Scissors/concept_template.py
class Double_Curved_Handle(ConceptTemplate):
    def __init__(self, root_size, root_rotation, arm_radius, arm_thickness, arm_exist_angle, arm_top_bottom_separation, arm_offset, arm_rotation, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        root_rotation = [x / 180 * np.pi for x in root_rotation]
        arm_exist_angle = [x / 180 * np.pi for x in arm_exist_angle]
        arm_rotation = [x / 180 * np.pi for x in arm_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.root_size = root_size
        self.root_rotation = root_rotation
        self.arm_radius = arm_radius
        self.arm_thickness = arm_thickness
        self.arm_exist_angle = arm_exist_angle
        self.arm_top_bottom_separation = arm_top_bottom_separation
        self.arm_offset = arm_offset
        self.arm_rotation = arm_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # root
        root_mesh_position_1 = [
            root_size[0] / 2, 
            0,
            0
        ]
        root_mesh_rotation_1 = [0, -root_rotation[0], 0]
        root_mesh_position = adjust_position_from_rotation(root_mesh_position_1, root_mesh_rotation_1)

        root_mesh_rotation_2 = [np.pi / 2, np.pi / 2, 0]
        root_mesh_rotation = list_add(root_mesh_rotation_1, root_mesh_rotation_2)

        self.root_mesh = Cuboid(root_size[0], root_size[3], root_size[1],
                                root_size[2], root_size[1],
                                position = root_mesh_position,
                                rotation = root_mesh_rotation)
        vertices_list.append(self.root_mesh.vertices)
        faces_list.append(self.root_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.root_mesh.vertices)

        # arm bottom
        bottom_mesh_position_1 = [
            arm_radius[1], 
            0,
            0
        ]
        bottom_mesh_rotation = [0, -arm_rotation[0], 0]
        bottom_mesh_position_1 = adjust_position_from_rotation(bottom_mesh_position_1, bottom_mesh_rotation)

        bottom_mesh_position_2 = [
            root_size[0] * np.cos(root_rotation[0]) - arm_offset[0] * np.tan(root_rotation[0]), 
            0,
            root_size[0] * np.sin(root_rotation[0]) + arm_offset[0]
        ]
        bottom_mesh_position = list_add(bottom_mesh_position_1, bottom_mesh_position_2)
        bottom_mesh_rotation[1] += -np.pi + arm_exist_angle[1] / 2

        self.bottom_mesh = Ring(arm_thickness[0], arm_radius[1], arm_radius[1] - arm_thickness[1], arm_exist_angle[1], 
                                position = bottom_mesh_position,
                                rotation = bottom_mesh_rotation)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        # arm top
        top_mesh_position_1 = [
            -arm_radius[0] * np.cos(arm_exist_angle[0] / 2) + arm_radius[1] * (1 - np.cos(arm_exist_angle[1] / 2)) + arm_top_bottom_separation[0], 
            0,
            0
        ]
        top_mesh_rotation = [0, -arm_rotation[0], 0]
        top_mesh_position_1 = adjust_position_from_rotation(top_mesh_position_1, top_mesh_rotation)

        top_mesh_position_2 = [
            root_size[0] * np.cos(root_rotation[0]) - arm_offset[0] * np.tan(root_rotation[0]), 
            0,
            root_size[0] * np.sin(root_rotation[0]) + arm_offset[0]
        ]
        top_mesh_position = list_add(top_mesh_position_1, top_mesh_position_2)
        top_mesh_rotation[1] += arm_exist_angle[0] / 2

        self.top_mesh = Ring(arm_thickness[0], arm_radius[0], arm_radius[0] - arm_thickness[1], arm_exist_angle[0], 
                             position = top_mesh_position,
                             rotation = top_mesh_rotation)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        # arm left
        arm_delta_z = arm_radius[0] * np.sin(arm_exist_angle[0] / 2) - arm_radius[1] * np.sin(arm_exist_angle[1] / 2)
        box_length = np.sqrt(arm_delta_z * arm_delta_z + arm_top_bottom_separation[0] * arm_top_bottom_separation[0])
        box_rotation = np.arctan(arm_delta_z / arm_top_bottom_separation[0])

        left_mesh_position_1 = [
            arm_radius[1] * (1 - np.cos(arm_exist_angle[1] / 2)) + arm_top_bottom_separation[0] / 2 + arm_thickness[1] / 2 * np.sin(box_rotation), 
            0,
            -(arm_radius[0] * np.sin(arm_exist_angle[0] / 2) + arm_radius[1] * np.sin(arm_exist_angle[1] / 2)) / 2 + arm_thickness[1] / 2 * np.cos(box_rotation)
        ]
        left_mesh_rotation = [0, -arm_rotation[0], 0]
        left_mesh_position_1 = adjust_position_from_rotation(left_mesh_position_1, left_mesh_rotation)

        left_mesh_position_2 = [
            root_size[0] * np.cos(root_rotation[0]) - arm_offset[0] * np.tan(root_rotation[0]), 
            0,
            root_size[0] * np.sin(root_rotation[0]) + arm_offset[0]
        ]
        left_mesh_position = list_add(left_mesh_position_1, left_mesh_position_2)
        left_mesh_rotation[1] += box_rotation

        self.left_mesh = Cuboid(arm_thickness[0], box_length, arm_thickness[1], 
                                position = left_mesh_position,
                                rotation = left_mesh_rotation)
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        # arm right
        right_mesh_position_1 = [
            arm_radius[1] * (1 - np.cos(arm_exist_angle[1] / 2)) + arm_top_bottom_separation[0] / 2 + arm_thickness[1] / 2 * np.sin(box_rotation), 
            0,
            (arm_radius[0] * np.sin(arm_exist_angle[0] / 2) + arm_radius[1] * np.sin(arm_exist_angle[1] / 2)) / 2 - arm_thickness[1] / 2 * np.cos(box_rotation)
        ]
        right_mesh_rotation = [0, -arm_rotation[0], 0]
        right_mesh_position_1 = adjust_position_from_rotation(right_mesh_position_1, right_mesh_rotation)

        right_mesh_position_2 = [
            root_size[0] * np.cos(root_rotation[0]) - arm_offset[0] * np.tan(root_rotation[0]), 
            0,
            root_size[0] * np.sin(root_rotation[0]) + arm_offset[0]
        ]
        right_mesh_position = list_add(right_mesh_position_1, right_mesh_position_2)
        right_mesh_rotation[1] += -box_rotation

        self.right_mesh = Cuboid(arm_thickness[0], box_length, arm_thickness[1], 
                                 position = right_mesh_position,
                                 rotation = right_mesh_rotation)
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Scissors/concept_template.py
class Triple_Curved_Handle(ConceptTemplate):
    def __init__(self, root_size, root_rotation, arm_radius, arm_thickness, arm_exist_angle, arm_top_bottom_separation, arm_offset, arm_rotation, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        root_rotation = [x / 180 * np.pi for x in root_rotation]
        arm_exist_angle = [x / 180 * np.pi for x in arm_exist_angle]
        arm_rotation = [x / 180 * np.pi for x in arm_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.root_size = root_size
        self.root_rotation = root_rotation
        self.arm_radius = arm_radius
        self.arm_thickness = arm_thickness
        self.arm_exist_angle = arm_exist_angle
        self.arm_top_bottom_separation = arm_top_bottom_separation
        self.arm_offset = arm_offset
        self.arm_rotation = arm_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # root
        root_mesh_position_1 = [
            root_size[0] / 2, 
            0,
            0
        ]
        root_mesh_rotation_1 = [0, -root_rotation[0], 0]
        root_mesh_position = adjust_position_from_rotation(root_mesh_position_1, root_mesh_rotation_1)

        root_mesh_rotation_2 = [np.pi / 2, np.pi / 2, 0]
        root_mesh_rotation = list_add(root_mesh_rotation_1, root_mesh_rotation_2)

        self.root_mesh = Cuboid(root_size[0], root_size[3], root_size[1],
                                root_size[2], root_size[1],
                                position = root_mesh_position,
                                rotation = root_mesh_rotation)
        vertices_list.append(self.root_mesh.vertices)
        faces_list.append(self.root_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.root_mesh.vertices)

        # arm bottom
        bottom_mesh_position_1 = [
            arm_radius[0], 
            0,
            0
        ]
        bottom_mesh_rotation = [0, -arm_rotation[0], 0]
        bottom_mesh_position_1 = adjust_position_from_rotation(bottom_mesh_position_1, bottom_mesh_rotation)

        bottom_mesh_position_2 = [
            root_size[0] * np.cos(root_rotation[0]) - arm_offset[0] * np.tan(root_rotation[0]), 
            0,
            root_size[0] * np.sin(root_rotation[0]) + arm_offset[0]
        ]
        bottom_mesh_position = list_add(bottom_mesh_position_1, bottom_mesh_position_2)
        bottom_mesh_rotation[1] += -np.pi + arm_exist_angle[0] / 2

        self.bottom_mesh = Ring(arm_thickness[0], arm_radius[0], arm_radius[0] - arm_thickness[1], arm_exist_angle[0], 
                                position = bottom_mesh_position,
                                rotation = bottom_mesh_rotation)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        # arm top
        top_mesh_position_1 = [
            -arm_radius[0] * np.cos(arm_exist_angle[0] / 2) + arm_radius[0] * (1 - np.cos(arm_exist_angle[0] / 2)) + arm_top_bottom_separation[0], 
            0,
            0
        ]
        top_mesh_rotation = [0, -arm_rotation[0], 0]
        top_mesh_position_1 = adjust_position_from_rotation(top_mesh_position_1, top_mesh_rotation)

        top_mesh_position_2 = [
            root_size[0] * np.cos(root_rotation[0]) - arm_offset[0] * np.tan(root_rotation[0]), 
            0,
            root_size[0] * np.sin(root_rotation[0]) + arm_offset[0]
        ]
        top_mesh_position = list_add(top_mesh_position_1, top_mesh_position_2)
        top_mesh_rotation[1] += arm_exist_angle[0] / 2

        self.top_mesh = Ring(arm_thickness[0], arm_radius[0], arm_radius[0] - arm_thickness[1], arm_exist_angle[0], 
                             position = top_mesh_position,
                             rotation = top_mesh_rotation)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        # arm left
        arm_delta_z = arm_radius[0] * np.sin(arm_exist_angle[0] / 2) - arm_radius[0] * np.sin(arm_exist_angle[0] / 2)
        box_length = np.sqrt(arm_delta_z * arm_delta_z + arm_top_bottom_separation[0] * arm_top_bottom_separation[0])
        box_rotation = np.arctan(arm_delta_z / arm_top_bottom_separation[0])

        left_mesh_position_1 = [
            arm_radius[0] * (1 - np.cos(arm_exist_angle[0] / 2)) + arm_top_bottom_separation[0] / 2 + arm_thickness[1] / 2 * np.sin(box_rotation), 
            0,
            -(arm_radius[0] * np.sin(arm_exist_angle[0] / 2) + arm_radius[0] * np.sin(arm_exist_angle[0] / 2)) / 2 + arm_thickness[1] / 2 * np.cos(box_rotation)
        ]
        left_mesh_rotation = [0, -arm_rotation[0], 0]
        left_mesh_position_1 = adjust_position_from_rotation(left_mesh_position_1, left_mesh_rotation)

        left_mesh_position_2 = [
            root_size[0] * np.cos(root_rotation[0]) - arm_offset[0] * np.tan(root_rotation[0]), 
            0,
            root_size[0] * np.sin(root_rotation[0]) + arm_offset[0]
        ]
        left_mesh_position = list_add(left_mesh_position_1, left_mesh_position_2)
        left_mesh_rotation[1] += box_rotation

        self.left_mesh = Cuboid(arm_thickness[0], box_length, arm_thickness[1], 
                                position = left_mesh_position,
                                rotation = left_mesh_rotation)
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        # arm right
        right_exist_angle = np.pi - arm_exist_angle[0]
        right_radius = arm_top_bottom_separation[0] / 2 / np.sin(right_exist_angle / 2)

        right_mesh_position_1 = [
            arm_radius[0] * (1 - np.cos(arm_exist_angle[0] / 2)) + arm_top_bottom_separation[0] / 2, 
            0,
            -right_radius * np.cos(right_exist_angle/ 2) + arm_radius[0] * np.sin(arm_exist_angle[0] / 2)
        ]
        right_mesh_rotation = [0, -arm_rotation[0], 0]
        right_mesh_position_1 = adjust_position_from_rotation(right_mesh_position_1, right_mesh_rotation)

        right_mesh_position_2 = [
            root_size[0] * np.cos(root_rotation[0]) - arm_offset[0] * np.tan(root_rotation[0]), 
            0,
            root_size[0] * np.sin(root_rotation[0]) + arm_offset[0]
        ]
        right_mesh_position = list_add(right_mesh_position_1, right_mesh_position_2)
        right_mesh_rotation[1] += -np.pi / 2 + right_exist_angle / 2

        self.right_mesh = Ring(arm_thickness[0], right_radius, right_radius - arm_thickness[1], right_exist_angle, 
                               position = right_mesh_position,
                               rotation = right_mesh_rotation)
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Scissors/concept_template.py
class Cuboidal_Ring_Handle(ConceptTemplate):
    def __init__(self, root_size, root_rotation, arm_length, arm_thickness, arm_top_bottom_offset, arm_top_bottom_rotation, arm_top_bottom_separation, arm_offset, arm_rotation, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        root_rotation = [x / 180 * np.pi for x in root_rotation]
        arm_top_bottom_rotation = [x / 180 * np.pi for x in arm_top_bottom_rotation]
        arm_rotation = [x / 180 * np.pi for x in arm_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.root_size = root_size
        self.root_rotation = root_rotation
        self.arm_length = arm_length
        self.arm_thickness = arm_thickness
        self.arm_top_bottom_offset = arm_top_bottom_offset
        self.arm_top_bottom_rotation = arm_top_bottom_rotation
        self.arm_top_bottom_separation = arm_top_bottom_separation
        self.arm_offset = arm_offset
        self.arm_rotation = arm_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # root
        root_mesh_position_1 = [
            root_size[0] / 2, 
            0,
            0
        ]
        root_mesh_rotation_1 = [0, -root_rotation[0], 0]
        root_mesh_position = adjust_position_from_rotation(root_mesh_position_1, root_mesh_rotation_1)

        root_mesh_rotation_2 = [np.pi / 2, np.pi / 2, 0]
        root_mesh_rotation = list_add(root_mesh_rotation_1, root_mesh_rotation_2)

        self.root_mesh = Cuboid(root_size[0], root_size[3], root_size[1],
                                root_size[2], root_size[1],
                                position = root_mesh_position,
                                rotation = root_mesh_rotation)
        vertices_list.append(self.root_mesh.vertices)
        faces_list.append(self.root_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.root_mesh.vertices)

        # arm bottom
        bottom_mesh_position_1 = [
            0, 
            0,
            0
        ]
        bottom_mesh_rotation = [0, -arm_rotation[0], 0]
        bottom_mesh_position_1 = adjust_position_from_rotation(bottom_mesh_position_1, bottom_mesh_rotation)

        bottom_mesh_position_2 = [
            root_size[0] * np.cos(root_rotation[0]) - arm_offset[0] * np.tan(root_rotation[0]), 
            0,
            root_size[0] * np.sin(root_rotation[0]) + arm_offset[0]
        ]
        bottom_mesh_position = list_add(bottom_mesh_position_1, bottom_mesh_position_2)
        bottom_mesh_rotation[1] += arm_top_bottom_rotation[1]

        self.bottom_mesh = Cuboid(arm_thickness[0], arm_thickness[1], arm_length[1], 
                                  position = bottom_mesh_position,
                                  rotation = bottom_mesh_rotation)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        # arm top
        top_mesh_position_1 = [
            arm_top_bottom_separation[0], 
            0,
            arm_top_bottom_offset[0]
        ]
        top_mesh_rotation = [0, -arm_rotation[0], 0]
        top_mesh_position_1 = adjust_position_from_rotation(top_mesh_position_1, top_mesh_rotation)

        top_mesh_position_2 = [
            root_size[0] * np.cos(root_rotation[0]) - arm_offset[0] * np.tan(root_rotation[0]), 
            0,
            root_size[0] * np.sin(root_rotation[0]) + arm_offset[0]
        ]
        top_mesh_position = list_add(top_mesh_position_1, top_mesh_position_2)
        top_mesh_rotation[1] += arm_top_bottom_rotation[0]

        self.top_mesh = Cuboid(arm_thickness[0], arm_thickness[1], arm_length[0], 
                               position = top_mesh_position,
                               rotation = top_mesh_rotation)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        # arm left
        left_arm_length_x = arm_top_bottom_separation[0] - arm_length[0] * np.sin(arm_top_bottom_rotation[0]) / 2 + arm_length[1] * np.sin(arm_top_bottom_rotation[1]) / 2
        left_arm_length_z = arm_length[0] * np.cos(arm_top_bottom_rotation[0]) / 2 - arm_length[1] * np.cos(arm_top_bottom_rotation[1]) / 2 - arm_top_bottom_offset[0]
        left_arm_length_t = np.sqrt(left_arm_length_x * left_arm_length_x + left_arm_length_z * left_arm_length_z)
        left_arm_offset_x = (arm_top_bottom_separation[0] - arm_length[0] * np.sin(arm_top_bottom_rotation[0]) / 2 - arm_length[1] * np.sin(arm_top_bottom_rotation[1]) / 2) / 2
        left_arm_offset_z = (arm_top_bottom_offset[0] - arm_length[0] * np.cos(arm_top_bottom_rotation[0]) / 2 - arm_length[1] * np.cos(arm_top_bottom_rotation[1]) / 2) / 2
        left_arm_rotation = np.arctan(left_arm_length_z / left_arm_length_x)

        left_mesh_position_1 = [
            left_arm_offset_x, 
            0,
            left_arm_offset_z
        ]
        left_mesh_rotation = [0, -arm_rotation[0], 0]
        left_mesh_position_1 = adjust_position_from_rotation(left_mesh_position_1, left_mesh_rotation)

        left_mesh_position_2 = [
            root_size[0] * np.cos(root_rotation[0]) - arm_offset[0] * np.tan(root_rotation[0]), 
            0,
            root_size[0] * np.sin(root_rotation[0]) + arm_offset[0]
        ]
        left_mesh_position = list_add(left_mesh_position_1, left_mesh_position_2)
        left_mesh_rotation[1] += left_arm_rotation

        self.left_mesh = Cuboid(arm_thickness[0], left_arm_length_t, arm_thickness[1], 
                                position = left_mesh_position,
                                rotation = left_mesh_rotation)
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        # arm right
        right_arm_length_x = arm_top_bottom_separation[0] + arm_length[0] * np.sin(arm_top_bottom_rotation[0]) / 2 - arm_length[1] * np.sin(arm_top_bottom_rotation[1]) / 2
        right_arm_length_z = arm_length[0] * np.cos(arm_top_bottom_rotation[0]) / 2 - arm_length[1] * np.cos(arm_top_bottom_rotation[1]) / 2 + arm_top_bottom_offset[0]
        right_arm_length_t = np.sqrt(right_arm_length_x * right_arm_length_x + right_arm_length_z * right_arm_length_z)
        right_arm_offset_x = (arm_top_bottom_separation[0] + arm_length[0] * np.sin(arm_top_bottom_rotation[0]) / 2 + arm_length[1] * np.sin(arm_top_bottom_rotation[1]) / 2) / 2
        right_arm_offset_z = (arm_top_bottom_offset[0] + arm_length[0] * np.cos(arm_top_bottom_rotation[0]) / 2 + arm_length[1] * np.cos(arm_top_bottom_rotation[1]) / 2) / 2
        right_arm_rotation = np.arctan(right_arm_length_z / right_arm_length_x)

        right_mesh_position_1 = [
            right_arm_offset_x, 
            0,
            right_arm_offset_z
        ]
        right_mesh_rotation = [0, -arm_rotation[0], 0]
        right_mesh_position_1 = adjust_position_from_rotation(right_mesh_position_1, right_mesh_rotation)

        right_mesh_position_2 = [
            root_size[0] * np.cos(root_rotation[0]) - arm_offset[0] * np.tan(root_rotation[0]), 
            0,
            root_size[0] * np.sin(root_rotation[0]) + arm_offset[0]
        ]
        right_mesh_position = list_add(right_mesh_position_1, right_mesh_position_2)
        right_mesh_rotation[1] += -right_arm_rotation

        self.right_mesh = Cuboid(arm_thickness[0], right_arm_length_t, arm_thickness[1], 
                                 position = right_mesh_position,
                                 rotation = right_mesh_rotation)
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Scissors/concept_template.py
class Cuboidal_Handle(ConceptTemplate):
    def __init__(self, root_size, root_rotation, arm_size, arm_offset, arm_rotation, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        root_rotation = [x / 180 * np.pi for x in root_rotation]
        arm_rotation = [x / 180 * np.pi for x in arm_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.root_size = root_size
        self.root_rotation = root_rotation
        self.arm_size = arm_size
        self.arm_offset = arm_offset
        self.arm_rotation = arm_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # root
        root_mesh_position_1 = [
            root_size[0] / 2, 
            0,
            0
        ]
        root_mesh_rotation_1 = [0, -root_rotation[0], 0]
        root_mesh_position = adjust_position_from_rotation(root_mesh_position_1, root_mesh_rotation_1)

        root_mesh_rotation_2 = [np.pi / 2, np.pi / 2, 0]
        root_mesh_rotation = list_add(root_mesh_rotation_1, root_mesh_rotation_2)

        self.root_mesh = Cuboid(root_size[0], root_size[3], root_size[1],
                                root_size[2], root_size[1],
                                position = root_mesh_position,
                                rotation = root_mesh_rotation)
        vertices_list.append(self.root_mesh.vertices)
        faces_list.append(self.root_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.root_mesh.vertices)

        # arm
        arm_mesh_position_1 = [
            arm_size[0] / 2, 
            0,
            0
        ]
        arm_mesh_rotation = [0, -arm_rotation[0], 0]
        arm_mesh_position_1 = adjust_position_from_rotation(arm_mesh_position_1, arm_mesh_rotation)

        arm_mesh_position_2 = [
            root_size[0] * np.cos(root_rotation[0]) - arm_offset[0] * np.tan(root_rotation[0]), 
            0,
            root_size[0] * np.sin(root_rotation[0]) + arm_offset[0]
        ]
        arm_mesh_position = list_add(arm_mesh_position_1, arm_mesh_position_2)

        self.arm_mesh = Cuboid(arm_size[1], arm_size[0], arm_size[2],
                               position = arm_mesh_position,
                               rotation = arm_mesh_rotation)
        vertices_list.append(self.arm_mesh.vertices)
        faces_list.append(self.arm_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.arm_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Refrigerator/concept_template.py
class Cuboidal_Handle(ConceptTemplate):
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
            0,
            size[2] / 2
        ]
        self.mesh = Cuboid(size[1], size[0], size[2],
                             position = mesh_position)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="ZXY")

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Refrigerator/concept_template.py
class Trifold_Handle(ConceptTemplate):
    def __init__(self, mounting_size, mounting_seperation, grip_size, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.mounting_size = mounting_size
        self.mounting_seperation = mounting_seperation
        self.grip_size = grip_size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        top_mesh_position = [
            0, 
            mounting_seperation[0] / 2, 
            mounting_size[2] / 2
        ]
        self.top_mesh = Cuboid(mounting_size[1], mounting_size[0], mounting_size[2], 
                               position = top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [
            0, 
            -mounting_seperation[0] / 2, 
            mounting_size[2] / 2
        ]
        self.bottom_mesh = Cuboid(mounting_size[1], mounting_size[0], mounting_size[2], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        vertical_mesh_position = [
            0, 
            0,
            mounting_size[2] + grip_size[2] / 2
        ]
        self.vertical_mesh = Cuboid(grip_size[1], grip_size[0], grip_size[2], 
                                    position = vertical_mesh_position)
        vertices_list.append(self.vertical_mesh.vertices)
        faces_list.append(self.vertical_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.vertical_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="ZXY")

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Refrigerator/concept_template.py
class Trifold_Curve_Handle(ConceptTemplate):
    def __init__(self, mounting_size, mounting_seperation, curve_size, curve_exist_angle, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        curve_exist_angle = [x / 180 * np.pi for x in curve_exist_angle]
        super().__init__(position, rotation)

        # Record Parameters
        self.mounting_size = mounting_size
        self.mounting_seperation = mounting_seperation
        self.curve_size = curve_size
        self.curve_exist_angle = curve_exist_angle

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        top_mesh_position = [
            0, 
            mounting_seperation[0] / 2, 
            mounting_size[2] / 2
        ]
        self.top_mesh = Cuboid(mounting_size[1], mounting_size[0], mounting_size[2], 
                               position = top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [
            0, 
            -mounting_seperation[0] / 2, 
            mounting_size[2] / 2
        ]
        self.bottom_mesh = Cuboid(mounting_size[1], mounting_size[0], mounting_size[2], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        curve_z_offset = mounting_size[2] - np.sqrt(curve_size[1] * curve_size[1] - (mounting_seperation[0] / 2) * (mounting_seperation[0] / 2))
        vertical_mesh_position = [
            0, 
            0,
            curve_z_offset
        ]
        vertical_mesh_rotation = [
            0, 
            -np.pi / 2 + curve_exist_angle[0] / 2,
            np.pi / 2
        ]
        self.vertical_mesh = Ring(curve_size[2], curve_size[0], curve_size[1], curve_exist_angle[0],
                                  position = vertical_mesh_position,
                                  rotation = vertical_mesh_rotation)
        vertices_list.append(self.vertical_mesh.vertices)
        faces_list.append(self.vertical_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.vertical_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="ZXY")

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Refrigerator/concept_template.py
class Curve_Handle(ConceptTemplate):
    def __init__(self, curve_size, curve_exist_angle, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        curve_exist_angle = [x / 180 * np.pi for x in curve_exist_angle]
        super().__init__(position, rotation)

        # Record Parameters
        self.curve_size = curve_size
        self.curve_exist_angle = curve_exist_angle

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        vertical_mesh_position = [
            0, 
            0,
            -curve_size[0] * np.cos(curve_exist_angle[0] / 2)
        ]
        vertical_mesh_rotation = [
            0, 
            -np.pi / 2 + curve_exist_angle[0] / 2,
            np.pi / 2
        ]
        self.vertical_mesh = Ring(curve_size[2], curve_size[0], curve_size[1], curve_exist_angle[0],
                                  position = vertical_mesh_position,
                                  rotation = vertical_mesh_rotation)
        vertices_list.append(self.vertical_mesh.vertices)
        faces_list.append(self.vertical_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.vertical_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="ZXY")

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Shaver/concept_template.py
class Regular_Body(ConceptTemplate):
    def __init__(self, bottom_size, middle_size, top_size, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.bottom_size = bottom_size
        self.middle_size = middle_size
        self.top_size = top_size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        base_mesh_position = [0, (top_size[0] - bottom_size[1]) / 2, 0]
        base_mesh_rotation = [0, 0, -np.pi / 2]
        self.base_mesh = Rectangular_Ring(
            bottom_size[0],
            top_size[0] + middle_size[0] + bottom_size[1],
            bottom_size[2],
            middle_size[0],
            bottom_size[2] - middle_size[1] * 2,
            inner_offset=[(top_size[0] - bottom_size[1]) / 2, 0],
            top_bottom_offset=[0, 0],
            position=base_mesh_position,
            rotation=base_mesh_rotation,
        )
        vertices_list.append(self.base_mesh.vertices)
        faces_list.append(self.base_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.base_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Pliers/concept_template.py
class Straight_Handle(ConceptTemplate):
    def __init__(self, front_size, behind_size, handle_separation, handle_rotation, front_behind_offset, left_right_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        handle_rotation = [x / 180 * np.pi for x in handle_rotation]
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.front_size = front_size
        self.behind_size = behind_size
        self.handle_separation = handle_separation
        self.handle_rotation = handle_rotation
        self.front_behind_offset = front_behind_offset
        self.left_right_offset = left_right_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # front_left
        front_1_mesh_position_1 = [
            0, 
            0,
            -front_size[2] / 2
        ]
        front_1_mesh_rotation = [0, -handle_rotation[0], 0]
        front_1_mesh_position_1 = adjust_position_from_rotation(front_1_mesh_position_1, front_1_mesh_rotation)

        front_1_mesh_position_2 = [
            handle_separation[0] / 2, 
            0,
            0
        ]
        front_1_mesh_position = list_add(front_1_mesh_position_1, front_1_mesh_position_2)

        self.front_1_mesh = Cuboid(front_size[1], front_size[0], front_size[2],
                                   position = front_1_mesh_position,
                                   rotation = front_1_mesh_rotation)
        vertices_list.append(self.front_1_mesh.vertices)
        faces_list.append(self.front_1_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.front_1_mesh.vertices)

        # behind_left
        behind_1_mesh_position_1 = [
            -behind_size[0] / 2, 
            0,
            -behind_size[2] / 2
        ]
        behind_1_mesh_rotation = [0, -handle_rotation[1], 0]
        behind_1_mesh_position_1 = adjust_position_from_rotation(behind_1_mesh_position_1, behind_1_mesh_rotation)

        behind_1_mesh_position_2 = [
            handle_separation[0] / 2 + front_size[0] / 2 * np.cos(handle_rotation[0]) + front_size[2] * np.sin(handle_rotation[0]) + front_behind_offset[0], 
            front_behind_offset[1],
            -front_size[2] * np.cos(handle_rotation[0]) + front_size[0] / 2 * np.sin(handle_rotation[0])
        ]
        behind_1_mesh_position = list_add(behind_1_mesh_position_1, behind_1_mesh_position_2)

        self.behind_1_mesh = Cuboid(behind_size[1], behind_size[0], behind_size[2],
                                    position = behind_1_mesh_position,
                                    rotation = behind_1_mesh_rotation)
        vertices_list.append(self.behind_1_mesh.vertices)
        faces_list.append(self.behind_1_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.behind_1_mesh.vertices)

        # front_right
        front_2_mesh_position_1 = [
            0, 
            0,
            -front_size[2] / 2
        ]
        front_2_mesh_rotation = [0, handle_rotation[0], 0]
        front_2_mesh_position_1 = adjust_position_from_rotation(front_2_mesh_position_1, front_2_mesh_rotation)

        front_2_mesh_position_2 = [
            -handle_separation[0] / 2, 
            left_right_offset[0],
            0
        ]
        front_2_mesh_position = list_add(front_2_mesh_position_1, front_2_mesh_position_2)

        self.front_2_mesh = Cuboid(front_size[1], front_size[0], front_size[2],
                                   position = front_2_mesh_position,
                                   rotation = front_2_mesh_rotation)
        vertices_list.append(self.front_2_mesh.vertices)
        faces_list.append(self.front_2_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.front_2_mesh.vertices)

        # behind_right
        behind_2_mesh_position_1 = [
            behind_size[0] / 2, 
            0,
            -behind_size[2] / 2
        ]
        behind_2_mesh_rotation = [0, handle_rotation[1], 0]
        behind_2_mesh_position_1 = adjust_position_from_rotation(behind_2_mesh_position_1, behind_2_mesh_rotation)

        behind_2_mesh_position_2 = [
            -handle_separation[0] / 2 - front_size[0] / 2 * np.cos(handle_rotation[0]) - front_size[2] * np.sin(handle_rotation[0]) - front_behind_offset[0], 
            front_behind_offset[1] + left_right_offset[0],
            -front_size[2] * np.cos(handle_rotation[0]) + front_size[0] / 2 * np.sin(handle_rotation[0])
        ]
        behind_2_mesh_position = list_add(behind_2_mesh_position_1, behind_2_mesh_position_2)

        self.behind_2_mesh = Cuboid(behind_size[1], behind_size[0], behind_size[2],
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

        self.semantic = 'Handle'


# Source: Pliers/concept_template.py
class Rear_Curved_Handle(ConceptTemplate):
    def __init__(self, front_size, behind_size, exist_angle, handle_separation, handle_rotation, front_behind_offset, left_right_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        exist_angle = [x / 180 * np.pi for x in exist_angle]
        handle_rotation = [x / 180 * np.pi for x in handle_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.front_size = front_size
        self.behind_size = behind_size
        self.exist_angle = exist_angle
        self.handle_separation = handle_separation
        self.handle_rotation = handle_rotation
        self.front_behind_offset = front_behind_offset
        self.left_right_offset = left_right_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # front_left
        front_1_mesh_position_1 = [
            0, 
            0,
            -front_size[2] / 2
        ]
        front_1_mesh_rotation = [0, -handle_rotation[0], 0]
        front_1_mesh_position_1 = adjust_position_from_rotation(front_1_mesh_position_1, front_1_mesh_rotation)

        front_1_mesh_position_2 = [
            handle_separation[0] / 2, 
            0,
            0
        ]
        front_1_mesh_position = list_add(front_1_mesh_position_1, front_1_mesh_position_2)

        self.front_1_mesh = Cuboid(front_size[1], front_size[0], front_size[2],
                                   position = front_1_mesh_position,
                                   rotation = front_1_mesh_rotation)
        vertices_list.append(self.front_1_mesh.vertices)
        faces_list.append(self.front_1_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.front_1_mesh.vertices)

        # behind_left
        behind_1_mesh_rotation_1 = [0, np.pi, np.pi]
        behind_1_mesh_position_1 = [
            -behind_size[1], 
            0,
            0
        ]
        behind_1_mesh_rotation_2 = [0, -handle_rotation[1], 0]
        behind_1_mesh_rotation_2_reverse = [0, handle_rotation[1], 0]
        behind_1_mesh_position_1 = adjust_position_from_rotation(behind_1_mesh_position_1, behind_1_mesh_rotation_2)

        behind_1_mesh_position_2 = [
            handle_separation[0] / 2 - front_size[0] / 2 * np.cos(handle_rotation[0]) + front_size[2] * np.sin(handle_rotation[0]) + front_behind_offset[0], 
            front_behind_offset[1],
            -front_size[2] * np.cos(handle_rotation[0]) + front_size[0] / 2 * np.sin(handle_rotation[0])
        ]
        behind_1_mesh_position = list_add(behind_1_mesh_position_1, behind_1_mesh_position_2)
        behind_1_mesh_rotation = list_add(behind_1_mesh_rotation_1, behind_1_mesh_rotation_2_reverse)

        self.behind_1_mesh = Ring(behind_size[2], behind_size[0], behind_size[1], exist_angle[0],
                                  position = behind_1_mesh_position,
                                  rotation = behind_1_mesh_rotation)
        vertices_list.append(self.behind_1_mesh.vertices)
        faces_list.append(self.behind_1_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.behind_1_mesh.vertices)

        # front_right
        front_2_mesh_position_1 = [
            0, 
            0,
            -front_size[2] / 2
        ]
        front_2_mesh_rotation = [0, handle_rotation[0], 0]
        front_2_mesh_position_1 = adjust_position_from_rotation(front_2_mesh_position_1, front_2_mesh_rotation)

        front_2_mesh_position_2 = [
            -handle_separation[0] / 2, 
            left_right_offset[0],
            0
        ]
        front_2_mesh_position = list_add(front_2_mesh_position_1, front_2_mesh_position_2)

        self.front_2_mesh = Cuboid(front_size[1], front_size[0], front_size[2],
                                   position = front_2_mesh_position,
                                   rotation = front_2_mesh_rotation)
        vertices_list.append(self.front_2_mesh.vertices)
        faces_list.append(self.front_2_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.front_2_mesh.vertices)

        # behind_right
        behind_2_mesh_rotation_1 = [0, np.pi, 0]
        behind_2_mesh_position_1 = [
            behind_size[1], 
            0,
            0
        ]
        behind_2_mesh_rotation_2 = [0, handle_rotation[1], 0]
        behind_2_mesh_position_1 = adjust_position_from_rotation(behind_2_mesh_position_1, behind_2_mesh_rotation_2)

        behind_2_mesh_position_2 = [
            -handle_separation[0] / 2 + front_size[0] / 2 * np.cos(handle_rotation[0]) - front_size[2] * np.sin(handle_rotation[0]) - front_behind_offset[0], 
            front_behind_offset[1],
            -front_size[2] * np.cos(handle_rotation[0]) + front_size[0] / 2 * np.sin(handle_rotation[0])
        ]
        behind_2_mesh_position = list_add(behind_2_mesh_position_1, behind_2_mesh_position_2)
        behind_2_mesh_rotation = list_add(behind_2_mesh_rotation_1, behind_2_mesh_rotation_2)

        self.behind_2_mesh = Ring(behind_size[2], behind_size[0], behind_size[1], exist_angle[0],
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

        self.semantic = 'Handle'


# Source: Pliers/concept_template.py
class Middle_Curved_Handle(ConceptTemplate):
    def __init__(self, front_size, middle_size, exist_angle, behind_size, handle_separation, handle_rotation, front_middle_offset, middle_behind_offset, left_right_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        exist_angle = [x / 180 * np.pi for x in exist_angle]
        handle_rotation = [x / 180 * np.pi for x in handle_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.front_size = front_size
        self.middle_size = middle_size
        self.exist_angle = exist_angle
        self.behind_size = behind_size
        self.handle_separation = handle_separation
        self.handle_rotation = handle_rotation
        self.front_middle_offset = front_middle_offset
        self.middle_behind_offset = middle_behind_offset
        self.left_right_offset = left_right_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # front_left
        front_1_mesh_position_1 = [
            0, 
            0,
            -front_size[2] / 2
        ]
        front_1_mesh_rotation = [0, -handle_rotation[0], 0]
        front_1_mesh_position_1 = adjust_position_from_rotation(front_1_mesh_position_1, front_1_mesh_rotation)

        front_1_mesh_position_2 = [
            handle_separation[0] / 2, 
            0,
            0
        ]
        front_1_mesh_position = list_add(front_1_mesh_position_1, front_1_mesh_position_2)

        self.front_1_mesh = Cuboid(front_size[1], front_size[0], front_size[2],
                                   position = front_1_mesh_position,
                                   rotation = front_1_mesh_rotation)
        vertices_list.append(self.front_1_mesh.vertices)
        faces_list.append(self.front_1_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.front_1_mesh.vertices)

        # middle_left
        middle_1_mesh_rotation_1 = [0, np.pi, np.pi]
        middle_1_mesh_position_1 = [
            -middle_size[1], 
            0,
            0
        ]
        middle_1_mesh_rotation_2 = [0, -handle_rotation[1], 0]
        middle_1_mesh_rotation_2_reverse = [0, handle_rotation[1], 0]
        middle_1_mesh_position_1 = adjust_position_from_rotation(middle_1_mesh_position_1, middle_1_mesh_rotation_2)

        middle_1_mesh_position_2 = [
            handle_separation[0] / 2 - front_size[0] / 2 * np.cos(handle_rotation[0]) + front_size[2] * np.sin(handle_rotation[0]) + front_middle_offset[0], 
            front_middle_offset[1],
            -front_size[2] * np.cos(handle_rotation[0]) + front_size[0] / 2 * np.sin(handle_rotation[0])
        ]
        middle_1_mesh_position = list_add(middle_1_mesh_position_1, middle_1_mesh_position_2)
        middle_1_mesh_rotation = list_add(middle_1_mesh_rotation_1, middle_1_mesh_rotation_2_reverse)

        self.middle_1_mesh = Ring(middle_size[2], middle_size[0], middle_size[1], exist_angle[0],
                                  position = middle_1_mesh_position,
                                  rotation = middle_1_mesh_rotation)
        vertices_list.append(self.middle_1_mesh.vertices)
        faces_list.append(self.middle_1_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.middle_1_mesh.vertices)

        # behind_left
        behind_1_mesh_position_1 = [
            behind_size[0] / 2, 
            0,
            -behind_size[2] / 2
        ]
        behind_1_mesh_rotation = [0, -handle_rotation[2], 0]
        behind_1_mesh_position_1 = adjust_position_from_rotation(behind_1_mesh_position_1, behind_1_mesh_rotation)

        curve_offset_x = middle_size[1] * (1 - np.cos(exist_angle))
        curve_offset_z = middle_size[1] * np.sin(exist_angle)
        middle_offset_x  = curve_offset_x * np.cos(handle_rotation[1]) - curve_offset_z * np.sin(handle_rotation[1])
        middle_offset_z  = curve_offset_x * np.sin(handle_rotation[1]) + curve_offset_z * np.cos(handle_rotation[1])
        behind_1_mesh_position_2 = [
            handle_separation[0] / 2 - front_size[0] / 2 * np.cos(handle_rotation[0]) + front_size[2] * np.sin(handle_rotation[0]) - middle_offset_x + front_middle_offset[0] + middle_behind_offset[0], 
            front_middle_offset[1] + middle_behind_offset[1],
            -front_size[2] * np.cos(handle_rotation[0]) + front_size[0] / 2 * np.sin(handle_rotation[0]) - middle_offset_z
        ]
        behind_1_mesh_position = list_add(behind_1_mesh_position_1, behind_1_mesh_position_2)

        self.behind_1_mesh = Cuboid(behind_size[1], behind_size[0], behind_size[2],
                                    position = behind_1_mesh_position,
                                    rotation = behind_1_mesh_rotation)
        vertices_list.append(self.behind_1_mesh.vertices)
        faces_list.append(self.behind_1_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.behind_1_mesh.vertices)

        # front_right
        front_2_mesh_position_1 = [
            0, 
            0,
            -front_size[2] / 2
        ]
        front_2_mesh_rotation = [0, handle_rotation[0], 0]
        front_2_mesh_position_1 = adjust_position_from_rotation(front_2_mesh_position_1, front_2_mesh_rotation)

        front_2_mesh_position_2 = [
            -handle_separation[0] / 2, 
            left_right_offset[0],
            0
        ]
        front_2_mesh_position = list_add(front_2_mesh_position_1, front_2_mesh_position_2)

        self.front_2_mesh = Cuboid(front_size[1], front_size[0], front_size[2],
                                   position = front_2_mesh_position,
                                   rotation = front_2_mesh_rotation)
        vertices_list.append(self.front_2_mesh.vertices)
        faces_list.append(self.front_2_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.front_2_mesh.vertices)

        # middle_right
        middle_2_mesh_rotation_1 = [0, np.pi, 0]
        middle_2_mesh_position_1 = [
            middle_size[1], 
            0,
            0
        ]
        middle_2_mesh_rotation_2 = [0, handle_rotation[1], 0]
        middle_2_mesh_position_1 = adjust_position_from_rotation(middle_2_mesh_position_1, middle_2_mesh_rotation_2)

        middle_2_mesh_position_2 = [
            -handle_separation[0] / 2 + front_size[0] / 2 * np.cos(handle_rotation[0]) - front_size[2] * np.sin(handle_rotation[0]) - front_middle_offset[0], 
            front_middle_offset[1],
            -front_size[2] * np.cos(handle_rotation[0]) + front_size[0] / 2 * np.sin(handle_rotation[0])
        ]
        middle_2_mesh_position = list_add(middle_2_mesh_position_1, middle_2_mesh_position_2)
        middle_2_mesh_rotation = list_add(middle_2_mesh_rotation_1, middle_2_mesh_rotation_2)

        self.middle_2_mesh = Ring(middle_size[2], middle_size[0], middle_size[1], exist_angle[0],
                                  position = middle_2_mesh_position,
                                  rotation = middle_2_mesh_rotation)
        vertices_list.append(self.middle_2_mesh.vertices)
        faces_list.append(self.middle_2_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.middle_2_mesh.vertices)

        # behind_right
        behind_2_mesh_position_1 = [
            -behind_size[0] / 2, 
            0,
            -behind_size[2] / 2
        ]
        behind_2_mesh_rotation = [0, handle_rotation[2], 0]
        behind_2_mesh_position_1 = adjust_position_from_rotation(behind_2_mesh_position_1, behind_2_mesh_rotation)

        curve_offset_x = middle_size[1] * (1 - np.cos(exist_angle))
        curve_offset_z = middle_size[1] * np.sin(exist_angle)
        middle_offset_x  = curve_offset_x * np.cos(handle_rotation[1]) - curve_offset_z * np.sin(handle_rotation[1])
        middle_offset_z  = curve_offset_x * np.sin(handle_rotation[1]) + curve_offset_z * np.cos(handle_rotation[1])
        behind_2_mesh_position_2 = [
            -handle_separation[0] / 2 + front_size[0] / 2 * np.cos(handle_rotation[0]) - front_size[2] * np.sin(handle_rotation[0]) + middle_offset_x - front_middle_offset[0] - middle_behind_offset[0], 
            front_middle_offset[1] + middle_behind_offset[1] + left_right_offset[0],
            -front_size[2] * np.cos(handle_rotation[0]) + front_size[0] / 2 * np.sin(handle_rotation[0]) - middle_offset_z
        ]
        behind_2_mesh_position = list_add(behind_2_mesh_position_1, behind_2_mesh_position_2)

        self.behind_2_mesh = Cuboid(behind_size[1], behind_size[0], behind_size[2],
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

        self.semantic = 'Handle'


# Source: Pliers/concept_template.py
class Asymmetric_Straight_Handle(ConceptTemplate):
    def __init__(self, left_front_size, left_behind_size, left_handle_rotation, left_front_behind_offset, right_front_size, right_behind_size, right_handle_rotation, right_front_behind_offset, handle_separation, left_right_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        left_handle_rotation = [x / 180 * np.pi for x in left_handle_rotation]
        right_handle_rotation = [x / 180 * np.pi for x in right_handle_rotation]
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.left_front_size = left_front_size
        self.left_behind_size = left_behind_size
        self.left_handle_rotation = left_handle_rotation
        self.left_front_behind_offset = left_front_behind_offset
        self.right_front_size = right_front_size
        self.right_behind_size = right_behind_size
        self.right_handle_rotation = right_handle_rotation
        self.right_front_behind_offset = right_front_behind_offset
        self.handle_separation = handle_separation
        self.left_right_offset = left_right_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # front_left
        front_1_mesh_position_1 = [
            0, 
            0,
            -left_front_size[2] / 2
        ]
        front_1_mesh_rotation = [0, left_handle_rotation[0], 0]
        front_1_mesh_position_1 = adjust_position_from_rotation(front_1_mesh_position_1, front_1_mesh_rotation)

        front_1_mesh_position_2 = [
            -handle_separation[0] / 2, 
            0,
            0
        ]
        front_1_mesh_position = list_add(front_1_mesh_position_1, front_1_mesh_position_2)

        self.front_1_mesh = Cuboid(left_front_size[1], left_front_size[0], left_front_size[2],
                                   position = front_1_mesh_position,
                                   rotation = front_1_mesh_rotation)
        vertices_list.append(self.front_1_mesh.vertices)
        faces_list.append(self.front_1_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.front_1_mesh.vertices)

        # behind_left
        behind_1_mesh_position_1 = [
            left_behind_size[0] / 2, 
            0,
            -left_behind_size[2] / 2
        ]
        behind_1_mesh_rotation = [0, left_handle_rotation[1], 0]
        behind_1_mesh_position_1 = adjust_position_from_rotation(behind_1_mesh_position_1, behind_1_mesh_rotation)

        behind_1_mesh_position_2 = [
            -handle_separation[0] / 2 - left_front_size[0] / 2 * np.cos(left_handle_rotation[0]) - left_front_size[2] * np.sin(left_handle_rotation[0]) - left_front_behind_offset[0], 
            left_front_behind_offset[1],
            -left_front_size[2] * np.cos(left_handle_rotation[0]) + left_front_size[0] / 2 * np.sin(left_handle_rotation[0])
        ]
        behind_1_mesh_position = list_add(behind_1_mesh_position_1, behind_1_mesh_position_2)

        self.behind_1_mesh = Cuboid(left_behind_size[1], left_behind_size[0], left_behind_size[2],
                                    position = behind_1_mesh_position,
                                    rotation = behind_1_mesh_rotation)
        vertices_list.append(self.behind_1_mesh.vertices)
        faces_list.append(self.behind_1_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.behind_1_mesh.vertices)

        # front_right
        front_2_mesh_position_1 = [
            0, 
            0,
            -right_front_size[2] / 2
        ]
        front_2_mesh_rotation = [0, -right_handle_rotation[0], 0]
        front_2_mesh_position_1 = adjust_position_from_rotation(front_2_mesh_position_1, front_2_mesh_rotation)

        front_2_mesh_position_2 = [
            handle_separation[0] / 2, 
            left_right_offset[0],
            0
        ]
        front_2_mesh_position = list_add(front_2_mesh_position_1, front_2_mesh_position_2)

        self.front_2_mesh = Cuboid(right_front_size[1], right_front_size[0], right_front_size[2],
                                   position = front_2_mesh_position,
                                   rotation = front_2_mesh_rotation)
        vertices_list.append(self.front_2_mesh.vertices)
        faces_list.append(self.front_2_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.front_2_mesh.vertices)

        # behind_right
        behind_2_mesh_position_1 = [
            -right_behind_size[0] / 2, 
            0,
            -right_behind_size[2] / 2
        ]
        behind_2_mesh_rotation = [0, -right_handle_rotation[1], 0]
        behind_2_mesh_position_1 = adjust_position_from_rotation(behind_2_mesh_position_1, behind_2_mesh_rotation)

        behind_2_mesh_position_2 = [
            handle_separation[0] / 2 + right_front_size[0] / 2 * np.cos(right_handle_rotation[0]) + right_front_size[2] * np.sin(right_handle_rotation[0]) + right_front_behind_offset[0], 
            right_front_behind_offset[1] + left_right_offset[0],
            -right_front_size[2] * np.cos(right_handle_rotation[0]) + right_front_size[0] / 2 * np.sin(right_handle_rotation[0])
        ]
        behind_2_mesh_position = list_add(behind_2_mesh_position_1, behind_2_mesh_position_2)

        self.behind_2_mesh = Cuboid(right_behind_size[1], right_behind_size[0], right_behind_size[2],
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

        self.semantic = 'Handle'


# Source: Door/concept_template.py
class LShape_Handle(ConceptTemplate):
    def __init__(self, existence_of_door, door_rotation, door_size, existence_of_handle, fixed_part_size, vertical_movable_size, horizontal_movable_size, interpiece_offset, offset_x, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        door_rotation = [x / 180 * np.pi for x in door_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.existence_of_handle = existence_of_handle
        self.door_size = door_size
        self.existence_of_door = existence_of_door
        self.door_rotation = door_rotation
        self.fixed_part_size = fixed_part_size
        self.vertical_movable_size = vertical_movable_size
        self.horizontal_movable_size = horizontal_movable_size
        self.interpiece_offset = interpiece_offset
        self.offset_x = offset_x

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.direction_settings = []

        double_door = 0
        if existence_of_door[0] and existence_of_door[1]:
            double_door = 1

        # parameter calculate
        for door in [0, 1]:
            if not existence_of_door[door]:
                continue
            for handle in [0, 1]:
                if not existence_of_handle[handle]:
                    continue
                # right_door(x+)
                if door:
                    handle_y_rotation = door_rotation[1]
                    handle_x_direction = 1
                    handle_y_axis = door_size[0] / 2
                # left_door(x-)
                else:
                    handle_y_rotation = -door_rotation[0]
                    handle_x_direction = -1
                    handle_y_axis = -door_size[0] / 2
                # front_handle(z+)
                if handle:
                    handle_z_direction = 1
                # back_handle(z-)
                else:
                    handle_z_direction = -1
                if double_door:
                    handle_x_position = handle_y_axis
                    handle_y_axis *= 2
                else:
                    handle_x_position = 0
                self.direction_settings.append(
                    {
                        "handle_x_direction": handle_x_direction,
                        "handle_x_position": handle_x_position,
                        "handle_z_direction": handle_z_direction,
                        "handle_y_axis": handle_y_axis,
                        "handle_y_rotation": handle_y_rotation,
                    }
                )

        # meshes definition
        for direction_setting in self.direction_settings:
            tmp_meshes = []

            base_mesh_position = [
                -direction_setting["handle_x_direction"] * offset_x[0] + direction_setting["handle_x_position"],
                0,
                direction_setting["handle_z_direction"] * (door_size[2] / 2 + fixed_part_size[2] / 2),
            ]
            self.base_mesh = Cuboid(fixed_part_size[1], fixed_part_size[0], fixed_part_size[2],
                               position=base_mesh_position)
            tmp_meshes.append(self.base_mesh)

            middle_mesh_position = [
                direction_setting["handle_x_position"] + interpiece_offset[0] - direction_setting["handle_x_direction"] * offset_x[0],
                interpiece_offset[1],
                direction_setting["handle_z_direction"] * (door_size[2] / 2 + fixed_part_size[2] + vertical_movable_size[2] / 2)
            ]
            self.middle_mesh = Cuboid(vertical_movable_size[1], vertical_movable_size[0], vertical_movable_size[2],
                                 position=middle_mesh_position)
            tmp_meshes.append(self.middle_mesh)

            top_mesh_position = [
                direction_setting["handle_x_position"]
                + interpiece_offset[0]
                + direction_setting["handle_x_direction"]
                * (
                    -offset_x[0]
                    + (horizontal_movable_size[0] - vertical_movable_size[0]) / 2
                ),
                interpiece_offset[1],
                direction_setting["handle_z_direction"]
                * (
                door_size[2] / 2
                    + fixed_part_size[2]
                    + vertical_movable_size[2]
                    + horizontal_movable_size[2] / 2
                ),
            ]
            self.top_mesh = Cuboid(horizontal_movable_size[1], horizontal_movable_size[0], horizontal_movable_size[2],
                              position=top_mesh_position)
            tmp_meshes.append(self.top_mesh)

            for tmp_mesh in tmp_meshes:
                tmp_mesh.vertices = apply_transformation(tmp_mesh.vertices, [-direction_setting["handle_y_axis"], 0, 0], [0, 0, 0])
                tmp_mesh.vertices = apply_transformation(tmp_mesh.vertices, [direction_setting["handle_y_axis"], 0, 0], [0, direction_setting["handle_y_rotation"], 0])
                vertices_list.append(tmp_mesh.vertices)
                faces_list.append(tmp_mesh.faces + total_num_vertices)
                total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Door/concept_template.py
class PiShape_Handle(ConceptTemplate):
    def __init__(self, existence_of_door, door_rotation, door_size, existence_of_handle, main_size, sub_size, separation, interpiece_offset, offset_x, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        door_rotation = [x / 180 * np.pi for x in door_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.existence_of_handle = existence_of_handle
        self.door_size = door_size
        self.existence_of_door = existence_of_door
        self.door_rotation = door_rotation
        self.main_size = main_size
        self.sub_size = sub_size
        self.separation = separation
        self.interpiece_offset = interpiece_offset
        self.offset_x = offset_x

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.direction_settings = []
        double_door = 0
        if existence_of_door[0] and existence_of_door[1]:
            double_door = 1

        # parameter calculate
        for door in [0, 1]:
            if not existence_of_door[door]:
                continue
            for handle in [0, 1]:
                if not existence_of_handle[handle]:
                    continue
                # right_door(x+)
                if door:
                    handle_y_rotation = door_rotation[1]
                    handle_x_direction = 1
                    handle_y_axis = door_size[0] / 2
                # left_door(x-)
                else:
                    handle_y_rotation = -door_rotation[0]
                    handle_x_direction = -1
                    handle_y_axis = -door_size[0] / 2
                # front_handle(z+)
                if handle:
                    handle_z_direction = -1
                # back_handle(z-)
                else:
                    handle_z_direction = 1
                if double_door:
                    handle_x_position = handle_y_axis
                    handle_y_axis *= 2
                else:
                    handle_x_position = 0
                self.direction_settings.append(
                    {
                        "handle_x_direction": handle_x_direction,
                        "handle_x_position": handle_x_position,
                        "handle_z_direction": handle_z_direction,
                        "handle_y_axis": handle_y_axis,
                        "handle_y_rotation": handle_y_rotation,
                    }
                )

        # meshes definition
        for direction_setting in self.direction_settings:
            tmp_meshes = []

            top_mesh_position = [
                direction_setting["handle_x_direction"] * offset_x[0] + direction_setting["handle_x_position"],
                separation[0] + sub_size[1],
                direction_setting["handle_z_direction"] * (door_size[2] / 2 + sub_size[2] / 2),
            ]
            self.top_mesh = Cuboid(sub_size[1], sub_size[0], sub_size[2],
                              position=top_mesh_position)
            tmp_meshes.append(self.top_mesh)

            bottom_mesh_position = [
                direction_setting["handle_x_direction"] * offset_x[0] + direction_setting["handle_x_position"],
                0,
                direction_setting["handle_z_direction"] * (door_size[2] / 2 + sub_size[2] / 2),
            ]
            self.bottom_mesh = Cuboid(sub_size[1], sub_size[0], sub_size[2],
                                 position=bottom_mesh_position)
            tmp_meshes.append(self.bottom_mesh)

            main_mesh_position = [
                direction_setting["handle_x_direction"] * offset_x[0] + direction_setting["handle_x_position"],
                interpiece_offset[0] + separation[0] / 2 + sub_size[1] / 2,
                direction_setting["handle_z_direction"] * (door_size[2] / 2 + sub_size[2] + main_size[2] / 2),
            ]
            self.main_mesh = Cuboid(main_size[1], main_size[0], main_size[2],
                               position=main_mesh_position)
            tmp_meshes.append(self.main_mesh)

            for tmp_mesh in tmp_meshes:
                tmp_mesh.vertices = apply_transformation(tmp_mesh.vertices, [-direction_setting["handle_y_axis"], 0, 0], [0, 0, 0])
                tmp_mesh.vertices = apply_transformation(tmp_mesh.vertices, [direction_setting["handle_y_axis"], 0, 0], [0, direction_setting["handle_y_rotation"], 0])
                vertices_list.append(tmp_mesh.vertices)
                faces_list.append(tmp_mesh.faces + total_num_vertices)
                total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Door/concept_template.py
class Cylindrical_Handle(ConceptTemplate):
    def __init__(self, existence_of_door, door_rotation, door_size, existence_of_handle, fixed_part_size, sub_size, main_size, offset_x, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        door_rotation = [x / 180 * np.pi for x in door_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.existence_of_handle = existence_of_handle
        self.door_size = door_size
        self.existence_of_door = existence_of_door
        self.door_rotation = door_rotation
        self.main_size = main_size
        self.sub_size = sub_size
        self.fixed_part_size = fixed_part_size
        self.offset_x = offset_x

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.direction_settings = []
        double_door = 0
        if existence_of_door[0] and existence_of_door[1]:
            double_door = 1

        # parameter calculate
        for door in [0, 1]:
            if not existence_of_door[door]:
                continue
            for handle in [0, 1]:
                if not existence_of_handle[handle]:
                    continue
                # right_door(x+)
                if door:
                    handle_y_rotation = door_rotation[1]
                    handle_x_direction = 1
                    handle_y_axis = door_size[0] / 2
                # left_door(x-)
                else:
                    handle_y_rotation = -door_rotation[0]
                    handle_x_direction = -1
                    handle_y_axis = -door_size[0] / 2
                # front_handle(z+)
                if handle:
                    handle_z_direction = 1
                # back_handle(z-)
                else:
                    handle_z_direction = -1
                if double_door:
                    handle_x_position = handle_y_axis
                    handle_y_axis *= 2
                else:
                    handle_x_position = 0
                self.direction_settings.append(
                    {
                        "handle_x_direction": handle_x_direction,
                        "handle_x_position": handle_x_position,
                        "handle_z_direction": handle_z_direction,
                        "handle_y_axis": handle_y_axis,
                        "handle_y_rotation": handle_y_rotation,
                    }
                )

        # meshes definition
        for direction_setting in self.direction_settings:
            tmp_meshes = []

            base_mesh_position = [
                -direction_setting["handle_x_direction"] * offset_x[0] + direction_setting["handle_x_position"],
                0,
                direction_setting["handle_z_direction"] * (door_size[2] / 2 + fixed_part_size[1] / 2),
            ]
            base_mesh_rotation = [np.pi / 2, 0, 0]
            self.base_mesh = Cylinder(fixed_part_size[1], fixed_part_size[0], fixed_part_size[0],
                                 position=base_mesh_position,
                                 rotation=base_mesh_rotation)
            tmp_meshes.append(self.base_mesh)

            middle_mesh_position = [
                -direction_setting["handle_x_direction"] * offset_x[0] + direction_setting["handle_x_position"],
                0,
                direction_setting["handle_z_direction"] * (door_size[2] / 2 + fixed_part_size[1] + sub_size[1] / 2),
            ]
            middle_mesh_rotation = [np.pi / 2, 0, 0]
            self.middle_mesh = Cylinder(sub_size[1], sub_size[0], sub_size[0],
                                   position=middle_mesh_position,
                                   rotation=middle_mesh_rotation)
            tmp_meshes.append(self.middle_mesh)

            main_mesh_position = [
                -direction_setting["handle_x_direction"] * offset_x[0] + direction_setting["handle_x_position"],
                0,
                direction_setting["handle_z_direction"] * (door_size[2] / 2 + fixed_part_size[1] + sub_size[1] + main_size[1] / 2)
            ]
            main_mesh_rotation = [np.pi / 2, 0, 0]
            self.main_mesh = Cylinder(main_size[1], main_size[0], main_size[0],
                                 position=main_mesh_position,
                                 rotation=main_mesh_rotation)
            tmp_meshes.append(self.main_mesh)

            for tmp_mesh in tmp_meshes:
                tmp_mesh.vertices = apply_transformation(tmp_mesh.vertices, [-direction_setting["handle_y_axis"], 0, 0], [0, 0, 0])
                tmp_mesh.vertices = apply_transformation(tmp_mesh.vertices, [direction_setting["handle_y_axis"], 0, 0], [0, direction_setting["handle_y_rotation"], 0])
                vertices_list.append(tmp_mesh.vertices)
                faces_list.append(tmp_mesh.faces + total_num_vertices)
                total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Door/concept_template.py
class Spherical_Handle(ConceptTemplate):
    def __init__(self, existence_of_door, door_rotation, door_size, existence_of_handle, fixed_part_size, sub_size, main_size, offset_x, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        door_rotation = [x / 180 * np.pi for x in door_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.existence_of_handle = existence_of_handle
        self.door_size = door_size
        self.existence_of_door = existence_of_door
        self.door_rotation = door_rotation
        self.main_size = main_size
        self.sub_size = sub_size
        self.fixed_part_size = fixed_part_size
        self.offset_x = offset_x

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.direction_settings = []
        double_door = 0
        if existence_of_door[0] and existence_of_door[1]:
            double_door = 1

        # parameter calculate
        for door in [0, 1]:
            if not existence_of_door[door]:
                continue
            for handle in [0, 1]:
                if not existence_of_handle[handle]:
                    continue
                # right_door(x+)
                if door:
                    handle_y_rotation = door_rotation[1]
                    handle_x_direction = 1
                    handle_y_axis = door_size[0] / 2
                # left_door(x-)
                else:
                    handle_y_rotation = -door_rotation[0]
                    handle_x_direction = -1
                    handle_y_axis = -door_size[0] / 2
                # front_handle(z+)
                if handle:
                    handle_z_direction = 1
                # back_handle(z-)
                else:
                    handle_z_direction = -1
                if double_door:
                    handle_x_position = handle_y_axis
                    handle_y_axis *= 2
                else:
                    handle_x_position = 0
                self.direction_settings.append(
                    {
                        "handle_x_direction": handle_x_direction,
                        "handle_x_position": handle_x_position,
                        "handle_z_direction": handle_z_direction,
                        "handle_y_axis": handle_y_axis,
                        "handle_y_rotation": handle_y_rotation,
                    }
                )
        # meshes definition
        for direction_setting in self.direction_settings:
            tmp_meshes = []

            base_mesh_position = [
                -direction_setting["handle_x_direction"] * offset_x[0] + direction_setting["handle_x_position"],
                0,
                direction_setting["handle_z_direction"] * (door_size[2] / 2 + fixed_part_size[1] / 2),
            ]
            base_mesh_rotation = [np.pi / 2, 0, 0]
            self.base_mesh = Cylinder(fixed_part_size[1], fixed_part_size[0], fixed_part_size[0],
                                      position=base_mesh_position,
                                      rotation=base_mesh_rotation)
            tmp_meshes.append(self.base_mesh)

            middle_mesh_position = [
                -direction_setting["handle_x_direction"] * offset_x[0] + direction_setting["handle_x_position"],
                0,
                direction_setting["handle_z_direction"] * (door_size[2] / 2 + fixed_part_size[1] + sub_size[1] / 2),
            ]
            middle_mesh_rotation = [np.pi / 2, 0, 0]
            self.middle_mesh = Cylinder(sub_size[1], sub_size[0], sub_size[0],
                                        position=middle_mesh_position,
                                        rotation=middle_mesh_rotation)
            tmp_meshes.append(self.middle_mesh)

            main_mesh_position = [
                -direction_setting["handle_x_direction"] * offset_x[0] + direction_setting["handle_x_position"],
                0,
                direction_setting["handle_z_direction"] * (door_size[2] / 2 + fixed_part_size[1] + sub_size[1] + main_size[1] / 2),
            ]
            self.main_mesh = Sphere(main_size[0], radius_y=main_size[1], radius_z=main_size[2],
                                    position=main_mesh_position)
            tmp_meshes.append(self.main_mesh)

            for tmp_mesh in tmp_meshes:
                tmp_mesh.vertices = apply_transformation(tmp_mesh.vertices, [-direction_setting["handle_y_axis"], 0, 0], [0, 0, 0])
                tmp_mesh.vertices = apply_transformation(tmp_mesh.vertices, [direction_setting["handle_y_axis"], 0, 0], [0, direction_setting["handle_y_rotation"], 0])
                vertices_list.append(tmp_mesh.vertices)
                faces_list.append(tmp_mesh.faces + total_num_vertices)
                total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)
        
        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Knife/concept_template.py
class Cuboidal_Handle(ConceptTemplate):
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

        self.semantic = 'Handle'


# Source: Knife/concept_template.py
class T_Shaped_Handle(ConceptTemplate):
    def __init__(self, main_size, bottom_size, bottom_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.main_size = main_size
        self.bottom_size = bottom_size
        self.bottom_offset = bottom_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.mesh = Cuboid(main_size[1], main_size[0], main_size[2])
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        bottom_mesh_position = [
            bottom_offset[0], 
            -(main_size[1] + bottom_size[1]) / 2,
            bottom_offset[1]
        ]
        self.bottom_mesh = Cuboid(bottom_size[1], bottom_size[0], bottom_size[2],
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

        self.semantic = 'Handle'


# Source: Knife/concept_template.py
class Cylindrical_Handle(ConceptTemplate):
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

        self.mesh = Cylinder(size[2], size[0], size[1])
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


# Source: Knife/concept_template.py
class Curved_Handle(ConceptTemplate):
    def __init__(self, radius, thickness, exist_angle, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        exist_angle = [x / 180 * np.pi for x in exist_angle]
        super().__init__(position, rotation)

        # Record Parameters
        self.radius = radius
        self.thickness = thickness
        self.exist_angle = exist_angle

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_position = [
            0,
            0,
            (radius[0] + radius[1]) / 2
        ]
        mesh_rotation = [np.pi / 2, np.pi / 2, 0]
        self.mesh = Ring(thickness[0], radius[0], radius[1], exist_angle[0],
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

        self.semantic = 'Handle'


# Source: Knife/concept_template.py
class Multideck_Handle(ConceptTemplate):
    def __init__(self, bottom_size, beside_size, beside_seperation, beside_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.bottom_size = bottom_size
        self.beside_size = beside_size
        self.beside_seperation = beside_seperation
        self.beside_offset = beside_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0,
            -beside_size[1] / 2,
            0
        ]
        self.bottom_mesh = Cuboid(bottom_size[1], bottom_size[0], bottom_size[2],
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        left_mesh_position = [
            beside_seperation[0] / 2 + beside_offset[0],
            bottom_size[1] / 2,
            beside_offset[1]
        ]
        self.left_mesh = Cuboid(beside_size[1], beside_size[0], beside_size[2],
                                position = left_mesh_position)
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        right_mesh_position = [
            -beside_seperation[0] / 2 + beside_offset[0],
            bottom_size[1] / 2,
            beside_offset[1]
        ]
        self.right_mesh = Cuboid(beside_size[1], beside_size[0], beside_size[2],
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

        self.semantic = 'Handle'


# Source: Knife/concept_template.py
class Enveloping_Handle(ConceptTemplate):
    def __init__(self, size, thickness, gap_width, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.thickness = thickness
        self.gap_width = gap_width

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0,
            -(size[1] - thickness[0]) / 2,
            0
        ]
        self.bottom_mesh = Cuboid(thickness[0], size[0], size[2],
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        behind_mesh_position = [
            -(size[0] - thickness[1]) / 2,
            thickness[0] / 2,
            0
        ]
        self.behind_mesh = Cuboid(size[1] - thickness[0], thickness[1], size[2],
                                  position = behind_mesh_position)
        vertices_list.append(self.behind_mesh.vertices)
        faces_list.append(self.behind_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.behind_mesh.vertices)

        left_mesh_position = [
            thickness[1] / 2,
            thickness[0] / 2,
            (size[2] - thickness[2]) / 2
        ]
        self.left_mesh = Cuboid(size[1] - thickness[0], size[0] - thickness[1], thickness[2],
                                position = left_mesh_position)
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        right_mesh_position = [
            thickness[1] / 2,
            thickness[0] / 2,
            -(size[2] - thickness[2]) / 2
        ]
        self.right_mesh = Cuboid(size[1] - thickness[0], size[0] - thickness[1], thickness[2],
                                 position = right_mesh_position)
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        left_front_mesh_position = [
            (size[0] - thickness[2]) / 2,
            thickness[0] / 2,
            size[2] / 2 - thickness[2] / 2 - (size[2] - gap_width[0]) / 4
        ]
        self.left_front_mesh = Cuboid(size[1] - thickness[0], thickness[2], (size[2] - gap_width[0]) / 2 - thickness[2],
                                      position = left_front_mesh_position)
        vertices_list.append(self.left_front_mesh.vertices)
        faces_list.append(self.left_front_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_front_mesh.vertices)

        right_front_mesh_position = [
            (size[0] - thickness[2]) / 2,
            thickness[0] / 2,
            -size[2] / 2 + thickness[2] / 2 + (size[2] - gap_width[0]) / 4
        ]
        self.right_front_mesh = Cuboid(size[1] - thickness[0], thickness[2], (size[2] - gap_width[0]) / 2 - thickness[2],
                                       position = right_front_mesh_position)
        vertices_list.append(self.right_front_mesh.vertices)
        faces_list.append(self.right_front_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_front_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'
