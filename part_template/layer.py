import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation
from knowledge_utils import *


class Regular_Sublayer(ConceptTemplate):
    """
    Semantic: Layer
    Geometry: one or more evenly-spaced flat cuboid shelves stacked along Y, with optional
              additional shelves at arbitrary positions encoded in a flat parameter list
    Used by: Table
    Parameters:
      subs_size [w, h, d]: dimensions of each primary shelf
      number_of_subs [n]: number of primary shelves
      subs_offset [y0]: Y position of the first shelf
      interval_between_subs [dy]: Y spacing between consecutive primary shelves
      additional_sublayers_params [n_extra, w,h,d,x,y,z,rx,ry,rz, ...]:
        first element is count; then groups of 9 per extra shelf
        positions are in world space (parent position is subtracted internally)
        rotation values in this flat list are pre-converted to radians in __init__
      position, rotation: global transform
    """
    def __init__(self, subs_size, number_of_subs, subs_offset, interval_between_subs,
                 additional_sublayers_params, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        # convert rotation fields (indices 6,7,8 within each 9-element group) to radians
        additional_sublayers_params = [
            x / 180 * np.pi if ((i > 1) and ((i - 1) % 9 in [6, 7, 8])) else x
            for i, x in enumerate(additional_sublayers_params)
        ]
        super().__init__(position, rotation)

        self.subs_size = subs_size
        self.number_of_subs = number_of_subs
        self.subs_offset = subs_offset
        self.interval_between_subs = interval_between_subs

        sw, sh, sd = subs_size
        n = int(number_of_subs[0])
        y0 = subs_offset[0]
        dy = interval_between_subs[0]
        n_extra = int(additional_sublayers_params[0])
        extra_attrs = additional_sublayers_params[1:]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # primary shelves — evenly spaced along Y
        for i in range(n):
            mesh_position = [0, y0 + i * dy, 0]
            tmp_mesh = Cuboid(sh, sw, sd, position=mesh_position)
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

        # additional shelves — world-space positions, subtract parent position
        for i in range(n_extra):
            ew, eh, ed = extra_attrs[9*i], extra_attrs[9*i+1], extra_attrs[9*i+2]
            mesh_position = [
                extra_attrs[9*i+3] - position[0],
                extra_attrs[9*i+4] - position[1],
                extra_attrs[9*i+5] - position[2]
            ]
            mesh_rotation = [extra_attrs[9*i+6], extra_attrs[9*i+7], extra_attrs[9*i+8]]
            tmp_mesh = Cuboid(eh, ew, ed, position=mesh_position, rotation=mesh_rotation)
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

        self.semantic = 'Layer'


class Cylindrical_Sublayer(ConceptTemplate):
    """
    Semantic: Layer
    Geometry: one or more evenly-spaced cylindrical shelves stacked along Y, with optional
              additional cuboid shelves at arbitrary positions
    Used by: Table
    Parameters:
      subs_size [radius, height]: radius and height of each primary cylinder shelf
      number_of_subs [n]: number of primary shelves
      subs_offset [y0]: Y position of the first shelf
      interval_between_subs [dy]: Y spacing between consecutive primary shelves
      additional_sublayers_params [n_extra, w,h,d,x,y,z,rx,ry,rz, ...]:
        same flat encoding as Regular_Sublayer; extra shelves are cuboids
        positions are already in world space (no parent subtraction)
      position, rotation: global transform
    """
    def __init__(self, subs_size, number_of_subs, subs_offset, interval_between_subs,
                 additional_sublayers_params, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        additional_sublayers_params = [
            x / 180 * np.pi if ((i > 1) and ((i - 1) % 9 in [6, 7, 8])) else x
            for i, x in enumerate(additional_sublayers_params)
        ]
        super().__init__(position, rotation)

        self.subs_size = subs_size
        self.number_of_subs = number_of_subs
        self.subs_offset = subs_offset
        self.interval_between_subs = interval_between_subs

        radius, height = subs_size[0], subs_size[1]
        n = int(number_of_subs[0])
        y0 = subs_offset[0]
        dy = interval_between_subs[0]
        n_extra = int(additional_sublayers_params[0])
        extra_attrs = additional_sublayers_params[1:]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(n):
            mesh_position = [0, y0 + i * dy, 0]
            tmp_mesh = Cylinder(height, radius, position=mesh_position)
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

        # additional shelves — positions already in world space
        for i in range(n_extra):
            ew, eh, ed = extra_attrs[9*i], extra_attrs[9*i+1], extra_attrs[9*i+2]
            mesh_position = [extra_attrs[9*i+3], extra_attrs[9*i+4], extra_attrs[9*i+5]]
            mesh_rotation = [extra_attrs[9*i+6], extra_attrs[9*i+7], extra_attrs[9*i+8]]
            tmp_mesh = Cuboid(eh, ew, ed, position=mesh_position, rotation=mesh_rotation)
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

        self.semantic = 'Layer'
