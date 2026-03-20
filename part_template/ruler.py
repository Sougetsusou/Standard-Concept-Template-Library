import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation
from knowledge_utils import *


class Symmetrical_Ruler(ConceptTemplate):
    """
    Semantic: Ruler
    Geometry: two mirror-image cuboid arms splayed symmetrically from a centre pivot, same size
    Used by: Ruler
    Parameters:
      size [w, h, d]: dimensions of each arm
      separation [gap]: half-gap between the two inner edges at the pivot
      left_right_offset [z]: z-offset (depth stagger) between the two arms
      body_rotation [angle_deg]: splay angle of each arm about the Z axis
      position, rotation: global transform
    """
    def __init__(self, size, separation, left_right_offset, body_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        body_rotation = [x / 180 * np.pi for x in body_rotation]
        super().__init__(position, rotation)

        self.size = size
        self.separation = separation
        self.left_right_offset = left_right_offset
        self.body_rotation = body_rotation

        width, height, depth = size
        gap = separation[0]
        z_off = left_right_offset[0]
        angle = body_rotation[0]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # left arm — rotated +angle, extends into negative x
        mesh_1_rotation = [0, 0, angle]
        mesh_1_position = [
            -gap - (width * np.cos(angle) + height * np.sin(angle)) / 2,
            (height * np.cos(angle) - width * np.sin(angle)) / 2,
            -z_off
        ]
        self.mesh_1 = Cuboid(height, width, depth,
                             position=mesh_1_position, rotation=mesh_1_rotation)
        vertices_list.append(self.mesh_1.vertices)
        faces_list.append(self.mesh_1.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_1.vertices)

        # right arm — rotated -angle, mirror of left
        mesh_2_rotation = [0, 0, -angle]
        mesh_2_position = [
            gap + (width * np.cos(angle) + height * np.sin(angle)) / 2,
            (height * np.cos(angle) - width * np.sin(angle)) / 2,
            z_off
        ]
        self.mesh_2 = Cuboid(height, width, depth,
                             position=mesh_2_position, rotation=mesh_2_rotation)
        vertices_list.append(self.mesh_2.vertices)
        faces_list.append(self.mesh_2.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_2.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # offset_first=True: translation applied before rotation (arms pivot around world origin)
        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Ruler'


class Asymmetrical_Ruler(ConceptTemplate):
    """
    Semantic: Ruler
    Geometry: two cuboid arms splayed from a centre pivot with independent sizes and opposite angles
    Used by: Ruler
    Parameters:
      left_size [w, h, d]: dimensions of the left arm
      right_size [w, h, d]: dimensions of the right arm
      separation [gap]: half-gap between inner edges at the pivot
      left_right_offset [z]: z-offset (depth stagger) between the two arms
      body_rotation [angle_deg]: splay angle magnitude; left arm +angle, right arm -angle
      position, rotation: global transform
    """
    def __init__(self, left_size, right_size, separation, left_right_offset, body_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        body_rotation = [x / 180 * np.pi for x in body_rotation]
        super().__init__(position, rotation)

        self.left_size = left_size
        self.right_size = right_size
        self.separation = separation
        self.left_right_offset = left_right_offset
        self.body_rotation = body_rotation

        lw, lh, ld = left_size
        rw, rh, rd = right_size
        gap = separation[0]
        z_off = left_right_offset[0]
        angle = body_rotation[0]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # left arm — rotated +angle
        mesh_1_rotation = [0, 0, angle]
        mesh_1_position = [
            -gap - lw / 2 * np.cos(angle) - lh / 2 * np.sin(angle),
            -lw / 2 * np.sin(angle) + lh / 2 * np.cos(angle),
            -z_off
        ]
        self.mesh_1 = Cuboid(lh, lw, ld, position=mesh_1_position, rotation=mesh_1_rotation)
        vertices_list.append(self.mesh_1.vertices)
        faces_list.append(self.mesh_1.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_1.vertices)

        # right arm — rotated -angle; sin(-angle) == -sin(angle), written explicitly for clarity
        mesh_2_rotation = [0, 0, -angle]
        mesh_2_position = [
            gap + rw / 2 * np.cos(angle) + rh / 2 * np.sin(angle),
            -rw / 2 * np.sin(angle) + rh / 2 * np.cos(angle),
            z_off
        ]
        self.mesh_2 = Cuboid(rh, rw, rd, position=mesh_2_position, rotation=mesh_2_rotation)
        vertices_list.append(self.mesh_2.vertices)
        faces_list.append(self.mesh_2.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_2.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # offset_first=True: translation applied before rotation (arms pivot around world origin)
        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Ruler'
