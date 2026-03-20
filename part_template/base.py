import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation
from knowledge_utils import *


class Cuboidal_Base(ConceptTemplate):
    """
    Semantic: Base
    Geometry: either (1) one or two stacked cuboid sections, or (2) a single flat cuboid slab
    Used by: Faucet, Laptop
    Parameters:
      size [w, h, d]: dimensions of flat slab mode (Laptop-style)
      number_of_box [n]: 1 or 2 sections in stacked mode
      size_0 [w, h, d]: dimensions of primary section in stacked mode
      size_1 [w, h, d]: dimensions of secondary section in stacked mode (used when n=2)
      offset_1 [x, y, z]: position offset of secondary section in stacked mode
      position, rotation: global transform
    """
    def __init__(self, number_of_box=None, size_0=None, size_1=None, offset_1=None, size=None,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        # Mode A: Laptop-style flat slab base.
        if size is not None:
          self.size = size

          width, height, depth = size

          self.mesh = Cuboid(height, width, depth)
          self.vertices = self.mesh.vertices
          self.faces = self.mesh.faces

          self.vertices = apply_transformation(self.vertices, position, rotation)
        else:
          # Mode B: Faucet-style stacked base sections.
          if number_of_box is None or size_0 is None or size_1 is None or offset_1 is None:
            raise ValueError(
              "Cuboidal_Base requires either size=[w,h,d] or "
              "(number_of_box, size_0, size_1, offset_1)."
            )

          self.number_of_box = number_of_box
          self.size_0 = size_0
          self.size_1 = size_1
          self.offset_1 = offset_1

          w0, h0, d0 = size_0
          w1, h1, d1 = size_1
          ox, oy, oz = offset_1

          vertices_list = []
          faces_list = []
          total_num_vertices = 0

          self.mesh_0 = Cuboid(h0, w0, d0, position=[0, -h0 / 2, -d0 / 2])
          vertices_list.append(self.mesh_0.vertices)
          faces_list.append(self.mesh_0.faces + total_num_vertices)
          total_num_vertices += len(self.mesh_0.vertices)

          if int(number_of_box[0]) == 2:
            self.mesh_1 = Cuboid(h1, w1, d1,
                       position=[ox, -h0 - h1 / 2 + oy, oz - d0 / 2])
            vertices_list.append(self.mesh_1.vertices)
            faces_list.append(self.mesh_1.faces + total_num_vertices)
            total_num_vertices += len(self.mesh_1.vertices)

          self.vertices = np.concatenate(vertices_list)
          self.faces = np.concatenate(faces_list)

          # offset_first=True: translation applied before rotation
          self.vertices = apply_transformation(self.vertices, position, rotation,
                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Base'


class Cylindrical_Base(ConceptTemplate):
    """
    Semantic: Base
    Geometry: one or two stacked cylinder base sections; second section optional
    Used by: Faucet
    Parameters:
      number_of_cylinder [n]: 1 or 2 sections
      size_0 [radius, h]: radius and height of the primary section
      size_1 [radius, h]: radius and height of the secondary section (used when n=2)
      offset_1 [x, y, z]: position offset of the secondary section relative to primary top
      position, rotation: global transform
    """
    def __init__(self, number_of_cylinder, size_0, size_1, offset_1,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.number_of_cylinder = number_of_cylinder
        self.size_0 = size_0
        self.size_1 = size_1
        self.offset_1 = offset_1

        r0, h0 = size_0[0], size_0[1]
        r1, h1 = size_1[0], size_1[1]
        ox, oy, oz = offset_1

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        self.mesh_0 = Cylinder(h0, r0, r0, position=[0, -h0 / 2, -r0])
        vertices_list.append(self.mesh_0.vertices)
        faces_list.append(self.mesh_0.faces + total_num_vertices)
        total_num_vertices += len(self.mesh_0.vertices)

        if int(number_of_cylinder[0]) == 2:
            self.mesh_1 = Cylinder(h1, r1, r1,
                                   position=[ox, -h0 - h1 / 2 + oy, oz - r0])
            vertices_list.append(self.mesh_1.vertices)
            faces_list.append(self.mesh_1.faces + total_num_vertices)
            total_num_vertices += len(self.mesh_1.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # offset_first=True: translation applied before rotation
        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Base'


class Curved_Base(ConceptTemplate):
    """
    Semantic: Base
    Geometry: arc-shaped Torus base, optionally tilted; arc geometry derived from size parameters
    Used by: Faucet
    Parameters:
      R [tube_radius]: cross-section radius of the torus tube
      size [span, rise]: horizontal span and vertical rise of the arc
      base_rotation [rx_deg]: additional X tilt applied after arc construction
      position, rotation: global transform
    """
    def __init__(self, R, size, base_rotation, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.R = R
        self.size = size
        self.base_rotation = base_rotation

        tube_r = R[0]
        span, rise = size[0], size[1]

        # derive arc centre and angle from span/rise geometry
        center_z = span ** 2 / 4 / rise
        center_angle = np.arctan(span / 2 / center_z) * 2
        center_radius = center_z / np.cos(center_angle / 2)
        center_position = [0, -span / 2, center_z]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        main_mesh_rotation = [center_angle / 2 + np.pi / 2, 0, -np.pi / 2]
        self.main_mesh = Torus(center_radius, tube_r, center_angle,
                               position=center_position,
                               rotation=main_mesh_rotation,
                               # ZXY order: Z rotation applied first to orient torus arc along base span
                               rotation_order="ZXY")
        # additional X tilt applied after torus construction
        self.main_mesh.vertices = apply_transformation(
            self.main_mesh.vertices, [0, 0, 0], [base_rotation[0], 0, 0]
        )
        vertices_list.append(self.main_mesh.vertices)
        faces_list.append(self.main_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.main_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # offset_first=True: translation applied before rotation
        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Base'


class UShapedXZ_Base(ConceptTemplate):
    """
    Semantic: Base
    Geometry: U-shaped base in the XZ plane — two vertical cylinder legs + one horizontal
              crossbar + two small foot cylinders at the bottom of each leg
    Used by: Faucet
    Parameters:
      R [tube_radius]: radius of all tube cylinders
      size_tube [span, leg_h]: X span between legs and height of each vertical leg
      size_base [foot_r, foot_h]: radius and height of each foot cylinder
      position, rotation: global transform
    """
    def __init__(self, R, size_tube, size_base, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.R = R
        self.size_tube = size_tube
        self.size_base = size_base

        r = R[0]
        span, leg_h = size_tube[0], size_tube[1]
        foot_r, foot_h = size_base[0], size_base[1]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # left vertical leg
        tmp_mesh = Cylinder(leg_h, r, r,
                            position=[-span / 2, 0, foot_h + leg_h / 2],
                            rotation=[np.pi / 2, 0, 0])
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        # right vertical leg
        tmp_mesh = Cylinder(leg_h, r, r,
                            position=[span / 2, 0, foot_h + leg_h / 2],
                            rotation=[np.pi / 2, 0, 0])
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        # horizontal crossbar at top
        tmp_mesh = Cylinder(span, r, r,
                            position=[0, 0, foot_h + leg_h],
                            rotation=[0, 0, np.pi / 2])
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        # right foot
        tmp_mesh = Cylinder(foot_h, foot_r, foot_r,
                            position=[span / 2, 0, foot_h / 2],
                            rotation=[np.pi / 2, 0, 0])
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        # left foot
        tmp_mesh = Cylinder(foot_h, foot_r, foot_r,
                            position=[-span / 2, 0, foot_h / 2],
                            rotation=[np.pi / 2, 0, 0])
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # offset_first=True: translation applied before rotation
        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Base'


class UShapedYZ_Base(ConceptTemplate):
    """
    Semantic: Base
    Geometry: U-shaped base in the YZ plane — two vertical cylinder legs + one horizontal
              crossbar at top + two small foot cylinders at the bottom of each leg
    Used by: Faucet
    Parameters:
      R [tube_radius]: radius of all tube cylinders
      size_tube [span, leg_h]: X span between legs and height of each vertical leg
      size_base [foot_r, foot_h]: radius and height of each foot cylinder
      position, rotation: global transform
    """
    def __init__(self, R, size_tube, size_base, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.R = R
        self.size_tube = size_tube
        self.size_base = size_base

        r = R[0]
        span, leg_h = size_tube[0], size_tube[1]
        foot_r, foot_h = size_base[0], size_base[1]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # left vertical leg
        tmp_mesh = Cylinder(leg_h, r, r, position=[-span / 2, -leg_h / 2, 0])
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        # right vertical leg
        tmp_mesh = Cylinder(leg_h, r, r, position=[span / 2, -leg_h / 2, 0])
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        # horizontal crossbar at top
        tmp_mesh = Cylinder(span, r, r, rotation=[0, 0, np.pi / 2])
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        # right foot
        tmp_mesh = Cylinder(foot_h, foot_r, foot_r,
                            position=[span / 2, -(foot_h / 2 + leg_h), 0])
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        # left foot
        tmp_mesh = Cylinder(foot_h, foot_r, foot_r,
                            position=[-span / 2, -(foot_h / 2 + leg_h), 0])
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        # offset_first=True: translation applied before rotation
        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Base'


class Round_Base(ConceptTemplate):
    """
    Semantic: Base
    Geometry: flat cylinder disc lying in the XZ plane (axis along Z)
    Used by: Faucet
    Parameters:
      size [radius, depth]: radius and depth of the disc
      position, rotation: global transform
    """
    def __init__(self, size, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.size = size

        radius, depth = size[0], size[1]

        self.mesh = Cylinder(depth, radius, radius,
                             position=[0, 0, -depth / 2],
                             rotation=[np.pi / 2, 0, 0])
        self.vertices = self.mesh.vertices
        self.faces = self.mesh.faces

        # offset_first=True: translation applied before rotation
        self.vertices = apply_transformation(self.vertices, position, rotation,
                                             rotation_order="YXZ", offset_first=True)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Base'


