"""
Refill Templates
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


# Source: Pen/concept_template.py
class Cylindrical_Refill(ConceptTemplate):
    def __init__(self, size, tip_radius, tip_height, tip_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.tip_radius = tip_radius
        self.tip_height = tip_height
        self.tip_offset = tip_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.mesh = Cylinder(size[1], size[0])
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        bottom_mesh_position = [
            0,
            -size[1] / 2 - tip_height[0] / 2, 
            0
        ]
        self.bottom_mesh = Cylinder(tip_height[0], tip_radius[0], 
                                    position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        tip_mesh_position = [
            0,
            -size[1] / 2 - tip_height[0], 
            0
        ]
        tip_mesh_rotation = [0, 0, np.pi]
        self.tip_mesh = Cone(tip_radius[0], tip_height[1], tip_offset,
                             position = tip_mesh_position,
                             rotation = tip_mesh_rotation)
        vertices_list.append(self.tip_mesh.vertices)
        faces_list.append(self.tip_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.tip_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Refill'
