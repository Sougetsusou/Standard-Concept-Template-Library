import numpy as np
import trimesh

from demo.shared.base_template import GeometryTemplate
from demo.shared.utils import apply_transformation


class Cuboid(GeometryTemplate):
    def __init__(
        self,
        height,
        top_length,
        top_width=None,
        bottom_length=None,
        bottom_width=None,
        top_offset=None,
        back_height=None,
        position=None,
        rotation=None,
        rotation_order="XYZ",
    ):
        if top_width is None:
            top_width = top_length
        if position is None:
            position = [0, 0, 0]
        if rotation is None:
            rotation = [0, 0, 0]

        super().__init__(position, rotation, rotation_order)
        mesh = trimesh.creation.box(extents=[top_length, height, top_width])
        self.vertices = apply_transformation(mesh.vertices, position, rotation, rotation_order)
        self.faces = mesh.faces


class Cylinder(GeometryTemplate):
    def __init__(
        self,
        height,
        top_radius,
        bottom_radius=None,
        top_radius_z=None,
        bottom_radius_z=None,
        is_half=False,
        is_quarter=False,
        position=None,
        rotation=None,
        rotation_order="XYZ",
    ):
        if position is None:
            position = [0, 0, 0]
        if rotation is None:
            rotation = [0, 0, 0]
        if bottom_radius is None:
            bottom_radius = top_radius

        super().__init__(position, rotation, rotation_order)
        radius = (top_radius + bottom_radius) / 2.0
        mesh = trimesh.creation.cylinder(radius=radius, height=height, sections=48)
        self.vertices = apply_transformation(mesh.vertices, position, rotation, rotation_order)
        self.faces = mesh.faces
