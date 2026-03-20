import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Regular_drawer(ConceptTemplate):
    """
    Semantic: Drawer
    Geometry: per-drawer assembly of 2 side walls + 2 front/back walls + bottom panel +
              front face panel + 1 or 2 handle cuboids; supports multiple drawers
    Used by: Table
    Parameters:
      number_of_drawer [n]: number of drawers (1..N)
      drawers_params [flat list]: stride-21 per-drawer parameters:
        [0:3]  drawer_size [w, h, d]
        [3]    bottom_size [t]: bottom panel thickness
        [4:7]  front_size [w, h, d]: front face panel dimensions
        [7]    front_offset [y]: Y offset of front face relative to drawer centre
        [8]    left_right_inner_size [t]: side wall thickness
        [9]    rear_front_inner_size [t]: front/back wall thickness
        [10]   number_of_handle [n]: 1 or 2 handles
        [11:14] handle_sizes [w, h, d]
        [14]   handle_rotation [deg]: Z rotation of handle
        [15:17] handle_offset [x, y]
        [17]   handle_separation [s]: X separation between two handles
        [18:21] drawer_offset [x, y, z]: global offset of this drawer
      position, rotation: global transform
    """
    def __init__(self, number_of_drawer, drawers_params,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        drawers_params = [x / 180 * np.pi if i % 21 in [14] else x
                          for i, x in enumerate(drawers_params)]
        super().__init__(position, rotation)

        self.number_of_drawer = number_of_drawer
        n = int(number_of_drawer[0])

        self.drawer_size             = [drawers_params[i * 21:     i * 21 + 3]  for i in range(n)]
        self.bottom_size             = [drawers_params[i * 21 + 3]               for i in range(n)]
        self.front_size              = [drawers_params[i * 21 + 4:  i * 21 + 7]  for i in range(n)]
        self.front_offset            = [drawers_params[i * 21 + 7]               for i in range(n)]
        self.left_right_inner_size   = [drawers_params[i * 21 + 8]               for i in range(n)]
        self.rear_front_inner_size   = [drawers_params[i * 21 + 9]               for i in range(n)]
        self.number_of_handle        = [drawers_params[i * 21 + 10]              for i in range(n)]
        self.handle_sizes            = [drawers_params[i * 21 + 11: i * 21 + 14] for i in range(n)]
        self.handle_rotation         = [drawers_params[i * 21 + 14]              for i in range(n)]
        self.handle_offset           = [drawers_params[i * 21 + 15: i * 21 + 17] for i in range(n)]
        self.handle_separation       = [drawers_params[i * 21 + 17]              for i in range(n)]
        self.drawer_offset           = [drawers_params[i * 21 + 18: i * 21 + 21] for i in range(n)]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for di in range(n):
            for mi in range(int(6 + self.number_of_handle[di])):
                if mi < 2:
                    sign = -1 if mi == 0 else 1
                    mesh_position = [
                        sign * (self.drawer_size[di][0] - self.left_right_inner_size[di]) / 2 + self.drawer_offset[di][0],
                        -self.drawer_size[di][1] / 2 + self.drawer_offset[di][1],
                        self.drawer_offset[di][2]]
                    tmp_mesh = Cuboid(self.drawer_size[di][1],
                                     self.left_right_inner_size[di],
                                     self.drawer_size[di][2],
                                     position=mesh_position)
                elif mi < 4:
                    sign = -1 if mi == 3 else 1
                    mesh_position = [
                        self.drawer_offset[di][0],
                        -self.drawer_size[di][1] / 2 + self.drawer_offset[di][1],
                        sign * (self.drawer_size[di][2] - self.rear_front_inner_size[di]) / 2 + self.drawer_offset[di][2]]
                    tmp_mesh = Cuboid(self.drawer_size[di][1],
                                     self.drawer_size[di][0] - 2 * self.left_right_inner_size[di],
                                     self.rear_front_inner_size[di],
                                     position=mesh_position)
                elif mi == 4:
                    mesh_position = [
                        self.drawer_offset[di][0],
                        -self.drawer_size[di][1] + self.drawer_offset[di][1] - self.bottom_size[di] / 2,
                        self.drawer_offset[di][2]]
                    tmp_mesh = Cuboid(self.bottom_size[di],
                                     self.drawer_size[di][0],
                                     self.drawer_size[di][2],
                                     position=mesh_position)
                elif mi == 5:
                    mesh_position = [
                        self.drawer_offset[di][0],
                        -self.drawer_size[di][1] / 2 + self.drawer_offset[di][1] + self.front_offset[di],
                        self.drawer_offset[di][2] + self.drawer_size[di][2] / 2 + self.front_size[di][2] / 2]
                    tmp_mesh = Cuboid(self.front_size[di][1],
                                     self.front_size[di][0],
                                     self.front_size[di][2],
                                     position=mesh_position)
                else:
                    sign = (1 if mi == 6 else -1) if self.number_of_handle[di] == 2 else 0
                    mesh_rotation = [0, 0, self.handle_rotation[di]]
                    mesh_position = [
                        self.drawer_offset[di][0] + self.handle_offset[di][0] + sign * self.handle_separation[di] / 2,
                        -self.drawer_size[di][1] / 2 + self.drawer_offset[di][1] + self.handle_offset[di][0],
                        self.drawer_offset[di][2] + self.drawer_size[di][2] / 2 + self.front_size[di][2] + self.front_size[di][2] / 2]
                    tmp_mesh = Cuboid(self.handle_sizes[di][1],
                                     self.handle_sizes[di][0],
                                     self.handle_sizes[di][2],
                                     position=mesh_position,
                                     rotation=mesh_rotation)

                vertices_list.append(tmp_mesh.vertices)
                faces_list.append(tmp_mesh.faces + total_num_vertices)
                total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Drawer'
