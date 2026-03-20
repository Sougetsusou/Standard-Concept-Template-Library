import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class CuboidalRear_Support(ConceptTemplate):
    """
    Semantic: Support
    Geometry: N Cuboids arranged along X axis, each X-rotated and offset to rear-bottom
    Used by: Display
    Parameters:
      number_of_supports [n]: number of supports
      size [w, h, d]: dimensions of each cuboid
      separation [s]: X gap between supports
      support_rotation [deg]: X rotation applied to each cuboid
      position, rotation: global transform
    """
    def __init__(self, number_of_supports, size, separation, support_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        support_rotation = [x / 180 * np.pi for x in support_rotation]
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.number_of_supports = number_of_supports
        self.size = size
        self.separation = separation
        self.support_rotation = support_rotation

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(int(number_of_supports[0])):
            tmp = Cuboid(size[1], size[0], size[2],
                         position=[(separation[0] + size[0]) * i, -size[1] / 2, -size[2] / 2])
            tmp.vertices = apply_transformation(tmp.vertices,
                                                position=[0, 0, 0],
                                                rotation=[support_rotation[0], 0, 0])
            vertices_list.append(tmp.vertices)
            faces_list.append(tmp.faces + total_num_vertices)
            total_num_vertices += len(tmp.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Support'


class Cuboidal_Support(ConceptTemplate):
    """
    Semantic: Support
    Geometry: N Cuboids arranged along X axis
    Used by: Display
    Parameters:
      number_of_supports [n]: number of supports
      size [w, h, d]: dimensions of each cuboid
      separation [s]: X gap between supports
      position, rotation: global transform
    """
    def __init__(self, number_of_supports, size, separation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.number_of_supports = number_of_supports
        self.size = size
        self.separation = separation

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(int(number_of_supports[0])):
            tmp = Cuboid(size[1], size[0], size[2],
                         position=[(separation[0] + size[0]) * i, -size[1] / 2, 0])
            vertices_list.append(tmp.vertices)
            faces_list.append(tmp.faces + total_num_vertices)
            total_num_vertices += len(tmp.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Support'


class Trifold_Support(ConceptTemplate):
    """
    Semantic: Support
    Geometry: optional upper Cuboid + optional middle Cuboid + optional bottom Cuboid (X-rotated)
    Used by: Display
    Parameters:
      has_upper_part [flag]: 1 to include upper cuboid
      upper_part_size [w, h, d]: dimensions of upper cuboid
      upper_offset [x, y, z]: position of upper cuboid
      has_middle_part [flag]: 1 to include middle cuboid
      middle_part_size [w, h, d]: dimensions of middle cuboid
      middle_offset [y]: Y offset of middle cuboid below upper
      has_bottom_part [flag]: 1 to include bottom cuboid
      bottom_part_size [w, h, d]: dimensions of bottom cuboid
      rotation_of_bottom [deg]: X rotation of bottom cuboid
      bottom_offset [z]: Z offset applied before bottom cuboid placement
      position, rotation: global transform
    """
    def __init__(self, has_upper_part, upper_part_size, upper_offset,
                 has_middle_part, middle_part_size, middle_offset,
                 has_bottom_part, bottom_part_size, rotation_of_bottom, bottom_offset,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation_of_bottom = [x / 180 * np.pi for x in rotation_of_bottom]
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.has_upper_part = has_upper_part
        self.upper_part_size = upper_part_size
        self.upper_offset = upper_offset
        self.has_middle_part = has_middle_part
        self.middle_part_size = middle_part_size
        self.middle_offset = middle_offset
        self.has_bottom_part = has_bottom_part
        self.bottom_part_size = bottom_part_size
        self.rotation_of_bottom = rotation_of_bottom
        self.bottom_offset = bottom_offset

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        base_position = [0, 0, 0]

        if has_upper_part[0]:
            tmp = Cuboid(upper_part_size[1], upper_part_size[0], upper_part_size[2],
                         position=[upper_offset[0],
                                   upper_offset[1],
                                   upper_offset[2] - upper_part_size[2] / 2])
            vertices_list.append(tmp.vertices)
            faces_list.append(tmp.faces + total_num_vertices)
            total_num_vertices += len(tmp.vertices)
            base_position = [base_position[0] + upper_offset[0],
                             base_position[1] + upper_offset[1],
                             base_position[2] + upper_offset[2] - upper_part_size[2]]

        if has_middle_part[0]:
            tmp = Cuboid(middle_part_size[1], middle_part_size[0], middle_part_size[2],
                         position=[base_position[0],
                                   base_position[1] + middle_offset[0] - middle_part_size[1] / 2,
                                   base_position[2] - middle_part_size[2] / 2])
            vertices_list.append(tmp.vertices)
            faces_list.append(tmp.faces + total_num_vertices)
            total_num_vertices += len(tmp.vertices)
            base_position = [base_position[0],
                             base_position[1] + middle_offset[0] - middle_part_size[1],
                             base_position[2] - middle_part_size[2]]

        if has_bottom_part[0]:
            base_position = [base_position[0],
                             base_position[1],
                             base_position[2] + bottom_offset[0]]
            tmp = Cuboid(bottom_part_size[1], bottom_part_size[0], bottom_part_size[2],
                         position=[0, -bottom_part_size[1] / 2, bottom_part_size[2] / 2])
            tmp.vertices = apply_transformation(tmp.vertices, base_position,
                                                [rotation_of_bottom[0], 0, 0])
            vertices_list.append(tmp.vertices)
            faces_list.append(tmp.faces + total_num_vertices)
            total_num_vertices += len(tmp.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Support'


class TShaped_Support(ConceptTemplate):
    """
    Semantic: Support
    Geometry: upper Cuboid + middle Cuboid forming a T-shape
    Used by: Display
    Parameters:
      upper_part_size [w, h, d]: dimensions of upper cuboid
      upper_offset [x, y, z]: position of upper cuboid
      middle_part_size [w, h, d]: dimensions of middle cuboid
      middle_offset [z]: Z offset of middle cuboid relative to upper
      position, rotation: global transform
    """
    def __init__(self, upper_part_size, upper_offset, middle_part_size, middle_offset,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.upper_part_size = upper_part_size
        self.upper_offset = upper_offset
        self.middle_part_size = middle_part_size
        self.middle_offset = middle_offset

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.top_mesh = Cuboid(upper_part_size[1], upper_part_size[0], upper_part_size[2],
                               position=[upper_offset[0],
                                         upper_offset[1],
                                         upper_offset[2] - upper_part_size[2] / 2])
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        self.middle_mesh = Cuboid(middle_part_size[1], middle_part_size[0], middle_part_size[2],
                                  position=[upper_offset[0],
                                            upper_offset[1] - middle_part_size[1] / 2 - upper_part_size[1] / 2,
                                            upper_offset[2] - middle_part_size[2] / 2 + middle_offset[0]])
        vertices_list.append(self.middle_mesh.vertices)
        faces_list.append(self.middle_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.middle_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Support'


class Standard_Support(ConceptTemplate):
    """
    Semantic: Support
    Geometry: 2 mirrored Cuboid supports (left and right), each ZXY-rotated
    Used by: Eyeglasses
    Parameters:
      size [w, h, d]: dimensions of each cuboid
      offset_x [x]: X offset of each support from centre
      support_rotation [x_deg, y_deg, z_deg]: rotation of each support (ZXY order)
      position, rotation: global transform
    """
    def __init__(self, size, offset_x, support_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        support_rotation = [x / 180 * np.pi for x in support_rotation]
        super().__init__(position, rotation)

        self.size = size
        self.support_rotation = support_rotation
        self.offset_x = offset_x

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.right_mesh = Cuboid(size[1], size[0], size[2],
                                 rotation=[support_rotation[0], support_rotation[1], support_rotation[2]],
                                 position=[offset_x[0], 0, 0],
                                 # ZXY order: Z rotation applied first to match support_rotation convention
                                 rotation_order="ZXY")
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        self.left_mesh = Cuboid(size[1], size[0], size[2],
                                rotation=[support_rotation[0], -support_rotation[1], -support_rotation[2]],
                                position=[-offset_x[0], 0, 0],
                                # ZXY order: Z rotation applied first to match support_rotation convention
                                rotation_order="ZXY")
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Support'
