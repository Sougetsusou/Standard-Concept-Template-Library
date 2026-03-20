import argparse
from pathlib import Path

import trimesh

import laptop_demo


DEMO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = DEMO_ROOT / "artifacts"


def maybe_show_open3d(vertices, faces):
    try:
        import open3d as o3d
    except Exception as exc:
        print(f"Open3D not available ({exc}). Mesh file is still exported.")
        return

    mesh = o3d.geometry.TriangleMesh(
        o3d.utility.Vector3dVector(vertices),
        o3d.utility.Vector3iVector(faces),
    )
    mesh.compute_vertex_normals()
    o3d.visualization.draw_geometries([mesh])


def main():
    parser = argparse.ArgumentParser(description="Visualize or export the laptop demo mesh")
    parser.add_argument(
        "--show",
        action="store_true",
        help="Open an Open3D viewer if open3d is installed",
    )
    parser.add_argument(
        "--output",
        default=str(ARTIFACT_ROOT / "laptop_demo_mesh.obj"),
        help="Output mesh path (.obj/.ply/.stl)",
    )
    args = parser.parse_args()

    prompt = "Create a practical laptop with rectangular base, hinged screen, and two side ports."
    stage1 = laptop_demo.stage1_part_generation(prompt)
    stage2 = laptop_demo.stage2_instance_assembly(stage1)
    stage2_source = getattr(laptop_demo, "FITTED_STAGE2_SOURCE", {"source": "code-default"})

    module = laptop_demo.load_laptop_module()
    vertices, faces, _ = laptop_demo.build_merged_mesh(module, stage2)

    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.output)
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    mesh.export(output_path)

    print(f"Exported mesh: {output_path}")
    print(f"Stage2 source: {stage2_source}")
    print(f"Vertex count: {len(vertices)} | Face count: {len(faces)}")

    if args.show:
        maybe_show_open3d(vertices, faces)


if __name__ == "__main__":
    main()
