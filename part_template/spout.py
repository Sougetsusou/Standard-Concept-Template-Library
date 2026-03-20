import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Straight_Spout(ConceptTemplate):
    """
    Semantic: Spout
    Geometry: tapered Cylinder spout body
    Used by: Kettle
    Parameters:
      size [r_bottom, r_top, h]: bottom radius, top radius, height
      spout_rotation [x_deg, y_deg, z_deg]: rotation of the spout
      position, rotation: global transform
    """
    def __init__(self, size, spout_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        spout_rotation = [x / 180 * np.pi for x in spout_rotation]
        super().__init__(position, rotation)

        self.size = size
        self.spout_rotation = spout_rotation

        self.mesh = Cylinder(size[2], size[0], size[1],
                             rotation=spout_rotation)

        self.vertices = self.mesh.vertices
        self.faces = self.mesh.faces

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Spout'


class Curved_Spout(ConceptTemplate):
    """
    Semantic: Spout
    Geometry: two chained Torus arc sections forming a curved spout
    Used by: Kettle
    Parameters:
      central_radius [r1, r2]: central (sweep) radius of each torus arc
      exist_angle [a1_deg, a2_deg]: arc angle of each torus section
      torus_radius [r_tube1, r_tube2, r_tube3]: tube radii (r_tube1 for top arc,
                                                 r_tube2 shared, r_tube3 for bottom arc)
      position, rotation: global transform
    """
    def __init__(self, central_radius, exist_angle, torus_radius,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        exist_angle = [x / 180 * np.pi for x in exist_angle]
        super().__init__(position, rotation)

        self.central_radius = central_radius
        self.exist_angle = exist_angle
        self.torus_radius = torus_radius

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.top_mesh = Torus(central_radius[0], torus_radius[0], exist_angle[0], torus_radius[1],
                              position=[0, central_radius[0], 0],
                              rotation=[0, 0, -np.pi / 2])
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        self.bottom_mesh = Torus(central_radius[1], torus_radius[1], exist_angle[1], torus_radius[2],
                                 position=[0,
                                           central_radius[0] * (1 - np.cos(exist_angle[0])) - central_radius[1] * np.cos(exist_angle[0]),
                                           central_radius[0] * np.sin(exist_angle[0]) + central_radius[1] * np.sin(exist_angle[0])],
                                 rotation=[-exist_angle[0], 0, np.pi / 2],
                                 # ZXY order: Z rotation applied first to align torus tangent with arc endpoint
                                 rotation_order="ZXY")
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Spout'
