"""
Spout Templates
Automatically extracted from concept_template.py files
Contains 8 class(es)
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


# Source: Kettle/concept_template.py
class Straight_Spout(ConceptTemplate):
    def __init__(self, num_of_sub_spouts, spout_1_radius, spout_1_thinkness, spout_1_length, spout_1_generatrix_offset, spout_1_rotation, spout_2_radius, spout_2_thinkness, spout_2_length, spout_2_generatrix_offset, spout_2_rotation, spout_3_radius, spout_3_thinkness, spout_3_length, spout_3_generatrix_offset, spout_3_rotation, spout_4_radius, spout_4_thinkness, spout_4_length, spout_4_generatrix_offset, spout_4_rotation, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        spout_1_rotation = [x / 180 * np.pi for x in spout_1_rotation]
        spout_2_rotation = [x / 180 * np.pi for x in spout_2_rotation]
        spout_3_rotation = [x / 180 * np.pi for x in spout_3_rotation]
        spout_4_rotation = [x / 180 * np.pi for x in spout_4_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.num_of_sub_spouts = num_of_sub_spouts
        self.spout_1_radius = spout_1_radius
        self.spout_1_thinkness = spout_1_thinkness
        self.spout_1_length = spout_1_length
        self.spout_1_generatrix_offset = spout_1_generatrix_offset
        self.spout_1_rotation = spout_1_rotation
        self.spout_2_radius = spout_2_radius
        self.spout_2_thinkness = spout_2_thinkness
        self.spout_2_length = spout_2_length
        self.spout_2_generatrix_offset = spout_2_generatrix_offset
        self.spout_2_rotation = spout_2_rotation
        self.spout_3_radius = spout_3_radius
        self.spout_3_thinkness = spout_3_thinkness
        self.spout_3_length = spout_3_length
        self.spout_3_generatrix_offset = spout_3_generatrix_offset
        self.spout_3_rotation = spout_3_rotation
        self.spout_4_radius = spout_4_radius
        self.spout_4_thinkness = spout_4_thinkness
        self.spout_4_length = spout_4_length
        self.spout_4_generatrix_offset = spout_4_generatrix_offset
        self.spout_4_rotation = spout_4_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        total_delta_y = -(spout_1_length[0] + spout_1_length[1]) / 4 * np.sin(spout_1_rotation[0])
        total_delta_z = -(spout_1_length[0] + spout_1_length[1]) / 4 * np.cos(spout_1_rotation[0])

        for i in range(num_of_sub_spouts[0]):
            total_delta_y += (locals()['spout_%d_length'%(i+1)][0] + locals()['spout_%d_length'%(i+1)][1]) / 4 * np.sin(locals()['spout_%d_rotation'%(i+1)][0])
            total_delta_z += (locals()['spout_%d_length'%(i+1)][0] + locals()['spout_%d_length'%(i+1)][1]) / 4 * np.cos(locals()['spout_%d_rotation'%(i+1)][0])
            mesh_position = [
                0, 
                total_delta_y, 
                total_delta_z
            ]
            total_delta_y += (locals()['spout_%d_length'%(i+1)][0] + locals()['spout_%d_length'%(i+1)][1]) / 4 * np.sin(locals()['spout_%d_rotation'%(i+1)][0])
            total_delta_z += (locals()['spout_%d_length'%(i+1)][0] + locals()['spout_%d_length'%(i+1)][1]) / 4 * np.cos(locals()['spout_%d_rotation'%(i+1)][0])
            mesh_rotation = [
                np.pi / 2 - locals()['spout_%d_rotation'%(i+1)][0], 
                np.pi / 2, 
                0
            ]
            self.mesh = Ring(height = locals()['spout_%d_length'%(i+1)][0], 
                             outer_top_radius = locals()['spout_%d_radius'%(i+1)][0], 
                             inner_top_radius = locals()['spout_%d_radius'%(i+1)][0] - locals()['spout_%d_thinkness'%(i+1)][0] * 2,
                             outer_bottom_radius = locals()['spout_%d_radius'%(i+1)][1], 
                             inner_bottom_radius = locals()['spout_%d_radius'%(i+1)][1] - locals()['spout_%d_thinkness'%(i+1)][0] * 2,
                             back_height = locals()['spout_%d_length'%(i+1)][1], 
                             generatrix_offset = locals()['spout_%d_generatrix_offset'%(i+1)][0], 
                             position = mesh_position,
                             rotation = mesh_rotation,
                             rotation_order = "YXZ")
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Spout'


# Source: Kettle/concept_template.py
class Curved_Spout(ConceptTemplate):
    def __init__(self, central_radius, exist_angle, torus_radius, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        exist_angle = [x / 180 * np.pi for x in exist_angle]
        super().__init__(position, rotation)

        # Record Parameters
        self.central_radius = central_radius
        self.exist_angle = exist_angle
        self.torus_radius = torus_radius

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        top_mesh_position = [
            0, 
            central_radius[0], 
            0
            ]
        top_mesh_rotation = [0, 0, -np.pi / 2]
        self.top_mesh = Torus(central_radius[0], torus_radius[0], exist_angle[0], torus_radius[1],
                               position = top_mesh_position,
                               rotation = top_mesh_rotation)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [
            0, 
            central_radius[0] * (1 - np.cos(exist_angle[0])) - central_radius[1] * np.cos(exist_angle[0]), 
            central_radius[0] * np.sin(exist_angle[0]) + central_radius[1] * np.sin(exist_angle[0])
            ]
        bottom_mesh_rotation = [
            -exist_angle[0], 
            0, 
            np.pi / 2
        ]
        self.bottom_mesh = Torus(central_radius[1], torus_radius[1], exist_angle[1], torus_radius[2],
                                 position=bottom_mesh_position,
                                 rotation=bottom_mesh_rotation,
                                 rotation_order = "ZXY")
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Spout'


# Source: Faucet/concept_template.py
class Trifold_Spout(ConceptTemplate):
    def __init__(self, R, position0, position1, position2, position3, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.R = R
        position1 = [position0[i] + position1[i] for i in range(3)]
        position2 = [position1[i] + position2[i] for i in range(3)]
        position3 = [position2[i] + position3[i] for i in range(3)]
        self.positions = [position0, position1, position2, position3]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        start_ends = [
            [position0, position1],
            [position1, position2],
            [position2, position3],
        ]

        for start_end in start_ends:
            vector = np.array(start_end[1]) - np.array(start_end[0])
            for i in range(3):
                if vector[i] <= 0.00001:
                    vector[i] += 0.00001 # prevent the rotation vector from being 0 
            length = np.linalg.norm(vector)

            tmp_mesh_position = [0, length / 2, 0]
            tmp_mesh = Cylinder(length, R[0], R[0],
                                position=tmp_mesh_position)
            tmp_mesh.vertices = apply_transformation(
                tmp_mesh.vertices,
                start_end[0],
                [np.arccos(vector[1] / length), np.arctan(vector[0] / vector[2]), 0],
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

        self.semantic = 'Spout'


# Source: Faucet/concept_template.py
class ShowerRose_Spout(ConceptTemplate):
    def __init__(self, R, position0, position1, position2, has_showerHead, showerHead_size, showerHead_offset, showerHead_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        showerHead_rotation = [-x / 180 * np.pi for x in showerHead_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        position1 = [position0[i] + position1[i] for i in range(3)]
        position2 = [position1[i] + position2[i] for i in range(3)]
        showerHead_offset = [
            showerHead_offset[0],
            showerHead_offset[1] + position2[1],
            showerHead_offset[2] + position2[2],
        ]
        self.R = R
        self.has_showerHead = has_showerHead
        self.showerHead_size = showerHead_size
        self.showerHead_offset = showerHead_offset
        self.showerHead_rotation = showerHead_rotation
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
                start_end[0],
                [np.arccos(vector[1] / length), np.arctan(vector[0] / vector[2]), 0],
            )
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

        if has_showerHead[0]:
            rose_mesh_position = [0, -showerHead_size[2] / 2, 0]
            rose_mesh = Cylinder(showerHead_size[2], showerHead_size[1], showerHead_size[0],
                                 position=rose_mesh_position)
            rose_mesh.vertices = apply_transformation(
                rose_mesh.vertices,
                position=[
                    showerHead_offset[0],
                    showerHead_offset[1],
                    showerHead_offset[2],
                ],
                rotation=[showerHead_rotation[0], 0, 0],
            )
            vertices_list.append(rose_mesh.vertices)
            faces_list.append(rose_mesh.faces + total_num_vertices)
            total_num_vertices += len(rose_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Spout'


# Source: Faucet/concept_template.py
class Quadfold_Spout(ConceptTemplate):
    def __init__(self, R, position0, position1, position2, position3, position4, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.R = R
        position1 = [position0[i] + position1[i] for i in range(3)]
        position2 = [position1[i] + position2[i] for i in range(3)]
        position3 = [position2[i] + position3[i] for i in range(3)]
        position4 = [position3[i] + position4[i] for i in range(3)]
        self.positions = [position0, position1, position2, position3, position4]

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        start_ends = [
            [position0, position1],
            [position1, position2],
            [position2, position3],
            [position3, position4],
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
            tmp_rotation = [
                np.arccos(vector[1] / length),
                np.arctan(vector[0] / vector[2]),
                0,
            ]
            if vector[2] <= 0:
                tmp_rotation[0] *= -1
            tmp_mesh.vertices = apply_transformation(
                tmp_mesh.vertices,
                start_end[0],
                tmp_rotation,
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

        self.semantic = 'Spout'


# Source: Faucet/concept_template.py
class Curved_Spout(ConceptTemplate):
    def __init__(self, R, L, bottom0, bottom1, center, spout_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        spout_rotation = [x / 180 * np.pi for x in spout_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.R = R
        self.L = L
        self.bottom0 = bottom0
        self.bottom1 = bottom1
        self.center = center
        self.spout_rotation = spout_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        vector = np.array(bottom1)
        for i in range(3):
            if vector[i] <= 0.00001:
                vector[i] += 0.00001
        length = np.linalg.norm(vector)

        tmp_mesh_position = [0, length / 2, 0]
        tmp_mesh = Cylinder(length, R[0], R[0],
                            position=tmp_mesh_position)
        tmp_mesh.vertices = apply_transformation(
            tmp_mesh.vertices,
            bottom0,
            [np.arccos(vector[1] / length), np.arctan(vector[0] / vector[2]), 0],
        )
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        r = np.sqrt(center[0] ** 2 + center[1] ** 2 + center[2] ** 2)
        r_in_xz = np.sqrt(center[0] ** 2 + center[2] ** 2)
        center_angle = np.arctan(-center[1] / r_in_xz)
        end_length = r * L[0] * (spout_rotation[0] + center_angle)
        torus_mesh_rotation = [
            -np.pi / 2, 
            np.arctan(center[0] / center[2]), 
            np.pi / 2
        ]
        self.torus_mesh = Torus(r, R[0],
                                exist_angle=center_angle + spout_rotation[0],
                                rotation=torus_mesh_rotation,
                                rotation_order="ZXY")
        lxz = np.sqrt(center[2] ** 2 + center[0] ** 2)
        self.torus_mesh.vertices = np.matmul(
            self.torus_mesh.vertices,
            get_rodrigues_matrix(
                [center[2] / lxz, 0, -center[0] / lxz],
                -np.arctan(center[1] / (center[2] / np.cos(np.arctan(center[0] / center[2])))),
            ).T,
        )

        self.torus_mesh.vertices += (np.array(bottom0) + np.array(bottom1) + np.array(center))
        vertices_list.append(self.torus_mesh.vertices)
        faces_list.append(self.torus_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.torus_mesh.vertices)

        end_mesh_position = [0, end_length / 2, 0]
        self.end_mesh = Cylinder(end_length, R[0], R[0],
                                 position=end_mesh_position)
        self.end_mesh.vertices = apply_transformation(self.end_mesh.vertices, [0, 0, 0], [0, np.arctan(center[0] / center[2]), 0])
        self.end_mesh.vertices = np.matmul(
            self.end_mesh.vertices,
            get_rodrigues_matrix(
                [center[2] / lxz, 0, -center[0] / lxz],
                -np.arctan(center[1] / (center[2] / np.cos(np.arctan(center[0] / center[2])))),
            ).T,
        )
        self.end_mesh.vertices += np.array(bottom0) + np.array(bottom1)
        self.end_mesh.vertices -= (np.array(bottom0) + np.array(bottom1) + np.array(center))
        self.end_mesh.vertices = np.matmul(
            self.end_mesh.vertices,
            get_rodrigues_matrix(
                [center[2] / lxz, 0, -center[0] / lxz],
                center_angle + spout_rotation[0],
            ).T,
        )
        self.end_mesh.vertices += (np.array(bottom0) + np.array(bottom1) + np.array(center))
        vertices_list.append(self.end_mesh.vertices)
        faces_list.append(self.end_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.end_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Spout'


# Source: Faucet/concept_template.py
class Cuboidal_Spout(ConceptTemplate):
    def __init__(self, main_part_size, head_size, head_offset, rotation_mainpart, rotation_head, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        rotation_head = [x / 180 * np.pi for x in rotation_head]
        rotation_mainpart = [-x / 180 * np.pi for x in rotation_mainpart]
        super().__init__(position, rotation)

        # Record Parameters
        self.main_part_size = main_part_size
        self.head_size = head_size
        self.head_offset = head_offset
        self.rotation_mainpart = rotation_mainpart
        self.rotation_head = rotation_head

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        head_mesh_position = [0, -head_size[1] / 2, 0]
        self.head_mesh = Cylinder(head_size[1], head_size[0], head_size[0],
                                  position=head_mesh_position)
        self.head_mesh.vertices = apply_transformation(
            self.head_mesh.vertices,
            [
                head_offset[0],
                head_offset[1],
                head_offset[2] + main_part_size[2] - head_size[0],
            ],
            [rotation_head[0], 0, 0],
        )
        self.head_mesh.vertices = apply_transformation(
            self.head_mesh.vertices,
            [0, 0, 0],
            [rotation_mainpart[0], 0, 0],
        )
        vertices_list.append(self.head_mesh.vertices)
        faces_list.append(self.head_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.head_mesh.vertices)

        main_mesh_position = [0, main_part_size[1] / 2, main_part_size[2] / 2]
        self.main_mesh = Cuboid(main_part_size[1], main_part_size[0], main_part_size[2],
                                position=main_mesh_position)
        self.main_mesh.vertices = apply_transformation(
            self.main_mesh.vertices,
            [0, 0, 0],
            [rotation_mainpart[0], 0, 0],
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

        self.semantic = 'Spout'


# Source: Faucet/concept_template.py
class Cylindrical_Spout(ConceptTemplate):
    def __init__(self, main_part_size, head_size, head_offset, rotation_mainpart, rotation_head, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        rotation_head = [x / 180 * np.pi for x in rotation_head]
        rotation_mainpart = [-x / 180 * np.pi for x in rotation_mainpart]
        super().__init__(position, rotation)

        # Record Parameters
        self.main_part_size = main_part_size
        self.head_size = head_size
        self.head_offset = head_offset
        self.rotation_mainpart = rotation_mainpart
        self.rotation_head = rotation_head

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        head_mesh_position = [0, -head_size[1] / 2, 0]
        self.head_mesh = Cylinder(head_size[1],head_size[0],head_size[0],
                                  position=head_mesh_position)
        self.head_mesh.vertices = apply_transformation(
            self.head_mesh.vertices,
            [
                head_offset[0],
                -head_offset[1],
                head_offset[2] + main_part_size[1] - head_size[0],
            ],
            [rotation_head[0], 0, 0],
        )
        self.head_mesh.vertices = apply_transformation(
            self.head_mesh.vertices,
            [0, 0, 0],
            [rotation_mainpart[0], 0, 0],
        )
        vertices_list.append(self.head_mesh.vertices)
        faces_list.append(self.head_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.head_mesh.vertices)

        main_mesh_position = [0, main_part_size[0], main_part_size[1] / 2]
        main_mesh_rotation = [np.pi / 2, 0, 0]
        self.main_mesh = Cylinder(main_part_size[1], main_part_size[0], main_part_size[0],
                                  position=main_mesh_position,
                                  rotation=main_mesh_rotation)
        self.main_mesh.vertices = apply_transformation(
            self.main_mesh.vertices,
            [0, 0, 0],
            [rotation_mainpart[0], 0, 0],
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

        self.semantic = 'Spout'
