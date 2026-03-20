import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import copy
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, get_rodrigues_matrix
from knowledge_utils import *


class Regular_Jaw(ConceptTemplate):
    """
    Semantic: Jaw
    Geometry: two mirror-image cuboid jaw plates, each rotated about X from a separation offset
    Used by: Clip
    Parameters:
      size [w, h, d]: dimensions of each jaw plate
      jaw_separation [gap]: Z offset of each plate from the centre plane
      jaw_rotation [angle_deg]: opening angle of each jaw about the X axis
      position, rotation: global transform
    """
    def __init__(self, size, jaw_separation, jaw_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        jaw_rotation = [x / 180 * np.pi for x in jaw_rotation]
        super().__init__(position, rotation)

        self.size = size
        self.jaw_separation = jaw_separation
        self.jaw_rotation = jaw_rotation

        width, height, depth = size
        gap = jaw_separation[0]
        angle = jaw_rotation[0]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # upper jaw — translated to +z, then rotated -angle about X (opens upward)
        # pivot-rotation anti-pattern: mesh placed at offset first, then rotated about origin
        mesh_1_position = [0, 0, gap]
        mesh_1_rotation = [-angle, 0, 0]
        self.mesh_1 = Cuboid(height, width, depth, position=mesh_1_position)
        # offset_first=True: rotation applied after translation so jaw pivots at its base
        self.mesh_1.vertices = apply_transformation(
            self.mesh_1.vertices, [0, 0, 0], mesh_1_rotation
        )
        vertices_list.append(self.mesh_1.vertices)
        faces_list.append(self.mesh_1.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_1.vertices)

        # lower jaw — translated to -z, rotated +angle about X (opens downward)
        mesh_2_position = [0, 0, -gap]
        mesh_2_rotation = [angle, 0, 0]
        self.mesh_2 = Cuboid(height, width, depth, position=mesh_2_position)
        self.mesh_2.vertices = apply_transformation(
            self.mesh_2.vertices, [0, 0, 0], mesh_2_rotation
        )
        vertices_list.append(self.mesh_2.vertices)
        faces_list.append(self.mesh_2.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_2.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # offset_first=True: global translation applied before rotation
        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Jaw'


class Curved_Jaw(ConceptTemplate):
    """
    Semantic: Jaw
    Geometry: two mirror-image arc-shaped jaw blades formed from partial Ring segments,
              each rotated about X from a separation offset; second jaw is a Z-reflection of the first
    Used by: Clip
    Parameters:
      size [outer_r, inner_r, depth]: outer radius, inner radius, depth of the Ring arc
      central_angle [arc_deg]: angular span of the arc
      jaw_separation [gap]: Z offset of each jaw from the centre plane
      jaw_rotation [angle_deg]: opening angle of each jaw about the X axis
      position, rotation: global transform
    """
    def __init__(self, size, central_angle, jaw_separation, jaw_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        central_angle = [x / 180 * np.pi for x in central_angle]
        jaw_rotation = [x / 180 * np.pi for x in jaw_rotation]
        super().__init__(position, rotation)

        self.size = size
        self.central_angle = central_angle
        self.jaw_separation = jaw_separation
        self.jaw_rotation = jaw_rotation

        outer_r, inner_r, depth = size
        arc = central_angle[0]
        gap = jaw_separation[0]
        angle = jaw_rotation[0]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # build first jaw arc, orient it, then rotate about its base pivot
        jaw_mesh_1_pre_rotation = [np.pi, np.pi / 2, -np.pi / 2]
        self.jaw_mesh_1 = Ring(depth, outer_r, inner_r,
                               exist_angle=arc, rotation=jaw_mesh_1_pre_rotation)
        pivot = [0, 0, -(outer_r + inner_r) / 2]
        jaw_mesh_1_rotation_matrix = get_rodrigues_matrix([1, 0, 0], angle)
        # rotate vertices about the pivot point using Rodrigues rotation
        self.jaw_mesh_1.vertices = (
            (self.jaw_mesh_1.vertices - pivot) @ jaw_mesh_1_rotation_matrix.T + pivot
        )
        self.jaw_mesh_1.vertices = apply_transformation(
            self.jaw_mesh_1.vertices, [0, 0, (outer_r + inner_r) / 2 - gap], [0, 0, 0]
        )
        vertices_list.append(self.jaw_mesh_1.vertices)
        faces_list.append(self.jaw_mesh_1.faces + total_num_vertices)
        total_num_vertices += len(self.jaw_mesh_1.vertices)

        # second jaw — Z-reflection of first jaw, faces wound in reverse to keep normals outward
        self.jaw_mesh_2 = copy.deepcopy(self.jaw_mesh_1)
        self.jaw_mesh_2.vertices = np.asarray(self.jaw_mesh_2.vertices)
        self.jaw_mesh_2.vertices[:, 2] = -self.jaw_mesh_2.vertices[:, 2]
        self.jaw_mesh_2.faces = np.asarray(self.jaw_mesh_2.faces)
        self.jaw_mesh_2.faces = self.jaw_mesh_2.faces[:, [0, 2, 1]]
        vertices_list.append(self.jaw_mesh_2.vertices)
        faces_list.append(self.jaw_mesh_2.faces + total_num_vertices)
        total_num_vertices += len(self.jaw_mesh_2.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # offset_first=True: global translation applied before rotation
        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Jaw'
