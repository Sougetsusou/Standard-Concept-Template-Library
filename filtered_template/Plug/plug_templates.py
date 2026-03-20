"""
Plug Templates
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


# Source: Switch/concept_template.py
class Cuboidal_Plug(ConceptTemplate):
    def __init__(self, column_of_contact, row_of_contact, size, interval, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.column_of_contact = column_of_contact
        self.row_of_contact = row_of_contact
        self.size = size
        self.interval = interval

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for j in range(row_of_contact[0]):
            for i in range(column_of_contact[0]):
                mesh_position = [
                    (interval[0] + size[0]) * i,
                    (interval[1] + size[1]) * j,
                    -size[2] / 2,
                ],
                self.mesh = Cuboid(size[1], size[0], size[2],
                                   position=mesh_position)
                vertices_list.append(self.mesh.vertices)
                faces_list.append(self.mesh.faces + total_num_vertices)
                total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Plug'


# Source: Switch/concept_template.py
class Standard_Plug(ConceptTemplate):
    def __init__(self, size, sub_offset, plug_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        plug_rotation = [x / 180 * np.pi for x in plug_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.sub_offset = sub_offset
        self.plug_rotation = plug_rotation
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
        mesh_rotation = [0, 0, plug_rotation[0]]
        self.mesh = Cuboid(size[1], size[0], size[2],
                           position=mesh_position,
                           rotation=mesh_rotation)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        mesh_position = [
            - sub_offset[0] * np.cos(plug_rotation[0]) + sub_offset[1] * np.sin(-plug_rotation[0]),
            sub_offset[1] * np.cos(-plug_rotation[0]) - sub_offset[0] * np.sin(plug_rotation[0]),
            -size[2] / 2,
        ]
        mesh_rotation = [0, 0, plug_rotation[0] + plug_rotation[1]]
        self.mesh = Cuboid(size[1], size[0], size[2],
                           position=mesh_position,
                           rotation=mesh_rotation)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        mesh_position = [
            sub_offset[0] * np.cos(plug_rotation[0]) + sub_offset[1] * np.sin(-plug_rotation[0]),
            sub_offset[1] * np.cos(-plug_rotation[0]) + sub_offset[0] * np.sin(plug_rotation[0]),
            -size[2] / 2,
        ]
        mesh_rotation = [0, 0, plug_rotation[0] - plug_rotation[1]]
        self.mesh = Cuboid(size[1], size[0], size[2],
                           position=mesh_position,
                           rotation=mesh_rotation)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Plug'


# Source: Switch/concept_template.py
class Cylindrical_Plug(ConceptTemplate):
    def __init__(self, column_of_contact, row_of_contact, size, interval, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.column_of_contact = column_of_contact
        self.row_of_contact = row_of_contact
        self.size = size
        self.interval = interval

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for j in range(row_of_contact[0]):
            for i in range(column_of_contact[0]):
                mesh_position = [
                    (interval[0] + size[0] * 2) * i,
                    (interval[1] + size[0] * 2) * j,
                    -size[1] / 2,
                ]
                mesh_rotation=[np.pi / 2, 0, 0]
                self.mesh = Cylinder(size[1], size[0], size[0],
                                     position=mesh_position,
                                     rotation=mesh_rotation)
                vertices_list.append(self.mesh.vertices)
                faces_list.append(self.mesh.faces + total_num_vertices)
                total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Plug'
