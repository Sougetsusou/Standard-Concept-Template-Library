import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation
from knowledge_utils import *


class Regular_Rack(ConceptTemplate):
    """
    Semantic: Rack
    Geometry: two flat cuboid panels hinged at a pivot, splayed symmetrically like an open book
    Used by: Foldingrack
    Parameters:
      size [w, h, d]: dimensions of each panel
      horizontal_rotation [angle_deg]: splay angle of each panel about the Z axis
      position, rotation: global transform
    """
    def __init__(self, size, horizontal_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        horizontal_rotation = [x / 180 * np.pi for x in horizontal_rotation]
        super().__init__(position, rotation)

        self.size = size
        self.horizontal_rotation = horizontal_rotation

        width, height, depth = size
        angle = horizontal_rotation[0]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # left panel — pivot corner at origin, panel extends in +x direction
        # apply_transformation used here as a pure vector rotation to find the panel centre
        mesh_1_rotation = [0, 0, angle]
        mesh_1_position = apply_transformation(
            [width / 2, -height / 2, 0],
            position=[0, 0, 0], rotation=mesh_1_rotation
        )
        self.mesh_1 = Cuboid(height, width, depth,
                             position=mesh_1_position, rotation=mesh_1_rotation)
        vertices_list.append(self.mesh_1.vertices)
        faces_list.append(self.mesh_1.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_1.vertices)

        # right panel — mirror of left panel
        mesh_2_rotation = [0, 0, -angle]
        mesh_2_position = apply_transformation(
            [width / 2, height / 2, 0],
            position=[0, 0, 0], rotation=mesh_2_rotation
        )
        self.mesh_2 = Cuboid(height, width, depth,
                             position=mesh_2_position, rotation=mesh_2_rotation)
        vertices_list.append(self.mesh_2.vertices)
        faces_list.append(self.mesh_2.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_2.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Rack'


class Curved_Rack(ConceptTemplate):
    """
    Semantic: Rack
    Geometry: two flat cuboid panels splayed at a pivot, with Ring arcs joining their tips
    Used by: Foldingrack
    Parameters:
      size [w, h, d]: dimensions of each panel
      edge_radius [r]: outer radius of the arc Ring at the panel tips
      edge_exist_rotation [arc_deg]: angular span of the arc
      horizontal_rotation [angle_deg]: splay angle of each panel about the Z axis
      position, rotation: global transform
    """
    def __init__(self, size, edge_radius, edge_exist_rotation, horizontal_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        edge_exist_rotation = [x / 180 * np.pi for x in edge_exist_rotation]
        horizontal_rotation = [x / 180 * np.pi for x in horizontal_rotation]
        super().__init__(position, rotation)

        self.size = size
        self.edge_radius = edge_radius
        self.edge_exist_rotation = edge_exist_rotation
        self.horizontal_rotation = horizontal_rotation

        width, height, depth = size
        r = edge_radius[0]
        arc = edge_exist_rotation[0]
        angle = horizontal_rotation[0]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_1_rotation = [0, 0, angle]
        mesh_1_position = apply_transformation(
            [width / 2, -height / 2, 0],
            position=[0, 0, 0], rotation=mesh_1_rotation
        )
        self.mesh_1 = Cuboid(height, width, depth,
                             position=mesh_1_position, rotation=mesh_1_rotation)
        vertices_list.append(self.mesh_1.vertices)
        faces_list.append(self.mesh_1.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_1.vertices)

        mesh_2_rotation = [0, 0, -angle]
        mesh_2_position = apply_transformation(
            [width / 2, height / 2, 0],
            position=[0, 0, 0], rotation=mesh_2_rotation
        )
        self.mesh_2 = Cuboid(height, width, depth,
                             position=mesh_2_position, rotation=mesh_2_rotation)
        vertices_list.append(self.mesh_2.vertices)
        faces_list.append(self.mesh_2.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_2.vertices)

        # top arc connecting the two panel tips
        mesh_3_rotation = [np.pi / 2, 0, np.pi - angle]
        mesh_3_position = [
            r * np.cos(angle) + height * np.sin(angle),
            height * np.cos(angle) - r * np.sin(angle),
            0
        ]
        self.mesh_3 = Ring(depth, r, r - width, arc,
                           position=mesh_3_position, rotation=mesh_3_rotation)
        vertices_list.append(self.mesh_3.vertices)
        faces_list.append(self.mesh_3.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_3.vertices)

        # bottom arc — mirror of top
        mesh_4_rotation = [-np.pi / 2, 0, np.pi + angle]
        mesh_4_position = [
            r * np.cos(angle) + height * np.sin(angle),
            -height * np.cos(angle) + r * np.sin(angle),
            0
        ]
        self.mesh_4 = Ring(depth, r, r - width, arc,
                           position=mesh_4_position, rotation=mesh_4_rotation)
        vertices_list.append(self.mesh_4.vertices)
        faces_list.append(self.mesh_4.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_4.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Rack'
