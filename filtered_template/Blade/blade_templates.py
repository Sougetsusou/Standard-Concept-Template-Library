"""
Blade Templates
Automatically extracted from concept_template.py files
Contains 6 class(es)
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


# Source: Scissors/concept_template.py
class Cusp_Blade(ConceptTemplate):
    def __init__(self, root_size, root_z_offset, tip_length, tip_z_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.root_size = root_size
        self.root_z_offset = root_z_offset
        self.tip_length = tip_length
        self.tip_z_offset = tip_z_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        root_mesh_position = [
            -root_size[0] / 2, 
            0,
            0
        ]
        root_mesh_rotation = [np.pi / 2, -np.pi / 2, 0]
        self.root_mesh = Cuboid(root_size[0], root_size[3], root_size[1], 
                                root_size[2], root_size[1], 
                                top_offset = [root_z_offset[0], 0],
                                position = root_mesh_position,
                                rotation = root_mesh_rotation)
        vertices_list.append(self.root_mesh.vertices)
        faces_list.append(self.root_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.root_mesh.vertices)

        tip_mesh_position = [
            -root_size[0] - tip_length[0] / 2, 
            0,
            root_z_offset[0]
        ]
        tip_mesh_rotation = [np.pi / 2, -np.pi / 2, 0]
        self.tip_mesh = Cuboid(tip_length[0], 0, root_size[1], 
                                root_size[3], root_size[1], 
                                top_offset = [tip_z_offset[0], 0],
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

        self.semantic = 'Blade'


# Source: Scissors/concept_template.py
class Curved_Blade(ConceptTemplate):
    def __init__(self, root_size, root_z_offset, tip_length, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.root_size = root_size
        self.root_z_offset = root_z_offset
        self.tip_length = tip_length

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        root_mesh_position = [
            -root_size[0] / 2, 
            0,
            0
        ]
        root_mesh_rotation = [np.pi / 2, -np.pi / 2, 0]
        self.root_mesh = Cuboid(root_size[0], root_size[3], root_size[1], 
                                root_size[2], root_size[1], 
                                top_offset = [root_z_offset[0], 0],
                                position = root_mesh_position,
                                rotation = root_mesh_rotation)
        vertices_list.append(self.root_mesh.vertices)
        faces_list.append(self.root_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.root_mesh.vertices)

        tip_mesh_position = [
            -root_size[0], 
            0,
            -root_size[3] / 2 + root_z_offset[0]
        ]
        tip_mesh_rotation = [0, 0, np.pi]
        self.tip_mesh = Cylinder(root_size[1], tip_length[0], tip_length[0],
                                  top_radius_z = root_size[3], bottom_radius_z = root_size[3],
                                  is_quarter = True,
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

        self.semantic = 'Blade'


# Source: Shaver/concept_template.py
class Regular_Blade(ConceptTemplate):
    def __init__(self, bottom_size, top_size, top_bottom_offset, root_offset, blade_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        blade_rotation = [-x / 180 * np.pi for x in blade_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.bottom_size = bottom_size
        self.top_size = top_size
        self.top_bottom_offset = top_bottom_offset
        self.root_offset = root_offset
        self.blade_rotation = blade_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            bottom_size[0] / 2 - root_offset[0], 
            -bottom_size[1] / 2, 
            0
        ]
        self.bottom_mesh = Cuboid(bottom_size[1], bottom_size[0], bottom_size[2],
                                  position=bottom_mesh_position)
        self.bottom_mesh.vertices = apply_transformation(self.bottom_mesh.vertices, [0, 0, 0], [0, 0, blade_rotation[0]])
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        top_mesh_position = [
            bottom_size[0] + top_size[0] / 2 - root_offset[0],
            top_bottom_offset[0] - bottom_size[1] / 2,
            0,
        ]
        self.top_mesh = Cuboid(top_size[1], top_size[0], top_size[2],
                               position=top_mesh_position)
        self.top_mesh.vertices = apply_transformation(self.top_mesh.vertices, [0, 0, 0], [0, 0, blade_rotation[0]])
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Blade'


# Source: Knife/concept_template.py
class Cuboidal_Blade(ConceptTemplate):
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

        self.semantic = 'Blade'


# Source: Knife/concept_template.py
class Cusp_Blade(ConceptTemplate):
    def __init__(self, root_size, root_z_offset, tip_length, tip_z_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.root_size = root_size
        self.root_z_offset = root_z_offset
        self.tip_length = tip_length
        self.tip_z_offset = tip_z_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_position = [
            0, 
            root_size[1] / 2,
            0
        ]
        self.mesh = Cuboid(root_size[1], root_size[0], root_size[3],
                           root_size[0], root_size[2],
                           top_offset = [0, root_z_offset[0]],
                           position = mesh_position)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        tip_mesh_position = [
            0, 
            root_size[1] + tip_length[0] / 2,
            root_z_offset[0]
        ]
        self.tip_mesh = Cuboid(tip_length[0], root_size[0], 0,
                               root_size[0], root_size[3],
                               top_offset = [0, tip_z_offset[0]],
                               position = tip_mesh_position)
        vertices_list.append(self.tip_mesh.vertices)
        faces_list.append(self.tip_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.tip_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Blade'


# Source: Knife/concept_template.py
class Curved_Blade(ConceptTemplate):
    def __init__(self, root_size, root_z_offset, tip_length, tip_angle, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        tip_angle = [x / 180 * np.pi for x in tip_angle]
        super().__init__(position, rotation)

        # Record Parameters
        self.root_size = root_size
        self.root_z_offset = root_z_offset
        self.tip_length = tip_length
        self.tip_angle = tip_angle

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_position = [
            0, 
            root_size[1] / 2,
            0
        ]
        self.mesh = Cuboid(root_size[1], root_size[0], root_size[3],
                           root_size[0], root_size[2],
                           top_offset = [0, root_z_offset[0]],
                           position = mesh_position)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        tip_mesh_position = [
            0, 
            root_size[1],
            root_z_offset[0] - root_size[3] / 2
        ]
        tip_mesh_rotation = [0, 0, np.pi / 2]
        self.tip_mesh = Cylinder(root_size[0], tip_length[0], tip_length[0],
                                 root_size[3], root_size[3],
                                 is_quarter = True,
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

        self.semantic = 'Blade'
