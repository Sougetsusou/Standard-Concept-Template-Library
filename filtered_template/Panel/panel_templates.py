"""
Panel Templates
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


# Source: StorageFurniture/concept_template.py
class Regular_front_panel(ConceptTemplate):
    def __init__(self, number_of_frontPanel, frontPanel_params, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.number_of_frontPanel = number_of_frontPanel
        self.frontPanel_size = [frontPanel_params[i * 6: i * 6 + 3] for i in range(number_of_frontPanel[0])]
        self.frontPanel_offset = [frontPanel_params[i * 6 + 3: i * 6 + 6] for i in range(number_of_frontPanel[0])]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for frontPanel_idx in range(number_of_frontPanel[0]):
            mesh_position = [self.frontPanel_offset[frontPanel_idx][0],
                             self.frontPanel_offset[frontPanel_idx][1],
                             self.frontPanel_offset[frontPanel_idx][2]]
            self.mesh = Cuboid(self.frontPanel_size[frontPanel_idx][1],
                               self.frontPanel_size[frontPanel_idx][0],
                               self.frontPanel_size[frontPanel_idx][2],
                               position=mesh_position)

            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Panel'
