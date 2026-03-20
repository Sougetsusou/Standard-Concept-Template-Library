"""
Door Templates
Automatically extracted from concept_template.py files
Contains 17 class(es)
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


# Source: Microwave/concept_template.py
class Cuboidal_Door(ConceptTemplate):
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
            0,
            size[2] / 2
        ]
        self.mesh = Cuboid(size[1], size[0], size[2],
                           position = mesh_position) 
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)\
        
        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Door'


# Source: Microwave/concept_template.py
class Sunken_Door(ConceptTemplate):
    def __init__(self, size, sunken_size, sunken_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.sunken_size = sunken_size
        self.sunken_offset = sunken_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0,
            0,
            -sunken_size[2] / 2 + size[2] / 2
        ]
        self.bottom_mesh = Cuboid(size[1], size[0], size[2] - sunken_size[2], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        top_mesh_position = [
            0,
            0,
            (size[2] - sunken_size[2]) / 2 + size[2] / 2
        ]
        top_mesh_rotation = [np.pi / 2, 0, 0]
        self.top_mesh = Rectangular_Ring(sunken_size[2], size[0], size[1], 
                                         sunken_size[0], sunken_size[1],
                                         [sunken_offset[0], -sunken_offset[1]],
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

        self.semantic = 'Door'


# Source: Safe/concept_template.py
class Cuboidal_Door(ConceptTemplate):
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
            0,
            size[2] / 2
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

        self.semantic = 'Door'


# Source: Safe/concept_template.py
class Behind_Double_Layer_Door(ConceptTemplate):
    def __init__(self, main_size, behind_size, behind_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.main_size = main_size
        self.behind_size = behind_size
        self.behind_offset = behind_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_position = [
            0,
            0,
            main_size[2] / 2
        ]
        self.mesh = Cuboid(main_size[1], main_size[0], main_size[2],
                           position = mesh_position) 
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        behind_mesh_position = [
            behind_offset[0],
            behind_offset[1],
            -behind_size[2] / 2
        ]
        self.behind_mesh = Cuboid(behind_size[1], behind_size[0], behind_size[2],
                                  position = behind_mesh_position) 
        vertices_list.append(self.behind_mesh.vertices)
        faces_list.append(self.behind_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.behind_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Door'


# Source: Safe/concept_template.py
class Front_Double_Layer_Door(ConceptTemplate):
    def __init__(self, main_size, front_size, front_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.main_size = main_size
        self.front_size = front_size
        self.front_offset = front_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_position = [
            0,
            0,
            main_size[2] / 2
        ]
        self.mesh = Cuboid(main_size[1], main_size[0], main_size[2],
                           position = mesh_position) 
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        front_mesh_position = [
            front_offset[0],
            front_offset[1],
            main_size[2] + front_size[2] / 2
        ]
        self.front_mesh = Cuboid(front_size[1], front_size[0], front_size[2],
                                  position = front_mesh_position) 
        vertices_list.append(self.front_mesh.vertices)
        faces_list.append(self.front_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.front_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Door'


# Source: Safe/concept_template.py
class Sunken_Door(ConceptTemplate):
    def __init__(self, size, sunken_size, sunken_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.sunken_size = sunken_size
        self.sunken_offset = sunken_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0,
            0,
            -sunken_size[2] / 2 + size[2] / 2
        ]
        self.bottom_mesh = Cuboid(size[1], size[0], size[2] - sunken_size[2], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        top_mesh_position = [
            0,
            0,
            (size[2] - sunken_size[2]) / 2 + size[2] / 2
        ]
        top_mesh_rotation = [np.pi / 2, 0, 0]
        self.top_mesh = Rectangular_Ring(sunken_size[2], size[0], size[1], 
                                         sunken_size[0], sunken_size[1],
                                         [sunken_offset[0], -sunken_offset[1]],
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

        self.semantic = 'Door'


# Source: Oven/concept_template.py
class Cuboidal_Door(ConceptTemplate):
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
            0,
            size[2] / 2
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

        self.semantic = 'Door'


# Source: Oven/concept_template.py
class Sunken_Door(ConceptTemplate):
    def __init__(self, size, sunken_size, sunken_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.sunken_size = sunken_size
        self.sunken_offset = sunken_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0,
            0,
            -sunken_size[2] / 2 + size[2] / 2
        ]
        self.bottom_mesh = Cuboid(size[1], size[0], size[2] - sunken_size[2], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        top_mesh_position = [
            0,
            0,
            (size[2] - sunken_size[2]) / 2 + size[2] / 2
        ]
        top_mesh_rotation = [np.pi / 2, 0, 0]
        self.top_mesh = Rectangular_Ring(sunken_size[2], size[0], size[1], 
                                         sunken_size[0], sunken_size[1],
                                         [sunken_offset[0], -sunken_offset[1]],
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

        self.semantic = 'Door'


# Source: Dishwasher/concept_template.py
class Cuboidal_Door(ConceptTemplate):
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
            0,
            size[2] / 2
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

        self.semantic = 'Door'


# Source: Dishwasher/concept_template.py
class Sunken_Door(ConceptTemplate):
    def __init__(self, size, sunken_size, sunken_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.sunken_size = sunken_size
        self.sunken_offset = sunken_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0,
            0,
            -sunken_size[2] / 2 + size[2] / 2
        ]
        self.bottom_mesh = Cuboid(size[1], size[0], size[2] - sunken_size[2], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        top_mesh_position = [
            0,
            0,
            (size[2] - sunken_size[2]) / 2 + size[2] / 2
        ]
        top_mesh_rotation = [np.pi / 2, 0, 0]
        self.top_mesh = Rectangular_Ring(sunken_size[2], size[0], size[1], 
                                         sunken_size[0], sunken_size[1],
                                         [sunken_offset[0], -sunken_offset[1]],
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

        self.semantic = 'Door'


# Source: StorageFurniture/concept_template.py
class Regular_door(ConceptTemplate):
    def __init__(self, number_of_door, doors_params, position=[0, 0, 0], rotation=[0, 0, 0]):
        
        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        doors_params = [x / 180 * np.pi if i % 12 in [8] else x for i, x in enumerate(doors_params)]
        super().__init__(position, rotation)

        # Record Parameters
        self.number_of_door = number_of_door
        self.door_size = [doors_params[i * 12: i * 12 + 3] for i in range(number_of_door[0])]
        self.handle_size = [doors_params[i * 12 + 3: i * 12 + 6] for i in range(number_of_door[0])]
        self.handle_offset = [doors_params[i * 12 + 6: i * 12 + 8] for i in range(number_of_door[0])]
        self.door_rotation = [doors_params[i * 12 + 8] for i in range(number_of_door[0])]
        self.door_offset = [doors_params[i * 12 + 9: i * 12 + 12] for i in range(number_of_door[0])]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for door_idx in range(self.number_of_door[0]):
            for mesh_idx in range(2):
                if mesh_idx == 0:
                    mesh_rotation = [0, self.door_rotation[door_idx], 0]
                    mesh_position = [self.door_offset[door_idx][0],
                                     self.door_offset[door_idx][1],
                                     self.door_offset[door_idx][2]]
                    self.mesh = Cuboid(self.door_size[door_idx][1], self.door_size[door_idx][0], self.door_size[door_idx][2], position=mesh_position, rotation=mesh_rotation)
                else:
                    mesh_rotation = [0, self.door_rotation[door_idx], 0]
                    mesh_position = [
                        self.door_offset[door_idx][0] + self.handle_offset[door_idx][0] * np.cos(self.door_rotation[door_idx]) + self.handle_size[door_idx][2] / 2 * np.sin(
                            self.door_rotation[door_idx]),
                        self.door_offset[door_idx][1] + self.handle_offset[door_idx][1],
                        self.door_offset[door_idx][2] - self.handle_offset[door_idx][0] * np.sin(self.door_rotation[door_idx]) + self.handle_size[door_idx][2] / 2 * np.cos(
                            self.door_rotation[door_idx])]
                    self.mesh = Cuboid(self.handle_size[door_idx][1], self.handle_size[door_idx][0], self.handle_size[door_idx][2], position=mesh_position, rotation=mesh_rotation)

                vertices_list.append(self.mesh.vertices)
                faces_list.append(self.mesh.faces + total_num_vertices)
                total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Door'


# Source: Table/concept_template.py
class Regular_door(ConceptTemplate):
    def __init__(self, number_of_door, doors_params, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        doors_params = [x / 180 * np.pi if i % 13 in [6, 9] else x for i, x in enumerate(doors_params)]
        super().__init__(position, rotation)

        # Record Parameters
        self.number_of_door = number_of_door
        self.door_size = [doors_params[i * 13: i * 13 + 3] for i in range(number_of_door[0])]
        self.handle_size = [doors_params[i * 13 + 3: i * 13 + 6] for i in range(number_of_door[0])]
        self.handle_rotation = [doors_params[i * 13 + 6] for i in range(number_of_door[0])]
        self.handle_offset = [doors_params[i * 13 + 7: i * 13 + 9] for i in range(number_of_door[0])]
        self.door_rotation = [doors_params[i * 13 + 9] for i in range(number_of_door[0])]
        self.door_offset = [doors_params[i * 13 + 10: i * 13 + 13] for i in range(number_of_door[0])]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for door_idx in range(self.number_of_door[0]):
            for mesh_idx in range(2):
                if mesh_idx == 0:
                    mesh_rotation = [0, self.door_rotation[door_idx], 0]
                    mesh_position = [self.door_offset[door_idx][0],
                                     self.door_offset[door_idx][1] - self.door_size[door_idx][1] / 2,
                                     self.door_offset[door_idx][2]]
                    self.mesh = Cuboid(self.door_size[door_idx][1], self.door_size[door_idx][0], self.door_size[door_idx][2],
                                       position=mesh_position, rotation=mesh_rotation)
                else:
                    mesh_rotation = [0, self.door_rotation[door_idx], self.handle_rotation[door_idx]]
                    mesh_position = [
                        self.door_offset[door_idx][0] + self.handle_offset[door_idx][0] * np.cos(self.door_rotation[door_idx]) + self.handle_size[door_idx][2] / 2 * np.sin(
                            self.door_rotation[door_idx]),
                        self.door_offset[door_idx][1] - self.door_size[door_idx][1] / 2 + self.handle_offset[door_idx][1],
                        self.door_offset[door_idx][2] - self.handle_offset[door_idx][0] * np.sin(self.door_rotation[door_idx]) + self.handle_size[door_idx][2] / 2 * np.cos(
                            self.door_rotation[door_idx])]
                    self.mesh = Cuboid(self.handle_size[door_idx][1], self.handle_size[door_idx][0], self.handle_size[door_idx][2],
                                       position=mesh_position, rotation=mesh_rotation)
                vertices_list.append(self.mesh.vertices)
                faces_list.append(self.mesh.faces + total_num_vertices)
                total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Door'


# Source: Washingmachine/concept_template.py
class Roller_Door(ConceptTemplate):
    def __init__(self, circle_size, middle_size, middle_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.circle_size = circle_size
        self.middle_size = middle_size
        self.middle_offset = middle_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        circle_mesh_position = [
            circle_size[0],
            0,
            circle_size[2] / 2
        ]
        circle_mesh_rotation = [np.pi / 2, 0, 0]
        self.circle_mesh = Ring(circle_size[2], circle_size[0], circle_size[1],
                                position = circle_mesh_position,
                                rotation = circle_mesh_rotation) 
        vertices_list.append(self.circle_mesh.vertices)
        faces_list.append(self.circle_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.circle_mesh.vertices)

        middle_mesh_position = [
            circle_size[0],
            0,
            circle_size[2] / 2
        ]
        middle_mesh_rotation = [np.pi / 2, 0, 0]
        self.middle_mesh = Ring(middle_size[1], circle_size[1], middle_size[0],
                                inner_offset = middle_offset,
                                position = middle_mesh_position,
                                rotation = middle_mesh_rotation) 
        vertices_list.append(self.middle_mesh.vertices)
        faces_list.append(self.middle_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.middle_mesh.vertices)

        center_mesh_position = [
            circle_size[0],
            middle_offset[0],
            circle_size[2] / 2 + middle_offset[1]
        ]
        center_mesh_rotation = [np.pi / 2, 0, 0]
        self.center_mesh = Cylinder(middle_size[1], middle_size[0],
                                    position = center_mesh_position,
                                    rotation = center_mesh_rotation) 
        vertices_list.append(self.center_mesh.vertices)
        faces_list.append(self.center_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.center_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Door'


# Source: Washingmachine/concept_template.py
class Cuboidal_Door(ConceptTemplate):
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

        self.semantic = 'Door'


# Source: Refrigerator/concept_template.py
class Cuboidal_Door(ConceptTemplate):
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
            0,
            size[2] / 2
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

        self.semantic = 'Door'


# Source: Refrigerator/concept_template.py
class Sunken_Door(ConceptTemplate):
    def __init__(self, size, sunken_size, sunken_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.sunken_size = sunken_size
        self.sunken_offset = sunken_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0,
            0,
            -sunken_size[2] / 2 + size[2] / 2
        ]
        self.bottom_mesh = Cuboid(size[1], size[0], size[2] - sunken_size[2], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        top_mesh_position = [
            0,
            0,
            (size[2] - sunken_size[2]) / 2 + size[2] / 2
        ]
        top_mesh_rotation = [np.pi / 2, 0, 0]
        self.top_mesh = Rectangular_Ring(sunken_size[2], size[0], size[1], 
                                         sunken_size[0], sunken_size[1],
                                         [sunken_offset[0], -sunken_offset[1]],
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

        self.semantic = 'Door'


# Source: Door/concept_template.py
class Standard_Door(ConceptTemplate):
    def __init__(self, existence_of_door, size, door_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        door_rotation = [x / 180 * np.pi for x in door_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.existence_of_door = existence_of_door
        self.size = size
        self.door_rotation = door_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        if existence_of_door[0] and existence_of_door[1]:
            left_mesh_position = [size[0] / 2, 0, 0]
            self.left_mesh = Cuboid(size[1], size[0], size[2],
                                    position=left_mesh_position)
            self.left_mesh.vertices = apply_transformation(self.left_mesh.vertices, rotation=[0, -door_rotation[0], 0], position=[-size[0], 0, 0])
            vertices_list.append(self.left_mesh.vertices)
            faces_list.append(self.left_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.left_mesh.vertices)

            self.right_mesh = Cuboid(size[1], size[0], size[2],
                                     position=[-size[0] / 2, 0, 0])
            self.right_mesh.vertices = apply_transformation(self.right_mesh.vertices, rotation=[0, door_rotation[1], 0], position=[size[0], 0, 0])
            vertices_list.append(self.right_mesh.vertices)
            faces_list.append(self.right_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.right_mesh.vertices)

        elif existence_of_door[0]:
            left_mesh_position = [size[0] / 2, 0, 0]
            self.left_mesh = Cuboid(size[1], size[0], size[2],
                                    position=left_mesh_position)
            self.left_mesh.vertices = apply_transformation(self.left_mesh.vertices, rotation=[0, -door_rotation[0], 0], position=[-size[0] / 2, 0, 0])
            vertices_list.append(self.left_mesh.vertices)
            faces_list.append(self.left_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.left_mesh.vertices)

        elif existence_of_door[1]:
            self.right_mesh = Cuboid(size[1], size[0], size[2],
                                     position=[-size[0] / 2, 0, 0])
            self.right_mesh.vertices = apply_transformation(self.right_mesh.vertices, rotation=[0, door_rotation[1], 0], position=[size[0] / 2, 0, 0])
            vertices_list.append(self.right_mesh.vertices)
            faces_list.append(self.right_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.right_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Door'
