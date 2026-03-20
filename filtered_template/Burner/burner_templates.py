"""
Burner Templates
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


# Source: Oven/concept_template.py
class Top_With_Burner(ConceptTemplate):
    def __init__(self, bottom_size, burner_1_size, burner_1_thickness, burner_1_offset, burner_1_central_size, burner_1_central_offset, burner_2_size, burner_2_thickness, burner_2_offset, burner_2_central_size, burner_2_central_offset, burner_3_size, burner_3_thickness, burner_3_offset, burner_3_central_size, burner_3_central_offset, burner_4_size, burner_4_thickness, burner_4_offset, burner_4_central_size, burner_4_central_offset, burner_5_size, burner_5_thickness, burner_5_offset, burner_5_central_size, burner_5_central_offset, burner_6_size, burner_6_thickness, burner_6_offset, burner_6_central_size, burner_6_central_offset, num_burners, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.bottom_size = bottom_size
        self.burner_1_size = burner_1_size
        self.burner_1_thickness = burner_1_thickness
        self.burner_1_offset = burner_1_offset
        self.burner_1_central_size = burner_1_central_size
        self.burner_1_central_offset = burner_1_central_offset
        self.burner_2_size = burner_2_size
        self.burner_2_thickness = burner_2_thickness
        self.burner_2_offset = burner_2_offset
        self.burner_2_central_size = burner_2_central_size
        self.burner_2_central_offset = burner_2_central_offset
        self.burner_3_size = burner_3_size
        self.burner_3_thickness = burner_3_thickness
        self.burner_3_offset = burner_3_offset
        self.burner_3_central_size = burner_3_central_size
        self.burner_3_central_offset = burner_3_central_offset
        self.burner_4_size = burner_4_size
        self.burner_4_thickness = burner_4_thickness
        self.burner_4_offset = burner_4_offset
        self.burner_4_central_size = burner_4_central_size
        self.burner_4_central_offset = burner_4_central_offset
        self.burner_5_size = burner_5_size
        self.burner_5_thickness = burner_5_thickness
        self.burner_5_offset = burner_5_offset
        self.burner_5_central_size = burner_5_central_size
        self.burner_5_central_offset = burner_5_central_offset
        self.burner_6_size = burner_6_size
        self.burner_6_thickness = burner_6_thickness
        self.burner_6_offset = burner_6_offset
        self.burner_6_central_size = burner_6_central_size
        self.burner_6_central_offset = burner_6_central_offset
        self.num_burners = num_burners

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_position = [
            0,
            bottom_size[1] / 2,
            0
        ]
        self.mesh = Cuboid(bottom_size[1], bottom_size[0], bottom_size[2],
                           position = mesh_position)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        for i in range(num_burners[0]):
            mesh_position = [
                locals()['burner_%d_offset'%(i+1)][0], 
                bottom_size[1] + locals()['burner_%d_size'%(i+1)][1] / 2, 
                locals()['burner_%d_offset'%(i+1)][1]
            ]
            self.mesh = Rectangular_Ring(locals()['burner_%d_size'%(i+1)][1], locals()['burner_%d_size'%(i+1)][0], locals()['burner_%d_size'%(i+1)][2], 
                                         locals()['burner_%d_size'%(i+1)][0] - locals()['burner_%d_thickness'%(i+1)][0] * 2,
                                         locals()['burner_%d_size'%(i+1)][2] - locals()['burner_%d_thickness'%(i+1)][0] * 2,
                                         position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

            center_mesh_position = [
                locals()['burner_%d_offset'%(i+1)][0] + locals()['burner_%d_central_offset'%(i+1)][0], 
                bottom_size[1] + locals()['burner_%d_central_size'%(i+1)][1] / 2, 
                locals()['burner_%d_offset'%(i+1)][1] + locals()['burner_%d_central_offset'%(i+1)][1]
            ]
            self.center_mesh = Cylinder(locals()['burner_%d_central_size'%(i+1)][1], locals()['burner_%d_central_size'%(i+1)][0],
                                        position = center_mesh_position)
            vertices_list.append(self.center_mesh.vertices)
            faces_list.append(self.center_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.center_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Burner'
