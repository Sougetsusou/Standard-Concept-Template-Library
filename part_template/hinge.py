import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Standard_Hinge(ConceptTemplate):
    """
    Semantic: Hinge
    Geometry: N cylindrical hinge pins per active door side, at two offset positions
    Used by: Door
    Parameters:
      existence_of_door [left, right]: 0/1 flags for left and right door sides
      number_of_hinge [n]: number of hinges per door side
      size [radius, height]: radius and height of each hinge cylinder
      separation [s1, ...]: gaps between consecutive hinges (length >= n-1)
      offset_1 [x, y, z]: hinge column position for first door side
      offset_2 [x, y, z]: hinge column position for second door side
    """
    def __init__(self, existence_of_door, number_of_hinge, size, separation,
                 offset_1, offset_2, position=[0, 0, 0], rotation=[0, 0, 0]):
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)
        self.existence_of_door = existence_of_door
        self.number_of_hinge = number_of_hinge
        self.size = size
        self.separation = separation
        self.offset_1 = offset_1
        self.offset_2 = offset_2

        radius, hinge_height = size[0], size[1]
        n = int(number_of_hinge[0])

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        active_offsets = [o for o, exists in zip([offset_1, offset_2], existence_of_door) if exists]
        for offset in active_offsets:
            ox, oy, oz = offset
            for i in range(n):
                tmp_mesh = Cylinder(hinge_height, radius, radius,
                                    position=[ox,
                                              oy + hinge_height * (i + 0.5) + sum(separation[0:i]),
                                              oz])
                vertices_list.append(tmp_mesh.vertices)
                faces_list.append(tmp_mesh.faces + total_num_vertices)
                total_num_vertices += len(tmp_mesh.vertices)

        if not vertices_list:
            raise ValueError(f"{self.__class__.__name__}: no geometry was instantiated")
        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)
        self.vertices = apply_transformation(self.vertices, position, rotation)
        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))
        self.semantic = 'Hinge'
