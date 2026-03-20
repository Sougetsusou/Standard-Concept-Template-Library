import numpy as np
import trimesh

from demo.shared.base_template import ConceptTemplate
from demo.shared.geometry_template import Cuboid
from demo.shared.knowledge_utils import SAMPLENUM
from demo.shared.utils import apply_transformation


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
                self.mesh_1 = Cuboid(
                    h1,
                    w1,
                    d1,
                    position=[ox, -h0 - h1 / 2 + oy, oz - d0 / 2],
                )
                vertices_list.append(self.mesh_1.vertices)
                faces_list.append(self.mesh_1.faces + total_num_vertices)
                total_num_vertices += len(self.mesh_1.vertices)

            self.vertices = np.concatenate(vertices_list)
            self.faces = np.concatenate(faces_list)

            # offset_first=True: translation applied before rotation
            self.vertices = apply_transformation(
                self.vertices,
                position,
                rotation,
                rotation_order="YXZ",
                offset_first=True,
            )

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = "Base"
