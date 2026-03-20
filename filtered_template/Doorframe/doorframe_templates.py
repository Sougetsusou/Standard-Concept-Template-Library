"""
Doorframe Templates
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
class Standard_Doorframe(ConceptTemplate):
    def __init__(self, door_size, existence_of_doorframe, main_outer_size, main_inner_outer_offset, main_offset, sub1_outer_size, sub1_inner_size, sub1_inner_outer_offset, sub1_offset,sub2_outer_size, sub2_inner_size, sub2_inner_outer_offset, sub2_offset, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.door_size = door_size
        self.existence_of_doorframe = existence_of_doorframe
        self.main_outer_size = main_outer_size
        self.main_inner_outer_offset = main_inner_outer_offset
        self.main_offset = main_offset
        self.sub1_outer_size = sub1_outer_size
        self.sub1_inner_size = sub1_inner_size
        self.sub1_inner_outer_offset = sub1_inner_outer_offset
        self.sub1_offset = sub1_offset
        self.sub2_outer_size = sub2_outer_size
        self.sub2_inner_size = sub2_inner_size
        self.sub2_inner_outer_offset = sub2_inner_outer_offset
        self.sub2_offset = sub2_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        main_top_size = [
            door_size[0],
            main_outer_size[1] + main_inner_outer_offset[1] - door_size[1],
            main_outer_size[2],
        ]
        main_left_size = [
            (main_outer_size[0] - door_size[0]) / 2 - main_inner_outer_offset[0],
            main_outer_size[1],
            main_outer_size[2],
        ]
        main_right_size = [
            (main_outer_size[0] - door_size[0]) / 2 + main_inner_outer_offset[0],
            main_outer_size[1],
            main_outer_size[2],
        ]

        main_top_mesh_position = [
            main_offset[0],
            door_size[1] / 2 + main_top_size[1] / 2,
            main_offset[1],
        ]
        self.main_top_mesh = Cuboid(main_top_size[1], main_top_size[0], main_top_size[2],
                                    position=main_top_mesh_position)
        vertices_list.append(self.main_top_mesh.vertices)
        faces_list.append(self.main_top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.main_top_mesh.vertices)

        main_left_mesh_position = [
            main_offset[0] - door_size[0] / 2 - main_left_size[0] / 2,
            -door_size[1] / 2 + main_outer_size[1] / 2 + main_inner_outer_offset[1],
            main_offset[1],
        ]
        self.main_left_mesh = Cuboid(main_left_size[1], main_left_size[0], main_left_size[2],
                                     position=main_left_mesh_position)
        vertices_list.append(self.main_left_mesh.vertices)
        faces_list.append(self.main_left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.main_left_mesh.vertices)

        main_right_mesh_position = [
            main_offset[0] + door_size[0] / 2 + main_right_size[0] / 2,
            -door_size[1] / 2 + main_outer_size[1] / 2 + main_inner_outer_offset[1],
            main_offset[1],
        ]
        self.main_right_mesh = Cuboid(main_right_size[1], main_right_size[0], main_right_size[2],
                                      position=main_right_mesh_position)
        vertices_list.append(self.main_right_mesh.vertices)
        faces_list.append(self.main_right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.main_right_mesh.vertices)

        if existence_of_doorframe[0]:
            front_top_size = [
                sub1_inner_size[0],
                sub1_outer_size[1] + sub1_inner_outer_offset[1] - sub1_inner_size[1],
                sub1_outer_size[2],
            ]
            front_left_size = [
                (sub1_outer_size[0] - sub1_inner_size[0]) / 2
                - sub1_inner_outer_offset[0],
                sub1_outer_size[1],
                sub1_outer_size[2],
            ]
            front_right_size = [
                (sub1_outer_size[0] - sub1_inner_size[0]) / 2
                + sub1_inner_outer_offset[0],
                sub1_outer_size[1],
                sub1_outer_size[2],
            ]

            front_top_mesh_position = [
                sub1_offset[0],
                sub1_offset[1] - door_size[1] / 2 + sub1_inner_size[1] + front_top_size[1] / 2,
                -sub1_outer_size[2] / 2 + main_offset[1] + main_outer_size[2] / 2,
            ]
            self.front_top_mesh = Cuboid(front_top_size[1], front_top_size[0], front_top_size[2],
                                         position=front_top_mesh_position)
            vertices_list.append(self.front_top_mesh.vertices)
            faces_list.append(self.front_top_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.front_top_mesh.vertices)

            front_left_mesh_position = [
                sub1_offset[0] - sub1_inner_size[0] / 2 - front_left_size[0] / 2,
                sub1_offset[1] - door_size[1] / 2 + sub1_outer_size[1] / 2 + sub1_inner_outer_offset[1],
                -sub1_outer_size[2] / 2 + main_offset[1] + main_outer_size[2] / 2,
            ]
            self.front_left_mesh = Cuboid(front_left_size[1], front_left_size[0], front_left_size[2],
                                          position=front_left_mesh_position)
            vertices_list.append(self.front_left_mesh.vertices)
            faces_list.append(self.front_left_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.front_left_mesh.vertices)

            front_right_mesh_position = [
                sub1_offset[0] + sub1_inner_size[0] / 2 + front_left_size[0] / 2,
                sub1_offset[1] - door_size[1] / 2 + sub1_outer_size[1] / 2 + sub1_inner_outer_offset[1],
                -sub1_outer_size[2] / 2 + main_offset[1] + main_outer_size[2] / 2,
            ]
            self.front_right_mesh = Cuboid(front_right_size[1], front_right_size[0], front_right_size[2],
                                           position=front_right_mesh_position)
            vertices_list.append(self.front_right_mesh.vertices)
            faces_list.append(self.front_right_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.front_right_mesh.vertices)

        if existence_of_doorframe[1]:
            back_top_size = [
                sub2_inner_size[0],
                sub2_outer_size[1] + sub2_inner_outer_offset[1] - sub2_inner_size[1],
                sub2_outer_size[2],
            ]
            back_left_size = [
                (sub2_outer_size[0] - sub2_inner_size[0]) / 2
                - sub2_inner_outer_offset[0],
                sub2_outer_size[1],
                sub2_outer_size[2],
            ]
            back_right_size = [
                (sub2_outer_size[0] - sub2_inner_size[0]) / 2
                + sub2_inner_outer_offset[0],
                sub2_outer_size[1],
                sub2_outer_size[2],
            ]

            back_top_mesh_position = [
                sub2_offset[0],
                sub2_offset[1] - door_size[1] / 2 + sub2_inner_size[1] + back_top_size[1] / 2,
                -sub2_outer_size[2] / 2 + main_offset[1] - main_outer_size[2] / 2,
            ]
            self.back_top_mesh = Cuboid(back_top_size[1], back_top_size[0], back_top_size[2],
                                        position=back_top_mesh_position)
            vertices_list.append(self.back_top_mesh.vertices)
            faces_list.append(self.back_top_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.back_top_mesh.vertices)

            back_left_mesh_position = [
                sub2_offset[0] - sub2_inner_size[0] / 2 - back_left_size[0] / 2,
                sub2_offset[1] - door_size[1] / 2 + sub2_outer_size[1] / 2 + sub2_inner_outer_offset[1],
                -sub2_outer_size[2] / 2 + main_offset[1] - main_outer_size[2] / 2,
            ]
            self.back_left_mesh = Cuboid(back_left_size[1], back_left_size[0], back_left_size[2],
                                         position=back_left_mesh_position)
            vertices_list.append(self.back_left_mesh.vertices)
            faces_list.append(self.back_left_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.back_left_mesh.vertices)

            back_right_mesh_position = [
                sub2_offset[0] + sub2_inner_size[0] / 2 + back_right_size[0] / 2,
                sub2_offset[1] - door_size[1] / 2 + sub2_outer_size[1] / 2 + sub2_inner_outer_offset[1],
                -sub2_outer_size[2] / 2 + main_offset[1] - main_outer_size[2] / 2,
            ]
            self.back_right_mesh = Cuboid(back_right_size[1], back_right_size[0], back_right_size[2],
                                          position=back_right_mesh_position)
            vertices_list.append(self.back_right_mesh.vertices)
            faces_list.append(self.back_right_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.back_right_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Doorframe'
