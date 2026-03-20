import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Cuboidal_Plug(ConceptTemplate):
    """
    Semantic: Plug
    Geometry: grid of Cuboid contacts (column_of_contact × row_of_contact)
    Used by: Switch
    Parameters:
      column_of_contact [n]: number of columns
      row_of_contact [n]: number of rows
      size [w, h, d]: dimensions of each contact cuboid
      interval [dx, dy]: spacing between contacts in X and Y
      position, rotation: global transform
    """
    def __init__(self, column_of_contact, row_of_contact, size, interval,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.column_of_contact = column_of_contact
        self.row_of_contact = row_of_contact
        self.size = size
        self.interval = interval

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for j in range(int(row_of_contact[0])):
            for i in range(int(column_of_contact[0])):
                tmp = Cuboid(size[1], size[0], size[2],
                             position=[(interval[0] + size[0]) * i,
                                       (interval[1] + size[1]) * j,
                                       -size[2] / 2])
                vertices_list.append(tmp.vertices)
                faces_list.append(tmp.faces + total_num_vertices)
                total_num_vertices += len(tmp.vertices)

        if not vertices_list:
            raise ValueError(f"{self.__class__.__name__}: no geometry was instantiated")
        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation, offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Plug'


class Standard_Plug(ConceptTemplate):
    """
    Semantic: Plug
    Geometry: 3 Cuboid prongs — one central + two offset and counter-rotated
    Used by: Switch
    Parameters:
      size [w, h, d]: dimensions of each prong cuboid
      sub_offset [x, y]: XY offset of the two side prongs from centre
      plug_rotation [base_deg, spread_deg]: base Z rotation and spread angle between prongs
      position, rotation: global transform
    """
    def __init__(self, size, sub_offset, plug_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        plug_rotation = [x / 180 * np.pi for x in plug_rotation]
        super().__init__(position, rotation)

        self.size = size
        self.sub_offset = sub_offset
        self.plug_rotation = plug_rotation

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # central prong
        tmp = Cuboid(size[1], size[0], size[2],
                     position=[0, 0, -size[2] / 2],
                     rotation=[0, 0, plug_rotation[0]])
        vertices_list.append(tmp.vertices)
        faces_list.append(tmp.faces + total_num_vertices)
        total_num_vertices += len(tmp.vertices)

        # left prong
        tmp = Cuboid(size[1], size[0], size[2],
                     position=[-sub_offset[0] * np.cos(plug_rotation[0]) + sub_offset[1] * np.sin(-plug_rotation[0]),
                                sub_offset[1] * np.cos(-plug_rotation[0]) - sub_offset[0] * np.sin(plug_rotation[0]),
                                -size[2] / 2],
                     rotation=[0, 0, plug_rotation[0] + plug_rotation[1]])
        vertices_list.append(tmp.vertices)
        faces_list.append(tmp.faces + total_num_vertices)
        total_num_vertices += len(tmp.vertices)

        # right prong
        tmp = Cuboid(size[1], size[0], size[2],
                     position=[sub_offset[0] * np.cos(plug_rotation[0]) + sub_offset[1] * np.sin(-plug_rotation[0]),
                                sub_offset[1] * np.cos(-plug_rotation[0]) + sub_offset[0] * np.sin(plug_rotation[0]),
                                -size[2] / 2],
                     rotation=[0, 0, plug_rotation[0] - plug_rotation[1]])
        vertices_list.append(tmp.vertices)
        faces_list.append(tmp.faces + total_num_vertices)
        total_num_vertices += len(tmp.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation, offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Plug'


class Cylindrical_Plug(ConceptTemplate):
    """
    Semantic: Plug
    Geometry: grid of Cylinder contacts (column_of_contact × row_of_contact)
    Used by: Switch
    Parameters:
      column_of_contact [n]: number of columns
      row_of_contact [n]: number of rows
      size [r, h]: radius and height of each contact cylinder
      interval [dx, dy]: spacing between contacts in X and Y
      position, rotation: global transform
    """
    def __init__(self, column_of_contact, row_of_contact, size, interval,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.column_of_contact = column_of_contact
        self.row_of_contact = row_of_contact
        self.size = size
        self.interval = interval

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for j in range(int(row_of_contact[0])):
            for i in range(int(column_of_contact[0])):
                tmp = Cylinder(size[1], size[0], size[0],
                               position=[(interval[0] + size[0] * 2) * i,
                                         (interval[1] + size[0] * 2) * j,
                                         -size[1] / 2],
                               rotation=[np.pi / 2, 0, 0])
                vertices_list.append(tmp.vertices)
                faces_list.append(tmp.faces + total_num_vertices)
                total_num_vertices += len(tmp.vertices)

        if not vertices_list:
            raise ValueError(f"{self.__class__.__name__}: no geometry was instantiated")
        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation, offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Plug'
