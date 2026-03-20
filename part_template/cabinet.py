import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared'))

import numpy as np
import trimesh
from base_template import ConceptTemplate
from geometry_template import *
from utils import apply_transformation, adjust_position_from_rotation, list_add
from knowledge_utils import *


class Regular_cabinet(ConceptTemplate):
    """
    Semantic: Cabinet
    Geometry: up to 2 top cabinets + up to 2 beneath cabinets, each built from:
              5 body cuboids (2 side walls + 2 top/bottom panels + 1 back panel) +
              N shelf layers + per-space drawers (5 cuboids + handles) or doors (panel + handle)
    Used by: Table
    Parameters:
      number_of_top_cabinet [n]: number of top cabinets (0..2)
      number_of_beneath_cabinet [n]: number of beneath cabinets (0..2)
      cab_backs_size [t, ...]: back panel thickness per cabinet
      cab_left_right_inner_sizes [t, ...]: side wall thickness per cabinet
      cab_up_down_inner_sizes [t, ...]: top/bottom panel thickness per cabinet
      drawer_inner_sizes [side_t, front_t]: drawer side and front wall thickness (shared)
      drawer_bottom_size [t]: drawer bottom panel thickness (shared)
      door_sizes [t]: door panel thickness (shared)
      number_of_layers [n, ...]: number of shelf layers per cabinet
      layers_sizes [t, ...]: shelf thickness per cabinet
      layers_offset [y, ...]: Y offset of first shelf from top per cabinet
      interval_between_layers [dy, ...]: Y spacing between shelves per cabinet
      cabinets_params [flat list]: stride-56 per-cabinet parameters (see source)
      position, rotation: global transform
    """
    def __init__(self, number_of_top_cabinet, number_of_beneath_cabinet,
                 cab_backs_size, cab_left_right_inner_sizes, cab_up_down_inner_sizes,
                 drawer_inner_sizes, drawer_bottom_size, door_sizes,
                 number_of_layers, layers_sizes, layers_offset, interval_between_layers,
                 cabinets_params, position=[0, 0, 0], rotation=[0, 0, 0]):

        rotation = [x / 180 * np.pi for x in rotation]
        cabinets_params = [x / 180 * np.pi if i % 56 in [22, 23, 24, 25, 41, 42, 43, 44] else x
                           for i, x in enumerate(cabinets_params)]
        super().__init__(position, rotation)

        self.number_of_top_cabinet    = number_of_top_cabinet[0]
        self.number_of_beneath_cabinet = number_of_beneath_cabinet[0]
        self.cab_backs_size            = cab_backs_size
        self.cab_left_right_inner_sizes = cab_left_right_inner_sizes
        self.cab_up_down_inner_sizes   = cab_up_down_inner_sizes
        self.drawer_inner_sizes        = drawer_inner_sizes
        self.drawer_bottom_size        = drawer_bottom_size
        self.door_sizes                = door_sizes
        self.number_of_layers          = number_of_layers
        self.layers_sizes              = layers_sizes
        self.layers_offset             = layers_offset
        self.interval_between_layers   = interval_between_layers

        ntop = int(self.number_of_top_cabinet)
        nbot = int(self.number_of_beneath_cabinet)

        def _unpack(i):
            base = i * 56
            return {
                'size':                    cabinets_params[base:     base + 3],
                'type_of_spaces':          cabinets_params[base + 3:  base + 7],
                'drawer_interval':         cabinets_params[base + 7:  base + 11],
                'drawer_offset':           cabinets_params[base + 11: base + 15],
                'drawer_number_of_handles': cabinets_params[base + 15: base + 19],
                'drawer_handles_size':     cabinets_params[base + 19: base + 22],
                'drawer_handles_rotation': cabinets_params[base + 22: base + 26],
                'drawer_handles_separation': cabinets_params[base + 26: base + 30],
                'drawer_handles_offsets':  list(zip(cabinets_params[base + 30: base + 34],
                                                    cabinets_params[base + 34: base + 38])),
                'door_handles_size':       cabinets_params[base + 38: base + 41],
                'door_handles_rotation':   cabinets_params[base + 41: base + 45],
                'door_handles_offsets':    list(zip(cabinets_params[base + 45: base + 49],
                                                    cabinets_params[base + 49: base + 53])),
                'cabinet_offset':          cabinets_params[base + 53: base + 56],
            }

        # top cabinets use indices 0,1; beneath cabinets use indices 2,3
        top_cabs    = [_unpack(i)       for i in range(ntop)]
        beneath_cabs = [_unpack(2 + i)  for i in range(nbot)]

        vertices_list = []
        faces_list = []
        total_num_vertices = 0

        def _add(mesh):
            nonlocal total_num_vertices
            vertices_list.append(mesh.vertices)
            faces_list.append(mesh.faces + total_num_vertices)
            total_num_vertices += len(mesh.vertices)

        # ── top cabinets ──────────────────────────────────────────────────────
        for ci, cab in enumerate(top_cabs):
            actual_idx = ci
            csz  = cab['size']
            coff = cab['cabinet_offset']
            lr   = cab_left_right_inner_sizes[actual_idx]
            ud   = cab_up_down_inner_sizes[actual_idx]
            back = cab_backs_size[actual_idx]
            nl   = int(number_of_layers[actual_idx])

            # 5 body cuboids
            for mi in range(5):
                sign = -1 if mi % 2 == 0 else 1
                if mi < 2:
                    pos = [sign * (csz[0] - lr) / 2 + coff[0],
                           coff[1] - csz[1] / 2,
                           coff[2]]
                    tmp = Cuboid(csz[1], lr, csz[2], position=pos)
                elif mi < 4:
                    pos = [coff[0],
                           sign * (csz[1] - ud) / 2 + coff[1] - csz[1] / 2,
                           coff[2]]
                    tmp = Cuboid(ud, csz[0] - 2 * lr, csz[2], position=pos)
                else:
                    pos = [coff[0],
                           coff[1] - csz[1] / 2,
                           coff[2] - (csz[2] + back) / 2]
                    tmp = Cuboid(csz[1], csz[0], back, position=pos)
                tmp.vertices[:, 1] += csz[1] / 2
                if ntop == 2:
                    tmp.vertices[:, 0] += (csz[0] / 2 if ci % 2 == 0 else -csz[0] / 2)
                _add(tmp)

            # shelf layers
            for li in range(nl):
                pos = [coff[0],
                       -(layers_offset[actual_idx] + li * interval_between_layers[actual_idx]) - csz[1] / 2,
                       coff[2]]
                tmp = Cuboid(layers_sizes[actual_idx], csz[0] - 2 * lr, csz[2], position=pos)
                tmp.vertices[:, 1] += csz[1] / 2
                if ntop == 2:
                    tmp.vertices[:, 0] += (csz[0] / 2 if ci % 2 == 0 else -csz[0] / 2)
                _add(tmp)

            # spaces (drawers / doors)
            for si in range(nl + 1):
                if nl == 0:
                    _h  = csz[1] - 2 * ud
                    _py = 0
                elif si == 0:
                    _h  = layers_offset[actual_idx] - ud - layers_sizes[actual_idx] / 2
                    _py = csz[1] - layers_offset[actual_idx] / 2 - ud / 2 + layers_sizes[actual_idx] / 4
                elif si == nl:
                    _h  = csz[1] - (layers_offset[actual_idx] + (si - 1) * interval_between_layers[actual_idx]) - ud - layers_sizes[actual_idx] / 2
                    _py = ud + _h / 2 - 5
                else:
                    _h  = interval_between_layers[0] - layers_sizes[actual_idx]
                    _py = csz[1] - layers_offset[actual_idx] - (2 * si - 1) / 2 * interval_between_layers[0]

                space_type = cab['type_of_spaces'][si]

                if space_type == 1:
                    nhandles = cab['drawer_number_of_handles'][si]
                    for mi in range(int(5 + nhandles)):
                        if mi < 2:
                            sign = -1 if mi == 0 else 1
                            pos = [sign * (csz[0] / 2 - lr - drawer_inner_sizes[0] / 2) + coff[0],
                                   _py + coff[1] - csz[1] / 2,
                                   coff[2] + cab['drawer_offset'][si] + cab['drawer_interval'][si] / 2]
                            tmp = Cuboid(_h, drawer_inner_sizes[0],
                                         csz[2] - cab['drawer_interval'][si], position=pos)
                        elif mi < 4:
                            sign = -1 if mi == 3 else 1
                            pos = [coff[0],
                                   _py + coff[1] - csz[1] / 2,
                                   coff[2] + sign * (csz[2] - drawer_inner_sizes[1]) / 2]
                            tmp = Cuboid(_h,
                                         csz[0] - 2 * lr - 2 * drawer_inner_sizes[0],
                                         drawer_inner_sizes[1], position=pos)
                        elif mi == 4:
                            pos = [coff[0],
                                   _py + coff[1] - (_h + drawer_bottom_size[0]) / 2 - csz[1] / 2,
                                   coff[2] + cab['drawer_interval'][si] / 2 + cab['drawer_offset'][si]]
                            tmp = Cuboid(drawer_bottom_size[0], csz[0] - 2 * lr,
                                         csz[2] - cab['drawer_interval'][si], position=pos)
                        else:
                            sign = (1 if mi == 5 else -1) if nhandles == 2 else 0
                            rot  = [0, 0, cab['drawer_handles_rotation'][si]]
                            hoff = cab['drawer_handles_offsets'][si]
                            pos  = [coff[0] + hoff[0] + sign * cab['drawer_handles_separation'][si],
                                    _py + coff[1] + hoff[1] - csz[1] / 2,
                                    coff[2] + (csz[2] + cab['drawer_handles_size'][2]) / 2 + cab['drawer_offset'][si]]
                            tmp  = Cuboid(cab['drawer_handles_size'][1],
                                          cab['drawer_handles_size'][0],
                                          cab['drawer_handles_size'][2],
                                          position=pos, rotation=rot)
                        tmp.vertices[:, 1] += csz[1] / 2
                        if ntop == 2:
                            tmp.vertices[:, 0] += (csz[0] / 2 if ci % 2 == 0 else -csz[0] / 2)
                        _add(tmp)

                elif space_type == 2:
                    for mi in range(2):
                        if mi == 0:
                            pos = [coff[0],
                                   _py + coff[1],
                                   coff[2] + (csz[2] + door_sizes[0]) / 2]
                            tmp = Cuboid(_h, csz[0] - 2 * lr, door_sizes[0], position=pos)
                        else:
                            rot  = [0, 0, cab['door_handles_rotation'][si]]
                            hoff = cab['door_handles_offsets'][si]
                            pos  = [coff[0] + hoff[0],
                                    _py + coff[1] + hoff[1],
                                    coff[2] + (csz[2] + door_sizes[0]) / 2 + (cab['door_handles_size'][2] + door_sizes[0]) / 2]
                            tmp  = Cuboid(cab['door_handles_size'][1],
                                          cab['door_handles_size'][0],
                                          cab['door_handles_size'][2],
                                          position=pos, rotation=rot)
                        tmp.vertices[:, 1] += csz[1] / 2
                        if ntop == 2:
                            tmp.vertices[:, 0] += (csz[0] / 2 if ci % 2 == 0 else -csz[0] / 2)
                        _add(tmp)

        # ── beneath cabinets ──────────────────────────────────────────────────
        for ci, cab in enumerate(beneath_cabs):
            actual_idx = 2 + ci
            csz  = cab['size']
            coff = cab['cabinet_offset']
            lr   = cab_left_right_inner_sizes[actual_idx]
            ud   = cab_up_down_inner_sizes[actual_idx]
            back = cab_backs_size[actual_idx]
            nl   = int(number_of_layers[actual_idx])

            # 5 body cuboids
            for mi in range(5):
                sign = -1 if mi % 2 == 0 else 1
                if mi < 2:
                    pos = [sign * (csz[0] - lr) / 2 + coff[0],
                           coff[1],
                           coff[2]]
                    tmp = Cuboid(csz[1], lr, csz[2], position=pos)
                elif mi < 4:
                    pos = [coff[0],
                           sign * (csz[1] - ud) / 2 + coff[1],
                           coff[2]]
                    tmp = Cuboid(ud, csz[0] - 2 * lr, csz[2], position=pos)
                else:
                    if back != 0:
                        pos = [coff[0], coff[1],
                               coff[2] - (csz[2] + back) / 2]
                        tmp = Cuboid(csz[1], csz[0], back, position=pos)
                    else:
                        continue
                _add(tmp)

            # shelf layers
            for li in range(nl):
                pos = [coff[0],
                       coff[1] + csz[1] / 2 - (layers_offset[actual_idx] + li * interval_between_layers[actual_idx]),
                       coff[2]]
                tmp = Cuboid(layers_sizes[actual_idx], csz[0] - 2 * lr, csz[2], position=pos)
                _add(tmp)

            # spaces (drawers / doors)
            for si in range(nl + 1):
                if nl == 0:
                    _h  = csz[1] - 2 * ud
                    _py = csz[1] / 2
                elif si == 0:
                    _h  = layers_offset[actual_idx] - ud - layers_sizes[actual_idx] / 2
                    _py = csz[1] - layers_offset[actual_idx] / 2 - ud / 2 + layers_sizes[actual_idx] / 4
                elif si == nl:
                    _h  = csz[1] - (layers_offset[actual_idx] + (si - 1) * interval_between_layers[0]) - ud - layers_sizes[actual_idx] / 2
                    _py = ud + _h / 2
                else:
                    _h  = interval_between_layers[0] - layers_sizes[actual_idx]
                    _py = csz[1] - layers_offset[actual_idx] - (2 * si - 1) / 2 * interval_between_layers[0]

                space_type = cab['type_of_spaces'][si]

                if space_type == 1:
                    nhandles = cab['drawer_number_of_handles'][si]
                    for mi in range(int(5 + nhandles)):
                        if mi < 2:
                            sign = -1 if mi == 0 else 1
                            pos = [sign * (csz[0] / 2 - lr - drawer_inner_sizes[0] / 2) + coff[0],
                                   _py + coff[1],
                                   coff[2] + cab['drawer_offset'][si] + cab['drawer_interval'][si] / 2]
                            tmp = Cuboid(_h, drawer_inner_sizes[0],
                                         csz[2] - cab['drawer_interval'][si], position=pos)
                        elif mi < 4:
                            sign = -1 if mi == 3 else 1
                            pos = [coff[0],
                                   _py + coff[1],
                                   coff[2] + sign * (csz[2] - drawer_inner_sizes[1]) / 2 + cab['drawer_offset'][si]]
                            tmp = Cuboid(_h,
                                         csz[0] - 2 * lr - 2 * drawer_inner_sizes[0],
                                         drawer_inner_sizes[1], position=pos)
                        elif mi == 4:
                            pos = [coff[0],
                                   _py + coff[1] - (_h + drawer_bottom_size[0]) / 2,
                                   coff[2] + cab['drawer_interval'][si] / 2 + cab['drawer_offset'][si]]
                            tmp = Cuboid(drawer_bottom_size[0], csz[0] - 2 * lr,
                                         csz[2] - cab['drawer_interval'][si], position=pos)
                        else:
                            sign = (1 if mi == 5 else -1) if nhandles == 2 else 0
                            rot  = [0, 0, cab['drawer_handles_rotation'][si]]
                            hoff = cab['drawer_handles_offsets'][si]
                            pos  = [coff[0] + hoff[0] + sign * cab['drawer_handles_separation'][si],
                                    _py + coff[1] + hoff[1],
                                    coff[2] + (csz[2] + cab['drawer_handles_size'][2]) / 2 + cab['drawer_offset'][si]]
                            tmp  = Cuboid(cab['drawer_handles_size'][1],
                                          cab['drawer_handles_size'][0],
                                          cab['drawer_handles_size'][2],
                                          position=pos, rotation=rot)
                        tmp.vertices[:, 1] -= csz[1] / 2
                        _add(tmp)

                elif space_type == 2:
                    for mi in range(2):
                        if mi == 0:
                            pos = [coff[0],
                                   _py + coff[1],
                                   coff[2] + (csz[2] + door_sizes[0]) / 2]
                            tmp = Cuboid(_h, csz[0] - 2 * lr, door_sizes[0], position=pos)
                        else:
                            rot  = [0, 0, cab['door_handles_rotation'][si]]
                            hoff = cab['door_handles_offsets'][si]
                            pos  = [coff[0] + hoff[0],
                                    _py + coff[1] + hoff[1],
                                    coff[2] + (csz[2] + door_sizes[0]) / 2 + (cab['door_handles_size'][2] + door_sizes[0]) / 2]
                            tmp  = Cuboid(cab['door_handles_size'][1],
                                          cab['door_handles_size'][0],
                                          cab['door_handles_size'][2],
                                          position=pos, rotation=rot)
                        tmp.vertices[:, 1] -= csz[1] / 2
                        _add(tmp)

        self.vertices = np.concatenate(vertices_list)
        self.faces = np.concatenate(faces_list)

        self.vertices = apply_transformation(self.vertices, position, rotation)

        self.overall_obj_mesh = trimesh.Trimesh(self.vertices, self.faces)
        self.overall_obj_pts = np.array(self.overall_obj_mesh.sample(SAMPLENUM))

        self.semantic = 'Cabinet'
