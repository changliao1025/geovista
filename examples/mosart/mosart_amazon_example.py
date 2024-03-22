import os, sys
import netCDF4 as nc
sPath_geovista = '/qfs/people/liao313/workspace/python/geovista/src'
#sPath_geovista = '/Users/liao313/workspace/python/geovista/src'
sys.path.append(sPath_geovista)

import geovista as gv

from geovista.pantry.data import mosart
import geovista.theme

# Load the sample data.

#sample = mosart()
sWorkspace_data = '/compyfs/liao313/e3sm_scratch/sag/e3sm20240103001/run'
sWorkspace_data = '/Users/liao313/workspace/python/geovista/data/mosart'
sFilename_domain = '/compyfs/liao313/04model/e3sm/sag/cases_aux/e3sm20240103001/mosart_sag_domain.nc'
sFilename_domain ="/compyfs/liao313/04model/e3sm/amazon/cases_aux/e3sm20240102001/mosart_amazon_domain.nc"
#fname = "mosart_hexwatershed.nc"
#processor = pooch.Decompress(method="auto", name=fname)
#resource = CACHE.fetch(f"{PANTRY_DATA}/{fname}.bz2", processor=processor)
dataset = nc.Dataset(sFilename_domain)
# load the lon/lat cell grid
lons = dataset.variables["xv"][:]
lats = dataset.variables["yv"][:]
#reshape to remove the second dimension
ni, nj, nv = lons.shape
lons = lons.reshape(ni, nv)
lats = lats.reshape(ni, nv)  
connectivity = lons.shape   
# load the mesh payload
sFilename_timeseries = sWorkspace_data + '/e3sm20240103001.mosart.h1.2019-01-02-00000.nc'
#ds = nc.Dataset("/compyfs/liao313/e3sm_scratch/amazon/e3sm20240102001/run/e3sm20240102001.mosart.h1.2019-01-02-00000.nc")
sFilename_timeseries = '/compyfs/liao313/e3sm_scratch/amazon/e3sm20240102001/run/e3sm20240102001.mosart.h0.2019-12.nc'
dataset = nc.Dataset(sFilename_timeseries)
data = dataset.variables["FLOODED_FRACTION"]

#name = capitalise(data.standard_name)
name = 'MOSART main channel water depth'
units = data.units

# Create the mesh from the sample data.
t = 0
mesh = gv.Transform.from_unstructured(lons, lats, data=data[t])

#mesh = gv.Transform.from_unstructured(sample.lons, sample.lats, data=sample.data)


# Plot the mesh.
plotter = gv.GeoPlotter()
#sargs = {"title": f"{name} / {units}"}
sargs = {
       "shadow": True,    "title_font_size": 10,    "label_font_size": 10,    "fmt": "%.1f",
}
plotter.add_mesh(mesh, scalar_bar_args=sargs)
plotter.view_xy()
plotter.camera.zoom(1.4)
plotter.add_coastlines()
plotter.add_axes()
plotter.show()
