import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Frustum_Screen(ConceptTemplate):
    """
    Semantic: Screen
    Geometry: tapered Cuboid back panel (frustum shape) + optional flat Cuboid front layer
    Used by: Display
    Parameters:
      has_additional_layer [flag]: 1 to include front layer
      additional_layer_size [w, h, d]: dimensions of the front layer cuboid
      size [w, h, d]: outer dimensions of the back panel
      back_part_offset [x, y]: top-face offset of the tapered back panel
      position, rotation: global transform
    """
    def __init__(self, has_additional_layer, additional_layer_size, size, back_part_offset,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.has_additional_layer = has_additional_layer
        self.additional_layer_size = additional_layer_size
        self.size = size
        self.back_part_offset = back_part_offset

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.back_mesh = Cuboid(size[2], size[0], size[1],
                                additional_layer_size[0], additional_layer_size[1],
                                [back_part_offset[0], back_part_offset[1]],
                                position=[0, 0, -size[2] / 2],
                                rotation=[-np.pi / 2, 0, 0])
        vertices_list.append(self.back_mesh.vertices)
        faces_list.append(self.back_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.back_mesh.vertices)

        if has_additional_layer[0]:
            self.front_mesh = Cuboid(additional_layer_size[1], additional_layer_size[0], additional_layer_size[2],
                                     position=[0, 0, additional_layer_size[2] / 2])
            vertices_list.append(self.front_mesh.vertices)
            faces_list.append(self.front_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.front_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Screen'


class Standard_Screen(ConceptTemplate):
    """
    Semantic: Screen
    Geometry: flat Cuboid front panel + optional Cuboid back layer
    Used by: Display
    Parameters:
      has_additional_layer [flag]: 1 to include back layer
      size [w, h, d]: dimensions of the front panel cuboid
      additional_layer_size [w, h, d]: dimensions of the back layer cuboid
      additional_layer_offset [x, y]: XY offset of the back layer
      position, rotation: global transform
    """
    def __init__(self, has_additional_layer, size, additional_layer_size, additional_layer_offset,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.has_additional_layer = has_additional_layer
        self.size = size
        self.additional_layer_size = additional_layer_size
        self.additional_layer_offset = additional_layer_offset

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.front_mesh = Cuboid(size[1], size[0], size[2])
        vertices_list.append(self.front_mesh.vertices)
        faces_list.append(self.front_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.front_mesh.vertices)

        if has_additional_layer[0]:
            self.back_mesh = Cuboid(additional_layer_size[1], additional_layer_size[0], additional_layer_size[2],
                                    position=[additional_layer_offset[0],
                                              additional_layer_offset[1],
                                              -size[2] / 2 - additional_layer_size[2] / 2])
            vertices_list.append(self.back_mesh.vertices)
            faces_list.append(self.back_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.back_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Screen'
