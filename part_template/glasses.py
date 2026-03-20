import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Trapezoidal_Glasses(ConceptTemplate):
    """
    Semantic: Glasses
    Geometry: 2 mirrored trapezoidal lens frames, each a single tapered Cuboid,
              pivot-rotated about the inner edge
    Used by: Eyeglasses
    Parameters:
      size [w_top, w_bottom, h, d]: top width, bottom width, height, depth of each lens
      interval [gap]: X gap between the two lenses
      glass_rotation [y_deg, z_deg]: Y and Z rotation of each lens
      position, rotation: global transform
    """
    def __init__(self, size, interval, glass_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        glass_rotation = [x / 180 * np.pi for x in glass_rotation]
        super().__init__(position, rotation)

        self.size = size
        self.interval = interval
        self.glass_rotation = glass_rotation

        w_top, w_bot, h, d = size[0], size[1], size[2], size[3]
        gap = interval[0]
        gr_y, gr_z = glass_rotation[0], glass_rotation[1]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        right_mesh = Cuboid(h, w_top, d, w_bot, d)
        right_mesh.vertices = np.concatenate(
            (right_mesh.vertices, np.array([[0, 0, -d / 2]])), axis=0)
        right_mesh.vertices = apply_transformation(
            right_mesh.vertices,
            rotation=[0, gr_y, gr_z],
            position=[0, 0, 0])
        center = right_mesh.vertices[-1]
        right_mesh.vertices = apply_transformation(
            right_mesh.vertices,
            position=[-center[0] + w_top * np.cos(gr_y) * np.cos(gr_z) / 2 + gap / 2,
                      -center[1],
                      -center[2] + w_top * np.sin(gr_y) / 2],
            rotation=[0, 0, 0])
        vertices_list.append(right_mesh.vertices)
        faces_list.append(right_mesh.faces + total_num_vertices)
        total_num_vertices += len(right_mesh.vertices)

        left_mesh = Cuboid(h, w_top, d, w_bot, d)
        left_mesh.vertices = np.concatenate(
            (left_mesh.vertices, np.array([[0, 0, -d / 2]])), axis=0)
        left_mesh.vertices = apply_transformation(
            left_mesh.vertices,
            rotation=[0, -gr_y, -gr_z],
            position=[0, 0, 0])
        center = left_mesh.vertices[-1]
        left_mesh.vertices = apply_transformation(
            left_mesh.vertices,
            position=[-center[0] - w_top * np.cos(gr_y) * np.cos(gr_z) / 2 - gap / 2,
                      -center[1],
                      -center[2] + w_top * np.sin(gr_y) / 2],
            rotation=[0, 0, 0])
        vertices_list.append(left_mesh.vertices)
        faces_list.append(left_mesh.faces + total_num_vertices)
        total_num_vertices += len(left_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Glasses'


class TrapezoidalFrame_Glasses(ConceptTemplate):
    """
    Semantic: Glasses
    Geometry: 2 mirrored trapezoidal lens frames, each built from 4 Cuboid border strips
              (top, bottom, left side, right side), pivot-rotated about the inner edge
    Used by: Eyeglasses
    Parameters:
      size [w_top, w_bottom, h, d]: outer top width, outer bottom width, height, depth
      interval [gap]: X gap between the two lenses
      glass_rotation [y_deg, z_deg]: Y and Z rotation of each lens frame
      top_offset [x]: X offset of the top edge relative to bottom
      width [t]: border strip width
      position, rotation: global transform
    """
    def __init__(self, size, interval, glass_rotation, top_offset, width,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        glass_rotation = [x / 180 * np.pi for x in glass_rotation]
        super().__init__(position, rotation)

        self.size = size
        self.interval = interval
        self.glass_rotation = glass_rotation
        self.top_offset = top_offset
        self.width = width

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        def _make_frame_meshes(sign):
            w = width[0]
            h = size[2]
            top_w = size[0]
            bot_w = size[1]
            d = size[3]
            tx = top_offset[0]

            meshes = [
                Cuboid(w, top_w, d,
                       bottom_length=(bot_w * w / h + top_w * (h - w) / h),
                       bottom_width=d,
                       top_offset=[-tx * w / h, 0],
                       position=[tx * w / h, (h - w) / 2, 0]),
                Cuboid(w, (bot_w * (h - w) / h + top_w * w / h), d,
                       bottom_length=bot_w, bottom_width=d,
                       top_offset=[-tx * w / h, 0],
                       position=[tx, -(h - w) / 2, 0]),
                Cuboid(h - 2 * w,
                       w * np.sqrt((top_w - tx - bot_w) ** 2 + h ** 2) / h, d,
                       bottom_length=w * np.sqrt((top_w - tx - bot_w) ** 2 + h ** 2) / h,
                       bottom_width=d,
                       top_offset=[-((bot_w * w / h + top_w * (h - w) / h) - (bot_w * (h - w) / h + top_w * w / h)) / 2 - tx * (h - 2 * w) / h, 0],
                       position=[(-(bot_w * (h - w) / h + top_w * w / h) / 2 + tx * (h - w) / h + (w * np.sqrt((top_w - tx - bot_w) ** 2 + h ** 2) / h) / 2), 0, 0]),
                Cuboid(h - 2 * w,
                       w * np.sqrt((top_w + tx - bot_w) ** 2 + h ** 2) / h, d,
                       bottom_length=w * np.sqrt((top_w + tx - bot_w) ** 2 + h ** 2) / h,
                       bottom_width=d,
                       top_offset=[((bot_w * w / h + top_w * (h - w) / h) - (bot_w * (h - w) / h + top_w * w / h)) / 2 - tx * (h - 2 * w) / h, 0],
                       position=[((bot_w * (h - w) / h + top_w * w / h) / 2 + tx * (h - w) / h - (w * np.sqrt((top_w + tx - bot_w) ** 2 + h ** 2) / h) / 2), 0, 0]),
            ]
            return meshes

        for sign, gr_y, gr_z, x_dir in [(1, glass_rotation[0], glass_rotation[1], 1),
                                         (-1, -glass_rotation[0], -glass_rotation[1], -1)]:
            meshes = _make_frame_meshes(sign)
            anchor = np.array([[top_offset[0], 0, -size[3] / 2]])
            meshes[0].vertices = np.concatenate((meshes[0].vertices, anchor), axis=0)
            for m in meshes:
                m.vertices = np.concatenate((m.vertices, anchor), axis=0)
                m.vertices = apply_transformation(m.vertices,
                                                  rotation=[0, gr_y, gr_z],
                                                  position=[0, 0, 0])
                center = m.vertices[-1]
                m.vertices = apply_transformation(
                    m.vertices,
                    position=[-center[0] + x_dir * size[0] * np.cos(glass_rotation[0]) * np.cos(glass_rotation[1]) / 2 + x_dir * interval[0] / 2,
                              -center[1],
                              -center[2] + size[0] * np.sin(glass_rotation[0]) / 2],
                    rotation=[0, 0, 0])
                vertices_list.append(m.vertices)
                faces_list.append(m.faces + total_num_vertices)
                total_num_vertices += len(m.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Glasses'


class Round_Glasses(ConceptTemplate):
    """
    Semantic: Glasses
    Geometry: 2 mirrored Ring (annular) lens frames, pivot-rotated about the inner edge
    Used by: Eyeglasses
    Parameters:
      size [outer_r, inner_r, d]: outer radius, inner radius, depth of each ring lens
      interval [gap]: X gap between the two lenses
      glass_rotation [y_deg, z_deg]: Y and Z rotation of each lens
      position, rotation: global transform
    """
    def __init__(self, size, interval, glass_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        glass_rotation = [x / 180 * np.pi for x in glass_rotation]
        super().__init__(position, rotation)

        self.size = size
        self.interval = interval
        self.glass_rotation = glass_rotation

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        outer_r, inner_r, d = size[0], size[1], size[2]
        gap = interval[0]
        gr_y, gr_z = glass_rotation[0], glass_rotation[1]

        self.right_mesh = Cylinder(d, outer_r, outer_r,
                                   inner_r, inner_r,
                                   rotation=[np.pi / 2, 0, 0])
        self.right_mesh.vertices = np.concatenate(
            (self.right_mesh.vertices, np.array([[0, 0, 0]])), axis=0)
        self.right_mesh.vertices = apply_transformation(
            self.right_mesh.vertices,
            rotation=[0, gr_y, gr_z],
            position=[0, 0, 0],
            # YZX order: pivot rotation about inner edge of ring lens
            rotation_order="YZX")
        center = self.right_mesh.vertices[-1]
        edge = [self.right_mesh.vertices[3], self.right_mesh.vertices[259]]
        self.right_mesh.vertices = apply_transformation(
            self.right_mesh.vertices,
            position=[[-edge[1][0] + gap / 2, -center[1], -edge[0][2]]],
            rotation=[0, 0, 0])
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        self.left_mesh = Cylinder(d, outer_r, outer_r,
                                  inner_r, inner_r,
                                  rotation=[np.pi / 2, 0, 0])
        self.left_mesh.vertices = np.concatenate(
            (self.left_mesh.vertices, np.array([[0, 0, 0]])), axis=0)
        self.left_mesh.vertices = apply_transformation(
            self.left_mesh.vertices,
            rotation=[0, -gr_y, -gr_z],
            position=[0, 0, 0],
            # YZX order: pivot rotation about inner edge of ring lens
            rotation_order="YZX")
        center = self.left_mesh.vertices[-1]
        edge = [self.left_mesh.vertices[3], self.left_mesh.vertices[259]]
        self.left_mesh.vertices = apply_transformation(
            self.left_mesh.vertices,
            position=[[-edge[0][0] - gap / 2, -center[1], -edge[1][2]]],
            rotation=[0, 0, 0])
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Glasses'


class RoundFrame_Glasses(ConceptTemplate):
    """
    Semantic: Glasses
    Geometry: 2 mirrored Ring (elliptical annular) lens frames, pivot-rotated about the inner edge
    Used by: Eyeglasses
    Parameters:
      size [outer_rx, outer_ry, d]: outer X-radius, outer Y-radius, depth
      interval [gap]: X gap between the two lenses
      width [t]: ring border width
      glass_rotation [y_deg, z_deg]: Y and Z rotation of each lens
      position, rotation: global transform
    """
    def __init__(self, size, interval, width, glass_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        glass_rotation = [x / 180 * np.pi for x in glass_rotation]
        super().__init__(position, rotation)

        self.size = size
        self.interval = interval
        self.glass_rotation = glass_rotation
        self.width = width

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        outer_rx, outer_ry, d = size[0], size[1], size[2]
        gap = interval[0]
        t = width[0]
        gr_y, gr_z = glass_rotation[0], glass_rotation[1]

        self.right_mesh = Ring(height=d,
                               inner_top_radius=outer_rx - t,
                               outer_top_radius=outer_rx,
                               x_z_ratio=outer_rx / outer_ry,
                               rotation=[np.pi / 2, 0, 0],
                               position=[0, 0, 0])
        self.right_mesh.vertices = np.concatenate(
            (self.right_mesh.vertices, np.array([[0, 0, 0]])), axis=0)
        self.right_mesh.vertices = apply_transformation(
            self.right_mesh.vertices,
            rotation=[0, gr_y, gr_z],
            position=[0, 0, 0],
            # YZX order: pivot rotation about inner edge of elliptical ring lens
            rotation_order="YZX")
        center = self.right_mesh.vertices[-1]
        edge = [self.right_mesh.vertices[1], self.right_mesh.vertices[513]]
        self.right_mesh.vertices = apply_transformation(
            self.right_mesh.vertices,
            position=[[-edge[1][0] + gap / 2, -center[1], -edge[0][2]]],
            rotation=[0, 0, 0])
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        self.left_mesh = Ring(height=d,
                              inner_top_radius=outer_rx - t,
                              outer_top_radius=outer_rx,
                              x_z_ratio=outer_rx / outer_ry,
                              rotation=[np.pi / 2, 0, 0],
                              position=[0, 0, 0])
        self.left_mesh.vertices = np.concatenate(
            (self.left_mesh.vertices, np.array([[0, 0, 0]])), axis=0)
        self.left_mesh.vertices = apply_transformation(
            self.left_mesh.vertices,
            rotation=[0, -gr_y, -gr_z],
            position=[0, 0, 0],
            # YZX order: pivot rotation about inner edge of elliptical ring lens
            rotation_order="YZX")
        center = self.left_mesh.vertices[-1]
        edge = [self.left_mesh.vertices[1], self.left_mesh.vertices[513]]
        self.left_mesh.vertices = apply_transformation(
            self.left_mesh.vertices,
            position=[[-edge[0][0] - gap / 2, -center[1], -edge[1][2]]],
            rotation=[0, 0, 0])
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Glasses'
