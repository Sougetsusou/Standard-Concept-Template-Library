import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Regular_Cap(ConceptTemplate):
    """
    Semantic: Cap
    Geometry: Rectangular_Ring skirt section + solid Cuboid end cap
    Used by: USB
    Parameters:
      size [w, h, d]: outer width, height, total depth of the cap
      inner_size [w, h, skirt_d]: inner width, height, skirt depth
      inner_outer_offset [x, y]: XY offset of inner opening relative to outer
      position, rotation: global transform
    """
    def __init__(self, size, inner_size, inner_outer_offset,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.size = size
        self.inner_size = inner_size
        self.inner_outer_offset = inner_outer_offset

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        ring_mesh_position = [0, 0, inner_size[2] / 2]
        ring_mesh_rotation = [np.pi / 2, 0, 0]
        self.ring_mesh = Rectangular_Ring(inner_size[2], size[0], size[1],
                                          inner_size[0], inner_size[1],
                                          inner_outer_offset,
                                          rotation=ring_mesh_rotation,
                                          position=ring_mesh_position)
        vertices_list.append(self.ring_mesh.vertices)
        faces_list.append(self.ring_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.ring_mesh.vertices)

        end_mesh_position = [0, 0, (inner_size[2] + size[2]) / 2]
        self.end_mesh = Cuboid(size[1], size[0], size[2] - inner_size[2],
                               position=end_mesh_position)
        vertices_list.append(self.end_mesh.vertices)
        faces_list.append(self.end_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.end_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Cap'


class SquareEnded_Cap(ConceptTemplate):
    """
    Semantic: Cap
    Geometry: two mirrored Cuboid jaw panels + a Ring arc connecting them at the back +
              optional pair of shaft Cylinders
    Used by: USB
    Parameters:
      size [w, h, d]: width, height, depth of each jaw cuboid
      proximal_interval [gap]: Y gap between the two jaws at the open end
      inclination [angle_deg]: splay angle of each jaw from horizontal
      cap_rotation [angle_deg]: Y rotation of the whole cap assembly
      has_shaft [flag]: 1 to add a pair of shaft cylinders
      shaft_size [r, h]: radius and height of each shaft cylinder
      shaft_offset [z]: Z offset of the shaft cylinders
      shaft_interval: Y gap between the two shaft cylinders
      position, rotation: global transform
    """
    def __init__(self, size, proximal_interval, inclination, cap_rotation,
                 has_shaft, shaft_size, shaft_offset, shaft_interval,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        inclination = [x / 180 * np.pi for x in inclination]
        cap_rotation = [x / 180 * np.pi for x in cap_rotation]
        super().__init__(position, rotation)

        self.size = size
        self.proximal_interval = proximal_interval
        self.inclination = inclination
        self.cap_rotation = cap_rotation
        self.shaft_size = shaft_size
        self.shaft_offset = shaft_offset
        self.has_shaft = has_shaft
        self.shaft_interval = shaft_interval

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        radius = proximal_interval[0] / 2 / np.cos(inclination[0]) + size[2] * np.tan(inclination[0])
        back_position = [
            0,
            0,
            -radius * np.sin(inclination[0]) - size[2] * np.cos(inclination[0]) - shaft_offset[0],
        ]
        middle_position = [
            back_position[0],
            (radius + size[1] / 2) * np.cos(inclination[0]) - size[2] * np.sin(inclination[0]) / 2 + back_position[1],
            (radius + size[1] / 2) * np.sin(inclination[0]) + size[2] * np.cos(inclination[0]) / 2 + back_position[2],
        ]

        topCuboid_mesh_position = [
            middle_position[0] * np.cos(cap_rotation[0]) + middle_position[2] * np.sin(cap_rotation[0]),
            middle_position[1],
            middle_position[0] * np.sin(cap_rotation[0]) + middle_position[2] * np.cos(cap_rotation[0]) + shaft_offset[0],
        ]
        topCuboid_mesh_rotation = [inclination[0], cap_rotation[0], 0]
        self.topCuboid_mesh = Cuboid(size[1], size[0], size[2],
                                     position=topCuboid_mesh_position,
                                     rotation=topCuboid_mesh_rotation)
        vertices_list.append(self.topCuboid_mesh.vertices)
        faces_list.append(self.topCuboid_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.topCuboid_mesh.vertices)

        bottomCuboid_mesh_position = [
            middle_position[0] * np.cos(cap_rotation[0]) + middle_position[2] * np.sin(cap_rotation[0]),
            -middle_position[1],
            middle_position[0] * np.sin(cap_rotation[0]) + middle_position[2] * np.cos(cap_rotation[0]) + shaft_offset[0],
        ]
        bottomCuboid_mesh_rotation = [-inclination[0], cap_rotation[0], 0]
        self.bottomCuboid_mesh = Cuboid(size[1], size[0], size[2],
                                        position=bottomCuboid_mesh_position,
                                        rotation=bottomCuboid_mesh_rotation)
        vertices_list.append(self.bottomCuboid_mesh.vertices)
        faces_list.append(self.bottomCuboid_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottomCuboid_mesh.vertices)

        c_mesh_position = [
            back_position[0] * np.cos(cap_rotation[0]) + back_position[2] * np.sin(cap_rotation[0]),
            back_position[1],
            back_position[0] * np.sin(cap_rotation[0]) + back_position[2] * np.cos(cap_rotation[0]) + shaft_offset[0],
        ]
        c_mesh_rotation = [0, np.pi, np.pi / 2]
        self.c_mesh = Ring(size[0], radius + size[1], radius,
                           exist_angle=np.pi + inclination[0] * 2,
                           rotation=c_mesh_rotation)
        self.c_mesh.vertices = apply_transformation(self.c_mesh.vertices, c_mesh_position, [0, cap_rotation[0], 0])
        vertices_list.append(self.c_mesh.vertices)
        faces_list.append(self.c_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.c_mesh.vertices)

        if has_shaft[0]:
            topShaft_mesh_position = [
                0,
                shaft_size[1] / 2 + shaft_interval / 2,
                shaft_offset[0],
            ]
            self.topShaft_mesh = Cylinder(shaft_size[1], shaft_size[0], shaft_size[0],
                                          position=topShaft_mesh_position)
            vertices_list.append(self.topShaft_mesh.vertices)
            faces_list.append(self.topShaft_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.topShaft_mesh.vertices)

            bottomShaft_mesh_position = [
                0,
                -shaft_size[1] / 2 - shaft_interval / 2,
                shaft_offset[0],
            ]
            self.bottomShaft_mesh = Cylinder(shaft_size[1], shaft_size[0], shaft_size[0],
                                             position=bottomShaft_mesh_position)
            vertices_list.append(self.bottomShaft_mesh.vertices)
            faces_list.append(self.bottomShaft_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.bottomShaft_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Cap'


class RoundEnded_Cap(ConceptTemplate):
    """
    Semantic: Cap
    Geometry: two mirrored Cuboid jaw panels + two half-Cylinder rounded ends +
              a Ring arc connecting them at the back + optional pair of shaft Cylinders
    Used by: USB
    Parameters:
      size [w, h, d]: width, height, depth of each jaw cuboid (d includes half-cylinder radius)
      proximal_interval [gap]: Y gap between the two jaws at the open end
      inclination [angle_deg]: splay angle of each jaw from horizontal
      cap_rotation [angle_deg]: Y rotation of the whole cap assembly
      has_shaft [flag]: 1 to add a pair of shaft cylinders
      shaft_size [r, h]: radius and height of each shaft cylinder
      shaft_offset [z]: Z offset of the shaft cylinders
      shaft_interval: Y gap between the two shaft cylinders
      position, rotation: global transform
    """
    def __init__(self, size, proximal_interval, inclination, cap_rotation,
                 has_shaft, shaft_size, shaft_offset, shaft_interval,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        inclination = [x / 180 * np.pi for x in inclination]
        cap_rotation = [x / 180 * np.pi for x in cap_rotation]
        super().__init__(position, rotation)

        self.size = size
        self.proximal_interval = proximal_interval
        self.inclination = inclination
        self.cap_rotation = cap_rotation
        self.shaft_size = shaft_size
        self.shaft_offset = shaft_offset
        self.has_shaft = has_shaft
        self.shaft_interval = shaft_interval

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        radius = proximal_interval[0] / 2 / np.cos(inclination[0]) + size[2] * np.tan(inclination[0])
        back_position = [
            0,
            0,
            -radius * np.sin(inclination[0]) - size[2] * np.cos(inclination[0]) - shaft_offset[0],
        ]
        middle_position = [
            back_position[0],
            (radius + size[1] / 2) * np.cos(inclination[0]) - (size[2] - size[0] / 2) * np.sin(inclination[0]) / 2 + back_position[1],
            (radius + size[1] / 2) * np.sin(inclination[0]) + (size[2] - size[0] / 2) * np.cos(inclination[0]) / 2 + back_position[2],
        ]
        end_position = [
            middle_position[0],
            (size[1] * np.cos(inclination[0]) + size[0] * np.sin(inclination[0]) + proximal_interval[0]) / 2,
            -(-size[1] * np.sin(inclination[0]) + size[0] * np.cos(inclination[0])) / 2 - shaft_offset[0],
        ]

        topCuboid_mesh_position = [
            middle_position[0] * np.cos(cap_rotation[0]) + middle_position[2] * np.sin(cap_rotation[0]),
            middle_position[1],
            middle_position[0] * np.sin(cap_rotation[0]) + middle_position[2] * np.cos(cap_rotation[0]) + shaft_offset[0],
        ]
        topCuboid_mesh_rotation = [inclination[0], cap_rotation[0], 0]
        self.topCuboid_mesh = Cuboid(size[1], size[0], size[2] - size[0] / 2,
                                     position=topCuboid_mesh_position,
                                     rotation=topCuboid_mesh_rotation)
        vertices_list.append(self.topCuboid_mesh.vertices)
        faces_list.append(self.topCuboid_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.topCuboid_mesh.vertices)

        bottomCuboid_mesh_position = [
            middle_position[0] * np.cos(cap_rotation[0]) + middle_position[2] * np.sin(cap_rotation[0]),
            -middle_position[1],
            middle_position[0] * np.sin(cap_rotation[0]) + middle_position[2] * np.cos(cap_rotation[0]) + shaft_offset[0],
        ]
        bottomCuboid_mesh_rotation = [-inclination[0], cap_rotation[0], 0]
        self.bottomCuboid_mesh = Cuboid(size[1], size[0], size[2] - size[0] / 2,
                                        position=bottomCuboid_mesh_position,
                                        rotation=bottomCuboid_mesh_rotation)
        vertices_list.append(self.bottomCuboid_mesh.vertices)
        faces_list.append(self.bottomCuboid_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottomCuboid_mesh.vertices)

        c_mesh_position = [
            back_position[0] * np.cos(cap_rotation[0]) + back_position[2] * np.sin(cap_rotation[0]),
            back_position[1],
            back_position[0] * np.sin(cap_rotation[0]) + back_position[2] * np.cos(cap_rotation[0]) + shaft_offset[0],
        ]
        c_mesh_rotation = [0, np.pi, np.pi / 2]
        self.c_mesh = Ring(size[0], radius + size[1], radius,
                           exist_angle=np.pi + inclination[0] * 2,
                           rotation=c_mesh_rotation)
        self.c_mesh.vertices = apply_transformation(self.c_mesh.vertices, c_mesh_position, [0, cap_rotation[0], 0])
        vertices_list.append(self.c_mesh.vertices)
        faces_list.append(self.c_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.c_mesh.vertices)

        topEnd_mesh_position = [
            end_position[0] * np.cos(cap_rotation[0]) + end_position[2] * np.sin(cap_rotation[0]),
            end_position[1],
            end_position[0] * np.sin(cap_rotation[0]) + end_position[2] * np.cos(cap_rotation[0]) + shaft_offset[0],
        ]
        topEnd_mesh_rotation = [inclination[0], cap_rotation[0], 0]
        self.topEnd_mesh = Cylinder(size[1], size[0] / 2, size[0] / 2, is_half=True,
                                    position=topEnd_mesh_position,
                                    rotation=topEnd_mesh_rotation)
        vertices_list.append(self.topEnd_mesh.vertices)
        faces_list.append(self.topEnd_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.topEnd_mesh.vertices)

        bottomEnd_mesh_position = [
            end_position[0] * np.cos(cap_rotation[0]) + end_position[2] * np.sin(cap_rotation[0]),
            -end_position[1],
            end_position[0] * np.sin(cap_rotation[0]) + end_position[2] * np.cos(cap_rotation[0]) + shaft_offset[0],
        ]
        bottomEnd_mesh_rotation = [-inclination[0], cap_rotation[0], 0]
        self.bottomEnd_mesh = Cylinder(size[1], size[0] / 2, size[0] / 2, is_half=True,
                                       position=bottomEnd_mesh_position,
                                       rotation=bottomEnd_mesh_rotation)
        vertices_list.append(self.bottomEnd_mesh.vertices)
        faces_list.append(self.bottomEnd_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottomEnd_mesh.vertices)

        if has_shaft[0]:
            topShaft_mesh_position = [
                0,
                shaft_size[1] / 2 + shaft_interval / 2,
                shaft_offset[0],
            ]
            self.topShaft_mesh = Cylinder(shaft_size[1], shaft_size[0], shaft_size[0],
                                          position=topShaft_mesh_position)
            vertices_list.append(self.topShaft_mesh.vertices)
            faces_list.append(self.topShaft_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.topShaft_mesh.vertices)

            bottomShaft_mesh_position = [
                0,
                -shaft_size[1] / 2 - shaft_interval / 2,
                shaft_offset[0],
            ]
            self.bottomShaft_mesh = Cylinder(shaft_size[1], shaft_size[0], shaft_size[0],
                                             position=bottomShaft_mesh_position)
            vertices_list.append(self.bottomShaft_mesh.vertices)
            faces_list.append(self.bottomShaft_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.bottomShaft_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Cap'
