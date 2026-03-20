"""
Back Templates
Automatically extracted from concept_template.py files
Contains 5 class(es)
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


# Source: Chair/concept_template.py
class Solid_back(ConceptTemplate):
    def __init__(self, size, back_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        back_rotation = [x / 180 * np.pi for x in back_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.back_rotation = back_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_rotation = [back_rotation[0], 0, 0]
        mesh_position = [0, size[1] / 2 * np.cos(back_rotation[0]), 0]
        self.back_mesh = Cuboid(self.size[1], self.size[0], self.size[2], 
                                position=mesh_position, rotation=mesh_rotation)
        vertices_list.append(self.back_mesh.vertices)
        faces_list.append(self.back_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.back_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Back'


# Source: Chair/concept_template.py
class Ladder_back(ConceptTemplate):
    def __init__(self, main_horizontal_piece_size, main_vertical_piece_size, sub_horizontal_piece_size,
                 main_vertical_separation, sub_offset, interval_between_subs, back_rotation, number_of_subs,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        back_rotation = [x / 180 * np.pi for x in back_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.main_horizontal_piece_size = main_horizontal_piece_size
        self.main_vertical_piece_size = main_vertical_piece_size
        self.sub_horizontal_piece_size = sub_horizontal_piece_size
        self.main_vertical_separation = main_vertical_separation
        self.sub_offset = sub_offset
        self.interval_between_subs = interval_between_subs
        self.back_rotation = back_rotation
        self.number_of_subs = number_of_subs

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(3 + number_of_subs[0]):
            mesh_rotation = [back_rotation[0], 0, 0]
            if i < 2:
                flag = 1 if i == 1 else -1
                vertical_position = [flag * main_vertical_separation[0] / 2,
                                     main_vertical_piece_size[1] / 2 * np.cos(back_rotation[0]), 0]
                self.mesh = Cuboid(self.main_vertical_piece_size[1], self.main_vertical_piece_size[0],
                                   self.main_vertical_piece_size[2],
                                   position=vertical_position, rotation=mesh_rotation)
            elif i == 2:
                horizontal_position = [0,
                                       (main_vertical_piece_size[1] + main_horizontal_piece_size[1] / 2) * np.cos(
                                           back_rotation[0]),
                                       (main_vertical_piece_size[1] + main_horizontal_piece_size[1]) / 2 * np.sin(
                                           back_rotation[0])]
                self.mesh = Cuboid(self.main_horizontal_piece_size[1], self.main_horizontal_piece_size[0],
                                   self.main_horizontal_piece_size[2],
                                   position=horizontal_position, rotation=mesh_rotation)
            else:
                sub_position = [0, (main_vertical_piece_size[1] / 2 + sub_offset[0] - (i - 3) * interval_between_subs[
                    0]) * np.cos(back_rotation[0]),
                                (sub_offset[0] - (i - 3) * interval_between_subs[0]) * np.sin(back_rotation[0])]
                self.mesh = Cuboid(self.sub_horizontal_piece_size[0],
                                   self.main_vertical_separation[0] - self.main_vertical_piece_size[0],
                                   self.sub_horizontal_piece_size[1],
                                   position=sub_position, rotation=mesh_rotation)

            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Back' 


# Source: Chair/concept_template.py
class Splat_back(ConceptTemplate):
    def __init__(self, main_horizontal_piece_size, main_vertical_piece_size, sub_vertical_piece_size,
                 main_vertical_separation, sub_offset, interval_between_subs, back_rotation, number_of_subs,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        back_rotation = [x / 180 * np.pi for x in back_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.main_horizontal_piece_size = main_horizontal_piece_size
        self.main_vertical_piece_size = main_vertical_piece_size
        self.sub_vertical_piece_size = sub_vertical_piece_size
        self.main_vertical_separation = main_vertical_separation
        self.sub_offset = sub_offset
        self.interval_between_subs = interval_between_subs
        self.back_rotation = back_rotation
        self.number_of_subs = number_of_subs

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(3 + number_of_subs[0]):
            mesh_rotation = [back_rotation[0], 0, 0]
            if i < 2:
                flag = 1 if i == 1 else -1
                vertical_position = [flag * main_vertical_separation[0] / 2,
                                     main_vertical_piece_size[1] / 2 * np.cos(back_rotation[0]), 0]
                self.mesh = Cuboid(self.main_vertical_piece_size[1], self.main_vertical_piece_size[0],
                                   self.main_vertical_piece_size[2],
                                   position=vertical_position, rotation=mesh_rotation)
            elif i == 2:
                horizontal_position = [0,
                                       (main_vertical_piece_size[1] + main_horizontal_piece_size[1] / 2) * np.cos(
                                           back_rotation[0]),
                                       (main_vertical_piece_size[1] + main_horizontal_piece_size[1]) / 2 * np.sin(
                                           back_rotation[0])]
                self.mesh = Cuboid(self.main_horizontal_piece_size[1], self.main_horizontal_piece_size[0],
                                   self.main_horizontal_piece_size[2],
                                   position=horizontal_position, rotation=mesh_rotation)
            else:
                sub_position = [sub_offset[0] + (i - 3) * interval_between_subs[0],
                                main_vertical_piece_size[1] / 2 * np.cos(back_rotation[0]), 0]
                self.mesh = Cuboid(self.main_vertical_piece_size[1],
                                   self.sub_vertical_piece_size[0],
                                   self.sub_vertical_piece_size[1],
                                   position=sub_position, rotation=mesh_rotation)

            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Back'


# Source: Chair/concept_template.py
class Latice_back(ConceptTemplate):
    def __init__(self, main_horizontal_piece_size, main_vertical_piece_size, main_vertical_separation,
                 sub_vertical_piece_size, sub_horizontal_piece_size, sub_horizontal_offset, sub_vertical_offset,
                 interval_between_subs, back_rotation, number_of_subs, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        back_rotation = [x / 180 * np.pi for x in back_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.main_horizontal_piece_size = main_horizontal_piece_size
        self.main_vertical_piece_size = main_vertical_piece_size
        self.sub_vertical_piece_size = sub_vertical_piece_size
        self.sub_horizontal_piece_size = sub_horizontal_piece_size
        self.main_vertical_separation = main_vertical_separation
        self.sub_horizontal_offset = sub_horizontal_offset
        self.sub_vertical_offset = sub_vertical_offset
        self.interval_between_subs = interval_between_subs
        self.back_rotation = back_rotation
        self.number_of_subs = number_of_subs

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(4 + number_of_subs[0]):
            mesh_rotation = [back_rotation[0], 0, 0]
            if i < 2:
                flag = 1 if i == 1 else -1
                vertical_position = [flag * main_vertical_separation[0] / 2,
                                     main_vertical_piece_size[1] / 2 * np.cos(back_rotation[0]), 0]
                self.mesh = Cuboid(self.main_vertical_piece_size[1], self.main_vertical_piece_size[0],
                                   self.main_vertical_piece_size[2],
                                   position=vertical_position, rotation=mesh_rotation)
            elif i == 2:
                horizontal_position = [0,
                                       (main_vertical_piece_size[1] + main_horizontal_piece_size[1] / 2) * np.cos(
                                           back_rotation[0]),
                                       (main_vertical_piece_size[1] + main_horizontal_piece_size[1]) / 2 * np.sin(
                                           back_rotation[0])]
                self.mesh = Cuboid(self.main_horizontal_piece_size[1], self.main_horizontal_piece_size[0],
                                   self.main_horizontal_piece_size[2],
                                   position=horizontal_position, rotation=mesh_rotation)
            elif i == 3:
                sub_horizontal_position = [0,
                                           (main_vertical_piece_size[1] / 2 + sub_horizontal_offset[0]) * np.cos(
                                               back_rotation[0]),
                                           sub_horizontal_offset[0] * np.sin(back_rotation[0])]
                self.mesh = Cuboid(self.sub_horizontal_piece_size[0],
                                   self.main_vertical_separation[0] - self.main_vertical_piece_size[0],
                                   self.sub_horizontal_piece_size[1],
                                   position=sub_horizontal_position, rotation=mesh_rotation)
            else:
                sub_vertical_position = [sub_vertical_offset[0] + (i - 4) * interval_between_subs[0],
                                         (main_vertical_piece_size[1] * 3 / 2 + sub_horizontal_offset[0] +
                                          sub_horizontal_piece_size[0] / 2) / 2 * np.cos(back_rotation[0]),
                                         (main_vertical_piece_size[1] / 2 + sub_horizontal_offset[0] +
                                          sub_horizontal_piece_size[0] / 2) / 2 * np.sin(back_rotation[0])]
                self.mesh = Cuboid(
                    self.main_vertical_piece_size[1] / 2 - sub_horizontal_piece_size[0] / 2 - sub_horizontal_offset[0],
                    self.sub_vertical_piece_size[0],
                    self.sub_vertical_piece_size[1],
                    position=sub_vertical_position, rotation=mesh_rotation)

            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)


        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Back'


# Source: Chair/concept_template.py
class Slat_back(ConceptTemplate):
    def __init__(self, main_vertical_piece_size, sub_horizontal_piece_size, main_vertical_separation,
                 sub_horizontal_offset, interval_between_subs, main_vertical_rotation, back_rotation, number_of_subs,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        back_rotation = [x / 180 * np.pi for x in back_rotation]
        main_vertical_rotation = [x / 180 * np.pi for x in main_vertical_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.main_vertical_piece_size = main_vertical_piece_size
        self.sub_horizontal_piece_size = sub_horizontal_piece_size
        self.main_vertical_separation = main_vertical_separation
        self.sub_horizontal_offset = sub_horizontal_offset
        self.interval_between_subs = interval_between_subs
        self.main_vertical_rotation = main_vertical_rotation
        self.back_rotation = back_rotation
        self.number_of_subs = number_of_subs

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(2 + number_of_subs[0]):
            if i < 2:
                flag = 1 if i == 1 else -1
                vertical_rotation = [back_rotation[0], flag * main_vertical_rotation[0], 0]
                vertical_position = [flag * main_vertical_separation[0] / 2,
                                     main_vertical_piece_size[1] / 2 * np.cos(back_rotation[0]), 0]
                self.mesh = Cuboid(self.main_vertical_piece_size[1], self.main_vertical_piece_size[0],
                                   self.main_vertical_piece_size[2],
                                   position=vertical_position, rotation=vertical_rotation, rotation_order="ZYX")
            else:
                sub_horizontal_rotation = [back_rotation[0], 0, 0]
                sub_horizontal_position = [0,
                                           (main_vertical_piece_size[1] / 2 + sub_horizontal_offset[0] -
                                            (i - 2) * interval_between_subs[0]) * np.cos(back_rotation[0]) -
                                           main_vertical_piece_size[0] / 2 * np.sin(main_vertical_rotation[0]) *
                                           np.sin(back_rotation[0]),
                                           (sub_horizontal_offset[0] - (i - 2) * interval_between_subs[0]) *
                                           np.sin(back_rotation[0]) + main_vertical_piece_size[0] / 2 *
                                           np.sin(main_vertical_rotation[0]) * np.cos(back_rotation[0])]
                self.mesh = Cuboid(
                    self.sub_horizontal_piece_size[0],
                    self.main_vertical_separation[0] - main_vertical_piece_size[0] * np.cos(main_vertical_rotation[0]),
                    self.sub_horizontal_piece_size[1],
                    position=sub_horizontal_position, rotation=sub_horizontal_rotation)

            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Back'
