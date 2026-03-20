"""
Glasses Templates
Automatically extracted from concept_template.py files
Contains 4 class(es)
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


# Source: Eyeglasses/concept_template.py
class Trapezoidal_Glasses(ConceptTemplate):
    def __init__(self, size, interval, glass_rotation, top_offset, position=[0, 0, 0], rotation=[0, 0, 0]):
        
        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        glass_rotation = [x / 180 * np.pi for x in glass_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.interval = interval
        self.glass_rotation = glass_rotation
        self.top_offset = top_offset
        
        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.right_mesh = Cuboid(size[2], size[0], size[3],
                                 size[1], size[3],
                                 [top_offset[0], 0])
        self.right_mesh.vertices = np.concatenate((self.right_mesh.vertices, np.array([[top_offset[0], 0, -size[3] / 2]])), axis=0) # for calculate center position
        self.right_mesh.vertices = apply_transformation(
            self.right_mesh.vertices,
            rotation=[0, glass_rotation[0], glass_rotation[1]],
            position=[0, 0, 0],
        )
        center = self.right_mesh.vertices[-1]
        self.right_mesh.vertices = apply_transformation(
            self.right_mesh.vertices,
            position=[
                -center[0] + size[0] * np.cos(glass_rotation[0]) * np.cos(glass_rotation[1]) / 2 + interval[0] / 2,
                -center[1],
                -center[2] + size[0] * np.sin(glass_rotation[0]) / 2,
            ],
            rotation=[0, 0, 0],
        )
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        self.left_mesh = Cuboid(size[2], size[0], size[3],
                           size[1], size[3],
                          [-top_offset[0], 0])
        self.left_mesh.vertices = np.concatenate((self.left_mesh.vertices, np.array([[-top_offset[0], 0, -size[3] / 2]])), axis=0)
        self.left_mesh.vertices = apply_transformation(
            self.left_mesh.vertices,
            rotation=[0, -glass_rotation[0], -glass_rotation[1]],
            position=[0, 0, 0],
        )
        center = self.left_mesh.vertices[-1]
        self.left_mesh.vertices = apply_transformation(
            self.left_mesh.vertices,
            position=[
                -center[0] - size[0] * np.cos(glass_rotation[0]) * np.cos(glass_rotation[1]) / 2 - interval[0] / 2,
                -center[1],
                -center[2] + size[0] * np.sin(glass_rotation[0]) / 2,
            ],
            rotation=[0, 0, 0],
        )
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Glasses'


# Source: Eyeglasses/concept_template.py
class TrapezoidalFrame_Glasses(ConceptTemplate):
    def __init__(self, size, interval, glass_rotation, top_offset, width, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        glass_rotation = [x / 180 * np.pi for x in glass_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.interval = interval
        self.glass_rotation = glass_rotation
        self.top_offset = top_offset
        self.width = width

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        right_meshes = [
            # top
            Cuboid(
                height=width[0],
                top_length=size[0],
                top_width=size[3],
                bottom_length=(size[1] * width[0] / size[2] + size[0] * (size[2] - width[0]) / size[2]),
                bottom_width=size[3],
                top_offset=[-top_offset[0] * width[0] / size[2], 0],
                position=[
                    top_offset[0] * width[0] / size[2], 
                    (size[2] - width[0]) / 2, 
                    0
                ],
            ),
            # bottom
            Cuboid(
                height=width[0],
                top_length=(size[1] * (size[2] - width[0]) / size[2] + size[0] * width[0] / size[2]),
                top_width=size[3],
                bottom_length=size[1],
                bottom_width=size[3],
                top_offset=[-top_offset[0] * width[0] / size[2], 0],
                position=[
                    top_offset[0], 
                    -(size[2] - width[0]) / 2, 
                    0
                ],
            ),
            # left
            Cuboid(
                height=size[2] - 2 * width[0],
                top_length=(width[0] * np.sqrt((size[0] - top_offset[0] - size[1]) ** 2 + size[2] ** 2) / size[2]),
                top_width=size[3],
                bottom_length=(width[0] * np.sqrt((size[0] - top_offset[0] - size[1]) ** 2 + size[2] ** 2) / size[2]),
                bottom_width=size[3],
                top_offset=[-((size[1] * width[0] / size[2] + size[0] * (size[2] - width[0]) / size[2]) - (size[1] * (size[2] - width[0]) / size[2] + size[0] * width[0] / size[2])) / 2 - top_offset[0] * (size[2] - 2 * width[0]) / size[2], 0],
                position=[
                    (-(size[1] * (size[2] - width[0]) / size[2] + size[0] * width[0] / size[2]) / 2 + top_offset[0] * (size[2] - width[0]) / size[2] + (width[0] * np.sqrt((size[0] - top_offset[0] - size[1]) ** 2 + size[2] ** 2) / size[2]) / 2),
                    0,
                    0,
                ],
            ),
            # right
            Cuboid(
                height=size[2] - 2 * width[0],
                top_length=(width[0] * np.sqrt((size[0] + top_offset[0] - size[1]) ** 2 + size[2] ** 2) / size[2]),
                top_width=size[3],
                bottom_length=width[0] * np.sqrt((size[0] + top_offset[0] - size[1]) ** 2 + size[2] ** 2) / size[2],
                bottom_width=size[3],
                top_offset=[((size[1] * width[0] / size[2] + size[0] * (size[2] - width[0]) / size[2]) - (size[1] * (size[2] - width[0]) / size[2] + size[0] * width[0] / size[2])) / 2 - top_offset[0] * (size[2] - 2 * width[0]) / size[2], 0,],
                position=[
                    ((size[1] * (size[2] - width[0]) / size[2] + size[0] * width[0] / size[2]) / 2 + top_offset[0] * (size[2] - width[0]) / size[2] - (width[0] * np.sqrt((size[0] + top_offset[0] - size[1]) ** 2 + size[2] ** 2) / size[2]) / 2),
                    0,
                    0,
                ],
            ),
        ]

        right_meshes[0].vertices = np.concatenate((right_meshes[0].vertices, np.array([[top_offset[0], 0, -size[3] / 2]])), axis=0)
        for right_mesh in right_meshes:
            right_mesh.vertices = np.concatenate((right_mesh.vertices, np.array([[top_offset[0], 0, -size[3] / 2]])), axis=0)
            right_mesh.vertices = apply_transformation(
                right_mesh.vertices,
                rotation=[0, glass_rotation[0], glass_rotation[1]],
                position=[0, 0, 0],
            )
            center = right_mesh.vertices[-1]
            right_mesh.vertices = apply_transformation(
                right_mesh.vertices,
                position=[-center[0] + size[0] * np.cos(glass_rotation[0]) * np.cos(glass_rotation[1]) / 2 + interval[0] / 2,
                    -center[1],
                    -center[2] + size[0] * np.sin(glass_rotation[0]) / 2,
                ],
                rotation=[0, 0, 0],
            )
            vertices_list.append(right_mesh.vertices)
            faces_list.append(right_mesh.faces + total_num_vertices)
            total_num_vertices += len(right_mesh.vertices)

        left_meshes = [
            # top
            Cuboid(
                height=width[0],
                top_length=size[0],
                top_width=size[3],
                bottom_length=(size[1] * width[0] / size[2] + size[0] * (size[2] - width[0]) / size[2]),
                bottom_width=size[3],
                top_offset=[-top_offset[0] * width[0] / size[2], 0],
                position=[
                    top_offset[0] * width[0] / size[2], 
                    (size[2] - width[0]) / 2, 
                    0
                ],
            ),
            # bottom
            Cuboid(
                height=width[0],
                top_length=(size[1] * (size[2] - width[0]) / size[2] + size[0] * width[0] / size[2]),
                top_width=size[3],
                bottom_length=size[1],
                bottom_width=size[3],
                top_offset=[-top_offset[0] * width[0] / size[2], 0],
                position=[
                    top_offset[0], 
                    -(size[2] - width[0]) / 2, 
                    0
                ],
            ),
            # left
            Cuboid(
                height=size[2] - 2 * width[0],
                top_length=(width[0] * np.sqrt((size[0] - top_offset[0] - size[1]) ** 2 + size[2] ** 2) / size[2]),
                top_width=size[3],
                bottom_length=(width[0] * np.sqrt((size[0] - top_offset[0] - size[1]) ** 2 + size[2] ** 2) / size[2]),
                bottom_width=size[3],
                top_offset=[-((size[1] * width[0] / size[2] + size[0] * (size[2] - width[0]) / size[2]) - (size[1] * (size[2] - width[0]) / size[2] + size[0] * width[0] / size[2])) / 2 - top_offset[0] * (size[2] - 2 * width[0]) / size[2], 0],
                position=[
                    (-(size[1] * (size[2] - width[0]) / size[2] + size[0] * width[0] / size[2]) / 2 + top_offset[0] * (size[2] - width[0]) / size[2] + (width[0] * np.sqrt((size[0] - top_offset[0] - size[1]) ** 2 + size[2] ** 2) / size[2]) / 2),
                    0,
                    0,
                ],
            ),
            # right
            Cuboid(
                height=size[2] - 2 * width[0],
                top_length=(width[0] * np.sqrt((size[0] + top_offset[0] - size[1]) ** 2 + size[2] ** 2) / size[2]),
                top_width=size[3],
                bottom_length=(width[0] * np.sqrt((size[0] + top_offset[0] - size[1]) ** 2 + size[2] ** 2) / size[2]),
                bottom_width=size[3],
                top_offset=[((size[1] * width[0] / size[2] + size[0] * (size[2] - width[0]) / size[2]) - (size[1] * (size[2] - width[0]) / size[2] + size[0] * width[0] / size[2])) / 2 - top_offset[0] * (size[2] - 2 * width[0]) / size[2], 0],
                position=[
                    ((size[1] * (size[2] - width[0]) / size[2] + size[0] * width[0] / size[2]) / 2 + top_offset[0] * (size[2] - width[0]) / size[2] - (width[0] * np.sqrt((size[0] + top_offset[0] - size[1]) ** 2 + size[2] ** 2) / size[2]) / 2),
                    0,
                    0,
                ],
            ),
        ]

        left_meshes[0].vertices = np.concatenate((left_meshes[0].vertices, np.array([[top_offset[0], 0, -size[3] / 2]])), axis=0)
        for left_mesh in left_meshes:
            left_mesh.vertices = np.concatenate((left_mesh.vertices, np.array([[top_offset[0], 0, -size[3] / 2]])), axis=0)
            left_mesh.vertices = apply_transformation(
                left_mesh.vertices,
                rotation=[0, -glass_rotation[0], -glass_rotation[1]],
                position=[0, 0, 0],
            )
            center = left_mesh.vertices[-1]
            left_mesh.vertices = apply_transformation(
                left_mesh.vertices,
                position=[
                    -center[0] - size[0] * np.cos(glass_rotation[0]) * np.cos(glass_rotation[1]) / 2 - interval[0] / 2,
                    -center[1],
                    -center[2] + size[0] * np.sin(glass_rotation[0]) / 2,
                ],
                rotation=[0, 0, 0],
            )
            vertices_list.append(left_mesh.vertices)
            faces_list.append(left_mesh.faces + total_num_vertices)
            total_num_vertices += len(left_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Glasses'


# Source: Eyeglasses/concept_template.py
class Round_Glasses(ConceptTemplate):
    def __init__(self, size, interval, glass_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        glass_rotation = [x / 180 * np.pi for x in glass_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.interval = interval
        self.glass_rotation = glass_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        right_mesh_rotation = [np.pi / 2, 0, 0]
        self.right_mesh = Cylinder(size[2], size[0], size[0],
                                   size[1], size[1],
                                   rotation=right_mesh_rotation)
        self.right_mesh.vertices = np.concatenate((self.right_mesh.vertices, np.array([[0, 0, 0]])), axis=0)
        self.right_mesh.vertices = apply_transformation(
            self.right_mesh.vertices,
            rotation=[0, glass_rotation[0], glass_rotation[1]],
            position=[0, 0, 0],
            rotation_order="YZX",
        )
        center = self.right_mesh.vertices[-1]
        edge = [self.right_mesh.vertices[3], self.right_mesh.vertices[259]] # for calculate edge position
        self.right_mesh.vertices = apply_transformation(
            self.right_mesh.vertices,
            position=[
                [
                    -edge[1][0] + interval[0] / 2,
                    -center[1],
                    -edge[0][2],
                ]
            ],
            rotation=[0, 0, 0],
        )
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        left_mesh_rotation = [np.pi / 2, 0, 0]
        self.left_mesh = Cylinder(size[2], size[0], size[0],
                                  size[1], size[1],
                                  rotation=left_mesh_rotation)
        self.left_mesh.vertices = np.concatenate((self.left_mesh.vertices, np.array([[0, 0, 0]])), axis=0)
        self.left_mesh.vertices = apply_transformation(
            self.left_mesh.vertices,
            rotation=[0, -glass_rotation[0], -glass_rotation[1]],
            position=[0, 0, 0],
            rotation_order="YZX",
        )
        center = self.left_mesh.vertices[-1]
        edge = [self.left_mesh.vertices[3], self.left_mesh.vertices[259]]
        self.left_mesh.vertices = apply_transformation(
            self.left_mesh.vertices,
            position=[
                [
                    -edge[0][0] - interval[0] / 2,
                    -center[1],
                    -edge[1][2],
                ]
            ],
            rotation=[0, 0, 0],
        )
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Glasses'


# Source: Eyeglasses/concept_template.py
class RoundFrame_Glasses(ConceptTemplate):
    def __init__(self, size, interval, width, glass_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        glass_rotation = [x / 180 * np.pi for x in glass_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.interval = interval
        self.glass_rotation = glass_rotation
        self.width = width

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.right_mesh = Ring(
            height=size[2],
            inner_top_radius=size[0] - width[0],
            outer_top_radius=size[0],
            x_z_ratio=size[0] / size[1],
            rotation=[np.pi / 2, 0, 0],
            position=[0, 0, 0],
        )
        self.right_mesh.vertices = np.concatenate((self.right_mesh.vertices, np.array([[0, 0, 0]])), axis=0)
        self.right_mesh.vertices = apply_transformation(
            self.right_mesh.vertices,
            rotation=[0, glass_rotation[0], glass_rotation[1]],
            position=[0, 0, 0],
            rotation_order="YZX",
        )
        center = self.right_mesh.vertices[-1]
        edge = [self.right_mesh.vertices[1], self.right_mesh.vertices[513]]
        self.right_mesh.vertices = apply_transformation(
            self.right_mesh.vertices,
            position=[
                [
                    -edge[1][0] + interval[0] / 2,
                    -center[1],
                    -edge[0][2],
                ]
            ],
            rotation=[0, 0, 0],
        )
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        self.left_mesh = Ring(
            height=size[2],
            inner_top_radius=size[0] - width[0],
            outer_top_radius=size[0],
            x_z_ratio=size[0] / size[1],
            rotation=[np.pi / 2, 0, 0],
            position=[0, 0, 0],
        )
        self.left_mesh.vertices = np.concatenate((self.left_mesh.vertices, np.array([[0, 0, 0]])), axis=0)
        self.left_mesh.vertices = apply_transformation(
            self.left_mesh.vertices,
            rotation=[0, -glass_rotation[0], -glass_rotation[1]],
            position=[0, 0, 0],
            rotation_order="YZX",
        )
        center = self.left_mesh.vertices[-1]
        edge = [self.left_mesh.vertices[1], self.left_mesh.vertices[513]]
        self.left_mesh.vertices = apply_transformation(
            self.left_mesh.vertices,
            position=[
                [
                    -edge[0][0] - interval[0] / 2,
                    -center[1],
                    -edge[1][2],
                ]
            ],
            rotation=[0, 0, 0],
        )
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Glasses'
