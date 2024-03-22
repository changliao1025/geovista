import os, sys
from pathlib import Path
from os.path import realpath
import netCDF4 as nc

#you only need change the path to the package if if it is not installed in your python environment, 
#this is for testing purpose
sPath_geovista = '/qfs/people/liao313/workspace/python/geovista/src'
#sPath_geovista = '/Users/liao313/workspace/python/geovista/src'
sVariable = 'FLOODED_FRACTION'

sys.path.append(sPath_geovista)

import geovista as gv
import geovista.theme

sPath = str( Path().resolve(2) )
print(sPath)
sWorkspace_data = realpath( sPath +  '/data/mosart/amazon' )
# Load the sample data.

sFilename_domain = sWorkspace_data + '/mosart_amazon_domain.nc'
sFilename_timeseries = sWorkspace_data + '/e3sm20240102001.mosart.h0.2019-01.nc'

dataset = nc.Dataset(sFilename_domain)
# load the lon/lat cell grid
lons = dataset.variables["xv"][:]
lats = dataset.variables["yv"][:]
#reshape to remove the second dimension
ni, nj, nv = lons.shape
lons = lons.reshape(ni, nv)
lats = lats.reshape(ni, nv)  
connectivity = lons.shape   
dataset = nc.Dataset(sFilename_timeseries)
data = dataset.variables[sVariable]
name = sVariable.capitalize()
units = data.units

# Create the mesh from the sample data.
t = 0
mesh = gv.Transform.from_unstructured(lons, lats, data=data[t])
# Plot the mesh.
plotter = gv.GeoPlotter()
sargs = {"title": f"{name} / {units}", 
       "shadow": True,    "title_font_size": 10,    "label_font_size": 10,    "fmt": "%.1f",
}
plotter.add_mesh(mesh, scalar_bar_args=sargs)
plotter.view_xy()
plotter.camera.zoom(1.4)
plotter.add_coastlines()
plotter.add_axes()
plotter.show()
