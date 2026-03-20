import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Standard_Cover(ConceptTemplate):
    """
    Semantic: Cover
    Geometry: tapered cylinder top cap + Ring skirt section + up to 5 stacked knob cylinders on top
    Used by: Kettle
    Parameters:
      outer_size [top_r, bottom_r, h]: outer top radius, outer bottom radius, total cover height
      inner_size [top_r, bottom_r, skirt_h]: inner top radius, inner bottom radius, skirt height
      num_knobs [n]: number of knob cylinders stacked on top (0..5)
      knob_N_size [top_r, bottom_r, h]: top radius, bottom radius, height of knob N (N=1..5)
      position, rotation: global transform
    """
    def __init__(self, outer_size, inner_size, num_knobs,
                 knob_1_size, knob_2_size, knob_3_size, knob_4_size, knob_5_size,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.outer_size = outer_size
        self.inner_size = inner_size
        self.num_knobs = num_knobs
        self.knob_1_size = knob_1_size
        self.knob_2_size = knob_2_size
        self.knob_3_size = knob_3_size
        self.knob_4_size = knob_4_size
        self.knob_5_size = knob_5_size

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_1_bottom_radius = (outer_size[1] * (1 - inner_size[2] / outer_size[2])
                                + outer_size[0] * inner_size[2] / outer_size[2])
        mesh_1_height = outer_size[2] - inner_size[2]
        top_mesh_position = [0, inner_size[2] / 2 + outer_size[2] / 2, 0]
        self.top_mesh = Cylinder(mesh_1_height, outer_size[0], mesh_1_bottom_radius,
                                 position=top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [0, -(outer_size[2] - inner_size[2]) / 2 + outer_size[2] / 2, 0]
        self.bottom_mesh = Ring(inner_size[2], mesh_1_bottom_radius, inner_size[0],
                                outer_bottom_radius=outer_size[1],
                                inner_bottom_radius=inner_size[1],
                                position=bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        knob_sizes = [knob_1_size, knob_2_size, knob_3_size, knob_4_size, knob_5_size]
        delta_height = outer_size[2]
        for i in range(int(num_knobs[0])):
            k_size = knob_sizes[i]
            delta_height += k_size[2] / 2
            knob_mesh_position = [0, delta_height, 0]
            tmp_knob_mesh = Cylinder(k_size[2], k_size[0], k_size[1],
                                     position=knob_mesh_position)
            delta_height += k_size[2] / 2
            vertices_list.append(tmp_knob_mesh.vertices)
            faces_list.append(tmp_knob_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_knob_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Cover'
