import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Regular_Body(ConceptTemplate):
    """
    Semantic: Body
    Geometry: main cuboid body + optional half-cylinder back cap + optional half-cylinder side caps
              + optional quarter-sphere corner pieces where back and side caps meet
    Used by: USB
    Parameters:
      size [w, h, d]: dimensions of the main cuboid
      has_back_part [flag]: 1 to add a half-cylinder cap at the back (Z-)
      has_side_part [flag]: 1 to add half-cylinder caps on left and right sides
      position, rotation: global transform
    """
    def __init__(self, size, has_back_part, has_side_part, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.size = size
        self.has_back_part = has_back_part
        self.has_side_part = has_side_part

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        main_mesh_position = [0, 0, -size[2] / 2]
        self.main_mesh = Cuboid(size[1], size[0], size[2],
                                position=main_mesh_position)
        vertices_list.append(self.main_mesh.vertices)
        faces_list.append(self.main_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.main_mesh.vertices)

        if has_back_part[0]:
            back_mesh_position = [0, 0, -size[2]]
            back_mesh_rotation = [0, np.pi, np.pi / 2]
            self.back_mesh = Cylinder(size[0], size[1] / 2, size[1] / 2, is_half=True,
                                      position=back_mesh_position,
                                      rotation=back_mesh_rotation)
            vertices_list.append(self.back_mesh.vertices)
            faces_list.append(self.back_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.back_mesh.vertices)

        if has_side_part[0]:
            left_mesh_position = [-size[0] / 2, 0, -size[2] / 2]
            left_mesh_rotation = [np.pi / 2, 0, -np.pi / 2]
            self.left_mesh = Cylinder(size[2], size[1] / 2, size[1] / 2, is_half=True,
                                      position=left_mesh_position,
                                      rotation=left_mesh_rotation)
            vertices_list.append(self.left_mesh.vertices)
            faces_list.append(self.left_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.left_mesh.vertices)

            right_mesh_position = [size[0] / 2, 0, -size[2] / 2]
            right_mesh_rotation = [np.pi / 2, 0, np.pi / 2]
            self.right_mesh = Cylinder(size[2], size[1] / 2, size[1] / 2, is_half=True,
                                       position=right_mesh_position,
                                       rotation=right_mesh_rotation)
            vertices_list.append(self.right_mesh.vertices)
            faces_list.append(self.right_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.right_mesh.vertices)

        if has_back_part[0] and has_side_part[0]:
            left_back_mesh_position = [-size[0] / 2, 0, -size[2]]
            left_back_mesh_rotation = [0, np.pi, 0]
            self.left_back_mesh = Sphere(radius=size[1] / 2, longitude_angle=np.pi / 2,
                                         position=left_back_mesh_position,
                                         rotation=left_back_mesh_rotation)
            vertices_list.append(self.left_back_mesh.vertices)
            faces_list.append(self.left_back_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.left_back_mesh.vertices)

            right_back_mesh_position = [size[0] / 2, 0, -size[2]]
            right_back_mesh_rotation = [0, np.pi / 2, 0]
            self.right_back_mesh = Sphere(radius=size[1] / 2, longitude_angle=np.pi / 2,
                                          position=right_back_mesh_position,
                                          rotation=right_back_mesh_rotation)
            vertices_list.append(self.right_back_mesh.vertices)
            faces_list.append(self.right_back_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.right_back_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


class RoundEnded_Body(ConceptTemplate):
    """
    Semantic: Body
    Geometry: main cuboid + a half-cylinder cap at the back (Z-) end
    Used by: USB
    Parameters:
      size [w, h, d]: dimensions of the main cuboid
      position, rotation: global transform
    """
    def __init__(self, size, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.size = size

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        main_mesh_position = [0, 0, -size[2] / 2]
        self.main_mesh = Cuboid(size[1], size[0], size[2],
                                position=main_mesh_position)
        vertices_list.append(self.main_mesh.vertices)
        faces_list.append(self.main_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.main_mesh.vertices)

        back_mesh_position = [0, 0, -size[2]]
        back_mesh_rotation = [0, np.pi, 0]
        self.back_mesh = Cylinder(size[1], size[0] / 2, size[0] / 2, is_half=True,
                                  position=back_mesh_position,
                                  rotation=back_mesh_rotation)
        vertices_list.append(self.back_mesh.vertices)
        faces_list.append(self.back_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.back_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


class Cylindrical_Body(ConceptTemplate):
    """
    Semantic: Body
    Geometry: tapered cylinder base section + Ring top section forming a hollow cylindrical body
    Used by: Mug
    Parameters:
      outer_size [top_r, bottom_r, h]: outer top radius, outer bottom radius, total height
      inner_size [top_r, bottom_r, wall_h]: inner top radius, inner bottom radius, wall height
      position, rotation: global transform
    """
    def __init__(self, outer_size, inner_size, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.outer_size = outer_size
        self.inner_size = inner_size

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        middle_radius = outer_size[0] * (1 - inner_size[2] / outer_size[2]) + outer_size[1] * inner_size[2] / outer_size[2]
        bottom_height = outer_size[2] - inner_size[2]
        bottom_mesh_position = [0, -inner_size[2] / 2, 0]
        self.bottom_mesh = Cylinder(bottom_height, middle_radius, outer_size[1],
                                    position=bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        top_mesh_position = [0, (outer_size[2] - inner_size[2]) / 2, 0]
        self.top_mesh = Ring(inner_size[2], outer_size[0], inner_size[0],
                             outer_bottom_radius=middle_radius,
                             inner_bottom_radius=inner_size[1],
                             position=top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


class Prismatic_Body(ConceptTemplate):
    """
    Semantic: Body
    Geometry: tapered square-prism base + Rectangular_Ring top section forming a hollow prismatic body
    Used by: Mug
    Parameters:
      outer_size [top_r, bottom_r, h]: outer top half-width, outer bottom half-width, total height
      inner_size [top_r, bottom_r, wall_h]: inner top half-width, inner bottom half-width, wall height
      position, rotation: global transform
    """
    def __init__(self, outer_size, inner_size, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.outer_size = outer_size
        self.inner_size = inner_size

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        middle_radius = outer_size[0] * (1 - inner_size[2] / outer_size[2]) + outer_size[1] * inner_size[2] / outer_size[2]
        bottom_height = outer_size[2] - inner_size[2]
        bottom_mesh_position = [0, -inner_size[2] / 2, 0]
        self.bottom_mesh = Cuboid(bottom_height,
                                  middle_radius * np.sqrt(2), middle_radius * np.sqrt(2),
                                  outer_size[1] * np.sqrt(2), outer_size[1] * np.sqrt(2),
                                  position=bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        top_mesh_position = [0, (outer_size[2] - inner_size[2]) / 2, 0]
        self.top_mesh = Rectangular_Ring(inner_size[2],
                                         outer_size[0] * np.sqrt(2), outer_size[0] * np.sqrt(2),
                                         inner_size[0] * np.sqrt(2), inner_size[0] * np.sqrt(2),
                                         outer_bottom_length=middle_radius * np.sqrt(2),
                                         outer_bottom_width=middle_radius * np.sqrt(2),
                                         inner_bottom_length=inner_size[1] * np.sqrt(2),
                                         inner_bottom_width=inner_size[1] * np.sqrt(2),
                                         position=top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'


class Cuboidal_Body(ConceptTemplate):
    """
    Semantic: Body
    Geometry: hollow box body — Rectangular_Ring wall section + tapered Cuboid bottom section
    Used by: Box
    Parameters:
      top_size [w, d]: top opening width and depth
      bottom_size [w, d]: bottom width and depth
      height [total_h, wall_h]: total height and wall (ring) height
      top_bottom_offset [x, z]: XZ offset of top face relative to bottom
      thickness [side_t, wall_h, front_t]: wall thickness (side, top, front)
      position, rotation: global transform
    """
    def __init__(self, top_size, bottom_size, height, top_bottom_offset, thickness,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.top_size = top_size
        self.bottom_size = bottom_size
        self.height = height
        self.top_bottom_offset = top_bottom_offset
        self.thickness = thickness

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        middle_x = top_size[0] * thickness[1] / height[0] + bottom_size[0] * (height[0] - thickness[1]) / height[0]
        middle_z = top_size[1] * thickness[1] / height[0] + bottom_size[1] * (height[0] - thickness[1]) / height[0]
        middle_offset_x = top_bottom_offset[0] * thickness[1] / height[0]
        middle_offset_z = top_bottom_offset[1] * thickness[1] / height[0]

        top_mesh_position = [middle_offset_x, thickness[1] / 2, middle_offset_z]
        self.top_mesh = Rectangular_Ring(height[0] - thickness[1],
                                         top_size[0], top_size[1],
                                         top_size[0] - thickness[0] * 2, top_size[1] - thickness[2] * 2,
                                         [0, 0], middle_x, middle_z,
                                         middle_x - thickness[0] * 2, middle_z - thickness[2] * 2,
                                         top_bottom_offset=[top_bottom_offset[0] - middle_offset_x,
                                                            top_bottom_offset[1] - middle_offset_z],
                                         position=top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [0, -(height[0] - thickness[1]) / 2, 0]
        self.bottom_mesh = Cuboid(thickness[1], middle_x, middle_z,
                                  bottom_size[0], bottom_size[1],
                                  top_offset=[middle_offset_x, middle_offset_z],
                                  position=bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Body'
