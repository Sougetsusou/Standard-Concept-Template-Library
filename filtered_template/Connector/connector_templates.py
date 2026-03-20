"""
Connector Templates
Automatically extracted from concept_template.py files
Contains 8 class(es)
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
class Cylindrical_Connecter(ConceptTemplate):
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

        self.mesh = Cylinder(size[1], size[0])
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Connector'


# Source: Safe/concept_template.py
class T_Shaped_Connecter(ConceptTemplate):
    def __init__(self, cylinder_size, lateral_cuboid_size, lateral_cuboid_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.cylinder_size = cylinder_size
        self.lateral_cuboid_size = lateral_cuboid_size
        self.lateral_cuboid_offset = lateral_cuboid_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.mesh = Cylinder(cylinder_size[1], cylinder_size[0])
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        beside_mesh_position = [
            cylinder_size[0] + lateral_cuboid_size[0] / 2,
            lateral_cuboid_offset[0],
            -cylinder_size[0] + lateral_cuboid_size[2] / 2
        ]
        self.beside_mesh = Cuboid(lateral_cuboid_size[1], lateral_cuboid_size[0], lateral_cuboid_size[2], 
                                  position = beside_mesh_position)
        vertices_list.append(self.beside_mesh.vertices)
        faces_list.append(self.beside_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.beside_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Connector'


# Source: USB/concept_template.py
class Simplied_Connector(ConceptTemplate):
    def __init__(self, size, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        back_mesh_position = [0, 0, size[2] / 2]
        self.main_mesh = Cuboid(size[1], size[0], size[2],
                                position=back_mesh_position)
        vertices_list.append(self.main_mesh.vertices)
        faces_list.append(self.main_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.main_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Connector'


# Source: USB/concept_template.py
class Regular_Connector(ConceptTemplate):
    def __init__(self, size, thickness, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.thickness = thickness

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        main_mesh_position = [0, 0, size[2] / 2]
        main_mesh_rotation = [np.pi / 2, 0, 0]
        self.main_mesh = Rectangular_Ring(size[2], size[0], size[1],
                                          size[0] - thickness[0] * 2, size[1] / 2 - thickness[0],
                                          [0, thickness[0] / 2 - size[1] / 4],
                                          rotation=main_mesh_rotation,
                                          position=main_mesh_position)
        vertices_list.append(self.main_mesh.vertices)
        faces_list.append(self.main_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.main_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Connector'


# Source: Eyeglasses/concept_template.py
class Standard_Connector(ConceptTemplate):
    def __init__(self, size, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        connector_mesh_position = [
            0, 
            0, 
            -size[2] / 2
        ]
        self.connector_mesh = Cuboid(size[1], size[0], size[2],
                                     position=connector_mesh_position)
        vertices_list.append(self.connector_mesh.vertices)
        faces_list.append(self.connector_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.connector_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Connector'


# Source: Eyeglasses/concept_template.py
class Dual_Connector(ConceptTemplate):
    def __init__(self, size_1, offset_1, size_2, offset_2, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size_1 = size_1
        self.offset_1 = offset_1
        self.size_2 = size_2
        self.offset_2 = offset_2

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        top_mesh_position = [
            offset_1[0], 
            offset_1[1], 
            offset_1[2] - size_1[2] / 2
        ]
        self.top_mesh = Cuboid(size_1[1], size_1[0], size_1[2],
                               position=top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [
            offset_2[0], 
            offset_2[1], 
            offset_2[2] - size_2[2] / 2
        ]
        self.bottom_mesh = Cuboid(size_2[1], size_2[0], size_2[2],
                                  position=bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)
        
        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Connector'


# Source: Laptop/concept_template.py
class Cuboidal_Connector(ConceptTemplate):
    def __init__(self, number_of_connector, size, separation,offset, connector_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        connector_rotation = [x / 180 * np.pi for x in connector_rotation]    
        super().__init__(position, rotation)

        # Record Parameters
        self.number_of_connector = number_of_connector
        self.size = size
        self.offset = offset
        self.separation = separation
        self.connector_rotation = connector_rotation
        
        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0
        
        for i in range(number_of_connector[0]):
            back_mesh_position = [
                offset[0] + i * size[0] + sum(separation[0:i]) + size[0] / 2, 
                offset[1], 
                offset[2]
            ]
            back_mesh_rotation = [connector_rotation[0], 0, 0]
            self.back_mesh = Cuboid(size[1], size[0], size[2],
                                    position=back_mesh_position,
                                    rotation=back_mesh_rotation)
            vertices_list.append(self.back_mesh.vertices)
            faces_list.append(self.back_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.back_mesh.vertices)

        self.vertices=np.concatenate(vertices_list)
        self.faces=np.concatenate(faces_list)

        # Global Transformation
        self.vertices=apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Connector'


# Source: Laptop/concept_template.py
class Cylindrical_Connector(ConceptTemplate):
    def __init__(self, number_of_connector, size, separation, offset, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)  

        # Record Parameters
        self.number_of_connector = number_of_connector
        self.size = size
        self.offset = offset
        self.separation = separation
        
        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0
         
        for i in range(number_of_connector[0]):
            back_mesh_position = [
                offset[0] + i * size[1] + sum(separation[0:i]) + size[1] / 2, 
                offset[1], 
                offset[2]
            ]
            back_mesh_rotation = [0, 0, np.pi / 2]
            self.back_mesh = Cylinder(size[1], size[0], size[0],
                                      position=back_mesh_position,
                                      rotation=back_mesh_rotation)
            vertices_list.append(self.back_mesh.vertices)
            faces_list.append(self.back_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.back_mesh.vertices)

        self.vertices=np.concatenate(vertices_list)
        self.faces=np.concatenate(faces_list)
        
        # Global Transformation
        self.vertices=apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Connector'
