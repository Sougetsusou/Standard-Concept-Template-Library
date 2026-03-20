import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Round_Shaft(ConceptTemplate):
    """
    Semantic: Shaft
    Geometry: main Cylinder + optional central shaft Cylinder
    Used by: Pliers
    Parameters:
      size [r, h]: radius and height of main cylinder
      has_central_shaft [flag]: 1 to add a central shaft cylinder
      central_shaft_size [r, h]: radius and height of central shaft
      central_shaft_offset [x, y, z]: position of central shaft
      position, rotation: global transform
    """
    def __init__(self, size, has_central_shaft, central_shaft_size, central_shaft_offset,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.size = size
        self.has_central_shaft = has_central_shaft
        self.central_shaft_size = central_shaft_size
        self.central_shaft_offset = central_shaft_offset

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        r, h = size[0], size[1]
        self.mesh = Cylinder(h, r)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        if has_central_shaft[0] == 1:
            cs_r, cs_h = central_shaft_size[0], central_shaft_size[1]
            cs_ox, cs_oy, cs_oz = central_shaft_offset
            tmp_mesh = Cylinder(cs_h, cs_r,
                                position=[cs_ox, cs_oy, cs_oz])
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Shaft'


class Rectangular_Shaft(ConceptTemplate):
    """
    Semantic: Shaft
    Geometry: 1–3 stacked Cuboid layers (each optionally Y-rotated) + optional central Cylinder shaft
    Used by: Pliers
    Parameters:
      num_layers [n]: number of cuboid layers (1..3)
      layer_1_size [w, h, d]: dimensions of layer 1
      layer_2_size [w, h, d]: dimensions of layer 2
      layer_2_offset [x, z]: XZ offset of layer 2
      layer_3_size [w, h, d]: dimensions of layer 3
      layer_3_offset [x, z]: XZ offset of layer 3
      layer_rotation [y1, y2, y3]: Y rotation per layer (deg)
      has_central_shaft [flag]: 1 to add central shaft cylinder
      central_shaft_size [r, h]: radius and height of central shaft
      central_shaft_offset [x, y, z]: position of central shaft
      position, rotation: global transform
    """
    def __init__(self, num_layers, layer_1_size, layer_2_size, layer_2_offset,
                 layer_3_size, layer_3_offset, layer_rotation,
                 has_central_shaft, central_shaft_size, central_shaft_offset,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        layer_rotation = [x / 180 * np.pi for x in layer_rotation]
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.num_layers = num_layers
        self.layer_1_size = layer_1_size
        self.layer_2_size = layer_2_size
        self.layer_2_offset = layer_2_offset
        self.layer_3_size = layer_3_size
        self.layer_3_offset = layer_3_offset
        self.layer_rotation = layer_rotation
        self.has_central_shaft = has_central_shaft
        self.central_shaft_size = central_shaft_size
        self.central_shaft_offset = central_shaft_offset

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.layer_1_mesh = Cuboid(layer_1_size[1], layer_1_size[0], layer_1_size[2],
                                   position=[0, -layer_1_size[1] / 2, 0],
                                   rotation=[0, layer_rotation[0], 0])
        vertices_list.append(self.layer_1_mesh.vertices)
        faces_list.append(self.layer_1_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.layer_1_mesh.vertices)

        if num_layers[0] >= 2:
            self.layer_2_mesh = Cuboid(layer_2_size[1], layer_2_size[0], layer_2_size[2],
                                       position=[layer_2_offset[0], layer_2_size[1] / 2, layer_2_offset[1]],
                                       rotation=[0, layer_rotation[1], 0])
            vertices_list.append(self.layer_2_mesh.vertices)
            faces_list.append(self.layer_2_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.layer_2_mesh.vertices)

        if num_layers[0] >= 3:
            self.layer_3_mesh = Cuboid(layer_3_size[1], layer_3_size[0], layer_3_size[2],
                                       position=[layer_3_offset[0], layer_2_size[1] + layer_3_size[1] / 2, layer_3_offset[1]],
                                       rotation=[0, layer_rotation[2], 0])
            vertices_list.append(self.layer_3_mesh.vertices)
            faces_list.append(self.layer_3_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.layer_3_mesh.vertices)

        if has_central_shaft[0] == 1:
            cs_r, cs_h = central_shaft_size[0], central_shaft_size[1]
            cs_ox, cs_oy, cs_oz = central_shaft_offset
            tmp_cs_mesh = Cylinder(cs_h, cs_r,
                                   position=[cs_ox, cs_oy, cs_oz])
            vertices_list.append(tmp_cs_mesh.vertices)
            faces_list.append(tmp_cs_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_cs_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Shaft'


class Regular_shaft(ConceptTemplate):
    """
    Semantic: Shaft
    Geometry: single Cuboid shaft
    Used by: Ruler
    Parameters:
      size [w, h, d]: dimensions of the shaft cuboid
      position, rotation: global transform
    """
    def __init__(self, size, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.size = size

        self.mesh = Cuboid(size[1], size[0], size[2])

        self.vertices = self.mesh.vertices
        self.faces = self.mesh.faces

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Shaft'
