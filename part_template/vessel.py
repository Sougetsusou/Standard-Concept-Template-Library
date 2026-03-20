import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Cuboidal_Vessel(ConceptTemplate):
    """
    Semantic: Vessel
    Geometry: bottom Cuboid base + top Rectangular_Ring opening
    Used by: Refrigerator
    Parameters:
      outer_size [w, h, d]: outer dimensions of the vessel
      inner_size [w, h, d]: inner opening dimensions (w, h used for ring; d for Z offset)
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

        self.bottom_mesh = Cuboid(outer_size[1] - inner_size[1], outer_size[0], outer_size[2],
                                  position=[0, -inner_size[1] / 2, -outer_size[2] / 2])
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        self.top_mesh = Rectangular_Ring(inner_size[1], outer_size[0], outer_size[2],
                                         inner_size[0], inner_size[2],
                                         inner_offset=[0, (outer_size[2] - inner_size[2]) / 2],
                                         position=[0, (outer_size[1] - inner_size[1]) / 2, -outer_size[2] / 2])
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Vessel'
