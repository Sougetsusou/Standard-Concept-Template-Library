"""
Dial Templates
Automatically extracted from concept_template.py files
Contains 1 class(es)
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


# Source: Safe/concept_template.py
class Cylindrical_Dial(ConceptTemplate):
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

        bottom_mesh_position = [
            0, 
            0, 
            bottom_size[2] / 2
        ]
        bottom_mesh_rotation = [-np.pi / 2, 0, 0]
        self.bottom_mesh = Cylinder(bottom_size[2], bottom_size[0], bottom_size[1],
                                    position = bottom_mesh_position,
                                    rotation = bottom_mesh_rotation)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        top_mesh_position = [
            0, 
            0, 
            bottom_size[2] + top_size[1] / 2
        ]
        top_mesh_rotation = [-np.pi / 2, 0, 0]
        self.top_mesh = Cylinder(top_size[1], top_size[0],
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

        self.semantic = 'Dial'
