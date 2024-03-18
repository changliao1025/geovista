import os, sys

sPath_geovista = '/qfs/people/liao313/workspace/python/geovista/src'
sys.path.append(sPath_geovista)

import geovista as gv
#from geovista.pantry.data import fvcom_tamar
from geovista.pantry.data import mosart
import geovista.theme

# Load the sample data.
#sample = fvcom_tamar()
sample = mosart()

# Create the mesh from the sample data.
mesh = gv.Transform.from_unstructured(
    sample.lons,
    sample.lats,
    connectivity=sample.connectivity,
    data=sample.face,
    name="face",
)

# Warp the mesh nodes by the bathymetry.
mesh = gv.Transform.from_unstructured(sample.lons, sample.lats, data=sample.data)

# Plot the mesh.
plotter = gv.GeoPlotter()
sargs = {"title": f"{sample.name} / {sample.units}"}
plotter.add_mesh(mesh, cmap="deep", scalar_bar_args=sargs)
plotter.add_axes()
#plotter.show()
plotter.save("mosart_sag_example.png")