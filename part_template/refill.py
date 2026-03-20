import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Cylindrical_Refill(ConceptTemplate):
    """
    Semantic: Refill
    Geometry: main cylinder body + small cylinder tip base + cone tip
    Used by: Pen
    Parameters:
      size [radius, height]: main body radius and height
      tip_radius [r]: radius of the tip base cylinder
      tip_height [h_cyl, h_cone]: height of tip base cylinder and cone
      tip_offset [offset]: cone tip lateral offset
    """
    def __init__(self, size, tip_radius, tip_height, tip_offset,
                 position=[0, 0, 0], rotation=[0, 0, 0]):
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)
        self.size = size
        self.tip_radius = tip_radius
        self.tip_height = tip_height
        self.tip_offset = tip_offset

        radius, height = size[0], size[1]
        tr = tip_radius[0]
        th_cyl, th_cone = tip_height[0], tip_height[1]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        tmp_mesh = Cylinder(height, radius)
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        tmp_mesh = Cylinder(th_cyl, tr,
                            position=[0, -height / 2 - th_cyl / 2, 0])
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        tmp_mesh = Cone(tr, th_cone, tip_offset,
                        position=[0, -height / 2 - th_cyl, 0])
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)
        self.vertices = apply_transformation(self.vertices, position, rotation)
        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))
        self.semantic = 'Refill'
