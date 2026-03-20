import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Standard_Door(ConceptTemplate):
    """
    Semantic: Door
    Geometry: one or two hinged Cuboid door panels, each pivot-rotated about its hinge edge
    Used by: Door
    Parameters:
      existence_of_door [left, right]: flags for left and right door panels
      size [w, h, d]: width, height, depth of each door panel
      door_rotation [left_deg, right_deg]: open angle of left and right panels
      position, rotation: global transform
    """
    def __init__(self, existence_of_door, size, door_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        door_rotation = [x / 180 * np.pi for x in door_rotation]
        super().__init__(position, rotation)

        self.existence_of_door = existence_of_door
        self.size = size
        self.door_rotation = door_rotation

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        if existence_of_door[0] and existence_of_door[1]:
            left_mesh_position = [size[0] / 2, 0, 0]
            self.left_mesh = Cuboid(size[1], size[0], size[2],
                                    position=left_mesh_position)
            self.left_mesh.vertices = apply_transformation(
                self.left_mesh.vertices, rotation=[0, -door_rotation[0], 0], position=[-size[0], 0, 0])
            vertices_list.append(self.left_mesh.vertices)
            faces_list.append(self.left_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.left_mesh.vertices)

            self.right_mesh = Cuboid(size[1], size[0], size[2],
                                     position=[-size[0] / 2, 0, 0])
            self.right_mesh.vertices = apply_transformation(
                self.right_mesh.vertices, rotation=[0, door_rotation[1], 0], position=[size[0], 0, 0])
            vertices_list.append(self.right_mesh.vertices)
            faces_list.append(self.right_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.right_mesh.vertices)

        elif existence_of_door[0]:
            left_mesh_position = [size[0] / 2, 0, 0]
            self.left_mesh = Cuboid(size[1], size[0], size[2],
                                    position=left_mesh_position)
            self.left_mesh.vertices = apply_transformation(
                self.left_mesh.vertices, rotation=[0, -door_rotation[0], 0], position=[-size[0] / 2, 0, 0])
            vertices_list.append(self.left_mesh.vertices)
            faces_list.append(self.left_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.left_mesh.vertices)

        elif existence_of_door[1]:
            self.right_mesh = Cuboid(size[1], size[0], size[2],
                                     position=[-size[0] / 2, 0, 0])
            self.right_mesh.vertices = apply_transformation(
                self.right_mesh.vertices, rotation=[0, door_rotation[1], 0], position=[size[0] / 2, 0, 0])
            vertices_list.append(self.right_mesh.vertices)
            faces_list.append(self.right_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.right_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Door'
