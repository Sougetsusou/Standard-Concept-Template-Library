import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation
from knowledge_utils import *


class Solid_Back(ConceptTemplate):
    """
    Semantic: Back
    Geometry: single flat cuboid back panel, tilted by back_rotation about X
    Used by: Chair
    Parameters:
      size [w, h, d]: width, height, depth of the back panel
      back_rotation [angle_deg]: tilt angle about X axis (recline)
      position, rotation: global transform
    """
    def __init__(self, size, back_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        back_rotation = [x / 180 * np.pi for x in back_rotation]
        super().__init__(position, rotation)

        self.size = size
        self.back_rotation = back_rotation

        width, height, depth = size
        angle = back_rotation[0]

        mesh_rotation = [angle, 0, 0]
        mesh_position = [0, height / 2 * np.cos(angle), 0]
        self.mesh = Cuboid(height, width, depth,
                           position=mesh_position, rotation=mesh_rotation)
        self.vertices = self.mesh.vertices
        self.faces = self.mesh.faces

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Back'


class Ladder_Back(ConceptTemplate):
    """
    Semantic: Back
    Geometry: two vertical side rails + one top horizontal rail + N evenly-spaced horizontal rungs,
              all tilted by back_rotation about X
    Used by: Chair
    Parameters:
      main_horizontal_piece_size [w, h, d]: top rail dimensions
      main_vertical_piece_size [w, h, d]: side rail dimensions
      sub_horizontal_piece_size [h, d]: rung height and depth (width spans between rails)
      main_vertical_separation [gap]: X distance between the two rail centres
      sub_offset [y0]: Y offset of the first rung from the bottom of the rails
      interval_between_subs [dy]: Y spacing between consecutive rungs (descending)
      back_rotation [angle_deg]: tilt angle about X axis
      number_of_subs [n]: number of rungs
      position, rotation: global transform
    """
    def __init__(self, main_horizontal_piece_size, main_vertical_piece_size,
                 sub_horizontal_piece_size, main_vertical_separation, sub_offset,
                 interval_between_subs, back_rotation, number_of_subs,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        back_rotation = [x / 180 * np.pi for x in back_rotation]
        super().__init__(position, rotation)

        self.main_horizontal_piece_size = main_horizontal_piece_size
        self.main_vertical_piece_size = main_vertical_piece_size
        self.sub_horizontal_piece_size = sub_horizontal_piece_size
        self.main_vertical_separation = main_vertical_separation
        self.sub_offset = sub_offset
        self.interval_between_subs = interval_between_subs
        self.back_rotation = back_rotation
        self.number_of_subs = number_of_subs

        hw, hh, hd = main_horizontal_piece_size
        vw, vh, vd = main_vertical_piece_size
        sh, sd = sub_horizontal_piece_size
        gap = main_vertical_separation[0]
        y0 = sub_offset[0]
        dy = interval_between_subs[0]
        angle = back_rotation[0]
        n = int(number_of_subs[0])

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_rotation = [angle, 0, 0]

        for i in range(3 + n):
            if i < 2:
                # left and right vertical rails
                flag = 1 if i == 1 else -1
                pos = [flag * gap / 2, vh / 2 * np.cos(angle), 0]
                tmp_mesh = Cuboid(vh, vw, vd, position=pos, rotation=mesh_rotation)
            elif i == 2:
                # top horizontal rail
                pos = [0,
                       (vh + hh / 2) * np.cos(angle),
                       (vh + hh) / 2 * np.sin(angle)]
                tmp_mesh = Cuboid(hh, hw, hd, position=pos, rotation=mesh_rotation)
            else:
                # rungs — width spans between inner faces of the rails
                rung_y = vh / 2 + y0 - (i - 3) * dy
                pos = [0,
                       rung_y * np.cos(angle),
                       (y0 - (i - 3) * dy) * np.sin(angle)]
                tmp_mesh = Cuboid(sh, gap - vw, sd, position=pos, rotation=mesh_rotation)

            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Back'


class Splat_Back(ConceptTemplate):
    """
    Semantic: Back
    Geometry: two vertical side rails + one top horizontal rail + N evenly-spaced vertical splats,
              all tilted by back_rotation about X
    Used by: Chair
    Parameters:
      main_horizontal_piece_size [w, h, d]: top rail dimensions
      main_vertical_piece_size [w, h, d]: side rail dimensions
      sub_vertical_piece_size [w, d]: splat width and depth (height matches side rails)
      main_vertical_separation [gap]: X distance between the two rail centres
      sub_offset [x0]: X position of the first splat
      interval_between_subs [dx]: X spacing between consecutive splats
      back_rotation [angle_deg]: tilt angle about X axis
      number_of_subs [n]: number of splats
      position, rotation: global transform
    """
    def __init__(self, main_horizontal_piece_size, main_vertical_piece_size,
                 sub_vertical_piece_size, main_vertical_separation, sub_offset,
                 interval_between_subs, back_rotation, number_of_subs,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        back_rotation = [x / 180 * np.pi for x in back_rotation]
        super().__init__(position, rotation)

        self.main_horizontal_piece_size = main_horizontal_piece_size
        self.main_vertical_piece_size = main_vertical_piece_size
        self.sub_vertical_piece_size = sub_vertical_piece_size
        self.main_vertical_separation = main_vertical_separation
        self.sub_offset = sub_offset
        self.interval_between_subs = interval_between_subs
        self.back_rotation = back_rotation
        self.number_of_subs = number_of_subs

        hw, hh, hd = main_horizontal_piece_size
        vw, vh, vd = main_vertical_piece_size
        sw, sd = sub_vertical_piece_size
        gap = main_vertical_separation[0]
        x0 = sub_offset[0]
        dx = interval_between_subs[0]
        angle = back_rotation[0]
        n = int(number_of_subs[0])

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_rotation = [angle, 0, 0]

        for i in range(3 + n):
            if i < 2:
                flag = 1 if i == 1 else -1
                pos = [flag * gap / 2, vh / 2 * np.cos(angle), 0]
                tmp_mesh = Cuboid(vh, vw, vd, position=pos, rotation=mesh_rotation)
            elif i == 2:
                pos = [0,
                       (vh + hh / 2) * np.cos(angle),
                       (vh + hh) / 2 * np.sin(angle)]
                tmp_mesh = Cuboid(hh, hw, hd, position=pos, rotation=mesh_rotation)
            else:
                # vertical splats — same height as side rails, spaced along X
                pos = [x0 + (i - 3) * dx, vh / 2 * np.cos(angle), 0]
                tmp_mesh = Cuboid(vh, sw, sd, position=pos, rotation=mesh_rotation)

            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Back'


class Slat_Back(ConceptTemplate):
    """
    Semantic: Back
    Geometry: two vertical side rails (each individually Y-rotated for a fanned look) +
              N evenly-spaced horizontal slats, all tilted by back_rotation about X
    Used by: Chair
    Parameters:
      main_vertical_piece_size [w, h, d]: side rail dimensions
      sub_horizontal_piece_size [h, d]: slat height and depth
      main_vertical_separation [gap]: X distance between the two rail centres
      sub_horizontal_offset [y0]: Y offset of the first slat from the bottom
      interval_between_subs [dy]: Y spacing between consecutive slats (descending)
      main_vertical_rotation [ry_deg]: Y fan angle of each rail
      back_rotation [angle_deg]: tilt angle about X axis
      number_of_subs [n]: number of slats
      position, rotation: global transform
    """
    def __init__(self, main_vertical_piece_size, sub_horizontal_piece_size,
                 main_vertical_separation, sub_horizontal_offset, interval_between_subs,
                 main_vertical_rotation, back_rotation, number_of_subs,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        back_rotation = [x / 180 * np.pi for x in back_rotation]
        main_vertical_rotation = [x / 180 * np.pi for x in main_vertical_rotation]
        super().__init__(position, rotation)

        self.main_vertical_piece_size = main_vertical_piece_size
        self.sub_horizontal_piece_size = sub_horizontal_piece_size
        self.main_vertical_separation = main_vertical_separation
        self.sub_horizontal_offset = sub_horizontal_offset
        self.interval_between_subs = interval_between_subs
        self.main_vertical_rotation = main_vertical_rotation
        self.back_rotation = back_rotation
        self.number_of_subs = number_of_subs

        vw, vh, vd = main_vertical_piece_size
        sh, sd = sub_horizontal_piece_size
        gap = main_vertical_separation[0]
        y0 = sub_horizontal_offset[0]
        dy = interval_between_subs[0]
        ry = main_vertical_rotation[0]
        angle = back_rotation[0]
        n = int(number_of_subs[0])

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(2 + n):
            if i < 2:
                flag = 1 if i == 1 else -1
                # rotation_order="ZYX": back tilt (X) then fan (Y) applied in ZYX order
                rail_rotation = [angle, flag * ry, 0]
                pos = [flag * gap / 2, vh / 2 * np.cos(angle), 0]
                tmp_mesh = Cuboid(vh, vw, vd, position=pos, rotation=rail_rotation,
                                  rotation_order="ZYX")
            else:
                slat_rotation = [angle, 0, 0]
                rung_y = vh / 2 + y0 - (i - 2) * dy
                pos = [0,
                       rung_y * np.cos(angle) - vw / 2 * np.sin(ry) * np.sin(angle),
                       (y0 - (i - 2) * dy) * np.sin(angle) + vw / 2 * np.sin(ry) * np.cos(angle)]
                slat_width = gap - vw * np.cos(ry)
                tmp_mesh = Cuboid(sh, slat_width, sd, position=pos, rotation=slat_rotation)

            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Back'
