import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation
from knowledge_utils import *


class Regular_Backboard(ConceptTemplate):
    """
    Semantic: Board
    Geometry: single flat cuboid panel positioned below the origin (backboard / back panel)
    Used by: Table
    Parameters:
      size [w, h, d]: width, height, depth of the board
      position, rotation: global transform
    """
    def __init__(self, size, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.size = size

        width, height, depth = size

        self.mesh = Cuboid(height, width, depth,
                           position=[0, -height / 2, 0])
        self.vertices = self.mesh.vertices
        self.faces = self.mesh.faces

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Board'


class Regular_Partition(ConceptTemplate):
    """
    Semantic: Board
    Geometry: up to three optional cuboid partition panels — left side, rear, and right side —
              controlled by a has_partition flag list
    Used by: Table
    Parameters:
      has_partition [left, rear, right]: 1 to include each panel, 0 to omit
      left_right_size [w, h, d]: dimensions of the left and right side panels
      rear_size [h, d]: height and depth of the rear panel
                        (width spans the full left_right_separation + 2*left_right_size[0])
      left_right_separation [gap]: X distance between the inner faces of the two side panels
      position, rotation: global transform
    """
    def __init__(self, has_partition, left_right_size, rear_size, left_right_separation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.has_partition = has_partition
        self.left_right_size = left_right_size
        self.rear_size = rear_size
        self.left_right_separation = left_right_separation

        lw, lh, ld = left_right_size
        rh, rd = rear_size[0], rear_size[1]
        gap = left_right_separation[0]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        if has_partition[0] == 1:
            tmp_mesh = Cuboid(lh, lw, ld,
                              position=[gap / 2 + lw / 2, lh / 2, 0])
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

        if has_partition[1] == 1:
            rear_width = gap + 2 * lw
            tmp_mesh = Cuboid(rh, rear_width, rd,
                              position=[0, rh / 2, -ld / 2 - rd / 2])
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

        if has_partition[2] == 1:
            tmp_mesh = Cuboid(lh, lw, ld,
                              position=[-gap / 2 - lw / 2, lh / 2, 0])
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

        self.semantic = 'Board'
