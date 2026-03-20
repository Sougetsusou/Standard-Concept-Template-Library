"""
Switch Templates
Automatically extracted from concept_template.py files
Contains 17 class(es)
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


# Source: Switch/concept_template.py
class Round_Switch(ConceptTemplate):
    def __init__(self, number_of_switch, size, offset_1, offset_2, offset_3, offset_4, offset_Z, switch_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        switch_rotation = [x / 180 * np.pi for x in switch_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.number_of_switch = number_of_switch
        self.size = size
        self.offset_1 = offset_1
        self.offset_2 = offset_2
        self.offset_3 = offset_3
        self.offset_4 = offset_4
        self.offset_Z = offset_Z
        self.switch_rotation = switch_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(number_of_switch[0]):
            base_mesh_position = [
                locals()['offset_%d'%(i+1)][0],
                locals()['offset_%d'%(i+1)][1],
                offset_Z[0]
            ]
            base_mesh_rotation = [np.pi / 2 + switch_rotation[0], 0, 0]
            self.base_mesh = Cylinder(size[1], size[0], size[0],
                                      position=base_mesh_position,
                                      rotation=base_mesh_rotation)
            vertices_list.append(self.base_mesh.vertices)
            faces_list.append(self.base_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.base_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Switch'


# Source: Switch/concept_template.py
class FlipX_Switch(ConceptTemplate):
    def __init__(self, number_of_switch, size, switch_rotation, separation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        switch_rotation = [x / 180 * np.pi for x in switch_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.number_of_switch = number_of_switch
        self.size = size
        self.separation = separation
        self.switch_rotation = switch_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(number_of_switch[0]):
            mesh_position = [
                (separation[0] + size[0]) * i, 
                0, 
                0
            ]
            mesh_rotation = [switch_rotation[0], 0, 0]
            self.mesh = Cuboid(size[1], size[0], size[2],
                               position=mesh_position,
                               rotation=mesh_rotation)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Switch'


# Source: Switch/concept_template.py
class FlipY_Switch(ConceptTemplate):
    def __init__(self, number_of_switch, size, switch_rotation, separation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        switch_rotation = [x / 180 * np.pi for x in switch_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.number_of_switch = number_of_switch
        self.size = size
        self.separation = separation
        self.switch_rotation = switch_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(number_of_switch[0]):
            mesh_position = [
                (separation[0] + size[0]) * i, 
                0, 
                0
            ]
            mesh_rotation = [0, switch_rotation[0], 0]
            self.mesh = Cuboid(size[1], size[0], size[2],
                               position=mesh_position,
                               rotation=mesh_rotation)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Switch'


# Source: Switch/concept_template.py
class Lever_Switch(ConceptTemplate):
    def __init__(self, number_of_switch, base_size, main_size, inter_offset, switch_rotation, separation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        switch_rotation = [x / 180 * np.pi for x in switch_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.number_of_switch = number_of_switch
        self.base_size = base_size
        self.main_size = main_size
        self.inter_offset = inter_offset
        self.switch_rotation = switch_rotation
        self.separation = separation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(number_of_switch[0]):
            base_mesh_position = [
                (separation[0] + main_size[0]) * i,
                0,
                base_size[1] / 2,
            ]
            base_mesh_rotation = [np.pi / 2, 0, 0]
            self.base_mesh = Cylinder(base_size[1], base_size[0], base_size[0],
                                      position=base_mesh_position,
                                      rotation=base_mesh_rotation)
            vertices_list.append(self.base_mesh.vertices)
            faces_list.append(self.base_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.base_mesh.vertices)

            main_mesh_position = [
                (separation[0] + main_size[0]) * i,
                0,
                main_size[2] / 2,
            ]
            main_mesh_rotation = [np.pi / 2, 0, 0]
            self.main_mesh = Cylinder(main_size[2], main_size[1], main_size[0],
                                      position=main_mesh_position,
                                      rotation=main_mesh_rotation)
            self.main_mesh.vertices = apply_transformation(
                self.main_mesh.vertices,
                position=[0, 0, 0],
                rotation=[switch_rotation[0], 0, 0],
            )
            self.main_mesh.vertices = apply_transformation(
                self.main_mesh.vertices,
                position=[
                    inter_offset[0],
                    inter_offset[1],
                    inter_offset[2] + base_size[1],
                ],
                rotation=[0, 0, 0],
            )
            vertices_list.append(self.main_mesh.vertices)
            faces_list.append(self.main_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.main_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Switch'


# Source: Faucet/concept_template.py
class SimplifiedZ_Switch(ConceptTemplate):
    def __init__(self, number_of_switch, size, offset_0_x, offset_1_x, offset_yz, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.number_of_switch = number_of_switch
        self.size = size
        self.offset_0_x = offset_0_x
        self.offset_1_x = offset_1_x
        self.offset_yz = offset_yz
        self.offsets = [
            [offset_0_x[0], offset_yz[0], offset_yz[1]],
            [offset_1_x[0], offset_yz[0], offset_yz[1]],
        ][0 : number_of_switch[0]]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for offset in self.offsets:
            tmp_mesh_rotation = [np.pi / 2, 0, 0]
            tmp_mesh = Cylinder(size[1], size[0], size[0],
                                position=offset,
                                rotation=tmp_mesh_rotation)
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Switch'


# Source: Faucet/concept_template.py
class Knob_Switch(ConceptTemplate):
    def __init__(self, number_of_switch, number_of_cylinder, size_0, size_1, size_2, offset, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.number_of_switch = number_of_switch
        self.number_of_cylinder = number_of_cylinder
        self.size_0 = size_0
        self.size_1 = size_1
        self.size_2 = size_2
        self.offset = offset
        self.sizes = [size_0, size_1, size_2]
        self.offsets = [
            [
                [offset[0], offset[2] + size_0[1] / 2, offset[3]],
                [
                    offset[0],
                    offset[2] + size_0[1] + size_1[1] / 2,
                    offset[3],
                ],
                [
                    offset[0],
                    offset[2] + size_0[1] + size_1[1] + size_2[1] / 2,
                    offset[3],
                ],
            ][0 : number_of_cylinder[0]],
            [
                [offset[1], offset[2] + size_0[1] / 2, offset[3]],
                [
                    offset[1],
                    offset[2] + size_0[1] + size_1[1] / 2,
                    offset[3],
                ],
                [
                    offset[1],
                    offset[2] + size_0[1] + size_1[1] + size_2[1] / 2,
                    offset[3],
                ],
            ][0 : number_of_cylinder[0]],
        ][0 : number_of_switch[0]]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for offset in self.offsets:
            for i in range(number_of_cylinder[0]):
                size = self.sizes[i]
                tmp_mesh = Cylinder(size[1], size[0], size[0],
                                    position=offset[i])
                vertices_list.append(tmp_mesh.vertices)
                faces_list.append(tmp_mesh.faces + total_num_vertices)
                total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Switch'


# Source: Faucet/concept_template.py
class HandleY_Switch(ConceptTemplate):
    def __init__(self, number_of_switch, number_of_cube, bottom_size, middle_size, top_size, bottom_middle_offset, bottom_top_offset, offset_0_x, offset_1_x, offset_yz, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.number_of_switch = number_of_switch
        self.number_of_cube = number_of_cube
        self.bottom_size = bottom_size
        self.middle_size = middle_size
        self.top_size = top_size
        self.bottom_middle_offset = bottom_middle_offset
        self.bottom_top_offset = bottom_top_offset
        self.offset_0_x = offset_0_x
        self.offset_1_x = offset_1_x
        self.offset_yz = offset_yz
        self.sizes = [bottom_size, middle_size, top_size]
        self.offsets = [
            [
                [offset_0_x[0], offset_yz[0] + bottom_size[1] / 2, offset_yz[1]],
                [
                    offset_0_x[0] + bottom_middle_offset[0],
                    offset_yz[0] + bottom_size[1] + middle_size[1] / 2,
                    offset_yz[1] + bottom_middle_offset[1],
                ],
                [
                    offset_0_x[0] + bottom_top_offset[0],
                    offset_yz[0] + bottom_size[1] + middle_size[1] + top_size[1] / 2,
                    offset_yz[1] + bottom_top_offset[1],
                ],
            ][0 : number_of_cube[0]],
            [
                [offset_1_x[0], offset_yz[0] + bottom_size[1] / 2, offset_yz[1]],
                [
                    offset_1_x[0] - bottom_middle_offset[0],
                    offset_yz[0] + bottom_size[1] + middle_size[1] / 2,
                    offset_yz[1] + bottom_middle_offset[1],
                ],
                [
                    offset_1_x[0] - bottom_top_offset[0],
                    offset_yz[0] + bottom_size[1] + middle_size[1] + top_size[1] / 2,
                    offset_yz[1] + bottom_top_offset[1],
                ],
            ][0 : number_of_cube[0]],
        ][0 : number_of_switch[0]]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for offset in self.offsets:
            for i in range(number_of_cube[0]):
                size = self.sizes[i]
                tmp_mesh = Cuboid(size[1], size[0], size[2],
                                  position=offset[i])
                vertices_list.append(tmp_mesh.vertices)
                faces_list.append(tmp_mesh.faces + total_num_vertices)
                total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Switch'


# Source: Faucet/concept_template.py
class HandleZ_Switch(ConceptTemplate):
    def __init__(self, number_of_switch, number_of_cube, bottom_size, middle_size, top_size, bottom_middle_offset, bottom_top_offset, offset_0_x, offset_1_x, offset_yz, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.number_of_switch = number_of_switch
        self.number_of_cube = number_of_cube
        self.bottom_size = bottom_size
        self.middle_size = middle_size
        self.top_size = top_size
        self.bottom_middle_offset = bottom_middle_offset
        self.bottom_top_offset = bottom_top_offset
        self.offset_0_x = offset_0_x
        self.offset_1_x = offset_1_x
        self.offset_yz = offset_yz
        self.sizes = [bottom_size, middle_size, top_size]
        self.offsets = [
            [
                [offset_0_x[0], offset_yz[0], offset_yz[1] + bottom_size[2] / 2],
                [
                    offset_0_x[0] + bottom_middle_offset[0],
                    offset_yz[0] + bottom_middle_offset[1],
                    offset_yz[1] + bottom_size[2] + middle_size[2] / 2,
                ],
                [
                    offset_0_x[0] + bottom_top_offset[0],
                    offset_yz[0] + bottom_top_offset[1],
                    offset_yz[1] + bottom_size[2] + middle_size[2] + top_size[2] / 2,
                ],
            ][0 : number_of_cube[0]],
            [
                [offset_1_x[0], offset_yz[0], offset_yz[1] + bottom_size[2] / 2],
                [
                    offset_1_x[0] - bottom_middle_offset[0],
                    offset_yz[0] + bottom_middle_offset[1],
                    offset_yz[1] + bottom_size[2] + middle_size[2] / 2,
                ],
                [
                    offset_1_x[0] - bottom_top_offset[0],
                    offset_yz[0] + bottom_top_offset[1],
                    offset_yz[1] + bottom_size[2] + middle_size[2] + top_size[2] / 2,
                ],
            ][0 : number_of_cube[0]],
        ][0 : number_of_switch[0]]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for offset in self.offsets:
            for i in range(number_of_cube[0]):
                size = self.sizes[i]
                tmp_mesh = Cuboid(size[1], size[0], size[2],
                                  position=offset[i],
                                  rotation=[0, 0, 0])
                vertices_list.append(tmp_mesh.vertices)
                faces_list.append(tmp_mesh.faces + total_num_vertices)
                total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Switch'


# Source: Faucet/concept_template.py
class RegularY_Switch(ConceptTemplate):
    def __init__(self, size, sub_size, sub_offset, rotation_Y, rotation_X, sub_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        rotation_X = [-x / 180 * np.pi for x in rotation_X]
        rotation_Y = [-x / 180 * np.pi for x in rotation_Y]
        sub_rotation = [-x / 180 * np.pi for x in sub_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.sub_size = sub_size
        self.sub_offset = sub_offset
        self.sub_rotation = sub_rotation
        self.rotation_Y = rotation_Y
        self.rotation_X = rotation_X

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        distance_to_center = (size[0] ** 2 - sub_size[0] ** 2) ** 0.5

        sub_mesh_position = [0, 0, sub_size[1] / 2 + sub_offset[1]]
        sub_mesh_rotation = [np.pi / 2, 0, 0]
        self.sub_mesh = Cylinder(sub_size[1], sub_size[0], sub_size[0],
                                 position=sub_mesh_position,
                                 rotation=sub_mesh_rotation)
        self.sub_mesh.vertices = apply_transformation(
            self.sub_mesh.vertices,
            [
                0,
                sub_offset[0],
                distance_to_center,
            ],
            [sub_rotation[0], 0, 0],
        )
        self.sub_mesh.vertices = apply_transformation(
            self.sub_mesh.vertices,
            [0, size[1] / 2, 0],
            [rotation_X[0], rotation_Y[0], 0],
        )
        vertices_list.append(self.sub_mesh.vertices)
        faces_list.append(self.sub_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.sub_mesh.vertices) 

        self.main_mesh = Cylinder(size[1], size[0], size[0])
        self.main_mesh.vertices = apply_transformation(
            self.main_mesh.vertices,
            [0, size[1] / 2, 0],
            [rotation_X[0], rotation_Y[0], 0],
        )
        vertices_list.append(self.main_mesh.vertices)
        faces_list.append(self.main_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.main_mesh.vertices) 

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Switch'


# Source: Faucet/concept_template.py
class RegularX_Switch(ConceptTemplate):
    def __init__(self, size, sub_size, sub_offset, rotation_Z, rotation_X, sub_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        rotation_X = [-x / 180 * np.pi for x in rotation_X]
        rotation_Z = [-x / 180 * np.pi for x in rotation_Z]
        sub_rotation = [-x / 180 * np.pi for x in sub_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.sub_size = sub_size
        self.sub_offset = sub_offset
        self.sub_rotation = sub_rotation
        self.rotation_Z = rotation_Z
        self.rotation_X = rotation_X

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        distance_to_center = (size[0] ** 2 - sub_size[0] ** 2) ** 0.5

        sub_mesh_position = [0, sub_size[1] / 2 + sub_offset[1], 0]
        self.sub_mesh = Cylinder(sub_size[1], sub_size[0], sub_size[0],
                                 position=sub_mesh_position)
        self.sub_mesh.vertices = apply_transformation(
            self.sub_mesh.vertices,
            [
                sub_offset[0],
                distance_to_center,
                0,
            ],
            [0, 0, sub_rotation[0]],
        )
        self.sub_mesh.vertices = apply_transformation(
            self.sub_mesh.vertices,
            [size[1] / 2, 0, 0],
            [rotation_X[0], 0, rotation_Z[0]],
        )
        vertices_list.append(self.sub_mesh.vertices)
        faces_list.append(self.sub_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.sub_mesh.vertices)

        main_mesh_rotation = [0, 0, np.pi / 2]
        self.main_mesh = Cylinder(size[1], size[0], size[0],
                                  rotation=main_mesh_rotation)
        self.main_mesh.vertices = apply_transformation(
            self.main_mesh.vertices,
            [size[1] / 2, 0, 0],
            [rotation_X[0], 0, rotation_Z[0]],
        )
        vertices_list.append(self.main_mesh.vertices)
        faces_list.append(self.main_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.main_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Switch'


# Source: Faucet/concept_template.py
class RegularZ_Switch(ConceptTemplate):
    def __init__(self, size, sub_size, sub_offset, rotation_Z, rotation_X, sub_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        rotation_X = [x / 180 * np.pi for x in rotation_X]
        rotation_Z = [x / 180 * np.pi for x in rotation_Z]
        sub_rotation = [x / 180 * np.pi for x in sub_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.sub_size = sub_size
        self.sub_offset = sub_offset
        self.sub_rotation = sub_rotation
        self.rotation_Z = rotation_Z
        self.rotation_X = rotation_X

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        distance_to_center = (size[0] ** 2 - sub_size[0] ** 2) ** 0.5

        sub_mesh_position = [0, sub_size[1] / 2 + sub_offset[1], 0]
        self.sub_mesh = Cylinder(sub_size[1], sub_size[0], sub_size[0],
                                 position=sub_mesh_position)
        self.sub_mesh.vertices = apply_transformation(
            self.sub_mesh.vertices,
            [
                0,
                distance_to_center,
                sub_offset[0],
            ],
            [sub_rotation[0], 0, 0],
        )
        self.sub_mesh.vertices = apply_transformation(
            self.sub_mesh.vertices,
            [0, 0, size[1] / 2],
            [rotation_X[0], 0, rotation_Z[0]],
        )
        vertices_list.append(self.sub_mesh.vertices)
        faces_list.append(self.sub_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.sub_mesh.vertices)

        main_mesh_rotation = [np.pi / 2, 0, 0]
        self.main_mesh = Cylinder(size[1], size[0], size[0],
                                  rotation=main_mesh_rotation)
        self.main_mesh.vertices = apply_transformation(
            self.main_mesh.vertices,
            [0, 0, size[1] / 2],
            [rotation_X[0], 0, rotation_Z[0]],
        )
        vertices_list.append(self.main_mesh.vertices)
        faces_list.append(self.main_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.main_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Switch'


# Source: Faucet/concept_template.py
class TShaped_Switch(ConceptTemplate):
    def __init__(self, size_1, size_2, size_3, sub_offset, switch_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        switch_rotation = [x / 180 * np.pi for x in switch_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size_1 = size_1
        self.size_2 = size_2
        self.size_3 = size_3
        self.sub_offset = sub_offset
        self.switch_rotation = switch_rotation
        self.sizes = [size_1, size_2, size_3]
        self.offsets = [
            [0, size_1[1] / 2, 0],
            [0, size_1[1] + size_2[1] / 2, 0],
            [0, size_1[1] + size_2[1] + size_3[1] / 2, sub_offset[0]],
        ]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        size = self.sizes[0]
        self.tmp_mesh = Cylinder(size[1], size[0], size[0],
                                 position=self.offsets[0])
        vertices_list.append(self.tmp_mesh.vertices)
        faces_list.append(self.tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.tmp_mesh.vertices)

        size = self.sizes[1]
        self.tmp_mesh = Cylinder(size[1], size[0], size[0],
                                 position=self.offsets[1])
        vertices_list.append(self.tmp_mesh.vertices)
        faces_list.append(self.tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.tmp_mesh.vertices)

        size = self.sizes[2]
        self.tmp_mesh = Cuboid(size[1], size[0], size[2],
                               position=self.offsets[2])
        self.tmp_mesh.vertices = apply_transformation(self.tmp_mesh.vertices, [0, 0, 0], [0, switch_rotation[0], 0])
        vertices_list.append(self.tmp_mesh.vertices)
        faces_list.append(self.tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Switch'


# Source: Faucet/concept_template.py
class Lever_Switch(ConceptTemplate):
    def __init__(self, size, R, position0, position1, position2, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.R = R
        self.size = size
        position1 = [position0[i] + position1[i] for i in range(3)]
        position2 = [position1[i] + position2[i] for i in range(3)]
        self.positions = [position0, position1, position2]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        start_ends = [
            [position0, position1],
            [position1, position2],
        ]

        for start_end in start_ends:
            vector = np.array(start_end[1]) - np.array(start_end[0])
            for i in range(3):
                if vector[i] <= 0.00001:
                    vector[i] += 0.00001
            length = np.linalg.norm(vector)

            tmp_mesh_position = [0, length / 2, 0]
            tmp_mesh = Cylinder(length, R[0], R[0],
                                position=tmp_mesh_position)
            tmp_mesh.vertices = apply_transformation(
                tmp_mesh.vertices,
                position=[
                    start_end[0][0],
                    start_end[0][1] + size[1],
                    start_end[0][2] + size[0],
                ],
                rotation=[
                    np.arccos(vector[1] / length),
                    np.arctan(vector[0] / vector[2]),
                    0,
                ],
            )
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)


        tmp_mesh_position = [0, size[1] / 2, 0]
        tmp_mesh = Cylinder(size[1], size[0], size[0],
                            position=tmp_mesh_position)
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)
        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Switch'


# Source: Faucet/concept_template.py
class Cuboidal_Switch(ConceptTemplate):
    def __init__(self, size, sub_size, sub_offset, switch_rotation, sub_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        sub_rotation = [x / 180 * np.pi for x in sub_rotation]
        switch_rotation = [x / 180 * np.pi for x in switch_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size
        self.sub_size = sub_size
        self.sub_offset = sub_offset
        self.switch_rotation = switch_rotation
        self.sub_rotation = sub_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        offset_z = sub_size[2] / 2 + sub_offset[1]
        sin_sub = np.sin(sub_rotation[0])
        cos_sub = np.cos(sub_rotation[0])

        sub_mesh_position = [
            0,
            offset_z * np.sin(sub_rotation[0]) + sub_offset[0] + size[1] / 2 - sub_size[1] / 2 * np.cos(sub_rotation[0]),
            offset_z * np.cos(sub_rotation[0]),
        ]
        sub_mesh_rotation = [-sub_rotation[0], 0, 0]
        self.sub_mesh = Cuboid(sub_size[1], sub_size[0], sub_size[2],
                               position=sub_mesh_position,
                               rotation=sub_mesh_rotation)
        self.sub_mesh.vertices = apply_transformation(
            self.sub_mesh.vertices,
            [0, size[1] / 2, 0],
            [0, -switch_rotation[0], 0],
        )
        vertices_list.append(self.sub_mesh.vertices)
        faces_list.append(self.sub_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.sub_mesh.vertices)

        main_mesh_position = [0, size[1] / 2, 0]
        main_mesh_rotation = [0, -switch_rotation[0], 0]
        self.main_mesh = Cuboid(size[1], size[0], size[2],
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

        self.semantic = 'Switch'


# Source: Faucet/concept_template.py
class RotaryX_Switch(ConceptTemplate):
    def __init__(self, main_size_1, main_size_2, offset_x, sub_size, sub_offset, tilt_angle, rotation0, rotation1, existence_of_switch, number_of_sub, interval, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation0 = [x / 180 * np.pi for x in rotation0]
        rotation1 = [x / 180 * np.pi for x in rotation1]
        rotation = [x / 180 * np.pi for x in rotation]
        tilt_angle = [x / 180 * np.pi for x in tilt_angle]
        super().__init__(position, rotation)

        # Record Parameters
        self.main_size_1 = main_size_1
        self.main_size_2 = main_size_2
        self.offset_x = offset_x
        self.sub_size = sub_size
        self.sub_offset = sub_offset
        self.tilt_angle = tilt_angle
        self.rotation0 = rotation0
        self.rotation1 = rotation1
        self.existence_of_switch = existence_of_switch
        self.number_of_sub = number_of_sub
        self.interval = interval
        rotations = [rotation0[0], rotation1[0]]
        existences = [existence_of_switch[0] * -1, existence_of_switch[1]]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        j = 0
        for existence in existences:
            if existence == 0:
                j += 1
                continue

            tmp_mesh_position = [
                offset_x[j] + existence * (interval / 2 + main_size_1[1] / 2),
                0,
                0,
            ]
            tmp_mesh_rotation = [0, 0, np.pi / 2]
            tmp_mesh = Cylinder(main_size_1[1], main_size_1[0], main_size_1[0],
                                position=tmp_mesh_position,
                                rotation=tmp_mesh_rotation)
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

            tmp_mesh_position = [
                offset_x[j] + existence * (interval / 2 + main_size_1[1] + main_size_2[1] / 2),
                0,
                0,
            ]
            tmp_mesh_rotation = [0, 0, np.pi / 2]
            tmp_mesh = Cylinder(main_size_2[1], main_size_2[0], main_size_2[0],
                                position=tmp_mesh_position,
                                rotation=tmp_mesh_rotation)
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

            for i in range(number_of_sub[0]):
                tmp_mesh_position = [0, np.cos(tilt_angle[0]) * sub_size[1] / 2, 0]
                tmp_mesh_rotation = [0, 0, -tilt_angle[0]]
                tmp_mesh = Cuboid(sub_size[1], sub_size[0], sub_size[2],
                                  position=tmp_mesh_position,
                                  rotation=tmp_mesh_rotation)
                tmp_mesh.vertices = apply_transformation(
                    tmp_mesh.vertices,
                    [
                        offset_x[j] + existence * (main_size_1[1] + main_size_2[1] - sub_size[0] / 2 + sub_offset[0] + interval / 2),
                        0,
                        0,
                    ],
                    [rotations[j] + np.pi * 2 * i / number_of_sub[0], 0, 0],
                )
                vertices_list.append(tmp_mesh.vertices)
                faces_list.append(tmp_mesh.faces + total_num_vertices)
                total_num_vertices += len(tmp_mesh.vertices)
            j += 1

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Switch'


# Source: Faucet/concept_template.py
class RotaryY_Switch(ConceptTemplate):
    def __init__(self, main_size_1, main_size_2, offset_x, sub_size, sub_offset, tilt_angle, rotation0, rotation1, number_of_switch, number_of_sub, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation0 = [x / 180 * np.pi for x in rotation0]
        rotation1 = [x / 180 * np.pi for x in rotation1]
        rotation = [x / 180 * np.pi for x in rotation]
        tilt_angle = [x / 180 * np.pi for x in tilt_angle]
        super().__init__(position, rotation)

        # Record Parameters
        self.main_size_1 = main_size_1
        self.main_size_2 = main_size_2
        self.offset_x = offset_x
        self.sub_size = sub_size
        self.sub_offset = sub_offset
        self.tilt_angle = tilt_angle
        self.rotation0 = rotation0
        self.rotation1 = rotation1
        self.number_of_switch = number_of_switch
        self.number_of_sub = number_of_sub
        rotations = [rotation0[0], rotation1[0]]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for j in range(number_of_switch[0]):
            tmp_mesh_position = [
                offset_x[j],
                main_size_1[1] / 2,
                0,
            ]
            tmp_mesh = Cylinder(main_size_1[1], main_size_1[0], main_size_1[0],
                                position=tmp_mesh_position)
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

            tmp_mesh_position = [
                offset_x[j],
                main_size_1[1] + main_size_2[1] / 2,
                0,
            ]
            tmp_mesh = Cylinder(main_size_2[1], main_size_2[0], main_size_2[0],
                                position=tmp_mesh_position)
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

            for i in range(number_of_sub[0]):
                tmp_mesh_position = [0, 0, np.cos(tilt_angle[0]) * sub_size[2] / 2]
                tmp_mesh_rotation = [-tilt_angle[0], 0, 0]

                tmp_mesh = Cuboid(sub_size[1], sub_size[0], sub_size[2],
                                  position=tmp_mesh_position,
                                  rotation=tmp_mesh_rotation)
                tmp_mesh.vertices = apply_transformation(
                    tmp_mesh.vertices,
                    [
                        offset_x[j],
                        main_size_1[1] + main_size_2[1] - sub_size[1] / 2 + sub_offset[0],
                        0,
                    ],
                    [0, rotations[j] + np.pi * 2 * i / number_of_sub[0], 0],
                )
                vertices_list.append(tmp_mesh.vertices)
                faces_list.append(tmp_mesh.faces + total_num_vertices)
                total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Switch'


# Source: Faucet/concept_template.py
class RotaryZ_Switch(ConceptTemplate):
    def __init__(self, main_size_1, main_size_2, offset_x, sub_size, sub_offset, tilt_angle, rotation0, rotation1, number_of_switch, number_of_sub, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation0 = [x / 180 * np.pi for x in rotation0]
        rotation1 = [x / 180 * np.pi for x in rotation1]
        rotation = [x / 180 * np.pi for x in rotation]
        tilt_angle = [x / 180 * np.pi for x in tilt_angle]
        super().__init__(position, rotation)

        # Record Parameters
        self.main_size_1 = main_size_1
        self.main_size_2 = main_size_2
        self.offset_x = offset_x
        self.sub_size = sub_size
        self.sub_offset = sub_offset
        self.tilt_angle = tilt_angle
        self.rotation0 = rotation0
        self.rotation1 = rotation1
        self.number_of_switch = number_of_switch
        self.number_of_sub = number_of_sub
        rotations = [rotation0[0], rotation1[0]]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for j in range(number_of_switch[0]):
            tmp_mesh_position = [
                offset_x[j],
                0,
                main_size_1[1] / 2,
            ]
            tmp_mesh_rotation = [np.pi / 2, 0, 0]
            tmp_mesh = Cylinder(main_size_1[1], main_size_1[0], main_size_1[0],
                                position=tmp_mesh_position,
                                rotation=tmp_mesh_rotation)
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

            tmp_mesh_position = [
                offset_x[j],
                0,
                main_size_1[1] + main_size_2[1] / 2,
            ]
            tmp_mesh_rotation = [np.pi / 2, 0, 0]
            tmp_mesh = Cylinder(main_size_2[1], main_size_2[0], main_size_2[0],
                                position=tmp_mesh_position,
                                rotation=tmp_mesh_rotation)
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

            for i in range(number_of_sub[0]):
                tmp_mesh_position = [np.cos(tilt_angle[0]) * sub_size[0] / 2, 0, 0]
                tmp_mesh_rotation = [0, -tilt_angle[0], 0]
                tmp_mesh = Cuboid(sub_size[1], sub_size[0], sub_size[2],
                                  position=tmp_mesh_position,
                                  rotation=tmp_mesh_rotation)
                tmp_mesh.vertices = apply_transformation(
                    tmp_mesh.vertices,
                    [
                        offset_x[j],
                        0,
                        main_size_1[1] + main_size_2[1] - sub_size[2] / 2 + sub_offset[0],
                    ],
                    [0, 0, rotations[j] + np.pi * 2 * i / number_of_sub[0]],
                )
                vertices_list.append(tmp_mesh.vertices)
                faces_list.append(tmp_mesh.faces + total_num_vertices)
                total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)


        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Switch'
