"""
Hinge Templates
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


# Source: Door/concept_template.py
class Standard_Hinge(ConceptTemplate):
    def __init__(self, existence_of_door, number_of_hinge, size, separation, offset_1, offset_2, position=[0, 0, 0], rotation=[0, 0, 0]):
        
        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.existence_of_door = existence_of_door
        self.number_of_hinge = number_of_hinge
        self.size = size
        self.separation = separation
        self.offset_1 = offset_1
        self.offset_2 = offset_2

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        offset = offset_1
        for existence in range(existence_of_door[0] + existence_of_door[1]):
            for i in range(number_of_hinge[0]):
                tmp_mesh_position = [
                    offset[0],
                    offset[1] + size[1] * (i + 0.5) + sum(separation[0:i]),
                    offset[2],
                ]
                self.tmp_mesh = Cylinder(size[1], size[0], size[0],
                                    position=tmp_mesh_position)

                vertices_list.append(self.tmp_mesh.vertices)
                faces_list.append(self.tmp_mesh.faces + total_num_vertices)
                total_num_vertices += len(self.tmp_mesh.vertices)
            
            offset = offset_2

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Hinge'
