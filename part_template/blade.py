import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation
from knowledge_utils import *


class Cuboidal_Blade(ConceptTemplate):
    """
    Semantic: Blade
    Geometry: single flat cuboid blade, positioned with its base at the origin
    Used by: Knife
    Parameters:
      size [w, h, d]: width, height, depth of the blade
      position, rotation: global transform
    """
    def __init__(self, size, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.size = size

        width, height, depth = size

        self.mesh = Cuboid(height, width, depth, position=[0, height / 2, 0])
        self.vertices = self.mesh.vertices
        self.faces = self.mesh.faces

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Blade'


class Cusp_Blade(ConceptTemplate):
    """
    Semantic: Blade
    Geometry: tapered cuboid root section + a pointed cuboid tip that narrows to a cusp
    Used by: Knife
    Parameters:
      root_size [w, h, back_d, front_d]: root width, height, back depth, front depth
      root_z_offset [z]: Z offset of the root top face (taper direction)
      tip_length [h]: height of the tip section
      tip_z_offset [z]: Z offset of the tip apex
      position, rotation: global transform
    """
    def __init__(self, root_size, root_z_offset, tip_length, tip_z_offset,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.root_size = root_size
        self.root_z_offset = root_z_offset
        self.tip_length = tip_length
        self.tip_z_offset = tip_z_offset

        rw, rh, rd_back, rd_front = root_size
        rz = root_z_offset[0]
        th = tip_length[0]
        tz = tip_z_offset[0]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # root — tapered cuboid (back depth rd_back, front depth rd_front, top offset rz)
        self.mesh = Cuboid(rh, rw, rd_back, rw, rd_front,
                           top_offset=[0, rz],
                           position=[0, rh / 2, 0])
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        # tip — narrows to zero width at apex
        self.tip_mesh = Cuboid(th, rw, 0, rw, rd_back,
                               top_offset=[0, tz],
                               position=[0, rh + th / 2, rz])
        vertices_list.append(self.tip_mesh.vertices)
        faces_list.append(self.tip_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.tip_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Blade'


class Curved_Blade(ConceptTemplate):
    """
    Semantic: Blade
    Geometry: tapered cuboid root + a quarter-cylinder tip that curves the blade edge
    Used by: Knife, Scissors
    Parameters:
      root_size [w, h, back_d, front_d]: root width, height, back depth, front depth
      root_z_offset [z]: Z offset of the root top face (taper direction)
      tip_length [radius]: radius of the quarter-cylinder tip
      tip_angle [angle_deg]: rotation of the quarter cylinder (unused in base version)
      position, rotation: global transform
    """
    def __init__(self, root_size, root_z_offset, tip_length, tip_angle,
                 position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        tip_angle = [x / 180 * np.pi for x in tip_angle]
        super().__init__(position, rotation)

        self.root_size = root_size
        self.root_z_offset = root_z_offset
        self.tip_length = tip_length
        self.tip_angle = tip_angle

        rw, rh, rd_back, rd_front = root_size
        rz = root_z_offset[0]
        tip_r = tip_length[0]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # root — tapered cuboid
        self.mesh = Cuboid(rh, rw, rd_back, rw, rd_front,
                           top_offset=[0, rz],
                           position=[0, rh / 2, 0])
        vertices_list.append(self.mesh.vertices)
        faces_list.append(self.mesh.faces + total_num_vertices)
        total_num_vertices += len(self.mesh.vertices)

        # tip — quarter cylinder curving the blade edge
        tip_mesh_position = [0, rh, rz - rd_back / 2]
        tip_mesh_rotation = [0, 0, np.pi / 2]
        self.tip_mesh = Cylinder(rw, tip_r, tip_r, rd_back, rd_back,
                                 is_quarter=True,
                                 position=tip_mesh_position,
                                 rotation=tip_mesh_rotation)
        vertices_list.append(self.tip_mesh.vertices)
        faces_list.append(self.tip_mesh.faces + total_num_vertices)
        total_num_vertices += len(self.tip_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Blade'
