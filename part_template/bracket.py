import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation
from knowledge_utils import *


class Semi_Ring_Bracket(ConceptTemplate):
    """
    Semantic: Bracket
    Geometry: one or two pivot cylinders (continuous or split) + optional sphere endpoints +
              a partial Ring arc bracket
    Used by: Globe
    Parameters:
      pivot_size [radius, h]: radius and height of each pivot cylinder
      pivot_continuity [flag]: 1 = single continuous pivot, 0 = two separate pivots with gap
      pivot_seperation [gap]: Y gap between the two split pivots (used when flag=0)
      has_top_endpoint [flag]: 1 to add a sphere at the top of the pivot
      has_bottom_endpoint [flag]: 1 to add a sphere at the bottom of the pivot
      endpoint_radius [r]: radius of the endpoint spheres
      bracket_size [outer_r, inner_r, depth]: Ring arc dimensions
      bracket_exist_angle [arc_deg]: angular span of the Ring arc
      bracket_offset [y]: Y position of the bracket arc centre
      bracket_rotation [angle_deg]: rotational offset of the arc start angle
      position, rotation: global transform
    """
    def __init__(self, pivot_size, pivot_continuity, pivot_seperation,
                 has_top_endpoint, has_bottom_endpoint, endpoint_radius,
                 bracket_size, bracket_exist_angle, bracket_offset, bracket_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        bracket_exist_angle = [x / 180 * np.pi for x in bracket_exist_angle]
        bracket_rotation = [x / 180 * np.pi for x in bracket_rotation]
        super().__init__(position, rotation)

        self.pivot_size = pivot_size
        self.pivot_continuity = pivot_continuity
        self.pivot_seperation = pivot_seperation
        self.has_top_endpoint = has_top_endpoint
        self.has_bottom_endpoint = has_bottom_endpoint
        self.endpoint_radius = endpoint_radius
        self.bracket_size = bracket_size
        self.bracket_exist_angle = bracket_exist_angle
        self.bracket_offset = bracket_offset
        self.bracket_rotation = bracket_rotation

        p_r, p_h = pivot_size[0], pivot_size[1]
        p_gap = pivot_seperation[0]
        ep_r = endpoint_radius[0]
        b_outer, b_inner, b_depth = bracket_size
        arc = bracket_exist_angle[0]
        b_y = bracket_offset[0]
        b_rot = bracket_rotation[0]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        if pivot_continuity[0] == 1:
            # single continuous pivot cylinder
            tmp_mesh = Cylinder(p_h, p_r)
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)
        else:
            # two separate pivot cylinders with a gap between them
            tmp_mesh = Cylinder(p_h, p_r, position=[0, p_gap / 2 + p_h / 2, 0])
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

            tmp_mesh = Cylinder(p_h, p_r, position=[0, -p_gap / 2 - p_h / 2, 0])
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

        if has_top_endpoint[0] == 1:
            if pivot_continuity[0] == 0:
                ep_y = p_gap / 2 + p_h + ep_r
            else:
                ep_y = p_h / 2 + ep_r
            tmp_mesh = Sphere(ep_r, position=[0, ep_y, 0])
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

        if has_bottom_endpoint[0] == 1:
            if pivot_continuity[0] == 0:
                ep_y = -(p_gap / 2 + p_h + ep_r)
            else:
                ep_y = -(p_h / 2 + ep_r)
            tmp_mesh = Sphere(ep_r, position=[0, ep_y, 0])
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

        # Ring arc bracket
        bracket_mesh_rotation = [0, -np.pi / 2 + arc / 2 - b_rot, np.pi / 2]
        tmp_mesh = Ring(b_depth, b_outer, b_inner, arc,
                        position=[0, b_y, 0],
                        rotation=bracket_mesh_rotation)
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        if not vertices_list:
            raise ValueError(f"{self.__class__.__name__}: no geometry was instantiated")

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Bracket'


class Tilted_Bracket(ConceptTemplate):
    """
    Semantic: Bracket
    Geometry: horizontal pivot cylinder + a half-Ring arc bracket + a full Ring disc
    Used by: Globe
    Parameters:
      pivot_size [radius, h]: radius and height of the pivot cylinder
      bracket_size [outer_r, inner_r, depth]: Ring arc dimensions
      circle_thickness [radial_t, axial_t]: radial and axial thickness of the full Ring disc
      circle_rotation [angle_deg]: Z rotation of the full Ring disc
      position, rotation: global transform
    """
    def __init__(self, pivot_size, bracket_size, circle_thickness, circle_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        circle_rotation = [x / 180 * np.pi for x in circle_rotation]
        super().__init__(position, rotation)

        self.pivot_size = pivot_size
        self.bracket_size = bracket_size
        self.circle_thickness = circle_thickness
        self.circle_rotation = circle_rotation

        p_r, p_h = pivot_size[0], pivot_size[1]
        b_outer, b_inner, b_depth = bracket_size
        ct_radial, ct_axial = circle_thickness[0], circle_thickness[1]
        c_rot = circle_rotation[0]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # horizontal pivot cylinder (lying along Z)
        self.pivot_mesh = Cylinder(p_h, p_r, rotation=[np.pi / 2, 0, 0])
        vertices_list.append(self.pivot_mesh.vertices)
        faces_list.append(self.pivot_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.pivot_mesh.vertices)

        # half-Ring arc bracket
        self.bracket_mesh = Ring(b_depth, b_outer, b_inner, np.pi,
                                 rotation=[np.pi / 2, np.pi / 2, 0])
        vertices_list.append(self.bracket_mesh.vertices)
        faces_list.append(self.bracket_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.bracket_mesh.vertices)

        # full Ring disc (equatorial ring)
        outer_r = b_inner + ct_radial / 2
        inner_r = b_inner - ct_radial / 2
        self.circle_mesh = Ring(ct_axial, outer_r, inner_r,
                                rotation=[0, 0, c_rot])
        vertices_list.append(self.circle_mesh.vertices)
        faces_list.append(self.circle_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.circle_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Bracket'


class Enclosed_Bracket(ConceptTemplate):
    """
    Semantic: Bracket
    Geometry: one or two half-Ring arc brackets forming an enclosure + a full Ring disc
    Used by: Globe
    Parameters:
      bracket_size [outer_r, inner_r, depth]: Ring arc dimensions
      circle_radius [r]: centre radius of the full Ring disc
      circle_thickness [radial_t, axial_t]: radial and axial thickness of the full Ring disc
      half_circle_number [n]: 1 or 2 half-Ring arcs
      position, rotation: global transform
    """
    def __init__(self, bracket_size, circle_radius, circle_thickness, half_circle_number,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.bracket_size = bracket_size
        self.circle_radius = circle_radius
        self.circle_thickness = circle_thickness
        self.half_circle_number = half_circle_number

        b_outer, b_inner, b_depth = bracket_size
        c_r = circle_radius[0]
        ct_radial, ct_axial = circle_thickness[0], circle_thickness[1]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # first half-Ring arc
        tmp_mesh = Ring(b_depth, b_outer, b_inner, np.pi,
                        rotation=[np.pi / 2, np.pi / 2, 0])
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        if int(half_circle_number[0]) == 2:
            # second half-Ring arc — rotated 90° to close the enclosure
            tmp_mesh = Ring(b_depth, b_outer, b_inner, np.pi,
                            rotation=[np.pi / 2, 0, 0])
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

        # full Ring disc
        outer_r = c_r + ct_radial / 2
        inner_r = c_r - ct_radial / 2
        tmp_mesh = Ring(ct_axial, outer_r, inner_r)
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Bracket'
