import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Standard_Wheel(ConceptTemplate):
    """
    Semantic: Wheel
    Geometry: 2 mirrored Z-rotated Cylinders (left and right wheels)
    Used by: Trashcan
    Parameters:
      size [r, h]: radius and height of each wheel cylinder
      seperation [x]: X offset of each wheel from centre
      position, rotation: global transform
    """
    def __init__(self, size, seperation, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.size = size
        self.seperation = seperation

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.left_mesh = Cylinder(size[1], size[0],
                                  position=[-seperation[0], 0, 0],
                                  rotation=[0, 0, np.pi / 2])
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        self.right_mesh = Cylinder(size[1], size[0],
                                   position=[seperation[0], 0, 0],
                                   rotation=[0, 0, np.pi / 2])
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Wheel'
