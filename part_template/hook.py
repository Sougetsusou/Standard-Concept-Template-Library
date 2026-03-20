import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Regular_hook(ConceptTemplate):
    """
    Semantic: Hook
    Geometry: wall-mount base cuboid + angled arm cuboid + semicircular ring tip
    Used by: Foldingrack
    Parameters:
      base_size [w, h, d]: wall-mount base plate dimensions
      middle_size [w, h, d]: angled arm dimensions
      middle_offset [y, z]: arm attachment offset from base edge
      middle_rotation [rx]: arm tilt angle in degrees
      circle_radius [outer]: outer radius of the hook ring tip
    """
    def __init__(self, base_size, middle_size, middle_offset,
                 middle_rotation, circle_radius, position=[0, 0, 0], rotation=[0, 0, 0]):
        middle_rotation = [x / 180 * np.pi for x in middle_rotation]
        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)
        self.base_size = base_size
        self.middle_size = middle_size
        self.middle_offset = middle_offset
        self.middle_rotation = middle_rotation
        self.circle_radius = circle_radius

        bw, bh, bd = base_size
        mw, mh, md = middle_size
        moy, moz = middle_offset
        mrx = middle_rotation[0]
        outer_r = circle_radius[0]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        tmp_mesh = Cuboid(bh, bw, bd, position=[-bw / 2, 0, 0])
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        tmp_mesh = Cuboid(mh, mw, md,
                          position=[-bw - mw / 2 * np.cos(mrx),
                                    mw / 2 * np.sin(mrx) + moy,
                                    moz],
                          rotation=[0, 0, -mrx])
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        inner_r = outer_r - mh
        assert inner_r > 0, f"Regular_hook: ring inner radius {inner_r} <= 0"
        tmp_mesh = Ring(md, outer_r, inner_r, np.pi,
                        position=[-bw - mw * np.cos(mrx) + mh / 2 * np.sin(mrx),
                                  mw * np.sin(mrx) + moy - outer_r + mh / 2 * np.cos(mrx),
                                  moz],
                        rotation=[np.pi / 2, 0, -np.pi / 2])
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)
        self.vertices = apply_transformation(self.vertices, position, rotation)
        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))
        self.semantic = 'Hook'
