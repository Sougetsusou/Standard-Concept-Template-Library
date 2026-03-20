import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Cylindrical_Shell(ConceptTemplate):
    """
    Semantic: Shell
    Geometry: tapered Ring (annular cylinder) shell
    Used by: Trashcan
    Parameters:
      outer_size [r_top, r_bottom, h]: outer top radius, outer bottom radius, height
      inner_size [r_top, r_bottom]: inner top radius, inner bottom radius
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

        self.mesh = Ring(outer_size[2], outer_size[0], inner_size[0],
                         outer_bottom_radius=outer_size[1],
                         inner_bottom_radius=inner_size[1])
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Shell'


class Cuboidal_Shell(ConceptTemplate):
    """
    Semantic: Shell
    Geometry: single Rectangular_Ring shell
    Used by: Trashcan
    Parameters:
      outer_size [w, h, d]: outer dimensions
      inner_size [w, d]: inner width and depth of the opening
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

        self.mesh = Rectangular_Ring(outer_size[1], outer_size[0], outer_size[2],
                                     inner_size[0], inner_size[1])
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Shell'
