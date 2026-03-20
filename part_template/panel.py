import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Regular_Front_Panel(ConceptTemplate):
    """
    Semantic: Panel
    Geometry: N cuboid front panels at specified positions
    Used by: StorageFurniture
    Parameters:
      number_of_frontPanel [n]: number of panels
      frontPanel_params [w0,h0,d0,x0,y0,z0, w1,...]: flat list, 6 values per panel
                                                       (size xyz, offset xyz)
    """
    def __init__(self, number_of_frontPanel, frontPanel_params, position=[0, 0, 0], rotation=[0, 0, 0]):
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)
        self.number_of_frontPanel = number_of_frontPanel

        n = int(number_of_frontPanel[0])
        sizes   = [frontPanel_params[i * 6:     i * 6 + 3] for i in range(n)]
        offsets = [frontPanel_params[i * 6 + 3: i * 6 + 6] for i in range(n)]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(n):
            w, h, d = sizes[i]
            ox, oy, oz = offsets[i]
            tmp_mesh = Cuboid(h, w, d, position=[ox, oy, oz])
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
        self.semantic = 'Panel'
