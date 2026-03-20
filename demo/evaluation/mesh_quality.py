import numpy as np


def check_mesh_non_degenerate(vertices, faces):
    """Return a tuple (ok, checks) for basic mesh validity."""
    v = np.asarray(vertices)
    f = np.asarray(faces)

    checks = {
        "has_vertices": bool(v.size > 0),
        "has_faces": bool(f.size > 0),
        "finite_vertices": bool(np.isfinite(v).all()) if v.size else False,
        "valid_vertex_shape": bool(v.ndim == 2 and v.shape[1] == 3) if v.size else False,
        "valid_face_shape": bool(f.ndim == 2 and f.shape[1] == 3) if f.size else False,
    }
    ok = all(checks.values())
    return ok, checks
