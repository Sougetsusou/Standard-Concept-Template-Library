import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Round_Switch(ConceptTemplate):
    """
    Semantic: Switch
    Geometry: N Cylinder discs arranged at given XY offsets
    Used by: Switch
    Parameters:
      number_of_switch [n]: number of switch cylinders
      size [r, h]: radius and height of each cylinder
      offset_1 [x, y]: XY position of switch 1
      offset_2 [x, y]: XY position of switch 2
      offset_3 [x, y]: XY position of switch 3
      offset_4 [x, y]: XY position of switch 4
      offset_Z [z]: shared Z offset
      switch_rotation [deg]: X rotation applied to each cylinder
      position, rotation: global transform
    """
    def __init__(self, number_of_switch, size, offset_1, offset_2, offset_3, offset_4,
                 offset_Z, switch_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        switch_rotation = [x / 180 * np.pi for x in switch_rotation]
        super().__init__(position, rotation)

        self.number_of_switch = number_of_switch
        self.size = size
        self.offset_1 = offset_1
        self.offset_2 = offset_2
        self.offset_3 = offset_3
        self.offset_4 = offset_4
        self.offset_Z = offset_Z
        self.switch_rotation = switch_rotation

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        offsets = [offset_1, offset_2, offset_3, offset_4]

        for i in range(int(number_of_switch[0])):
            tmp = Cylinder(size[1], size[0], size[0],
                           position=[offsets[i][0], offsets[i][1], offset_Z[0]],
                           rotation=[np.pi / 2 + switch_rotation[0], 0, 0])
            vertices_list.append(tmp.vertices)
            faces_list.append(tmp.faces + total_num_vertices)
            total_num_vertices += len(tmp.vertices)

        if not vertices_list:
            raise ValueError(f"{self.__class__.__name__}: no geometry was instantiated")
        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation, offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Switch'


class FlipX_Switch(ConceptTemplate):
    """
    Semantic: Switch
    Geometry: N Cuboids arranged along X axis, each X-rotated
    Used by: Switch
    Parameters:
      number_of_switch [n]: number of switches
      size [w, h, d]: dimensions of each cuboid
      switch_rotation [deg]: X rotation of each cuboid
      separation [s]: X gap between switches
      position, rotation: global transform
    """
    def __init__(self, number_of_switch, size, switch_rotation, separation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        switch_rotation = [x / 180 * np.pi for x in switch_rotation]
        super().__init__(position, rotation)

        self.number_of_switch = number_of_switch
        self.size = size
        self.separation = separation
        self.switch_rotation = switch_rotation

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(int(number_of_switch[0])):
            tmp = Cuboid(size[1], size[0], size[2],
                         position=[(separation[0] + size[0]) * i, 0, 0],
                         rotation=[switch_rotation[0], 0, 0])
            vertices_list.append(tmp.vertices)
            faces_list.append(tmp.faces + total_num_vertices)
            total_num_vertices += len(tmp.vertices)

        if not vertices_list:
            raise ValueError(f"{self.__class__.__name__}: no geometry was instantiated")
        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation, offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Switch'


class FlipY_Switch(ConceptTemplate):
    """
    Semantic: Switch
    Geometry: N Cuboids arranged along X axis, each Y-rotated
    Used by: Switch
    Parameters:
      number_of_switch [n]: number of switches
      size [w, h, d]: dimensions of each cuboid
      switch_rotation [deg]: Y rotation of each cuboid
      separation [s]: X gap between switches
      position, rotation: global transform
    """
    def __init__(self, number_of_switch, size, switch_rotation, separation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        switch_rotation = [x / 180 * np.pi for x in switch_rotation]
        super().__init__(position, rotation)

        self.number_of_switch = number_of_switch
        self.size = size
        self.separation = separation
        self.switch_rotation = switch_rotation

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(int(number_of_switch[0])):
            tmp = Cuboid(size[1], size[0], size[2],
                         position=[(separation[0] + size[0]) * i, 0, 0],
                         rotation=[0, switch_rotation[0], 0])
            vertices_list.append(tmp.vertices)
            faces_list.append(tmp.faces + total_num_vertices)
            total_num_vertices += len(tmp.vertices)

        if not vertices_list:
            raise ValueError(f"{self.__class__.__name__}: no geometry was instantiated")
        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation, offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Switch'


class Lever_Switch(ConceptTemplate):
    """
    Semantic: Switch
    Geometry: N lever assemblies, each a base Cylinder + a tapered main Cylinder pivot-rotated
    Used by: Switch
    Parameters:
      number_of_switch [n]: number of lever switches
      base_size [r, h]: radius and height of base cylinder
      main_size [r_bottom, r_top, h]: bottom radius, top radius, height of main cylinder
      inter_offset [x, y, z]: offset applied to main cylinder after rotation
      switch_rotation [deg]: X rotation of main cylinder
      separation [s]: X spacing between levers
      position, rotation: global transform
    """
    def __init__(self, number_of_switch, base_size, main_size, inter_offset,
                 switch_rotation, separation, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        switch_rotation = [x / 180 * np.pi for x in switch_rotation]
        super().__init__(position, rotation)

        self.number_of_switch = number_of_switch
        self.base_size = base_size
        self.main_size = main_size
        self.inter_offset = inter_offset
        self.switch_rotation = switch_rotation
        self.separation = separation

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(int(number_of_switch[0])):
            x_off = (separation[0] + main_size[0]) * i

            tmp_base = Cylinder(base_size[1], base_size[0], base_size[0],
                                position=[x_off, 0, base_size[1] / 2],
                                rotation=[np.pi / 2, 0, 0])
            vertices_list.append(tmp_base.vertices)
            faces_list.append(tmp_base.faces + total_num_vertices)
            total_num_vertices += len(tmp_base.vertices)

            tmp_main = Cylinder(main_size[2], main_size[1], main_size[0],
                                position=[x_off, 0, main_size[2] / 2],
                                rotation=[np.pi / 2, 0, 0])
            tmp_main.vertices = apply_transformation(tmp_main.vertices,
                                                     position=[0, 0, 0],
                                                     rotation=[switch_rotation[0], 0, 0])
            tmp_main.vertices = apply_transformation(tmp_main.vertices,
                                                     position=[inter_offset[0],
                                                               inter_offset[1],
                                                               inter_offset[2] + base_size[1]],
                                                     rotation=[0, 0, 0])
            vertices_list.append(tmp_main.vertices)
            faces_list.append(tmp_main.faces + total_num_vertices)
            total_num_vertices += len(tmp_main.vertices)

        if not vertices_list:
            raise ValueError(f"{self.__class__.__name__}: no geometry was instantiated")
        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation, offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Switch'
