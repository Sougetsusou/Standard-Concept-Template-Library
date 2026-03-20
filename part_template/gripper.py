import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Cusp_Gripper(ConceptTemplate):
    """
    Semantic: Gripper
    Geometry: 2 mirrored gripper arms, each a tapered front Cuboid + tapered behind Cuboid,
              both Y-rotated about the gripper centre
    Used by: Pliers
    Parameters:
      behind_size [w_top, w_bottom, d, h]: behind cuboid top-width, bottom-width, depth, height
      front_size [w_top, w_bottom, d, h]: front cuboid top-width, bottom-width, depth, height
      gripper_separation [s]: X separation between the two arms
      gripper_rotation [deg]: Y rotation of each arm
      position, rotation: global transform
    """
    def __init__(self, behind_size, front_size, gripper_separation, gripper_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        gripper_rotation = [x / 180 * np.pi for x in gripper_rotation]
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.behind_size = behind_size
        self.front_size = front_size
        self.gripper_separation = gripper_separation
        self.gripper_rotation = gripper_rotation

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # front_left
        p1 = [front_size[0] / 2, 0, behind_size[3] + front_size[3] / 2]
        r2 = [0, gripper_rotation[0], 0]
        p1 = adjust_position_from_rotation(p1, r2)
        p2 = [gripper_separation[0] / 2, 0, 0]
        self.front_1_mesh = Cuboid(front_size[3], front_size[1], front_size[2],
                                   front_size[0], front_size[2],
                                   top_offset=[(front_size[1] - front_size[0]) / 2, 0],
                                   position=list_add(p1, p2),
                                   rotation=list_add([np.pi / 2, 0, 0], r2))
        vertices_list.append(self.front_1_mesh.vertices)
        faces_list.append(self.front_1_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.front_1_mesh.vertices)

        # behind_left
        p1 = [behind_size[0] / 2, 0, behind_size[3] / 2]
        r2 = [0, gripper_rotation[0], 0]
        p1 = adjust_position_from_rotation(p1, r2)
        p2 = [gripper_separation[0] / 2, 0, 0]
        self.behind_1_mesh = Cuboid(behind_size[3], behind_size[1], behind_size[2],
                                    behind_size[0], behind_size[2],
                                    top_offset=[-(behind_size[1] - behind_size[0]) / 2, 0],
                                    position=list_add(p1, p2),
                                    rotation=list_add([np.pi / 2, 0, 0], r2))
        vertices_list.append(self.behind_1_mesh.vertices)
        faces_list.append(self.behind_1_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.behind_1_mesh.vertices)

        # front_right
        p1 = [-front_size[0] / 2, 0, behind_size[3] + front_size[3] / 2]
        r2 = [0, -gripper_rotation[0], 0]
        p1 = adjust_position_from_rotation(p1, r2)
        p2 = [-gripper_separation[0] / 2, 0, 0]
        self.front_2_mesh = Cuboid(front_size[3], front_size[1], front_size[2],
                                   front_size[0], front_size[2],
                                   top_offset=[-(front_size[1] - front_size[0]) / 2, 0],
                                   position=list_add(p1, p2),
                                   rotation=list_add([np.pi / 2, 0, 0], r2))
        vertices_list.append(self.front_2_mesh.vertices)
        faces_list.append(self.front_2_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.front_2_mesh.vertices)

        # behind_right
        p1 = [-behind_size[0] / 2, 0, behind_size[3] / 2]
        r2 = [0, -gripper_rotation[0], 0]
        p1 = adjust_position_from_rotation(p1, r2)
        p2 = [-gripper_separation[0] / 2, 0, 0]
        self.behind_2_mesh = Cuboid(behind_size[3], behind_size[1], behind_size[2],
                                    behind_size[0], behind_size[2],
                                    top_offset=[(behind_size[1] - behind_size[0]) / 2, 0],
                                    position=list_add(p1, p2),
                                    rotation=list_add([np.pi / 2, 0, 0], r2))
        vertices_list.append(self.behind_2_mesh.vertices)
        faces_list.append(self.behind_2_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.behind_2_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Gripper'


class Curved_Gripper(ConceptTemplate):
    """
    Semantic: Gripper
    Geometry: 2 mirrored quarter-ellipse Cylinder arms
    Used by: Pliers
    Parameters:
      radius [rx, rz]: X and Z radii of each quarter-cylinder arm
      thickness [h]: height (thickness) of each arm
      gripper_separation [s]: X separation between the two arms
      gripper_rotation [deg]: Y rotation of each arm
      position, rotation: global transform
    """
    def __init__(self, radius, thickness, gripper_separation, gripper_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        gripper_rotation = [x / 180 * np.pi for x in gripper_rotation]
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.radius = radius
        self.thickness = thickness
        self.gripper_separation = gripper_separation
        self.gripper_rotation = gripper_rotation

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.left_mesh = Cylinder(thickness[0], radius[0], radius[0],
                                  top_radius_z=radius[1], bottom_radius_z=radius[1],
                                  is_quarter=True,
                                  position=[gripper_separation[0] / 2, 0, 0],
                                  rotation=[0, gripper_rotation[0], 0])
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        self.right_mesh = Cylinder(thickness[0], radius[0], radius[0],
                                   top_radius_z=radius[1], bottom_radius_z=radius[1],
                                   is_quarter=True,
                                   position=[-gripper_separation[0] / 2, 0, 0],
                                   rotation=[0, -gripper_rotation[0], np.pi],
                                   # ZYX order: Z flip applied first, then Y rotation to mirror left gripper
                                   rotation_order='ZYX')
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Gripper'
