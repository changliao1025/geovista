import os, sys
from pathlib import Path
from os.path import realpath
import numpy as np
import netCDF4 as nc

#you only need change the path to the package if if it is not installed in your python environment,
#this is for testing purpose
sPath = str( Path().resolve(2) )
print(sPath)
iFlag_platform = 1 #debug from window
iFlag_monthly = 1 #only check monthly data
if iFlag_monthly ==0:
    sVariable = 'FLOODED_FRACTION'
    sVariable = 'Main_Channel_Water_Depth_LIQ'
else:
    sVariable = 'Main_Channel_Water_Depth_LIQ'

sCase = 'e3sm20240102001'
sYear = '2019'

if iFlag_platform == 1:
    sPath_geovista = '/qfs/people/liao313/workspace/python/geovista/src' #linux hpc
    sWorkspace_data = realpath( sPath +  '/data/mosart/amazon' )
    sWorkspace_data_aux = sWorkspace_data
else:
    if iFlag_platform ==2:
       sPath_geovista = '/Users/liao313/workspace/python/geovista/src' #mac
       sWorkspace_data = realpath( sPath +  '/data/mosart/amazon' )
       sWorkspace_data_aux = sWorkspace_data
    else:
       sPath_geovista = 'C:\workspace\python\geovista\src'  #windows, we may also use mapped driver as data source
       sWorkspace_data_aux = os.path.join(r"Z:\04model\e3sm\amazon\cases_aux" , sCase  )
       sWorkspace_data = os.path.join( r"Z:\e3sm_scratch\amazon" , sCase  ,  "run" )


sys.path.append(sPath_geovista)

import geovista as gv
import geovista.theme

# Load the sample data.

sFilename_domain = sWorkspace_data_aux + '/mosart_amazon_domain.nc'
if iFlag_monthly == 1:
    sFilename_timeseries = os.path.join( sWorkspace_data , sCase+'.mosart.h0.'+sYear+'-01.nc')
else:
    sFilename_timeseries = os.path.join( sWorkspace_data , sCase+'.mosart.h1.'+sYear+'-01-02-00000.nc')

print(sFilename_timeseries)

dataset = nc.Dataset(sFilename_domain)
# load the lon/lat cell grid
lons = dataset.variables["xv"][:]
lats = dataset.variables["yv"][:]
#reshape to remove the second dimension
ni, nj, nv = lons.shape
lons = lons.reshape(ni, nv)
lats = lats.reshape(ni, nv)
connectivity = lons.shape
#check the file existing or not
if not os.path.exists(sFilename_timeseries):
    print(sFilename_timeseries)
    exit

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

# Calculate the center
center_lat = np.mean(lats[np.where(lats != -9999)])
center_lon = np.mean(lons[np.where(lats != -9999)])
center_lat = np.deg2rad(center_lat)
center_lon = np.deg2rad(center_lon)
x =  np.cos(center_lat) * np.cos(center_lon)
y =  np.cos(center_lat) * np.sin(center_lon)
z =  np.sin(center_lat)
print(x, y, z)
plotter.camera.focal_point = [-x,-y,-z]
plotter.camera.position =np.array([x,y,z]) * 2.6
plotter.camera.zoom(1.5)
plotter.add_coastlines()
plotter.add_axes()
#plotter.reset_camera()
plotter.show()
