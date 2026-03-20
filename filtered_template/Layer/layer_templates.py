"""
Layer Templates
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


# Source: Table/concept_template.py
class Regular_sublayer(ConceptTemplate):
    def __init__(self, subs_size, number_of_subs, subs_offset, interval_between_subs,
                 additional_sublayers_params, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        additional_sublayers_params = [x / 180 * np.pi if ((i > 1) and ((i - 1) % 9 in [6, 7, 8])) else x for i, x in
                                       enumerate(additional_sublayers_params)]
        super().__init__(position, rotation)

        # Record Parameters
        self.subs_size = subs_size
        self.number_of_subs = number_of_subs
        self.subs_offset = subs_offset
        self.interval_between_subs = interval_between_subs
        self.number_of_additional_sublayers = additional_sublayers_params[0]
        self.additional_sublayers_attributes = additional_sublayers_params[1:]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(number_of_subs[0]):
            mesh_rotation = [0, 0, 0]
            mesh_position = [0, subs_offset[0] + i * interval_between_subs[0], 0]
            self.mesh = Cuboid(subs_size[1], subs_size[0], subs_size[2],
                               position=mesh_position, rotation=mesh_rotation)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        for i in range(self.number_of_additional_sublayers):
            mesh_position = [self.additional_sublayers_attributes[9 * i + 3] - position[0],
                             self.additional_sublayers_attributes[9 * i + 4] - position[1],
                             self.additional_sublayers_attributes[9 * i + 5] - position[2]]
            mesh_rotation = [self.additional_sublayers_attributes[9 * i + 6],
                             self.additional_sublayers_attributes[9 * i + 7],
                             self.additional_sublayers_attributes[9 * i + 8]]
            self.additional_mesh = Cuboid(self.additional_sublayers_attributes[9 * i + 1],
                                          self.additional_sublayers_attributes[9 * i],
                                          self.additional_sublayers_attributes[9 * i + 2],
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

        self.semantic = 'Layer'


# Source: Table/concept_template.py
class Cylindrical_sublayer(ConceptTemplate):
    def __init__(self, subs_size, number_of_subs, subs_offset, interval_between_subs,
                 additional_sublayers_params, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        additional_sublayers_params = [x / 180 * np.pi if ((i > 1) and ((i - 1) % 9 in [6, 7, 8])) else x for i, x in
                                       enumerate(additional_sublayers_params)]
        super().__init__(position, rotation)

        # Record Parameters
        self.subs_size = subs_size
        self.number_of_subs = number_of_subs
        self.subs_offset = subs_offset
        self.interval_between_subs = interval_between_subs
        self.number_of_additional_sublayers = additional_sublayers_params[0]
        self.additional_sublayers_attributes = additional_sublayers_params[1:]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(number_of_subs[0]):
            mesh_rotation = [0, 0, 0]
            mesh_position = [0, subs_offset[0] + i * interval_between_subs[0], 0]
            self.mesh = Cylinder(subs_size[1], subs_size[0],
                                 position=mesh_position, rotation=mesh_rotation)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        for i in range(self.number_of_additional_sublayers):
            mesh_position = [self.additional_sublayers_attributes[9 * i + 3],
                             self.additional_sublayers_attributes[9 * i + 4],
                             self.additional_sublayers_attributes[9 * i + 5]]
            mesh_rotation = [self.additional_sublayers_attributes[9 * i + 6],
                             self.additional_sublayers_attributes[9 * i + 7],
                             self.additional_sublayers_attributes[9 * i + 8]]
            self.additional_mesh = Cuboid(self.additional_sublayers_attributes[9 * i + 1],
                                          self.additional_sublayers_attributes[9 * i],
                                          self.additional_sublayers_attributes[9 * i + 2],
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

        self.semantic = 'Layer'
