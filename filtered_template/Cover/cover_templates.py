"""
Cover Templates
Automatically extracted from concept_template.py files
Contains 19 class(es)
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


# Source: Box/concept_template.py
class Fourfold_Cover(ConceptTemplate):
    def __init__(self, has_cover, front_behind_size, left_right_size, cover_separation, cover_rotation, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        cover_rotation = [x / 180 * np.pi for x in cover_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.has_cover = has_cover
        self.front_behind_size = front_behind_size
        self.left_right_size = left_right_size
        self.cover_separation = cover_separation
        self.cover_rotation = cover_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        if has_cover[0] == 1:
            mesh_position = [
                0, 
                front_behind_size[1] * np.cos(cover_rotation[0]) / 2, 
                cover_separation[0] / 2 + front_behind_size[1] * np.sin(cover_rotation[0]) / 2
            ]
            mesh_rotation = [
                cover_rotation[0], 
                0, 
                0
            ]
            self.mesh = Cuboid(front_behind_size[1], front_behind_size[0], front_behind_size[2],
                               position = mesh_position,
                               rotation = mesh_rotation)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        if has_cover[1] == 1:
            mesh_position = [
                0, 
                front_behind_size[1] * np.cos(cover_rotation[1]) / 2, 
                -cover_separation[0] / 2 + front_behind_size[1] * np.sin(cover_rotation[1]) / 2
            ]
            mesh_rotation = [
                cover_rotation[1], 
                0, 
                0
            ]
            self.mesh = Cuboid(front_behind_size[1], front_behind_size[0], front_behind_size[2],
                               position = mesh_position,
                               rotation = mesh_rotation)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        if has_cover[2] == 1:
            mesh_position = [
                -cover_separation[1] / 2 - left_right_size[1] * np.sin(cover_rotation[2]) / 2, 
                left_right_size[1] * np.cos(cover_rotation[2]) / 2, 
                0
            ]
            mesh_rotation = [
                0, 
                0, 
                cover_rotation[2]
            ]
            self.mesh = Cuboid(left_right_size[1], left_right_size[0], left_right_size[2],
                               position = mesh_position,
                               rotation = mesh_rotation)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        if has_cover[3] == 1:
            mesh_position = [
                cover_separation[1] / 2 - left_right_size[1] * np.sin(cover_rotation[3]) / 2, 
                left_right_size[1] * np.cos(cover_rotation[3]) / 2, 
                0
            ]
            mesh_rotation = [
                0, 
                0, 
                cover_rotation[3]
            ]
            self.mesh = Cuboid(left_right_size[1], left_right_size[0], left_right_size[2],
                               position = mesh_position,
                               rotation = mesh_rotation)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)


        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Cover'


# Source: Box/concept_template.py
class Regular_Cover(ConceptTemplate):
    def __init__(self, outer_size, inner_size, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.outer_size = outer_size
        self.inner_size = inner_size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        top_mesh_position = [
            0,
            (outer_size[1] + inner_size[1]) / 2,
            outer_size[2] / 2
        ]
        self.top_mesh = Cuboid(outer_size[1] - inner_size[1], outer_size[0], outer_size[2],
                               position = top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [
            0, 
            inner_size[1] / 2,
            outer_size[2] / 2
        ]
        self.bottom_mesh = Rectangular_Ring(inner_size[1], outer_size[0], outer_size[2], inner_size[0], inner_size[2],
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

        self.semantic = 'Cover'


# Source: Gluestick/concept_template.py
class Domed_Cover(ConceptTemplate):
    def __init__(self, bottom_size, sphere_radius, sphere_exist_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        sphere_exist_rotation = [x / 180 * np.pi for x in sphere_exist_rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.bottom_size = bottom_size
        self.sphere_radius = sphere_radius
        self.sphere_exist_rotation = sphere_exist_rotation

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0,
            bottom_size[2] / 2,
            0,
        ]
        self.bottom_mesh = Cylinder(bottom_size[2], bottom_size[0], bottom_size[1],
                                    position=bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        top_mesh_position = [
            0,
            bottom_size[2] - sphere_radius[1] * np.cos(sphere_exist_rotation[0]),
            0,
        ]
        self.top_mesh = Sphere(
            radius=sphere_radius[0],
            top_angle=0,
            bottom_angle=sphere_exist_rotation[0],
            radius_y=sphere_radius[1],
            position=top_mesh_position,
        )
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Cover'


# Source: Gluestick/concept_template.py
class Cylindrical_Cover(ConceptTemplate):
    def __init__(self, outer_size, inner_size, position=[0, 0, 0], rotation=[0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.outer_size = outer_size
        self.inner_size = inner_size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        radius_middle = outer_size[0] + (outer_size[2] - inner_size[2]) * (outer_size[1] - outer_size[0]) / outer_size[2]

        ring_mesh_position = [0, inner_size[2] / 2, 0]
        self.ring_mesh = Ring(
            height=inner_size[2],
            outer_top_radius=radius_middle,
            inner_top_radius=inner_size[0],
            outer_bottom_radius=outer_size[1],
            inner_bottom_radius=inner_size[1],
            position=ring_mesh_position,
        )
        vertices_list.append(self.ring_mesh.vertices)
        faces_list.append(self.ring_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.ring_mesh.vertices)

        top_mesh_position = [
            0, 
            (inner_size[2] + outer_size[2]) / 2, 
            0
        ]
        self.top_mesh = Cylinder(outer_size[2] - inner_size[2], outer_size[0], radius_middle,
                                 position=top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)
        
        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation, rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Cover'


# Source: Stapler/concept_template.py
class Simplified_Cover(ConceptTemplate):
    def __init__(self, size, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_position = [
            0,
            size[1] / 2,
            size[2] / 2
        ]
        self.mesh = Cuboid(size[1], size[0], size[2],
                           position = mesh_position)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Cover'


# Source: Stapler/concept_template.py
class Carved_Cover(ConceptTemplate):
    def __init__(self, outer_size, inner_size, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.outer_size = outer_size
        self.inner_size = inner_size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        top_mesh_position = [
            0,
            (outer_size[1] + inner_size[1]) / 2,
            outer_size[2] / 2
        ]
        self.top_mesh = Cuboid(outer_size[1] - inner_size[1], outer_size[0], outer_size[2],
                               position = top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [
            0, 
            inner_size[1] / 2,
            outer_size[2] / 2
        ]
        self.bottom_mesh = Rectangular_Ring(inner_size[1], outer_size[0], outer_size[2], inner_size[0], inner_size[2],
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

        self.semantic = 'Cover'


# Source: Dishwasher/concept_template.py
class Cuboidal_Topcover(ConceptTemplate):
    def __init__(self, size, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_position = [
            0,
            size[1] / 2,
            0
        ]
        self.mesh = Cuboid(size[1], size[0], size[2],
                             position = mesh_position)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Cover'


# Source: KitchenPot/concept_template.py
class Cylindrical_Cover(ConceptTemplate):
    def __init__(self, size, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.mesh = Cylinder(size[1], size[0])
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Cover'


# Source: KitchenPot/concept_template.py
class Carved_Cylindrical_Cover(ConceptTemplate):
    def __init__(self, outer_size, inner_size, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.outer_size = outer_size
        self.inner_size = inner_size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        middle_radius = outer_size[1] * (1 - inner_size[2] / outer_size[2]) + outer_size[0] * inner_size[2] / outer_size[2]
        top_height = outer_size[2] - inner_size[2]
        top_mesh_position = [0, inner_size[2] / 2, 0]
        self.top_mesh = Cylinder(top_height, outer_size[0], middle_radius,
                                 position = top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [0, -(outer_size[2] - inner_size[2]) / 2, 0]
        self.bottom_mesh = Ring(inner_size[2], middle_radius, inner_size[0], 
                             outer_bottom_radius = outer_size[1],
                             inner_bottom_radius = inner_size[1],
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

        self.semantic = 'Cover'


# Source: KitchenPot/concept_template.py
class Semi_Spherical_Cover(ConceptTemplate):
    def __init__(self, radius, exist_angle, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        exist_angle = [x / 180 * np.pi for x in exist_angle]
        super().__init__(position, rotation)

        # Record Parameters
        self.radius = radius
        self.exist_angle = exist_angle

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_position = [
            0,
            -radius[0] * np.cos(exist_angle[0]),
            0
        ]
        self.mesh = Sphere(radius[0], 0, exist_angle[0],
                           position = mesh_position)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Cover'


# Source: Kettle/concept_template.py
class Standard_Cover(ConceptTemplate):
    def __init__(self, outer_size, inner_size, num_knobs, knob_1_size, knob_2_size, knob_3_size, knob_4_size, knob_5_size, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.outer_size = outer_size
        self.inner_size = inner_size
        self.num_knobs = num_knobs
        self.knob_1_size = knob_1_size
        self.knob_2_size = knob_2_size
        self.knob_3_size = knob_3_size
        self.knob_4_size = knob_4_size
        self.knob_5_size = knob_5_size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_1_bottom_radius = outer_size[1] * (1 - inner_size[2] / outer_size[2]) + outer_size[0] * inner_size[2] / outer_size[2]
        mesh_1_height = outer_size[2] - inner_size[2]
        top_mesh_position = [
            0, 
            inner_size[2] / 2 + outer_size[2] / 2, 
            0
        ]
        self.top_mesh = Cylinder(mesh_1_height, outer_size[0], mesh_1_bottom_radius, 
                                 position = top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [
            0, 
            -(outer_size[2] - inner_size[2]) / 2 + outer_size[2] / 2, 
            0
        ]
        self.bottom_mesh = Ring(inner_size[2], mesh_1_bottom_radius, inner_size[0], 
                             outer_bottom_radius = outer_size[1],
                             inner_bottom_radius = inner_size[1],
                             position=bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        delta_height = outer_size[2]
        for i in range(num_knobs[0]):
            delta_height += locals()['knob_%d_size'%(i+1)][2] / 2
            knob_mesh_position = [0, delta_height, 0]
            self.knob_mesh = Cylinder(locals()['knob_%d_size'%(i+1)][2], locals()['knob_%d_size'%(i+1)][0], locals()['knob_%d_size'%(i+1)][1], 
                                      position=knob_mesh_position)
            delta_height += locals()['knob_%d_size'%(i+1)][2] / 2
            vertices_list.append(self.knob_mesh.vertices)
            faces_list.append(self.knob_mesh.faces + total_num_vertices)
            total_num_vertices += len(self.knob_mesh.vertices)


        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Cover'


# Source: Lighter/concept_template.py
class Regular_Cover(ConceptTemplate):
    def __init__(self, outer_size, inner_size, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.outer_size = outer_size
        self.inner_size = inner_size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        top_mesh_position = [
            0,
            (outer_size[1] + inner_size[1]) / 2,
            -outer_size[2] / 2
        ]
        self.top_mesh = Cuboid(outer_size[1] - inner_size[1], outer_size[0], outer_size[2],
                               position = top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        bottom_mesh_position = [
            0, 
            inner_size[1] / 2,
            -outer_size[2] / 2
        ]
        self.bottom_mesh = Rectangular_Ring(inner_size[1], outer_size[0], outer_size[2], inner_size[0], inner_size[2],
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

        self.semantic = 'Cover'


# Source: Trashcan/concept_template.py
class Cylindrical_Cover(ConceptTemplate):
    def __init__(self, size, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.mesh = Cylinder(size[1], size[0])
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Cover'


# Source: Trashcan/concept_template.py
class Cuboidal_Cover(ConceptTemplate):
    def __init__(self, top_size, bottom_size, height, top_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.top_size = top_size
        self.bottom_size = bottom_size
        self.height = height
        self.top_offset = top_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_position = [
            0,
            height[0] / 2,
            bottom_size[1] / 2
        ]
        self.mesh = Cuboid(height[0], top_size[0], top_size[1], 
                           bottom_size[0], bottom_size[1], 
                           [top_offset[0], top_offset[1]],
                           back_height = height[1],
                           position = mesh_position)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Cover'


# Source: Trashcan/concept_template.py
class Double_Layer_Cuboidal_Cover(ConceptTemplate):
    def __init__(self, top_size, bottom_size, top_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.top_size = top_size
        self.bottom_size = bottom_size
        self.top_offset = top_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        bottom_mesh_position = [
            0,
            bottom_size[1] / 2,
            bottom_size[2] / 2
        ]
        self.bottom_mesh = Cuboid(bottom_size[1], bottom_size[0], bottom_size[2],
                                  position = bottom_mesh_position)
        vertices_list.append(self.bottom_mesh.vertices)
        faces_list.append(self.bottom_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bottom_mesh.vertices)

        top_mesh_position = [
            top_offset[0],
            bottom_size[1] + top_size[1] / 2,
            bottom_size[2] / 2 + top_offset[1]
        ]
        self.top_mesh = Cuboid(top_size[1], top_size[0], top_size[2],
                               position = top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Cover'


# Source: Trashcan/concept_template.py
class Cylindrical_Hollow_Cover(ConceptTemplate):
    def __init__(self, size, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.size = size

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_position = [
            0,
            size[2] / 2,
            0
        ]
        self.mesh = Ring(size[2], size[0], size[1],
                         position = mesh_position)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Cover'


# Source: Trashcan/concept_template.py
class Cuboidal_Hollow_Cover(ConceptTemplate):
    def __init__(self, outer_size, inner_size, inner_offset, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.outer_size = outer_size
        self.inner_size = inner_size
        self.inner_offset = inner_offset

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        mesh_position = [
            0,
            outer_size[1] / 2,
            0
        ]
        self.mesh = Rectangular_Ring(outer_size[1], outer_size[0], outer_size[2],
                                    inner_size[0], inner_size[1], 
                                    [inner_offset[0], inner_offset[1]],
                                    position = mesh_position)
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Cover'


# Source: Trashcan/concept_template.py
class Holed_Cylindrical_Cover(ConceptTemplate):
    def __init__(self, radius, height, exist_angle, num_sides, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        exist_angle = [x / 180 * np.pi for x in exist_angle]
        super().__init__(position, rotation)

        # Record Parameters
        self.radius = radius
        self.height = height
        self.exist_angle = exist_angle
        self.num_sides = num_sides

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(num_sides[0]):
            rotation_y = i * np.pi * 2 / num_sides[0]
            mesh_position = [
                0,
                height[2] / 2,
                0
            ]
            mesh_rotation = [0, rotation_y, 0]
            self.mesh = Ring(height[2], radius[0], radius[1], exist_angle[0],
                             position = mesh_position,
                             rotation = mesh_rotation)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        top_mesh_position = [
            0,
            height[2] + height[1] + (height[0] - height[1]) / 2,
            0
        ]
        self.top_mesh = Cylinder(height[0] - height[1], radius[0], 
                                 position = top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        middle_mesh_position = [
            0,
            height[2] + height[1] / 2,
            0
        ]
        self.middle_mesh = Ring(height[1], radius[0], radius[1], 
                                position = middle_mesh_position)
        vertices_list.append(self.middle_mesh.vertices)
        faces_list.append(self.middle_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.middle_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Cover'


# Source: Trashcan/concept_template.py
class Holed_Cuboidal_Cover(ConceptTemplate):
    def __init__(self, outer_size, inner_size, front_behind_hole_size, left_right_hole_size, has_hole, position = [0, 0, 0], rotation = [0, 0, 0]):

        # Process rotation param
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Record Parameters
        self.outer_size = outer_size
        self.inner_size = inner_size
        self.front_behind_hole_size = front_behind_hole_size
        self.left_right_hole_size = left_right_hole_size
        self.has_hole = has_hole

        # Instantiate component geometries
        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # top part
        top_mesh_position = [
            0,
            outer_size[1] / 2 + inner_size[1] / 2,
            0
        ]
        self.top_mesh = Cuboid(outer_size[1] - inner_size[1], outer_size[0], outer_size[2], 
                               position = top_mesh_position)
        vertices_list.append(self.top_mesh.vertices)
        faces_list.append(self.top_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.top_mesh.vertices)

        # front part
        if has_hole[0] == 0:
            mesh_position = [
                0,
                inner_size[1] / 2,
                (outer_size[2] + inner_size[2]) / 4
            ]
            self.mesh = Cuboid(inner_size[1], outer_size[0], (outer_size[2] - inner_size[2]) / 2, 
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        elif has_hole[0] == 1:
            mesh_1_position = [
                -(outer_size[0] + front_behind_hole_size[0]) / 4,
                inner_size[1] / 2,
                (outer_size[2] + inner_size[2]) / 4
            ]
            self.mesh_1 = Cuboid(inner_size[1], (outer_size[0] - front_behind_hole_size[0]) / 2, (outer_size[2] - inner_size[2]) / 2, 
                                 position = mesh_1_position)
            vertices_list.append(self.mesh_1.vertices)
            faces_list.append(self.mesh_1.faces + total_num_vertices)
            total_num_vertices += len(self.mesh_1.vertices)

            mesh_2_position = [
                (outer_size[0] + front_behind_hole_size[0]) / 4,
                inner_size[1] / 2,
                (outer_size[2] + inner_size[2]) / 4
            ]
            self.mesh_2 = Cuboid(inner_size[1], (outer_size[0] - front_behind_hole_size[0]) / 2, (outer_size[2] - inner_size[2]) / 2, 
                                 position = mesh_2_position)
            vertices_list.append(self.mesh_2.vertices)
            faces_list.append(self.mesh_2.faces + total_num_vertices)
            total_num_vertices += len(self.mesh_2.vertices)

            mesh_3_position = [
                0,
                (inner_size[1] + front_behind_hole_size[1]) / 2,
                (outer_size[2] + inner_size[2]) / 4
            ]
            self.mesh_3 = Cuboid(inner_size[1] - front_behind_hole_size[1], front_behind_hole_size[0], (outer_size[2] - inner_size[2]) / 2, 
                                 position = mesh_3_position)
            vertices_list.append(self.mesh_3.vertices)
            faces_list.append(self.mesh_3.faces + total_num_vertices)
            total_num_vertices += len(self.mesh_3.vertices)

        # behind part
        if has_hole[1] == 0:
            mesh_position = [
                0,
                inner_size[1] / 2,
                -(outer_size[2] + inner_size[2]) / 4
            ]
            self.mesh = Cuboid(inner_size[1], outer_size[0], (outer_size[2] - inner_size[2]) / 2, 
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        elif has_hole[1] == 1:
            mesh_1_position = [
                -(outer_size[0] + front_behind_hole_size[0]) / 4,
                inner_size[1] / 2,
                -(outer_size[2] + inner_size[2]) / 4
            ]
            self.mesh_1 = Cuboid(inner_size[1], (outer_size[0] - front_behind_hole_size[0]) / 2, (outer_size[2] - inner_size[2]) / 2, 
                                 position = mesh_1_position)
            vertices_list.append(self.mesh_1.vertices)
            faces_list.append(self.mesh_1.faces + total_num_vertices)
            total_num_vertices += len(self.mesh_1.vertices)

            mesh_2_position = [
                (outer_size[0] + front_behind_hole_size[0]) / 4,
                inner_size[1] / 2,
                -(outer_size[2] + inner_size[2]) / 4
            ]
            self.mesh_2 = Cuboid(inner_size[1], (outer_size[0] - front_behind_hole_size[0]) / 2, (outer_size[2] - inner_size[2]) / 2, 
                                 position = mesh_2_position)
            vertices_list.append(self.mesh_2.vertices)
            faces_list.append(self.mesh_2.faces + total_num_vertices)
            total_num_vertices += len(self.mesh_2.vertices)

            mesh_3_position = [
                0,
                (inner_size[1] + front_behind_hole_size[1]) / 2,
                -(outer_size[2] + inner_size[2]) / 4
            ]
            self.mesh_3 = Cuboid(inner_size[1] - front_behind_hole_size[1], front_behind_hole_size[0], (outer_size[2] - inner_size[2]) / 2, 
                                 position = mesh_3_position)
            vertices_list.append(self.mesh_3.vertices)
            faces_list.append(self.mesh_3.faces + total_num_vertices)
            total_num_vertices += len(self.mesh_3.vertices)

        # left part
        if has_hole[2] == 0:
            mesh_position = [
                -(outer_size[0] + inner_size[0]) / 4,
                inner_size[1] / 2,
                0
            ]
            self.mesh = Cuboid(inner_size[1], (outer_size[0] - inner_size[0]) / 2, inner_size[2], 
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        elif has_hole[2] == 1:
            mesh_1_position = [
                -(outer_size[0] + inner_size[0]) / 4,
                inner_size[1] / 2,
                -(inner_size[2] + left_right_hole_size[0]) / 4
            ]
            self.mesh_1 = Cuboid(inner_size[1], (outer_size[0] - inner_size[0]) / 2, (inner_size[2] - left_right_hole_size[0]) / 2,  
                                 position = mesh_1_position)
            vertices_list.append(self.mesh_1.vertices)
            faces_list.append(self.mesh_1.faces + total_num_vertices)
            total_num_vertices += len(self.mesh_1.vertices)

            mesh_2_position = [
                -(outer_size[0] + inner_size[0]) / 4,
                inner_size[1] / 2,
                (inner_size[2] + left_right_hole_size[0]) / 4
            ]
            self.mesh_2 = Cuboid(inner_size[1], (outer_size[0] - inner_size[0]) / 2, (inner_size[2] - left_right_hole_size[0]) / 2,  
                                 position = mesh_2_position)
            vertices_list.append(self.mesh_2.vertices)
            faces_list.append(self.mesh_2.faces + total_num_vertices)
            total_num_vertices += len(self.mesh_2.vertices)

            mesh_3_position = [
                -(outer_size[0] + inner_size[0]) / 4,
                (inner_size[1] + left_right_hole_size[1]) / 2,
                0
            ]
            self.mesh_3 = Cuboid(inner_size[1] - left_right_hole_size[1], (outer_size[2] - inner_size[2]) / 2, left_right_hole_size[0], 
                                 position = mesh_3_position)
            vertices_list.append(self.mesh_3.vertices)
            faces_list.append(self.mesh_3.faces + total_num_vertices)
            total_num_vertices += len(self.mesh_3.vertices)

        # right part
        if has_hole[3] == 0:
            mesh_position = [
                (outer_size[0] + inner_size[0]) / 4,
                inner_size[1] / 2,
                0
            ]
            self.mesh = Cuboid(inner_size[1], (outer_size[0] - inner_size[0]) / 2, inner_size[2], 
                               position = mesh_position)
            vertices_list.append(self.mesh.vertices)
            faces_list.append(self.mesh.faces + total_num_vertices)
            total_num_vertices += len(self.mesh.vertices)

        elif has_hole[3] == 1:
            mesh_1_position = [
                (outer_size[0] + inner_size[0]) / 4,
                inner_size[1] / 2,
                -(inner_size[2] + left_right_hole_size[0]) / 4
            ]
            self.mesh_1 = Cuboid(inner_size[1], (outer_size[0] - inner_size[0]) / 2, (inner_size[2] - left_right_hole_size[0]) / 2,  
                                 position = mesh_1_position)
            vertices_list.append(self.mesh_1.vertices)
            faces_list.append(self.mesh_1.faces + total_num_vertices)
            total_num_vertices += len(self.mesh_1.vertices)

            mesh_2_position = [
                (outer_size[0] + inner_size[0]) / 4,
                inner_size[1] / 2,
                (inner_size[2] + left_right_hole_size[0]) / 4
            ]
            self.mesh_2 = Cuboid(inner_size[1], (outer_size[0] - inner_size[0]) / 2, (inner_size[2] - left_right_hole_size[0]) / 2,  
                                 position = mesh_2_position)
            vertices_list.append(self.mesh_2.vertices)
            faces_list.append(self.mesh_2.faces + total_num_vertices)
            total_num_vertices += len(self.mesh_2.vertices)

            mesh_3_position = [
                (outer_size[0] + inner_size[0]) / 4,
                (inner_size[1] + left_right_hole_size[1]) / 2,
                0
            ]
            self.mesh_3 = Cuboid(inner_size[1] - left_right_hole_size[1], (outer_size[2] - inner_size[2]) / 2, left_right_hole_size[0], 
                                 position = mesh_3_position)
            vertices_list.append(self.mesh_3.vertices)
            faces_list.append(self.mesh_3.faces + total_num_vertices)
            total_num_vertices += len(self.mesh_3.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # Global Transformation
        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Cover'
