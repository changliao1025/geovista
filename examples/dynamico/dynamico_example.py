import os, sys

sPath_geovista = '/qfs/people/liao313/workspace/python/geovista/src'
sys.path.append(sPath_geovista)
import geovista as gv
from geovista.pantry.data import dynamico
import geovista.theme

# Load sample data.
sample = dynamico()

# Create the mesh from the sample data.
mesh = gv.Transform.from_unstructured(sample.lons, sample.lats, data=sample.data)

# Plot the mesh.
plotter = gv.GeoPlotter()
sargs = {"title": f"{sample.name} / {sample.units}"}
plotter.add_mesh(mesh, scalar_bar_args=sargs)
plotter.add_coastlines()
plotter.add_axes()
plotter.show()