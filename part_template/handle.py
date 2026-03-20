import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Regular_handle(ConceptTemplate):
    """
    Semantic: Handle
    Geometry: base Cuboid + vertical Cuboid connector + horizontal Cuboid grip, stacked along Z
    Used by: Doorhandle
    Parameters:
      fixed_part_size [w, h, d]: dimensions of the base (wall-mount) cuboid
      vertical_movable_size [w, h, d]: dimensions of the vertical connector cuboid
      horizontal_movable_size [w, h, d]: dimensions of the horizontal grip cuboid
      interpiece_offset_1 [x, y]: XY offset between base and vertical connector
      interpiece_offset_2 [x, y]: XY offset between vertical connector and grip
      position, rotation: global transform
    """
    def __init__(self, fixed_part_size, vertical_movable_size, horizontal_movable_size,
                 interpiece_offset_1, interpiece_offset_2,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.fixed_part_size = fixed_part_size
        self.vertical_movable_size = vertical_movable_size
        self.horizontal_movable_size = horizontal_movable_size
        self.interpiece_offset_1 = interpiece_offset_1
        self.interpiece_offset_2 = interpiece_offset_2

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.base_mesh = Cuboid(fixed_part_size[1], fixed_part_size[0], fixed_part_size[2],
                                position=[0, 0, fixed_part_size[2] / 2])
        vertices_list.append(self.base_mesh.vertices)
        faces_list.append(self.base_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.base_mesh.vertices)

        self.middle_mesh = Cuboid(vertical_movable_size[1], vertical_movable_size[0], vertical_movable_size[2],
                                  position=[interpiece_offset_1[0],
                                            interpiece_offset_1[1],
                                            fixed_part_size[2] + vertical_movable_size[2] / 2])
        vertices_list.append(self.middle_mesh.vertices)
        faces_list.append(self.middle_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.middle_mesh.vertices)

        self.main_mesh = Cuboid(horizontal_movable_size[1], horizontal_movable_size[0], horizontal_movable_size[2],
                                position=[interpiece_offset_1[0] + interpiece_offset_2[0],
                                          interpiece_offset_1[1] + interpiece_offset_2[1],
                                          fixed_part_size[2] + vertical_movable_size[2] + horizontal_movable_size[2] / 2])
        vertices_list.append(self.main_mesh.vertices)
        faces_list.append(self.main_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.main_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


class Knob_handle(ConceptTemplate):
    """
    Semantic: Handle
    Geometry: 3 stacked Z-axis Cylinders (base + sub + main knob), all X-rotated 90°
    Used by: Doorhandle
    Parameters:
      fixed_part_size [r, h]: radius and height of the base cylinder
      sub_size [r, h]: radius and height of the sub (neck) cylinder
      main_size [r, h]: radius and height of the main (knob) cylinder
      position, rotation: global transform
    """
    def __init__(self, fixed_part_size, sub_size, main_size,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.fixed_part_size = fixed_part_size
        self.sub_size = sub_size
        self.main_size = main_size

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.base_mesh = Cylinder(fixed_part_size[1], fixed_part_size[0], fixed_part_size[0],
                                  position=[0, 0, fixed_part_size[1] / 2],
                                  rotation=[np.pi / 2, 0, 0])
        vertices_list.append(self.base_mesh.vertices)
        faces_list.append(self.base_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.base_mesh.vertices)

        self.middle_mesh = Cylinder(sub_size[1], sub_size[0], sub_size[0],
                                    position=[0, 0, fixed_part_size[1] + sub_size[1] / 2],
                                    rotation=[np.pi / 2, 0, 0])
        vertices_list.append(self.middle_mesh.vertices)
        faces_list.append(self.middle_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.middle_mesh.vertices)

        self.main_mesh = Cylinder(main_size[1], main_size[0], main_size[0],
                                  position=[0, 0, fixed_part_size[1] + sub_size[1] + main_size[1] / 2],
                                  rotation=[np.pi / 2, 0, 0])
        vertices_list.append(self.main_mesh.vertices)
        faces_list.append(self.main_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.main_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'


class TShaped_handle(ConceptTemplate):
    """
    Semantic: Handle
    Geometry: base Cylinder stem + Cuboid crossbar forming a T-shape
    Used by: Doorhandle
    Parameters:
      sub_size [d, h]: diameter and height of the stem cylinder (radius = d/2)
      main_size [w, h, d]: dimensions of the crossbar cuboid
      interpiece_offset [x, y]: XY offset of crossbar relative to stem top
      position, rotation: global transform
    """
    def __init__(self, sub_size, main_size, interpiece_offset,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.sub_size = sub_size
        self.main_size = main_size
        self.interpiece_offset = interpiece_offset

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.sub_mesh = Cylinder(sub_size[1], sub_size[0] / 2, sub_size[0] / 2,
                                 position=[0, 0, sub_size[1] / 2],
                                 rotation=[np.pi / 2, 0, 0])
        vertices_list.append(self.sub_mesh.vertices)
        faces_list.append(self.sub_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.sub_mesh.vertices)

        self.main_mesh = Cuboid(main_size[1], main_size[0], main_size[2],
                                position=[interpiece_offset[0],
                                          interpiece_offset[1],
                                          sub_size[1] + main_size[2] / 2])
        vertices_list.append(self.main_mesh.vertices)
        faces_list.append(self.main_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.main_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Handle'
