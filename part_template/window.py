import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Symmetrical_Window(ConceptTemplate):
    """
    Semantic: Window
    Geometry: outer Rectangular_Ring frame + N inner sub-frames (each a Rectangular_Ring)
              + N glass Cuboid panes
    Used by: Window
    Parameters:
      outside_frame_size [w, h, d]: outer dimensions of the outer frame
      outside_frame_inner_size [w, h]: inner opening of the outer frame
      outside_frame_inner_outer_offset [x, y]: XY offset of inner opening within outer frame
      number_of_window [n]: number of inner sub-frames (0..4)
      size_0..3 [w, d]: width and depth of each sub-frame (height shared from outer inner)
      glass_size_0..3 [w, h, d]: dimensions of each glass pane
      glass_offset_0..3 [x, y, z]: position offset of each glass pane
      offset_x [x0..x3]: X positions of each sub-frame
      offset_z [z]: shared Z offset for all sub-frames
      position, rotation: global transform
    """
    def __init__(self, outside_frame_size, outside_frame_inner_size,
                 outside_frame_inner_outer_offset,
                 number_of_window,
                 size_0, glass_size_0, glass_offset_0,
                 size_1, glass_size_1, glass_offset_1,
                 size_2, glass_size_2, glass_offset_2,
                 size_3, glass_size_3, glass_offset_3,
                 offset_x, offset_z,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.outside_frame_size = outside_frame_size
        self.outside_frame_inner_size = outside_frame_inner_size
        self.outside_frame_inner_outer_offset = outside_frame_inner_outer_offset
        self.number_of_window = number_of_window

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # outer frame
        outer_frame = Rectangular_Ring(outside_frame_size[2],
                                       outside_frame_size[0],
                                       outside_frame_size[1],
                                       outside_frame_inner_size[0],
                                       outside_frame_inner_size[1],
                                       outside_frame_inner_outer_offset,
                                       rotation=[np.pi / 2, 0, 0])
        vertices_list.append(outer_frame.vertices)
        faces_list.append(outer_frame.faces + total_num_vertices)
        total_num_vertices += len(outer_frame.vertices)

        # inner sub-frames and glass panes
        window_size = [
            {"frame_size": size_0, "glass_size": glass_size_0, "glass_offset": glass_offset_0},
            {"frame_size": size_1, "glass_size": glass_size_1, "glass_offset": glass_offset_1},
            {"frame_size": size_2, "glass_size": glass_size_2, "glass_offset": glass_offset_2},
            {"frame_size": size_3, "glass_size": glass_size_3, "glass_offset": glass_offset_3},
        ]
        for ws in window_size:
            ws["frame_size"] = [ws["frame_size"][0], outside_frame_inner_size[1], ws["frame_size"][1]]

        layer_z = [
            offset_z[0],
            outside_frame_size[1] / 2 + size_1[1] / 2 + offset_z[0],
            outside_frame_size[1] / 2 + size_1[1] + size_2[1] / 2 + offset_z[0],
            outside_frame_size[1] / 2 + size_1[1] + size_2[1] + size_3[1] / 2 + offset_z[0],
        ]

        for i in range(int(number_of_window[0])):
            ws = window_size[i]
            pos = [offset_x[i], outside_frame_inner_outer_offset[1], layer_z[i]]

            tmp_frame = Rectangular_Ring(ws["frame_size"][2],
                                         ws["frame_size"][0],
                                         ws["frame_size"][1],
                                         ws["glass_size"][0],
                                         ws["glass_size"][1],
                                         [ws["glass_offset"][0], -ws["glass_offset"][1]],
                                         position=pos,
                                         rotation=[np.pi / 2, 0, 0])
            vertices_list.append(tmp_frame.vertices)
            faces_list.append(tmp_frame.faces + total_num_vertices)
            total_num_vertices += len(tmp_frame.vertices)

            glass_pos = [pos[j] + ws["glass_offset"][j] for j in range(3)]
            tmp_glass = Cuboid(ws["glass_size"][1], ws["glass_size"][0], ws["glass_size"][2],
                               position=glass_pos)
            vertices_list.append(tmp_glass.vertices)
            faces_list.append(tmp_glass.faces + total_num_vertices)
            total_num_vertices += len(tmp_glass.vertices)

        if not vertices_list:
            raise ValueError(f"{self.__class__.__name__}: no geometry was instantiated")
        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Window'


class Asymmetrical_Window(ConceptTemplate):
    """
    Semantic: Window
    Geometry: N inner sub-frames (each a Rectangular_Ring) + N glass Cuboid panes,
              stacked along Z with individual X offsets; no outer frame
    Used by: Window
    Parameters:
      outside_frame_inner_size [w, h]: shared inner height for all sub-frames
      outside_frame_inner_outer_offset [x, y]: shared XY offset for sub-frame positioning
      number_of_window [n]: number of sub-frames (0..4)
      size_0..3 [w, d]: width and depth of each sub-frame
      glass_size_0..3 [w, h, d]: dimensions of each glass pane
      glass_offset_0..3 [x, y, z]: position offset of each glass pane
      offset_x [x0..x3]: X positions of each sub-frame
      offset_z [z]: base Z offset
      position, rotation: global transform
    """
    def __init__(self, outside_frame_inner_size, outside_frame_inner_outer_offset,
                 number_of_window,
                 size_0, glass_size_0, glass_offset_0,
                 size_1, glass_size_1, glass_offset_1,
                 size_2, glass_size_2, glass_offset_2,
                 size_3, glass_size_3, glass_offset_3,
                 offset_x, offset_z,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.outside_frame_inner_size = outside_frame_inner_size
        self.outside_frame_inner_outer_offset = outside_frame_inner_outer_offset
        self.number_of_window = number_of_window

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        window_size = [
            {"frame_size": size_0, "glass_size": glass_size_0, "glass_offset": glass_offset_0},
            {"frame_size": size_1, "glass_size": glass_size_1, "glass_offset": glass_offset_1},
            {"frame_size": size_2, "glass_size": glass_size_2, "glass_offset": glass_offset_2},
            {"frame_size": size_3, "glass_size": glass_size_3, "glass_offset": glass_offset_3},
        ]
        for ws in window_size:
            ws["frame_size"] = [ws["frame_size"][0], outside_frame_inner_size[1], ws["frame_size"][1]]

        layer_z = [
            offset_z[0],
            size_0[1] / 2 + size_1[1] / 2 + offset_z[0],
            size_0[1] / 2 + size_1[1] + size_2[1] / 2 + offset_z[0],
            size_0[1] / 2 + size_1[1] + size_2[1] + size_3[1] / 2 + offset_z[0],
        ]

        for i in range(int(number_of_window[0])):
            ws = window_size[i]
            pos = [offset_x[i], outside_frame_inner_outer_offset[1], layer_z[i]]

            tmp_frame = Rectangular_Ring(ws["frame_size"][2],
                                         ws["frame_size"][0],
                                         ws["frame_size"][1],
                                         ws["glass_size"][0],
                                         ws["glass_size"][1],
                                         [ws["glass_offset"][0], -ws["glass_offset"][1]],
                                         position=pos,
                                         rotation=[np.pi / 2, 0, 0])
            vertices_list.append(tmp_frame.vertices)
            faces_list.append(tmp_frame.faces + total_num_vertices)
            total_num_vertices += len(tmp_frame.vertices)

            glass_pos = [pos[j] + ws["glass_offset"][j] for j in range(3)]
            tmp_glass = Cuboid(ws["glass_size"][1], ws["glass_size"][0], ws["glass_size"][2],
                               position=glass_pos)
            vertices_list.append(tmp_glass.vertices)
            faces_list.append(tmp_glass.faces + total_num_vertices)
            total_num_vertices += len(tmp_glass.vertices)

        if not vertices_list:
            raise ValueError(f"{self.__class__.__name__}: no geometry was instantiated")
        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Window'
