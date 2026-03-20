"""
Cabinet Templates
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


# Source: Table/concept_template.py
class Regular_cabinet(ConceptTemplate):
    def __init__(self, number_of_top_cabinet, number_of_beneath_cabinet, cab_backs_size,
                 cab_left_right_inner_sizes, cab_up_down_inner_sizes, drawer_inner_sizes,
                 drawer_bottom_size, door_sizes, number_of_layers, layers_sizes, layers_offset,
                 interval_between_layers, cabinets_params, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        cabinets_params = [x / 180 * np.pi if i % 56 in [22, 23, 24, 25, 41, 42, 43, 44] else x for i, x in enumerate(cabinets_params)]
        super().__init__(position, rotation)

        # Record Parameters
        self.number_of_top_cabinet = number_of_top_cabinet[0]
        self.number_of_beneath_cabinet = number_of_beneath_cabinet[0]
        self.cab_backs_size = cab_backs_size
        self.cab_left_right_inner_sizes = cab_left_right_inner_sizes
        self.cab_up_down_inner_sizes = cab_up_down_inner_sizes
        self.drawer_inner_sizes = drawer_inner_sizes
        self.drawer_bottom_size = drawer_bottom_size
        self.door_sizes = door_sizes
        self.number_of_layers = number_of_layers
        self.layers_sizes = layers_sizes
        self.layers_offset = layers_offset
        self.interval_between_layers = interval_between_layers
        self.cabinet_size = [cabinets_params[i * 56: i * 56 + 3] for i in range(self.number_of_top_cabinet)
                             ] + [cabinets_params[(i + 2) * 56: (i + 2) * 56 + 3] for i in range(self.number_of_beneath_cabinet)]
        self.type_of_spaces = [
                                  cabinets_params[i * 56 + 3: i * 56 + 7]
                                  for i in range(self.number_of_top_cabinet)
                              ] + [
                                  cabinets_params[(i + 2) * 56 + 3: (i + 2) * 56 + 7]
                                  for i in range(self.number_of_beneath_cabinet)
                              ]

        self.drawer_interval = [
                                   cabinets_params[i * 56 + 7: i * 56 + 11]
                                   for i in range(self.number_of_top_cabinet)
                               ] + [
                                   cabinets_params[(i + 2) * 56 + 6: (i + 2) * 56 + 11]
                                   for i in range(self.number_of_beneath_cabinet)
                               ]

        self.drawer_offset = [
                                 cabinets_params[i * 56 + 11: i * 56 + 15]
                                 for i in range(self.number_of_top_cabinet)
                             ] + [
                                 cabinets_params[(i + 2) * 56 + 11: (i + 2) * 56 + 15]
                                 for i in range(self.number_of_beneath_cabinet)
                             ]

        self.drawer_number_of_handles = [
                                            cabinets_params[i * 56 + 15: i * 56 + 19]
                                            for i in range(self.number_of_top_cabinet)
                                        ] + [
                                            cabinets_params[(i + 2) * 56 + 15: (i + 2) * 56 + 19]
                                            for i in range(self.number_of_beneath_cabinet)
                                        ]

        self.drawer_handles_size = [
                                       cabinets_params[i * 56 + 19: i * 56 + 22]
                                       for i in range(self.number_of_top_cabinet)
                                   ] + [
                                       cabinets_params[(i + 2) * 56 + 19: (i + 2) * 56 + 22]
                                       for i in range(self.number_of_beneath_cabinet)
                                   ]

        self.drawer_handles_rotation = [
                                           cabinets_params[i * 56 + 22: i * 56 + 26]
                                           for i in range(self.number_of_top_cabinet)
                                       ] + [
                                           cabinets_params[(i + 2) * 56 + 22: (i + 2) * 56 + 26]
                                           for i in range(self.number_of_beneath_cabinet)
                                       ]

        self.drawer_handles_separation = [
                                             cabinets_params[i * 56 + 26: i * 56 + 30]
                                             for i in range(self.number_of_top_cabinet)
                                         ] + [
                                             cabinets_params[(i + 2) * 56 + 26: (i + 2) * 56 + 30]
                                             for i in range(self.number_of_beneath_cabinet)
                                         ]

        self.drawer_handles_offsets = [
                                          [
                                              [x_offset, y_offset]
                                              for x_offset, y_offset in zip(
                                              cabinets_params[i * 56 + 30: i * 56 + 34],
                                              cabinets_params[i * 56 + 34: i * 56 + 38]
                                          )
                                          ]
                                          for i in range(self.number_of_top_cabinet)
                                      ] + [
                                          [
                                              [x_offset, y_offset]
                                              for x_offset, y_offset in zip(
                                              cabinets_params[(i + 2) * 56 + 30: (i + 2) * 56 + 34],
                                              cabinets_params[(i + 2) * 56 + 34: (i + 2) * 56 + 38]
                                          )
                                          ]
                                          for i in range(self.number_of_beneath_cabinet)
                                      ]

        self.door_handles_size = [
                                     cabinets_params[i * 56 + 38: i * 56 + 41]
                                     for i in range(self.number_of_top_cabinet)
                                 ] + [
                                     cabinets_params[(i + 2) * 56 + 38: (i + 2) * 56 + 41]
                                     for i in range(self.number_of_beneath_cabinet)
                                 ]

        self.door_handles_rotation = [
                                         cabinets_params[i * 56 + 41: i * 56 + 45]
                                         for i in range(self.number_of_top_cabinet)
                                     ] + [
                                         cabinets_params[(i + 2) * 56 + 41: (i + 2) * 56 + 45]
                                         for i in range(self.number_of_beneath_cabinet)
                                     ]

        self.door_handles_offsets = [
                                        [
                                            [x_offset, y_offset]
                                            for x_offset, y_offset in zip(
                                            cabinets_params[i * 56 + 45: i * 56 + 49],
                                            cabinets_params[i * 56 + 49: i * 56 + 53]
                                        )
                                        ]
                                        for i in range(self.number_of_top_cabinet)
                                    ] + [
                                        [
                                            [x_offset, y_offset]
                                            for x_offset, y_offset in zip(
                                            cabinets_params[(i + 2) * 56 + 45: (i + 2) * 56 + 49],
                                            cabinets_params[(i + 2) * 56 + 49: (i + 2) * 56 + 53]
                                        )
                                        ]
                                        for i in range(self.number_of_beneath_cabinet)
                                    ]

        self.cabinet_offset = [
                                  cabinets_params[i * 56 + 53: i * 56 + 56]
                                  for i in range(self.number_of_top_cabinet)
                              ] + [
                                  cabinets_params[(i + 2) * 56 + 53: (i + 2) * 56 + 56]
                                  for i in range(self.number_of_beneath_cabinet)
                              ]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # top cabinet
        for cabinet_idx in range(self.number_of_top_cabinet):
            actual_idx = cabinet_idx
            cabinet_body_mesh = 5
            layers_mesh = number_of_layers[cabinet_idx]
            cabinet_doors_mesh = sum(2 for type_of_space in self.type_of_spaces[cabinet_idx] if type_of_space == 2)
            cabinet_drawers_mesh = sum(
                (5 + self.drawer_number_of_handles[cabinet_idx][space_idx]) for space_idx, type_of_space in enumerate(self.type_of_spaces[cabinet_idx]) if type_of_space == 1)
            total_mesh_list = [cabinet_body_mesh, layers_mesh, cabinet_doors_mesh, cabinet_drawers_mesh]

            # build cabinet body and layers
            for mesh_idx in range(sum(total_mesh_list[:2])):
                if mesh_idx < sum(total_mesh_list[:1]):
                    position_sign = -1 if mesh_idx % 2 == 0 else 1
                    if mesh_idx < 2:
                        mesh_position = [
                            position_sign * (self.cabinet_size[cabinet_idx][0] - self.cab_left_right_inner_sizes[cabinet_idx]) / 2 + self.cabinet_offset[cabinet_idx][0],
                            self.cabinet_offset[cabinet_idx][1] - self.cabinet_size[cabinet_idx][1] / 2,
                            self.cabinet_offset[cabinet_idx][2]]
                        self.mesh = Cuboid(self.cabinet_size[cabinet_idx][1], self.cab_left_right_inner_sizes[cabinet_idx], self.cabinet_size[cabinet_idx][2],
                                           position=mesh_position)
                    elif mesh_idx < 4:
                        mesh_position = [
                            self.cabinet_offset[cabinet_idx][0],
                            position_sign * (self.cabinet_size[cabinet_idx][1] - self.cab_up_down_inner_sizes[cabinet_idx]) / 2 + self.cabinet_offset[cabinet_idx][1] - self.cabinet_size[cabinet_idx][1] / 2,
                            self.cabinet_offset[cabinet_idx][2]]
                        self.mesh = Cuboid(self.cab_up_down_inner_sizes[cabinet_idx],
                                           self.cabinet_size[cabinet_idx][0] - 2 * self.cab_left_right_inner_sizes[cabinet_idx],
                                           self.cabinet_size[cabinet_idx][2],
                                           position=mesh_position)
                    else:
                        mesh_position = [
                            self.cabinet_offset[cabinet_idx][0],
                            self.cabinet_offset[cabinet_idx][1] - self.cabinet_size[cabinet_idx][1] / 2,
                            self.cabinet_offset[cabinet_idx][2] - (self.cabinet_size[cabinet_idx][2] + self.cab_backs_size[cabinet_idx]) / 2]
                        self.mesh = Cuboid(self.cabinet_size[cabinet_idx][1],
                                           self.cabinet_size[cabinet_idx][0],
                                           self.cab_backs_size[cabinet_idx],
                                           position=mesh_position)
                else:
                    mesh_position = [
                        self.cabinet_offset[cabinet_idx][0],
                        - (self.layers_offset[cabinet_idx] + (mesh_idx - sum(total_mesh_list[:1])) * self.interval_between_layers[cabinet_idx]) - self.cabinet_size[cabinet_idx][1] / 2,
                        self.cabinet_offset[cabinet_idx][2]]
                    self.mesh = Cuboid(self.layers_sizes[cabinet_idx],
                                       self.cabinet_size[cabinet_idx][0] - 2 * self.cab_left_right_inner_sizes[cabinet_idx],
                                       self.cabinet_size[cabinet_idx][2],
                                       position=mesh_position)

                # special case for top and beneath cabinet to adjust the position of the cabinet 

                # Y-axis adjustment
                self.mesh.vertices[:, 1] += self.cabinet_size[cabinet_idx][1] / 2

                # X-axis adjustment
                if self.number_of_top_cabinet == 2:
                    if cabinet_idx % 2 == 0:
                        self.mesh.vertices[:, 0] += self.cabinet_size[cabinet_idx][0] / 2
                    else:
                        self.mesh.vertices[:, 0] -= self.cabinet_size[cabinet_idx][0] / 2

                vertices_list.append(self.mesh.vertices)
                faces_list.append(self.mesh.faces + total_num_vertices)
                total_num_vertices += len(self.mesh.vertices)

            # build doors and drawers
            for space_idx in range(self.number_of_layers[cabinet_idx] + 1):
                if self.number_of_layers[cabinet_idx] == 0:
                    _height = self.cabinet_size[cabinet_idx][1] - 2 * self.cab_up_down_inner_sizes[cabinet_idx]
                    _pos = 0
                elif space_idx == 0:
                    _height = self.layers_offset[actual_idx] - self.cab_up_down_inner_sizes[cabinet_idx] - self.layers_sizes[cabinet_idx] / 2
                    _pos = self.cabinet_size[cabinet_idx][1] - self.layers_offset[actual_idx] / 2 - self.cab_up_down_inner_sizes[cabinet_idx] / 2 + self.layers_sizes[cabinet_idx] / 4
                elif space_idx == self.number_of_layers[cabinet_idx]:
                    _height = self.cabinet_size[cabinet_idx][1] - (self.layers_offset[1] + (space_idx - 1) * self.interval_between_layers[1]) - \
                              self.cab_up_down_inner_sizes[cabinet_idx] - self.layers_sizes[cabinet_idx] / 2
                    _pos = self.cab_up_down_inner_sizes[cabinet_idx] + _height / 2 - 5
                else:
                    _height = self.interval_between_layers[0] - self.layers_sizes[cabinet_idx]
                    _pos = self.cabinet_size[cabinet_idx][1] - self.layers_offset[actual_idx] - (2 * space_idx - 1) / 2 * self.interval_between_layers[0]

                if self.type_of_spaces[cabinet_idx][space_idx] == 1:
                    for mesh_idx in range(5 + self.drawer_number_of_handles[cabinet_idx][space_idx]):
                        if mesh_idx < 2:
                            position_sign = -1 if mesh_idx == 0 else 1
                            mesh_position = [position_sign * (
                                    self.cabinet_size[cabinet_idx][0] / 2 - self.cab_left_right_inner_sizes[cabinet_idx] - self.drawer_inner_sizes[0] / 2) +
                                             self.cabinet_offset[cabinet_idx][0],
                                             _pos + self.cabinet_offset[cabinet_idx][1] - self.cabinet_size[cabinet_idx][1] / 2,
                                             self.cabinet_offset[cabinet_idx][2] + self.drawer_offset[cabinet_idx][space_idx] + self.drawer_interval[cabinet_idx][space_idx] / 2]
                            self.mesh = Cuboid(_height,
                                               self.drawer_inner_sizes[0],
                                               self.cabinet_size[cabinet_idx][2] - self.drawer_interval[cabinet_idx][space_idx],
                                               position=mesh_position)
                        elif mesh_idx < 4:
                            position_sign = -1 if mesh_idx == 3 else 1
                            mesh_position = [self.cabinet_offset[cabinet_idx][0],
                                             _pos + self.cabinet_offset[cabinet_idx][1] - self.cabinet_size[cabinet_idx][1] / 2,
                                             self.cabinet_offset[cabinet_idx][2] + position_sign * (self.cabinet_size[cabinet_idx][2] - self.drawer_inner_sizes[1]) / 2]
                            self.mesh = Cuboid(_height,
                                               self.cabinet_size[cabinet_idx][0] - 2 * self.cab_left_right_inner_sizes[cabinet_idx] - 2 * self.drawer_inner_sizes[0],
                                               self.drawer_inner_sizes[1],
                                               position=mesh_position)
                        elif mesh_idx == 4:
                            mesh_position = [self.cabinet_offset[cabinet_idx][0],
                                             _pos + self.cabinet_offset[cabinet_idx][1] - (_height + self.drawer_bottom_size[0]) / 2 - self.cabinet_size[cabinet_idx][1] / 2,
                                             self.cabinet_offset[cabinet_idx][2] + self.drawer_interval[cabinet_idx][space_idx] / 2 + self.drawer_offset[cabinet_idx][space_idx]]
                            self.mesh = Cuboid(self.drawer_bottom_size[0],
                                               self.cabinet_size[cabinet_idx][0] - 2 * self.cab_left_right_inner_sizes[cabinet_idx],
                                               self.cabinet_size[cabinet_idx][2] - self.drawer_interval[cabinet_idx][space_idx],
                                               position=mesh_position)
                        else:
                            if self.drawer_number_of_handles[cabinet_idx][space_idx] == 2:
                                position_sign = 1 if mesh_idx == 5 else -1
                            else:
                                position_sign = 0
                            mesh_rotation = [0, 0, self.drawer_handles_rotation[cabinet_idx][space_idx]]
                            mesh_position = [self.cabinet_offset[cabinet_idx][0] + self.drawer_handles_offsets[cabinet_idx][space_idx][0] +
                                             position_sign * self.drawer_handles_separation[cabinet_idx][space_idx],
                                             _pos + self.cabinet_offset[cabinet_idx][1] + self.drawer_handles_offsets[cabinet_idx][space_idx][1] - self.cabinet_size[cabinet_idx][1] / 2,
                                             self.cabinet_offset[cabinet_idx][2] + (self.cabinet_size[cabinet_idx][2] + self.drawer_handles_size[cabinet_idx][2]) / 2 +
                                             self.drawer_offset[cabinet_idx][space_idx]]
                            self.mesh = Cuboid(self.drawer_handles_size[cabinet_idx][1], self.drawer_handles_size[cabinet_idx][0], self.drawer_handles_size[cabinet_idx][2],
                                               position=mesh_position, rotation=mesh_rotation)

                        # special case for top and beneath cabinet to adjust the position of the cabinet 

                        # Y-axis adjustment
                        self.mesh.vertices[:, 1] += self.cabinet_size[cabinet_idx][1] / 2

                        # X-axis adjustment
                        if self.number_of_top_cabinet == 2:
                            if cabinet_idx % 2 == 0:
                                self.mesh.vertices[:, 0] += self.cabinet_size[cabinet_idx][0] / 2
                            else:
                                self.mesh.vertices[:, 0] -= self.cabinet_size[cabinet_idx][0] / 2

                        vertices_list.append(self.mesh.vertices)
                        faces_list.append(self.mesh.faces + total_num_vertices)
                        total_num_vertices += len(self.mesh.vertices)
                elif self.type_of_spaces[cabinet_idx][space_idx] == 2:
                    for mesh_idx in range(2):
                        if mesh_idx == 0:
                            mesh_position = [self.cabinet_offset[cabinet_idx][0],
                                             _pos + self.cabinet_offset[cabinet_idx][1],
                                             self.cabinet_offset[cabinet_idx][2] + (self.cabinet_size[cabinet_idx][2] + self.door_sizes[0]) / 2]
                            self.mesh = Cuboid(_height,
                                               self.cabinet_size[cabinet_idx][0] - 2 * self.cab_left_right_inner_sizes[cabinet_idx],
                                               self.door_sizes[0],
                                               position=mesh_position)
                        else:
                            mesh_rotation = [0, 0, self.door_handles_rotation[cabinet_idx][space_idx]]
                            mesh_position = [self.cabinet_offset[cabinet_idx][0] + self.door_handles_offsets[cabinet_idx][space_idx][0],
                                             _pos + self.cabinet_offset[cabinet_idx][1] + self.door_handles_offsets[cabinet_idx][space_idx][1],
                                             self.cabinet_offset[cabinet_idx][2] + (self.cabinet_size[cabinet_idx][2] + self.door_sizes[0]) / 2 + (
                                                     self.door_handles_size[cabinet_idx][2] + self.door_sizes[0]) / 2]
                            self.mesh = Cuboid(self.door_handles_size[1], self.door_handles_size[0], self.door_handles_size[2],
                                               position=mesh_position, rotation=mesh_rotation)
                    # special case for top and beneath cabinet to adjust the position of the cabinet 

                    # Y-axis adjustment
                    self.mesh.vertices[:, 1] += self.cabinet_size[cabinet_idx][1] / 2

                    # X-axis adjustment
                    if self.number_of_top_cabinet == 2:
                        if cabinet_idx % 2 == 0:
                            self.mesh.vertices[:, 0] += self.cabinet_size[cabinet_idx][0] / 2
                        else:
                            self.mesh.vertices[:, 0] -= self.cabinet_size[cabinet_idx][0] / 2
                        vertices_list.append(self.mesh.vertices)
                        faces_list.append(self.mesh.faces + total_num_vertices)
                        total_num_vertices += len(self.mesh.vertices)
                else:
                    pass

        # beneath cabinet
        for cabinet_idx in range(self.number_of_beneath_cabinet):
            actual_idx = 2 + cabinet_idx
            cabinet_body_mesh = 5
            layers_mesh = number_of_layers[actual_idx]
            cabinet_doors_mesh = sum(2 for type_of_space in self.type_of_spaces[cabinet_idx] if type_of_space == 2)
            cabinet_drawers_mesh = sum(
                (5 + self.drawer_number_of_handles[cabinet_idx][space_idx]) for space_idx, type_of_space in enumerate(self.type_of_spaces[cabinet_idx]) if type_of_space == 1)
            total_mesh_list = [cabinet_body_mesh, layers_mesh, cabinet_doors_mesh, cabinet_drawers_mesh]

            # build cabinet body and layers
            for mesh_idx in range(sum(total_mesh_list[:2])):
                if mesh_idx < sum(total_mesh_list[:1]):
                    position_sign = -1 if mesh_idx % 2 == 0 else 1
                    if mesh_idx < 2:
                        mesh_position = [
                            position_sign * (self.cabinet_size[cabinet_idx][0] - self.cab_left_right_inner_sizes[actual_idx]) / 2 + self.cabinet_offset[cabinet_idx][0],
                            self.cabinet_offset[cabinet_idx][1],
                            self.cabinet_offset[cabinet_idx][2]]
                        self.mesh = Cuboid(self.cabinet_size[cabinet_idx][1], self.cab_left_right_inner_sizes[actual_idx], self.cabinet_size[cabinet_idx][2],
                                           position=mesh_position)
                    elif mesh_idx < 4:
                        mesh_position = [
                            self.cabinet_offset[cabinet_idx][0],
                            position_sign * (self.cabinet_size[cabinet_idx][1] - self.cab_up_down_inner_sizes[actual_idx]) / 2 + self.cabinet_offset[cabinet_idx][1],
                            self.cabinet_offset[cabinet_idx][2]]
                        self.mesh = Cuboid(self.cab_up_down_inner_sizes[actual_idx],
                                           self.cabinet_size[cabinet_idx][0] - 2 * self.cab_left_right_inner_sizes[actual_idx],
                                           self.cabinet_size[cabinet_idx][2],
                                           position=mesh_position)
                    else:
                        if self.cab_backs_size[actual_idx] != 0:
                            mesh_position = [
                                self.cabinet_offset[cabinet_idx][0],
                                self.cabinet_offset[cabinet_idx][1],
                                self.cabinet_offset[cabinet_idx][2] - (self.cabinet_size[cabinet_idx][2] + self.cab_backs_size[actual_idx]) / 2]
                            self.mesh = Cuboid(self.cabinet_size[cabinet_idx][1],
                                               self.cabinet_size[cabinet_idx][0],
                                               self.cab_backs_size[actual_idx],
                                               position=mesh_position)
                        else:
                            pass
                else:
                    mesh_position = [
                        self.cabinet_offset[cabinet_idx][0],
                        self.cabinet_offset[cabinet_idx][1] + self.cabinet_size[cabinet_idx][1] / 2 - (
                                self.layers_offset[actual_idx] + (mesh_idx - sum(total_mesh_list[:1])) * self.interval_between_layers[actual_idx]),
                        self.cabinet_offset[cabinet_idx][2]]
                    self.mesh = Cuboid(self.layers_sizes[actual_idx],
                                       self.cabinet_size[cabinet_idx][0] - 2 * self.cab_left_right_inner_sizes[actual_idx],
                                       self.cabinet_size[cabinet_idx][2],
                                       position=mesh_position)

                vertices_list.append(self.mesh.vertices)
                faces_list.append(self.mesh.faces + total_num_vertices)
                total_num_vertices += len(self.mesh.vertices)

            # build doors and drawers
            for space_idx in range(self.number_of_layers[actual_idx] + 1):
                if self.number_of_layers[actual_idx] == 0:
                    _height = self.cabinet_size[cabinet_idx][1] - 2 * self.cab_up_down_inner_sizes[actual_idx]
                    _pos = self.cabinet_size[cabinet_idx][1] / 2
                elif space_idx == 0:
                    _height = self.layers_offset[actual_idx] - self.cab_up_down_inner_sizes[actual_idx] - self.layers_sizes[actual_idx] / 2
                    _pos = self.cabinet_size[cabinet_idx][1] - self.layers_offset[actual_idx] / 2 - self.cab_up_down_inner_sizes[actual_idx] / 2 + self.layers_sizes[actual_idx] / 4
                elif space_idx == self.number_of_layers[actual_idx]:
                    _height = self.cabinet_size[cabinet_idx][1] - (self.layers_offset[actual_idx] + (space_idx - 1) * self.interval_between_layers[0]) - \
                              self.cab_up_down_inner_sizes[actual_idx] - self.layers_sizes[actual_idx] / 2
                    _pos = self.cab_up_down_inner_sizes[actual_idx] + _height / 2
                else:
                    _height = self.interval_between_layers[0] - self.layers_sizes[actual_idx]
                    _pos = self.cabinet_size[cabinet_idx][1] - self.layers_offset[actual_idx] - (2 * space_idx - 1) / 2 * self.interval_between_layers[0]

                if self.type_of_spaces[cabinet_idx][space_idx] == 1:
                    for mesh_idx in range(5 + self.drawer_number_of_handles[cabinet_idx][space_idx]):
                        if mesh_idx < 2:
                            position_sign = -1 if mesh_idx == 0 else 1
                            mesh_position = [position_sign * (
                                    self.cabinet_size[cabinet_idx][0] / 2 - self.cab_left_right_inner_sizes[actual_idx] - self.drawer_inner_sizes[0] / 2) +
                                             self.cabinet_offset[cabinet_idx][0],
                                             _pos + self.cabinet_offset[cabinet_idx][1],
                                             self.cabinet_offset[cabinet_idx][2] + self.drawer_offset[cabinet_idx][space_idx] + self.drawer_interval[cabinet_idx][space_idx] / 2]
                            self.mesh = Cuboid(_height,
                                               self.drawer_inner_sizes[0],
                                               self.cabinet_size[cabinet_idx][2] - self.drawer_interval[cabinet_idx][space_idx],
                                               position=mesh_position)
                        elif mesh_idx < 4:
                            position_sign = -1 if mesh_idx == 3 else 1
                            mesh_position = [self.cabinet_offset[cabinet_idx][0],
                                             _pos + self.cabinet_offset[cabinet_idx][1],
                                             self.cabinet_offset[cabinet_idx][2] + position_sign * (self.cabinet_size[cabinet_idx][2] - self.drawer_inner_sizes[1]) / 2 + self.drawer_offset[cabinet_idx][space_idx]]
                            self.mesh = Cuboid(_height,
                                               self.cabinet_size[cabinet_idx][0] - 2 * self.cab_left_right_inner_sizes[actual_idx] - 2 * self.drawer_inner_sizes[0],
                                               self.drawer_inner_sizes[1],
                                               position=mesh_position)
                        elif mesh_idx == 4:
                            mesh_position = [self.cabinet_offset[cabinet_idx][0],
                                             _pos + self.cabinet_offset[cabinet_idx][1] - (_height + self.drawer_bottom_size[0]) / 2,
                                             self.cabinet_offset[cabinet_idx][2] + self.drawer_interval[cabinet_idx][space_idx] / 2 + self.drawer_offset[cabinet_idx][space_idx]]
                            self.mesh = Cuboid(self.drawer_bottom_size[0],
                                               self.cabinet_size[cabinet_idx][0] - 2 * self.cab_left_right_inner_sizes[actual_idx],
                                               self.cabinet_size[cabinet_idx][2] - self.drawer_interval[cabinet_idx][space_idx],
                                               position=mesh_position)
                        else:
                            if self.drawer_number_of_handles[cabinet_idx][space_idx] == 2:
                                position_sign = 1 if mesh_idx == 5 else -1
                            else:
                                position_sign = 0
                            mesh_rotation = [0, 0, self.drawer_handles_rotation[cabinet_idx][space_idx]]
                            mesh_position = [self.cabinet_offset[cabinet_idx][0] + self.drawer_handles_offsets[cabinet_idx][space_idx][0] +
                                             position_sign * self.drawer_handles_separation[cabinet_idx][space_idx],
                                             _pos + self.cabinet_offset[cabinet_idx][1] + self.drawer_handles_offsets[cabinet_idx][space_idx][1],
                                             self.cabinet_offset[cabinet_idx][2] + (self.cabinet_size[cabinet_idx][2] + self.drawer_handles_size[cabinet_idx][2]) / 2 +
                                             self.drawer_offset[cabinet_idx][space_idx]]
                            self.mesh = Cuboid(self.drawer_handles_size[cabinet_idx][1], self.drawer_handles_size[cabinet_idx][0], self.drawer_handles_size[cabinet_idx][2],
                                               position=mesh_position, rotation=mesh_rotation)

                        # special case for top and beneath cabinet to adjust the position of the cabinet 

                        # Y-axis adjustment
                        self.mesh.vertices[:, 1] -= self.cabinet_size[cabinet_idx][1] / 2

                        vertices_list.append(self.mesh.vertices)
                        faces_list.append(self.mesh.faces + total_num_vertices)
                        total_num_vertices += len(self.mesh.vertices)
                elif self.type_of_spaces[cabinet_idx][space_idx] == 2:
                    for mesh_idx in range(2):
                        if mesh_idx == 0:
                            mesh_position = [self.cabinet_offset[cabinet_idx][0],
                                             _pos + self.cabinet_offset[cabinet_idx][1],
                                             self.cabinet_offset[cabinet_idx][2] + (self.cabinet_size[cabinet_idx][2] + self.door_sizes[0]) / 2]
                            self.mesh = Cuboid(_height,
                                               self.cabinet_size[cabinet_idx][0] - 2 * self.cab_left_right_inner_sizes[actual_idx],
                                               self.door_sizes[0],
                                               position=mesh_position)
                        else:
                            mesh_rotation = [0, 0, self.door_handles_rotation[cabinet_idx][space_idx]]
                            mesh_position = [self.cabinet_offset[cabinet_idx][0] + self.door_handles_offsets[cabinet_idx][space_idx][0],
                                             _pos + self.cabinet_offset[cabinet_idx][1] + self.door_handles_offsets[cabinet_idx][space_idx][1],
                                             self.cabinet_offset[cabinet_idx][2] + (self.cabinet_size[cabinet_idx][2] + self.door_sizes[0]) / 2 + (
                                                     self.door_handles_size[cabinet_idx][2] + self.door_sizes[0]) / 2]
                            self.mesh = Cuboid(self.door_handles_size[cabinet_idx][1], self.door_handles_size[cabinet_idx][0], self.door_handles_size[cabinet_idx][2],
                                               position=mesh_position, rotation=mesh_rotation)

                    # special case for top and beneath cabinet to adjust the position of the cabinet 

                        # Y-axis adjustment
                        self.mesh.vertices[:, 1] -= self.cabinet_size[cabinet_idx][1] / 2

                        vertices_list.append(self.mesh.vertices)
                        faces_list.append(self.mesh.faces + total_num_vertices)
                        total_num_vertices += len(self.mesh.vertices)
                else:
                    pass

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Cabinet'
