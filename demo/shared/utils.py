import numpy as np


def _rot_x(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def _rot_y(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def _rot_z(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def apply_transformation(vertices, position, rotation, rotation_order="XYZ", offset_first=False):
    v = np.asarray(vertices).copy()
    p = np.asarray(position)

    rot_map = {
        "X": _rot_x(rotation[0]),
        "Y": _rot_y(rotation[1]),
        "Z": _rot_z(rotation[2]),
    }

    if offset_first:
        v = v + p

    for axis in rotation_order:
        v = v @ rot_map[axis].T

    if not offset_first:
        v = v + p

    return v


def sample_points_from_vertices(vertices, sample_num):
    """Return a deterministic resampled point set from vertices only."""
    v = np.asarray(vertices)
    if v.size == 0:
        return np.zeros((0, 3), dtype=float)
    if len(v) >= sample_num:
        idx = np.linspace(0, len(v) - 1, sample_num, dtype=int)
        return v[idx]
    reps = int(np.ceil(sample_num / len(v)))
    tiled = np.tile(v, (reps, 1))
    return tiled[:sample_num]
