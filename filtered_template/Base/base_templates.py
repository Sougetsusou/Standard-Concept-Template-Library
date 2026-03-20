"""
Base Templates
Automatically extracted from concept_template.py files
Contains 16 class(es)
"""

from base_template import ConceptTemplate
from geometry_template import *
from knowledge_utils import *
from math import degrees, atan2, sqrt
from utils import apply_transformation
from utils import apply_transformation, adjust_position_from_rotation, list_add
from utils import apply_transformation, get_rodrigues_matrix
import copy
import numpy as np
import open3d as o3d
import trimesh


# Source: Globe/concept_template.py
class Cylindrical_Base(ConceptTemplate):
    def __init__(self, bottom_size, top_size, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.bottom_size = bottom_size
        self.top_size = top_size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        top_mesh_position = [
            0,
            -top_size[2] / 2,
            0
        ]
        self.top_mesh = Cylinder(top_size[2], top_size[0], top_size[1],
                                 position = top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [
            0,
            -top_size[2] - bottom_size[2] / 2,
            0
        ]
        self.bottom_mesh = Cylinder(bottom_size[2], bottom_size[0], bottom_size[1],
                                    position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Base'


# Source: Globe/concept_template.py
class Cuboidal_Base(ConceptTemplate):
    def __init__(self, bottom_size, top_size, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.bottom_size = bottom_size
        self.top_size = top_size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        top_mesh_position = [
            0,
            -top_size[1] / 2,
            0
        ]
        self.top_mesh = Cuboid(top_size[1], top_size[0], top_size[2],
                               position = top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [
            0,
            -top_size[1] - bottom_size[1] / 2,
            0
        ]
        self.bottom_mesh = Cuboid(bottom_size[1], bottom_size[0], bottom_size[2],
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Base'


# Source: Globe/concept_template.py
class Star_Shaped_Base(ConceptTemplate):
    def __init__(self, top_size, sub_size, num_legs, tilt_angle, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        tilt_angle = [x / 180 * np.pi for x in tilt_angle]
        super().__init__(position, rotation)

        # Record Parameters
        self.top_size = top_size
        self.sub_size = sub_size
        self.num_legs = num_legs
        self.tilt_angle = tilt_angle

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        top_mesh_position = [
            0,
            -top_size[1] / 2,
            0
        ]
        self.top_mesh = Cylinder(top_size[1], top_size[0], 
                                 position = top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        for i in range(num_legs[0]):

            rot = np.pi * 2 / num_legs[0] * i
            claw_mesh_rotation = [
                tilt_angle[0],
                -rot,
                0
            ]
            x_ = sub_size[2] / 2 * np.cos(tilt_angle[0]) * np.sin(rot)
            z_ = sub_size[2] / 2 * np.cos(tilt_angle[0]) * np.cos(rot)
            y__ = -top_size[1] + sub_size[1] / 2 - sub_size[2] * np.sin(tilt_angle[0]) / 2
            claw_mesh_position = [
                -x_,
                y__,
                z_
            ]
            self.claw_mesh = Cuboid(sub_size[1], sub_size[0], sub_size[2],
                                    position = claw_mesh_position,
                                    rotation = claw_mesh_rotation)
            vertices_list.append(self.claw_mesh.vertices)
            faces_list.append(self.claw_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.claw_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Base'


# Source: Globe/concept_template.py
class Special_Base(ConceptTemplate):
    def __init__(self, radius, top_size, top_rotation, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        top_rotation = [x / 180 * np.pi for x in top_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.radius = radius
        self.top_size = top_size
        self.top_rotation = top_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        top_mesh_position = [
            0,
            -top_size[1] / 2 * np.cos(top_rotation[0]),
            -top_size[1] / 2 * np.sin(top_rotation[0])
        ]
        top_mesh_rotation = [
            top_rotation[0],
            0,
            0
        ]
        self.top_mesh = Cylinder(top_size[1], top_size[0],
                                 position = top_mesh_position,
                                 rotation = top_mesh_rotation)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [
            0,
            -top_size[1] * np.cos(top_rotation[0]),
            radius[0] - top_size[1] * np.sin(top_rotation[0])
        ]
        self.bottom_mesh = Torus(radius[0], radius[1], 
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Base'


# Source: Globe/concept_template.py
class Table_Like_Base(ConceptTemplate):
    def __init__(self, circle_size, num_legs, leg_size, leg_seperation, has_bottom_part, bottom_size, bottom_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.circle_size = circle_size
        self.num_legs = num_legs
        self.leg_size = leg_size
        self.leg_seperation = leg_seperation
        self.has_bottom_part = has_bottom_part
        self.bottom_size = bottom_size
        self.bottom_offset = bottom_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.ring_mesh = Ring(circle_size[2], circle_size[0], circle_size[1])
        vertices_list.append(self.ring_mesh.vertices)
        faces_list.append(self.ring_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.ring_mesh.vertices)

        for i in range(num_legs[0]):
            rotation_tmp = np.pi * 2 / num_legs[0] * i
            leg_mesh_position = [
                leg_seperation[0] * np.cos(rotation_tmp),
                -circle_size[2] / 2 - leg_size[1] / 2,
                leg_seperation[0] * np.sin(rotation_tmp)
            ]
            self.leg_mesh = Cylinder(leg_size[1], leg_size[0], 
                                     position = leg_mesh_position)
            vertices_list.append(self.leg_mesh.vertices)
            faces_list.append(self.leg_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.leg_mesh.vertices)

            if has_bottom_part[0] == 1:
                bottom_mesh_position = [
                    bottom_size[0] / 2 * np.cos(rotation_tmp),
                    -circle_size[2] / 2 - leg_size[1] + bottom_size[1] / 2 + bottom_offset[0],
                    bottom_size[0] / 2 * np.sin(rotation_tmp)
                ]
                bottom_mesh_rotation = [
                    0,
                    -rotation_tmp,
                    0
                ]
                self.bottom_mesh = Cuboid(bottom_size[1], bottom_size[0], bottom_size[2],
                                          position = bottom_mesh_position,
                                          rotation = bottom_mesh_rotation)
                vertices_list.append(self.bottom_mesh.vertices)
                faces_list.append(self.bottom_mesh.faces + total_num_vertices)
                total_num_vertices += len(self.bottom_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Base'


# Source: Display/concept_template.py
class Cuboidal_Base(ConceptTemplate):
    def __init__(self, size, base_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        base_rotation = [x / 180 * np.pi for x in base_rotation]
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.base_rotation = base_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        base_mesh_position = [
            0, 
            -size[1] / 2, 
            0
        ]
        base_mesh_rotation = [base_rotation[0], 0, 0]
        self.base_mesh = Cuboid(size[1], size[0], size[2],
                                position=base_mesh_position,
                                rotation=base_mesh_rotation)
        vertices_list.append(self.base_mesh.vertices)
        faces_list.append(self.base_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.base_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Base'


# Source: Display/concept_template.py
class Round_Base(ConceptTemplate):
    def __init__(self, size, base_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        base_rotation = [x / 180 * np.pi for x in base_rotation]
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.base_rotation = base_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # meshes definition
        base_mesh_position = [
            0, 
            -size[1] / 2, 
            0
        ]
        base_mesh_rotation = [base_rotation[0], 0, 0]
        self.base_mesh = Cylinder(size[1], size[0], size[0],
                                  position=base_mesh_position,
                                  rotation=base_mesh_rotation)
        vertices_list.append(self.base_mesh.vertices)
        faces_list.append(self.base_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.base_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Base'


# Source: Display/concept_template.py
class TShaped_Base(ConceptTemplate):
    def __init__(self, main_size, sub_size, base_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        base_rotation = [x / 180 * np.pi for x in base_rotation]
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.main_size = main_size
        self.sub_size = sub_size
        self.base_rotation = base_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        sub_mesh_position = [
            0, 
            -main_size[1] / 2, 
            0
        ]
        sub_mesh_rotation = [base_rotation[0], 0, 0]
        self.sub_mesh = Cuboid(main_size[1], sub_size[0], sub_size[1],
                               position=sub_mesh_position,
                               rotation=sub_mesh_rotation)
        vertices_list.append(self.sub_mesh.vertices)
        faces_list.append(self.sub_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.sub_mesh.vertices)

        main_mesh_position = [
            0,
            -main_size[1] / 2 - (main_size[2] + sub_size[1]) * np.sin(base_rotation[0]) / 2,
            (main_size[2] + sub_size[1]) * np.cos(base_rotation[0]) / 2,
        ]
        main_mesh_rotation = [base_rotation[0], 0, 0]
        self.main_mesh = Cuboid(main_size[1], main_size[0], main_size[2],
                                position=main_mesh_position,
                                rotation=main_mesh_rotation)
        vertices_list.append(self.main_mesh.vertices)
        faces_list.append(self.main_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.main_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Base'


# Source: Display/concept_template.py
class Vshaped_Base(ConceptTemplate):
    def __init__(self, size, open_angle, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        open_angle = [x / 180 * np.pi for x in open_angle]
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.open_angle = open_angle

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        left_mesh_position = [0, -size[1] / 2, size[2] / 2]
        self.left_mesh = Cuboid(size[1], size[0], size[2], 
                                position=left_mesh_position)
        self.left_mesh.vertices = apply_transformation(self.left_mesh.vertices, position=[0, 0, 0], rotation=[0, -open_angle[0] / 2, 0])
        vertices_list.append(self.left_mesh.vertices)
        faces_list.append(self.left_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.left_mesh.vertices)

        right_mesh_position = [0, -size[1] / 2, size[2] / 2]
        self.right_mesh = Cuboid(size[1], size[0], size[2], 
                                 position=right_mesh_position)
        self.right_mesh.vertices = apply_transformation(self.right_mesh.vertices, position=[0, 0, 0], rotation=[0, open_angle[0] / 2, 0])
        vertices_list.append(self.right_mesh.vertices)
        faces_list.append(self.right_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.right_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Base'


# Source: Faucet/concept_template.py
class Cuboidal_Base(ConceptTemplate):
    def __init__(self, number_of_box, size_0, size_1, offset_1, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.number_of_box = number_of_box
        self.size_0 = size_0
        self.size_1 = size_1
        self.offset_1 = offset_1

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        back_mesh_position = [0, -size_0[1] / 2, -size_0[2] / 2]
        self.back_mesh = Cuboid(size_0[1], size_0[0], size_0[2],
                                position=back_mesh_position)
        vertices_list.append(self.back_mesh.vertices)
        faces_list.append(self.back_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.back_mesh.vertices)

        if number_of_box[0] == 2:
            back_mesh_position = [
                offset_1[0],
                -size_0[1] - size_1[1] / 2 + offset_1[1],
                offset_1[2] - size_0[2] / 2,
            ]
            self.back_mesh = Cuboid(size_1[1], size_1[0], size_1[2], 
                                    position=back_mesh_position)
            vertices_list.append(self.back_mesh.vertices)
            faces_list.append(self.back_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.back_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Base'


# Source: Faucet/concept_template.py
class Cylindrical_Base(ConceptTemplate):
    def __init__(self, number_of_cylinder, size_0, size_1, offset_1, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.number_of_cylinder = number_of_cylinder
        self.size_0 = size_0
        self.size_1 = size_1
        self.offset_1 = offset_1

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        back_mesh_position = [0, -size_0[1] / 2, -size_0[0]]
        self.back_mesh = Cylinder(size_0[1], size_0[0], size_0[0],
                                  position=back_mesh_position)
        vertices_list.append(self.back_mesh.vertices)
        faces_list.append(self.back_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.back_mesh.vertices)

        if number_of_cylinder[0] == 2:
            back_mesh_position = [
                offset_1[0],
                -size_0[1] - size_1[1] / 2 + offset_1[1],
                offset_1[2] - size_0[0],
            ]
            self.back_mesh = Cylinder(size_1[1], size_1[0], size_1[0], 
                                      position=back_mesh_position)
            vertices_list.append(self.back_mesh.vertices)
            faces_list.append(self.back_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.back_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Base'


# Source: Faucet/concept_template.py
class Curved_Base(ConceptTemplate):
    def __init__(self, R, size, base_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.R = R
        self.size = size
        self.base_rotation = base_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        center_position = [0, -size[0] / 2, size[0] ** 2 / 4 / size[1]]
        center_angle = np.arctan(size[0] / 2 / center_position[2]) * 2
        center_radius = center_position[2] / np.cos(center_angle / 2)

        main_mesh_rotation = [center_angle / 2 + np.pi / 2, 0, -np.pi / 2]
        self.main_mesh = Torus(center_radius, R[0], center_angle,
                               position=center_position,
                               rotation=main_mesh_rotation,
                               rotation_order="ZXY")
        self.main_mesh.vertices = apply_transformation(self.main_mesh.vertices, [0, 0, 0], [base_rotation[0], 0, 0])
        vertices_list.append(self.main_mesh.vertices)
        faces_list.append(self.main_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.main_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Base'


# Source: Faucet/concept_template.py
class UShapedXZ_Base(ConceptTemplate):
    def __init__(self, R, size_tube, size_base, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.R = R
        self.size_tube = size_tube
        self.size_base = size_base

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        tmp_mesh_position = [
            -size_tube[0] / 2, 
            0, 
            size_base[1] + size_tube[1] / 2
        ]
        tmp_mesh_rotation = [np.pi / 2, 0, 0]
        self.tmp_mesh = Cylinder(size_tube[1], R[0], R[0],
                                 position=tmp_mesh_position,
                                 rotation=tmp_mesh_rotation)
        vertices_list.append(self.tmp_mesh.vertices)
        faces_list.append(self.tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.tmp_mesh.vertices)

        tmp_mesh_position = [
            size_tube[0] / 2, 
            0, 
            size_base[1] + size_tube[1] / 2
        ]
        tmp_mesh_rotation = [np.pi / 2, 0, 0]
        self.tmp_mesh = Cylinder(size_tube[1], R[0], R[0],
                                 position=tmp_mesh_position,
                                 rotation=tmp_mesh_rotation)
        vertices_list.append(self.tmp_mesh.vertices)
        faces_list.append(self.tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.tmp_mesh.vertices)

        tmp_mesh_position = [0, 0, size_base[1] + size_tube[1]]
        tmp_mesh_rotation = [0, 0, np.pi / 2]
        self.tmp_mesh = Cylinder(size_tube[0], R[0], R[0],
                                 position=tmp_mesh_position,
                                 rotation=tmp_mesh_rotation)
        vertices_list.append(self.tmp_mesh.vertices)
        faces_list.append(self.tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.tmp_mesh.vertices)

        tmp_mesh_position = [size_tube[0] / 2, 0, size_base[1] / 2]
        tmp_mesh_rotation = [np.pi / 2, 0, 0]
        self.tmp_mesh = Cylinder(size_base[1], size_base[0], size_base[0],
                                 position=tmp_mesh_position,
                                 rotation=tmp_mesh_rotation)
        vertices_list.append(self.tmp_mesh.vertices)
        faces_list.append(self.tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.tmp_mesh.vertices)

        tmp_mesh_position = [-size_tube[0] / 2, 0, size_base[1] / 2]
        tmp_mesh_rotation = [np.pi / 2, 0, 0]
        self.tmp_mesh = Cylinder(size_base[1], size_base[0], size_base[0],
                                 position=tmp_mesh_position,
                                 rotation=tmp_mesh_rotation)
        vertices_list.append(self.tmp_mesh.vertices)
        faces_list.append(self.tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Base'


# Source: Faucet/concept_template.py
class UShapedYZ_Base(ConceptTemplate):
    def __init__(self, R, size_tube, size_base, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.R = R
        self.size_tube = size_tube
        self.size_base = size_base

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        tmp_mesh_position = [-size_tube[0] / 2, -size_tube[1] / 2, 0]
        self.tmp_mesh = Cylinder(size_tube[1], R[0], R[0],
                                 position=tmp_mesh_position)
        vertices_list.append(self.tmp_mesh.vertices)
        faces_list.append(self.tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.tmp_mesh.vertices)

        tmp_mesh_position = [size_tube[0] / 2, -size_tube[1] / 2, 0]
        self.tmp_mesh = Cylinder(size_tube[1], R[0], R[0],
                                 position=tmp_mesh_position)
        vertices_list.append(self.tmp_mesh.vertices)
        faces_list.append(self.tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.tmp_mesh.vertices)

        tmp_mesh_rotation = [0, 0, np.pi / 2]
        self.tmp_mesh = Cylinder(size_tube[0], R[0], R[0],
                                 rotation=tmp_mesh_rotation)
        vertices_list.append(self.tmp_mesh.vertices)
        faces_list.append(self.tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.tmp_mesh.vertices)

        tmp_mesh_position = [
            size_tube[0] / 2,
            -(size_base[1] / 2 + size_tube[1]),
            0,
        ]
        self.tmp_mesh = Cylinder(size_base[1], size_base[0], size_base[0],
                                 position=tmp_mesh_position)
        vertices_list.append(self.tmp_mesh.vertices)
        faces_list.append(self.tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.tmp_mesh.vertices)

        tmp_mesh_position = [
            -size_tube[0] / 2, 
            -(size_base[1] / 2 + size_tube[1]), 
            0
        ]
        self.tmp_mesh = Cylinder(size_base[1], size_base[0], size_base[0],
                                 position=tmp_mesh_position)
        vertices_list.append(self.tmp_mesh.vertices)
        faces_list.append(self.tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Base'


# Source: Faucet/concept_template.py
class Round_Base(ConceptTemplate):
    def __init__(self, size, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        main_mesh_position = [0, 0, -size[1] / 2]
        main_mesh_rotation = [np.pi / 2, 0, 0]
        self.main_mesh = Cylinder(size[1], size[0], size[0],
                                  position=main_mesh_position,
                                  rotation=main_mesh_rotation)
        vertices_list.append(self.main_mesh.vertices)
        faces_list.append(self.main_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.main_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Base'


# Source: Laptop/concept_template.py
class Regular_Base(ConceptTemplate):
    def __init__(self, size, position=[0, 0, 0], rotation=[0, 0, 0]):
        
        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0
        
        self.back_mesh = Cuboid(size[1], size[0], size[2])
        vertices_list.append(self.back_mesh.vertices)
        faces_list.append(self.back_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.back_mesh.vertices)

        self.vertices=np.concatenate(vertices_list)
        self.faces=np.concatenate(faces_list)

        # Global Transformation
        self.vertices=apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Base'
