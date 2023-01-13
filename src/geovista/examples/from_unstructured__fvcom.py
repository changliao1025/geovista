#!/usr/bin/env python3
"""
This example demonstrates how to create a mesh from 1-D latitude and longitude
unstructured cell points. The resulting mesh contains triangular cells.

It uses an unstructured grid Finite Volume Community Ocean Model (FVCOM) mesh of
sea floor depth below geoid data.

Note that, the data is on the mesh faces/cells, but also on the nodes/points
which can then be used to extrude the mesh to reveal the bathymetry of the
Plymouth Sound and Tamar River in Cornwall, UK.

"""

import geovista as gv
from geovista.pantry import fvcom_tamar
import geovista.theme  # noqa: F401


def main() -> None:
    # load the sample data
    sample = fvcom_tamar()

    # create the mesh from the sample data
    mesh = gv.Transform.from_unstructured(
        sample.lons,
        sample.lats,
        connectivity=sample.connectivity,
        data=sample.face,
        name="face",
    )

    # warp the mesh nodes by the bathymetry
    mesh.point_data["node"] = sample.node
    mesh.compute_normals(cell_normals=False, point_normals=True, inplace=True)
    mesh.warp_by_scalar(scalars="node", inplace=True, factor=2e-5)

    # plot the mesh
    plotter = gv.GeoPlotter()
    sargs = dict(title=f"{sample.name} / {sample.units}", shadow=True)
    plotter.add_mesh(mesh, scalars="face", show_edges=True, scalar_bar_args=sargs)
    plotter.add_axes()
    plotter.add_text(
        "PML FVCOM Tamar",
        position="upper_left",
        font_size=10,
        shadow=True,
    )
    plotter.show()


if __name__ == "__main__":
    main()
