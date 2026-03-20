import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Carved_Magazine(ConceptTemplate):
    """
    Semantic: Magazine
    Geometry: top Cuboid cap + bottom Rectangular_Ring body (Z-rotated 180°)
    Used by: Stapler
    Parameters:
      outer_size [w, h, d]: outer dimensions of the magazine
      inner_size [w, h, d]: inner opening dimensions (w, h for ring height/opening; d for ring depth)
      position, rotation: global transform
    """
    def __init__(self, outer_size, inner_size, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.outer_size = outer_size
        self.inner_size = inner_size

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.top_mesh = Cuboid(outer_size[1] - inner_size[1], outer_size[0], outer_size[2],
                               position=[0, (outer_size[1] + inner_size[1]) / 2, outer_size[2] / 2],
                               rotation=[0, 0, np.pi])
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        self.bottom_mesh = Rectangular_Ring(inner_size[1], outer_size[0], outer_size[2],
                                            inner_size[0], inner_size[2],
                                            position=[0, inner_size[1] / 2, outer_size[2] / 2],
                                            rotation=[0, 0, np.pi])
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Magazine'


class Complex_Magazine(ConceptTemplate):
    """
    Semantic: Magazine
    Geometry: bottom Cuboid floor + back Cuboid wall + front Cuboid wall
              + left Cuboid side panel + right Cuboid side panel
    Used by: Stapler
    Parameters:
      size [w, h, d]: overall outer dimensions
      thickness [t]: wall thickness
      front_height [h]: height of the front wall
      beside_length [l]: depth of the side panels
      beside_offset [z]: Z offset of the side panels from centre
      position, rotation: global transform
    """
    def __init__(self, size, thickness, front_height, beside_length, beside_offset,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.size = size
        self.thickness = thickness
        self.front_height = front_height
        self.beside_length = beside_length
        self.beside_offset = beside_offset

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.bottom_mesh = Cuboid(thickness[0], size[0], size[2],
                                  position=[0, thickness[0] / 2, size[2] / 2])
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        self.behind_mesh = Cuboid(size[1], size[0], thickness[0],
                                  position=[0, thickness[0] / 2, size[2] / 2])
        vertices_list.append(self.behind_mesh.vertices)
        faces_list.append(self.behind_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.behind_mesh.vertices)

        self.front_mesh = Cuboid(front_height[0], size[0], thickness[0],
                                 position=[0, front_height[0] / 2, size[2] - thickness[0] / 2])
        vertices_list.append(self.front_mesh.vertices)
        faces_list.append(self.front_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.front_mesh.vertices)

        self.left_mesh = Cuboid(size[1], thickness[0], beside_length[0],
                                position=[size[0] / 2 - thickness[0] / 2,
                                          size[1] / 2,
                                          size[2] / 2 + beside_offset[0]])
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        self.right_mesh = Cuboid(size[1], thickness[0], beside_length[0],
                                 position=[-size[0] / 2 + thickness[0] / 2,
                                           size[1] / 2,
                                           size[2] / 2 + beside_offset[0]])
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Magazine'
