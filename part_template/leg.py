import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Regular_Leg(ConceptTemplate):
    """
    Semantic: Leg
    Geometry: 2 mirrored arms, each a middle Cuboid + top Cuboid (tip), pivot-rotated
    Used by: Eyeglasses
    Parameters:
      glass_interval [gap]: X gap between the two lens centres
      size1 [w, h, d]: dimensions of the middle (main) cuboid
      size2 [w, h, d]: dimensions of the top (tip) cuboid
      rotation_1 [x_deg, y_deg]: rotation applied to the whole arm
      rotation_2 [x_deg, y_deg]: rotation applied to the tip relative to the arm
      offset_x [x]: X offset from lens edge to arm hinge
      position, rotation: global transform
    """
    def __init__(self, glass_interval, size1, size2, rotation_1, rotation_2, offset_x,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        rotation_1 = [x / 180 * np.pi for x in rotation_1]
        rotation_2 = [x / 180 * np.pi for x in rotation_2]
        super().__init__(position, rotation)

        self.size1 = size1
        self.size2 = size2
        self.glass_interval = glass_interval
        self.rotation_1 = rotation_1
        self.rotation_2 = rotation_2
        self.offset_x = offset_x

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        leg_interval = offset_x[0] * 2 + glass_interval[0]

        for direction in [-1, 1]:
            tmp_meshes = []

            top_mesh = Cuboid(size2[1], size2[0], size2[2],
                              position=[-direction * size2[0] / 2, -size2[1] / 2, -size2[2] / 2])
            tmp_meshes.append(top_mesh)
            top_mesh.vertices = apply_transformation(
                top_mesh.vertices,
                position=[0, 0, -size1[2]],
                rotation=[-rotation_2[0], -direction * rotation_2[1], 0],
                rotation_order="YXZ")

            middle_mesh = Cuboid(size1[1], size1[0], size1[2],
                                 position=[-direction * size1[0] / 2, -size1[1] / 2, -size1[2] / 2])
            tmp_meshes.append(middle_mesh)

            for mesh in tmp_meshes:
                mesh.vertices = apply_transformation(
                    mesh.vertices,
                    position=[direction * leg_interval / 2, 0, 0],
                    rotation=[-rotation_1[0], -direction * rotation_1[1], 0],
                    rotation_order="YXZ")
                vertices_list.append(mesh.vertices)
                faces_list.append(mesh.faces + total_num_vertices)
                total_num_vertices += len(mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Leg'


class Trifold_Leg(ConceptTemplate):
    """
    Semantic: Leg
    Geometry: 2 mirrored arms, each a middle Cuboid + top Cuboid (tip) + bottom connector Cuboid
    Used by: Eyeglasses
    Parameters:
      glass_interval [gap]: X gap between the two lens centres
      size1 [w, h, d]: dimensions of the middle (main) cuboid
      size2 [w, h, d]: dimensions of the top (tip) cuboid
      rotation_1 [x_deg, y_deg]: rotation applied to the whole arm
      rotation_2 [x_deg, y_deg]: rotation applied to the tip relative to the arm
      connector_size [w, h, d]: dimensions of the bottom connector cuboid
      offset_x [x]: X offset from lens edge to arm hinge
      position, rotation: global transform
    """
    def __init__(self, glass_interval, size1, size2, rotation_1, rotation_2,
                 connector_size, offset_x, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        rotation_1 = [x / 180 * np.pi for x in rotation_1]
        rotation_2 = [x / 180 * np.pi for x in rotation_2]
        super().__init__(position, rotation)

        self.size1 = size1
        self.size2 = size2
        self.glass_interval = glass_interval
        self.rotation_1 = rotation_1
        self.rotation_2 = rotation_2
        self.offset_x = offset_x
        self.connector_size = connector_size

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        leg_interval = offset_x[0] * 2 + glass_interval[0]

        for direction in [-1, 1]:
            tmp_meshes = []

            top_mesh = Cuboid(size2[1], size2[0], size2[2],
                              position=[-direction * size2[0] / 2, -size2[1] / 2, -size2[2] / 2])
            tmp_meshes.append(top_mesh)
            top_mesh.vertices = apply_transformation(
                top_mesh.vertices,
                position=[0, 0, -size1[2]],
                rotation=[-rotation_2[0], -direction * rotation_2[1], 0],
                rotation_order="XYZ")

            middle_mesh = Cuboid(size1[1], size1[0], size1[2],
                                 position=[-direction * size1[0] / 2, -size1[1] / 2, -size1[2] / 2])
            tmp_meshes.append(middle_mesh)

            for mesh in tmp_meshes:
                mesh.vertices = apply_transformation(
                    mesh.vertices,
                    position=[0, 0, 0],
                    rotation=[-rotation_1[0], -direction * rotation_1[1], 0],
                    rotation_order="XYZ")

            bottom_mesh = Cuboid(connector_size[1], connector_size[0], connector_size[2],
                                 position=[-direction * connector_size[0] / 2,
                                           -connector_size[1] / 2,
                                           connector_size[2] / 2])
            tmp_meshes.append(bottom_mesh)

            for mesh in tmp_meshes:
                mesh.vertices = apply_transformation(
                    mesh.vertices,
                    position=[direction * leg_interval / 2 + offset_x[0] + direction * connector_size[0],
                              connector_size[1] / 2,
                              0],
                    rotation=[0, 0, 0])
                vertices_list.append(mesh.vertices)
                faces_list.append(mesh.faces + total_num_vertices)
                total_num_vertices += len(mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Leg'
