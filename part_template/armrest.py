import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation
from knowledge_utils import *


class Solid_Armrest(ConceptTemplate):
    """
    Semantic: Armrest
    Geometry: two mirror-image cuboid armrests, one on each side, each tilted by two rotation angles
    Used by: Chair
    Parameters:
      size [w, h, d]: dimensions of each armrest cuboid
      armrest_separation [gap]: X distance between the two armrest centres
      armrest_rotation [rx, rz_deg]: X tilt and Z splay angle of each armrest
      position, rotation: global transform
    """
    def __init__(self, size, armrest_separation, armrest_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        armrest_rotation = [x / 180 * np.pi for x in armrest_rotation]
        super().__init__(position, rotation)

        self.size = size
        self.armrest_separation = armrest_separation
        self.armrest_rotation = armrest_rotation

        width, height, depth = size
        gap = armrest_separation[0]
        rx, rz = armrest_rotation[0], armrest_rotation[1]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        for i in range(2):
            flag = 1 if i == 0 else -1
            mesh_rotation = [rx, 0, flag * rz]
            mesh_position = [
                -flag * gap / 2,
                height / 2 * np.cos(rz) * np.cos(rx) - depth / 2 * np.sin(rx),
                0
            ]
            tmp_mesh = Cuboid(height, width, depth,
                              position=mesh_position, rotation=mesh_rotation)
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Armrest'


class Office_Armrest(ConceptTemplate):
    """
    Semantic: Armrest
    Geometry: two pairs of armrests (left + right), each pair consisting of a vertical support
              cuboid and a horizontal support cuboid, assembled with compound rotations
    Used by: Chair
    Parameters:
      horizontal_support_sizes [w, h, d]: dimensions of the horizontal (top) support
      vertical_support_sizes [w, h, d]: dimensions of the vertical (upright) support
      supports_contact_offset [z]: Z position where vertical and horizontal supports meet
      vertical_support_rotation [rx_deg]: X tilt of the vertical support
      horizontal_support_rotation [rx_deg]: X tilt of the horizontal support
      armrest_separation [gap]: X distance between the two armrest centres
      armrest_rotation [rz_deg]: Z splay angle of each armrest pair
      position, rotation: global transform
    """
    def __init__(self, horizontal_support_sizes, vertical_support_sizes,
                 supports_contact_offset, vertical_support_rotation,
                 horizontal_support_rotation, armrest_separation, armrest_rotation,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        vertical_support_rotation = [x / 180 * np.pi for x in vertical_support_rotation]
        horizontal_support_rotation = [x / 180 * np.pi for x in horizontal_support_rotation]
        armrest_rotation = [x / 180 * np.pi for x in armrest_rotation]
        super().__init__(position, rotation)

        self.horizontal_support_sizes = horizontal_support_sizes
        self.vertical_support_sizes = vertical_support_sizes
        self.supports_contact_offset = supports_contact_offset
        self.vertical_support_rotation = vertical_support_rotation
        self.horizontal_support_rotation = horizontal_support_rotation
        self.armrest_separation = armrest_separation
        self.armrest_rotation = armrest_rotation

        hw, hh, hd = horizontal_support_sizes
        vw, vh, vd = vertical_support_sizes
        z_contact = supports_contact_offset[0]
        v_rx = vertical_support_rotation[0]
        h_rx = horizontal_support_rotation[0]
        gap = armrest_separation[0]
        rz = armrest_rotation[0]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # i=0,1 → horizontal supports (left, right); i=2,3 → vertical supports (left, right)
        for i in range(4):
            flag = 1 if (i % 2 == 0) else -1
            if i < 2:
                # horizontal support — rotation_order="YXZ" for compound tilt + splay
                mesh_rotation = [h_rx, 0, flag * rz]
                mesh_position = [
                    -flag * (gap / 2 + (vh * np.cos(v_rx) + hh) / 2 * np.sin(rz)),
                    (vh * np.cos(v_rx) * 2 + hh) / 2 * np.cos(rz) +
                    (z_contact - vh / 2 * np.sin(v_rx)) * np.tan(h_rx),
                    0
                ]
                tmp_mesh = Cuboid(hh, hw, hd,
                                  position=mesh_position, rotation=mesh_rotation,
                                  rotation_order="YXZ")
            else:
                # vertical support — rotation_order="YXZ" for compound tilt + splay
                mesh_rotation = [v_rx, 0, flag * rz]
                mesh_position = [
                    -flag * gap / 2,
                    vh / 2 * np.cos(v_rx) * np.cos(rz),
                    z_contact
                ]
                tmp_mesh = Cuboid(vh, vw, vd,
                                  position=mesh_position, rotation=mesh_rotation,
                                  rotation_order="YXZ")

            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Armrest'
