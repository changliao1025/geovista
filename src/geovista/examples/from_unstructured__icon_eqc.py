#!/usr/bin/env python3
"""
This example demonstrates how to create a mesh from 2-D latitude and longitude
unstructured cell points. The resulting mesh contains triangular cells.

It uses Icosahedral Nonhydrostatic Weather and Climate Model (ICON) global 160km
resolution soil type data, as developed by the Deutscher Wetterdienst (DWD) and
the Max-Planck-Institut für Meteorologie (MPI-M). The data targets the mesh
faces/cells.

Note that, the mesh is transformed to the Equidistant Cylindrical (Plate Carrée)
conformal cylindrical projection..

"""

import matplotlib.pyplot as plt

import geovista as gv
from geovista.pantry import icon_soil
import geovista.theme  # noqa: F401


def main() -> None:
    # load the sample data
    sample = icon_soil()

    # create the mesh from the sample data
    mesh = gv.Transform.from_unstructured(sample.lons, sample.lats, data=sample.data)

    # provide mesh diagnostics via logging
    gv.logger.info("%s", mesh)

    # plot the mesh
    plotter = gv.GeoPlotter(crs=(projection := "+proj=eqc"))
    sargs = dict(title=f"{sample.name} / {sample.units}", shadow=True)
    cmap = plt.cm.get_cmap("cet_CET_L17", lut=9)
    plotter.add_mesh(mesh, cmap=cmap, show_edges=True, scalar_bar_args=sargs)
    plotter.add_axes()
    plotter.add_text(
        f"ICON 160km Resolution Triangular Mesh ({projection})",
        position="upper_left",
        font_size=10,
        shadow=True,
    )
    plotter.view_xy()
    plotter.camera.zoom(1.5)
    plotter.show()


if __name__ == "__main__":
    main()