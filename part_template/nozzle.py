import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Press_Nozzle(ConceptTemplate):
    """
    Semantic: Nozzle
    Geometry: N stacked Cylinders (body levels) + 1 or 2 angled Cuboid nozzle segments
    Used by: Dispenser
    Parameters:
      num_levels [n]: number of body cylinder levels (1..5)
      level_1..5_size [r, h]: radius and height of each level cylinder
      num_nozzles [n]: number of nozzle segments (1 or 2)
      nozzle_size [w, h]: width and height of each nozzle cuboid cross-section
      nozzle_length [l1, l2]: length of each nozzle segment
      nozzle_offset [y]: Y offset of nozzle base from top of body
      nozzle_rotation [x1_deg, x2_deg]: X rotation of each nozzle segment
      position, rotation: global transform
    """
    def __init__(self, num_levels, level_1_size, level_2_size, level_3_size, level_4_size, level_5_size,
                 num_nozzles, nozzle_size, nozzle_length, nozzle_offset, nozzle_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        nozzle_rotation = [x / 180 * np.pi for x in nozzle_rotation]
        super().__init__(position, rotation)

        self.num_levels = num_levels
        self.level_1_size = level_1_size
        self.level_2_size = level_2_size
        self.level_3_size = level_3_size
        self.level_4_size = level_4_size
        self.level_5_size = level_5_size
        self.num_nozzles = num_nozzles
        self.nozzle_size = nozzle_size
        self.nozzle_length = nozzle_length
        self.nozzle_offset = nozzle_offset
        self.nozzle_rotation = nozzle_rotation

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        level_sizes = [level_1_size, level_2_size, level_3_size, level_4_size, level_5_size]
        nozzle_w, nozzle_h = nozzle_size[0], nozzle_size[1]
        nozzle_l1 = nozzle_length[0]
        nozzle_off = nozzle_offset[0]
        nozzle_rot1 = nozzle_rotation[0]

        delta_height = 0
        for i in range(int(num_levels[0])):
            lv_r, lv_h = level_sizes[i][0], level_sizes[i][1]
            delta_height += lv_h / 2
            tmp_mesh = Cylinder(lv_h, lv_r,
                                position=[0, delta_height, 0])
            delta_height += lv_h / 2
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

        top_r = level_sizes[int(num_levels[0]) - 1][0]
        total_offset_z = nozzle_l1 / 2 * np.cos(nozzle_rot1) + top_r
        self.nozzle_mesh = Cuboid(nozzle_h, nozzle_w, nozzle_l1,
                                  position=[0,
                                            delta_height + nozzle_off - nozzle_l1 / 2 * np.sin(nozzle_rot1),
                                            total_offset_z],
                                  rotation=[nozzle_rot1, 0, 0])
        vertices_list.append(self.nozzle_mesh.vertices)
        faces_list.append(self.nozzle_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.nozzle_mesh.vertices)

        if num_nozzles[0] == 2:
            nozzle_l2 = nozzle_length[1]
            nozzle_rot2 = nozzle_rotation[1]
            total2_offset_z = (nozzle_l1 * np.cos(nozzle_rot1) + top_r
                               + nozzle_l2 * np.cos(nozzle_rot2) / 2)
            self.nozzle_mesh2 = Cuboid(nozzle_h, nozzle_w, nozzle_l2,
                                       position=[0,
                                                 delta_height + nozzle_off
                                                 - nozzle_l1 * np.sin(nozzle_rot1)
                                                 - nozzle_l2 / 2 * np.sin(nozzle_rot2),
                                                 total2_offset_z],
                                       rotation=[nozzle_rot2, 0, 0])
            vertices_list.append(self.nozzle_mesh2.vertices)
            faces_list.append(self.nozzle_mesh2.faces + total_num_vertices)
            total_num_vertices += len(self.nozzle_mesh2.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order='YXZ')

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Nozzle'


class Spray_Nozzle(ConceptTemplate):
    """
    Semantic: Nozzle
    Geometry: bottom Cylinder body + middle Cuboid + angled top Cuboid cap
              + Cylinder nozzle tip + angled Cuboid handle
    Used by: Dispenser
    Parameters:
      bottom_size [r, h]: radius and height of the bottom cylinder
      middle_size [w, h, d]: dimensions of the middle cuboid
      top_size [w, h, d]: dimensions of the top cap cuboid
      top_offset [z]: Z offset of the top cap from middle top
      top_rotation [x_deg]: X rotation of the top cap
      nozzle_size [r, h]: radius and height of the nozzle cylinder tip
      handle_size [w, h, d]: dimensions of the handle cuboid
      handle_offset [z]: Z offset of handle along top cap
      handle_rotation [x_deg]: X rotation of handle relative to top cap
      position, rotation: global transform
    """
    def __init__(self, bottom_size, middle_size, top_size, top_offset, top_rotation,
                 nozzle_size, handle_size, handle_offset, handle_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        top_rotation = [x / 180 * np.pi for x in top_rotation]
        handle_rotation = [x / 180 * np.pi for x in handle_rotation]
        super().__init__(position, rotation)

        self.bottom_size = bottom_size
        self.middle_size = middle_size
        self.top_size = top_size
        self.top_offset = top_offset
        self.top_rotation = top_rotation
        self.nozzle_size = nozzle_size
        self.handle_size = handle_size
        self.handle_offset = handle_offset
        self.handle_rotation = handle_rotation

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        delta_height = bottom_size[1] / 2
        self.bottom_mesh = Cylinder(bottom_size[1], bottom_size[0],
                                    position=[0, delta_height, 0])
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        delta_height += bottom_size[1] / 2 + middle_size[1] / 2
        self.middle_mesh = Cuboid(middle_size[1], middle_size[0], middle_size[2],
                                  position=[0, delta_height, 0])
        vertices_list.append(self.middle_mesh.vertices)
        faces_list.append(self.middle_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.middle_mesh.vertices)

        top_offset_y = -top_offset[0] * np.tan(top_rotation[0])
        delta_height += middle_size[1] / 2 + top_size[1] / 2
        self.top_mesh = Cuboid(top_size[1], top_size[0], top_size[2],
                               position=[0,
                                         delta_height + top_offset_y + top_offset[0] * np.sin(top_rotation[0]),
                                         top_offset[0] * np.cos(top_rotation[0])],
                               rotation=[top_rotation[0], 0, 0])
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        nozzle_total_offset_z = top_offset[0] + (top_size[2] + nozzle_size[1]) / 2
        self.nozzle_mesh = Cylinder(nozzle_size[1], nozzle_size[0],
                                    position=[0,
                                              delta_height + top_offset_y - nozzle_total_offset_z * np.sin(top_rotation[0]),
                                              nozzle_total_offset_z * np.cos(top_rotation[0])],
                                    rotation=[top_rotation[0] + np.pi / 2, 0, 0])
        vertices_list.append(self.nozzle_mesh.vertices)
        faces_list.append(self.nozzle_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.nozzle_mesh.vertices)

        handle_total_offset_z = (top_offset[0] + top_size[2] / 2 + handle_offset[0]
                                 - handle_size[2] / 2 - handle_size[1] / 2 * np.sin(handle_rotation[0]))
        handle_total_offset_y = -handle_size[1] / 2 * np.cos(handle_rotation[0]) - top_size[1] / 2
        handle_mesh_rotation = [top_rotation[0], 0, 0]
        handle_mesh_position_1 = adjust_position_from_rotation(
            [0, handle_total_offset_y, handle_total_offset_z], handle_mesh_rotation)
        handle_mesh_position = list_add(handle_mesh_position_1, [0, delta_height + top_offset_y, 0])
        handle_mesh_rotation[0] += handle_rotation[0]
        self.handle_mesh = Cuboid(handle_size[1], handle_size[0], handle_size[2],
                                  position=handle_mesh_position,
                                  rotation=handle_mesh_rotation)
        vertices_list.append(self.handle_mesh.vertices)
        faces_list.append(self.handle_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.handle_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order='YXZ')

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Nozzle'
