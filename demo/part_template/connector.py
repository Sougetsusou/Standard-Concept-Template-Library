import numpy as np
import trimesh

from demo.shared.base_template import ConceptTemplate
from demo.shared.geometry_template import Cuboid, Cylinder
from demo.shared.knowledge_utils import SAMPLENUM
from demo.shared.utils import apply_transformation


class Cuboidal_Connector(ConceptTemplate):
    """
    Semantic: Connector
    Geometry: row of cuboid connectors with per-gap separations
    Used by: Laptop
    Parameters:
      number_of_connector [n]: number of connectors in the row
      size [w, h, d]: connector width, height, depth
      separation [s1, ...]: gaps between adjacent connectors
      offset [x, y, z]: position offset of the first connector centerline
      connector_rotation [rx]: per-connector X rotation in degrees
      position, rotation: global transform
    """

    def __init__(self, number_of_connector, size, separation, offset, connector_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        connector_rotation = [x / 180 * np.pi for x in connector_rotation]
        super().__init__(position, rotation)

        count = int(number_of_connector[0])
        width, height, depth = size
        ox, oy, oz = offset
        rot_x = connector_rotation[0]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(count):
            connector_position = [ox + i * width + sum(separation[:i]) + width / 2, oy, oz]
            connector_rot = [rot_x, 0, 0]
            tmp_mesh = Cuboid(height, width, depth,
                              position=connector_position,
                              rotation=connector_rot)
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

        self.semantic = "Connector"


class Cylindrical_Connector(ConceptTemplate):
    """
    Semantic: Connector
    Geometry: row of cylindrical connectors with per-gap separations
    Used by: Laptop
    Parameters:
      number_of_connector [n]: number of connectors in the row
      size [r, h]: connector radius and length
      separation [s1, ...]: gaps between adjacent connectors
      offset [x, y, z]: position offset of the first connector centerline
      position, rotation: global transform
    """

    def __init__(self, number_of_connector, size, separation, offset,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        count = int(number_of_connector[0])
        radius, length = size
        ox, oy, oz = offset

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(count):
            connector_position = [ox + i * length + sum(separation[:i]) + length / 2, oy, oz]
            connector_rot = [0, 0, np.pi / 2]
            tmp_mesh = Cylinder(length, radius, radius,
                                position=connector_position,
                                rotation=connector_rot)
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

        self.semantic = "Connector"
