"""
Jaw Templates
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


# Source: Clip/concept_template.py
class Regular_jaw(ConceptTemplate):
    def __init__(self, size, jaw_separation, jaw_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        jaw_rotation = [x / 180 * np.pi for x in jaw_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.jaw_separation = jaw_separation
        self.jaw_rotation = jaw_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_1_position = [0, 0, jaw_separation[0]]
        mesh_1_rotation = [-jaw_rotation[0], 0, 0]
        self.mesh_1 = Cuboid(size[1], size[0], size[2], position=mesh_1_position)
        self.mesh_1.vertices = apply_transformation(
            self.mesh_1.vertices, [0, 0, 0], mesh_1_rotation
        )
        vertices_list.append(self.mesh_1.vertices)
        faces_list.append(self.mesh_1.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_1.vertices)

        mesh_2_position = [0, 0, -jaw_separation[0]]
        mesh_2_rotation = [jaw_rotation[0], 0, 0]
        self.mesh_2 = Cuboid(size[1], size[0], size[2], position=mesh_2_position)
        self.mesh_2.vertices = apply_transformation(
            self.mesh_2.vertices, [0, 0, 0], mesh_2_rotation
        )
        vertices_list.append(self.mesh_2.vertices)
        faces_list.append(self.mesh_2.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_2.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Jaw'


# Source: Clip/concept_template.py
class Curved_jaw(ConceptTemplate):
    def __init__(self, size, central_angle, jaw_separation, jaw_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):
        
        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        central_angle = [x / 180 * np.pi for x in central_angle]
        jaw_rotation = [x / 180 * np.pi for x in jaw_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.central_angle = central_angle
        self.jaw_separation = jaw_separation
        self.jaw_rotation = jaw_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        jaw_mesh_1_pre_rotation = [np.pi, np.pi / 2, -np.pi / 2]
        self.jaw_mesh_1 = Ring(size[2], size[0], size[1], exist_angle=central_angle[0], rotation=jaw_mesh_1_pre_rotation)
        jaw_mesh_1_position = [0, 0, -(size[0] + size[1]) / 2]
        jaw_mesh_1_rotation_matrix = get_rodrigues_matrix([1, 0, 0], jaw_rotation[0])
        self.jaw_mesh_1.vertices = (self.jaw_mesh_1.vertices - jaw_mesh_1_position) @ jaw_mesh_1_rotation_matrix.T + jaw_mesh_1_position
        self.jaw_mesh_1.vertices = apply_transformation(self.jaw_mesh_1.vertices, [0, 0, (size[0] + size[1]) / 2-jaw_separation[0]], [0, 0, 0])
        vertices_list.append(self.jaw_mesh_1.vertices)
        faces_list.append(self.jaw_mesh_1.faces + total_num_vertices)
        total_num_vertices += len(self.jaw_mesh_1.vertices)

        self.jaw_mesh_2 = copy.deepcopy(self.jaw_mesh_1)
        self.jaw_mesh_2.vertices = np.asarray(self.jaw_mesh_2.vertices)
        self.jaw_mesh_2.vertices[:, 2] = -self.jaw_mesh_2.vertices[:, 2]
        self.jaw_mesh_2.faces = np.asarray(self.jaw_mesh_2.faces)
        self.jaw_mesh_2.faces = self.jaw_mesh_2.faces[:, [0, 2, 1]]
        vertices_list.append(self.jaw_mesh_2.vertices)
        faces_list.append(self.jaw_mesh_2.faces + total_num_vertices)
        total_num_vertices += len(self.jaw_mesh_2.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Jaw'
