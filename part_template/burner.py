import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation
from knowledge_utils import *


class Top_With_Burner(ConceptTemplate):
    """
    Semantic: Burner
    Geometry: flat cuboid cooktop surface + up to 6 burners, each consisting of a
              Rectangular_Ring outer ring and a Cylinder central knob
    Used by: Oven
    Parameters:
      bottom_size [w, h, d]: dimensions of the cooktop surface
      burner_N_size [w, h, d]: outer dimensions of burner N's ring (N = 1..6)
      burner_N_thickness [t]: wall thickness of burner N's ring
      burner_N_offset [x, z]: XZ position of burner N on the cooktop
      burner_N_central_size [radius, h]: radius and height of burner N's central knob
      burner_N_central_offset [x, z]: XZ offset of the central knob within burner N
      num_burners [n]: number of active burners (1..6)
      position, rotation: global transform
    """
    def __init__(self, bottom_size,
                 burner_1_size, burner_1_thickness, burner_1_offset,
                 burner_1_central_size, burner_1_central_offset,
                 burner_2_size, burner_2_thickness, burner_2_offset,
                 burner_2_central_size, burner_2_central_offset,
                 burner_3_size, burner_3_thickness, burner_3_offset,
                 burner_3_central_size, burner_3_central_offset,
                 burner_4_size, burner_4_thickness, burner_4_offset,
                 burner_4_central_size, burner_4_central_offset,
                 burner_5_size, burner_5_thickness, burner_5_offset,
                 burner_5_central_size, burner_5_central_offset,
                 burner_6_size, burner_6_thickness, burner_6_offset,
                 burner_6_central_size, burner_6_central_offset,
                 num_burners, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        super().__init__(position, rotation)

        self.bottom_size = bottom_size
        self.num_burners = num_burners

        bw, bh, bd = bottom_size
        n = int(num_burners[0])

        # collect per-burner params into lists for loop access
        burner_sizes    = [burner_1_size,    burner_2_size,    burner_3_size,
                           burner_4_size,    burner_5_size,    burner_6_size]
        burner_thicks   = [burner_1_thickness, burner_2_thickness, burner_3_thickness,
                           burner_4_thickness, burner_5_thickness, burner_6_thickness]
        burner_offsets  = [burner_1_offset,  burner_2_offset,  burner_3_offset,
                           burner_4_offset,  burner_5_offset,  burner_6_offset]
        central_sizes   = [burner_1_central_size,   burner_2_central_size,
                           burner_3_central_size,   burner_4_central_size,
                           burner_5_central_size,   burner_6_central_size]
        central_offsets = [burner_1_central_offset, burner_2_central_offset,
                           burner_3_central_offset, burner_4_central_offset,
                           burner_5_central_offset, burner_6_central_offset]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        # cooktop surface
        tmp_mesh = Cuboid(bh, bw, bd, position=[0, bh / 2, 0])
        vertices_list.append(tmp_mesh.vertices)
        faces_list.append(tmp_mesh.faces + total_num_vertices)
        total_num_vertices += len(tmp_mesh.vertices)

        for i in range(n):
            bsz = burner_sizes[i]
            bt  = burner_thicks[i]
            bof = burner_offsets[i]
            csz = central_sizes[i]
            cof = central_offsets[i]

            bsw, bsh, bsd = bsz
            thick = bt[0]
            c_r, c_h = csz[0], csz[1]

            # outer burner ring
            ring_pos = [bof[0], bh + bsh / 2, bof[1]]
            tmp_mesh = Rectangular_Ring(bsh, bsw, bsd,
                                        bsw - thick * 2, bsd - thick * 2,
                                        position=ring_pos)
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

            # central knob cylinder
            knob_pos = [bof[0] + cof[0], bh + c_h / 2, bof[1] + cof[1]]
            tmp_mesh = Cylinder(c_h, c_r, position=knob_pos)
            vertices_list.append(tmp_mesh.vertices)
            faces_list.append(tmp_mesh.faces + total_num_vertices)
            total_num_vertices += len(tmp_mesh.vertices)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Burner'
