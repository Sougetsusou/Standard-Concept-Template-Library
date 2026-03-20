import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation
from knowledge_utils import *


class Rectangular_Baffle(ConceptTemplate):
    """
    Semantic: Baffle
    Geometry: two mirror-image cuboid baffles splayed symmetrically about the Y axis
    Used by: Pliers
    Parameters:
      size [w, h, d]: dimensions of each baffle
      baffle_separation [gap]: X distance between the two baffle centres
      baffle_rotation [angle_deg]: Y rotation of each baffle (splay angle)
      position, rotation: global transform
    """
    def __init__(self, size, baffle_separation, baffle_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        baffle_rotation = [x / 180 * np.pi for x in baffle_rotation]
        super().__init__(position, rotation)

        self.size = size
        self.baffle_separation = baffle_separation
        self.baffle_rotation = baffle_rotation

        width, height, depth = size
        gap = baffle_separation[0]
        angle = baffle_rotation[0]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.mesh_right = Cuboid(height, width, depth,
                                 position=[gap / 2, 0, 0],
                                 rotation=[0, angle, 0])
        vertices_list.append(self.mesh_right.vertices)
        faces_list.append(self.mesh_right.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_right.vertices)

        self.mesh_left = Cuboid(height, width, depth,
                                position=[-gap / 2, 0, 0],
                                rotation=[0, -angle, 0])
        vertices_list.append(self.mesh_left.vertices)
        faces_list.append(self.mesh_left.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_left.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Baffle'


class Curved_Baffle(ConceptTemplate):
    """
    Semantic: Baffle
    Geometry: two mirror-image arc-shaped Ring baffles forming a V-gap between them
    Used by: Pliers
    Parameters:
      radius [outer_r, inner_r]: outer and inner radius of the Ring arc
      height [h]: depth of the Ring arc
      exist_angle [arc_deg]: angular span of each arc
      seperation_rotation [angle_deg]: half-angle of the V-gap between the two arcs
      position, rotation: global transform
    """
    def __init__(self, radius, height, exist_angle, seperation_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        exist_angle = [x / 180 * np.pi for x in exist_angle]
        seperation_rotation = [x / 180 * np.pi for x in seperation_rotation]
        super().__init__(position, rotation)

        self.radius = radius
        self.height = height
        self.exist_angle = exist_angle
        self.seperation_rotation = seperation_rotation

        outer_r, inner_r = radius[0], radius[1]
        h = height[0]
        arc = exist_angle[0]
        half_gap = seperation_rotation[0]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.mesh_left = Ring(h, outer_r, inner_r, arc,
                              rotation=[0, np.pi / 2 - half_gap / 2, 0])
        vertices_list.append(self.mesh_left.vertices)
        faces_list.append(self.mesh_left.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_left.vertices)

        # right arc — rotated 180° about Z to mirror the left arc
        self.mesh_right = Ring(h, outer_r, inner_r, arc,
                               rotation=[0, np.pi / 2 - half_gap / 2, np.pi])
        vertices_list.append(self.mesh_right.vertices)
        faces_list.append(self.mesh_right.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_right.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Baffle'
