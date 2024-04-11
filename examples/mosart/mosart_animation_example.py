import os, sys
from pathlib import Path
from os.path import realpath
import cftime
import netCDF4 as nc
import numpy as np
sPath = str( Path().resolve(2) )
print(sPath)
iFlag_platform = 3
iFlag_monthly = 1
sVariable = 'FLOODED_FRACTION'
#sVariable = 'Main_Channel_Water_Depth_LIQ'

#clim = (0.0, 1.0) #change limit if needed
    
sCase = 'e3sm20240102001' #diffusive wave method
#sCase = 'e3sm20240102002' #kinetic wave method
#sCase = 'e3sm20240102003' #kinetic wave method with 50 twid
iYear_start = 2000
iYear_end = 2019

sYear_start = '{:04}'.format(iYear_start)
sYear_end = '{:04}'.format(iYear_end)

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
        sWorkspace_data = os.path.join( r"Z:\e3sm_scratch\amazon" , sCase  ,  "run" )
        sWorkspace_data_aux = os.path.join(r"Z:\04model\e3sm\amazon\cases_aux" , sCase  )
        sWorkspace_analysis = os.path.join(r"Z:\04model\e3sm\amazon\analysis" , sCase  )

sys.path.append(sPath_geovista)
import geovista
import geovista.theme

sFilename_domain = os.path.join(sWorkspace_data_aux , 'mosart_amazon_domain.nc')
sFilename_animation = os.path.join(sWorkspace_analysis , 'mosart_amazon_animation_'+sVariable.lower()+'.mp4' )

ds = nc.Dataset(sFilename_domain)
xv = ds.variables["xv"][:]
yv = ds.variables["yv"][:]
xv = xv[:, 0]
yv = yv[:, 0]

fmt = "%Y-%m-%d"

date_list = list()
data_list=list()
clim = [float('inf'), float('-inf')]
if iFlag_monthly ==1:
    n_steps = 12 * (iYear_end - iYear_start + 1)
    for iYear in range(iYear_start,iYear_end+1,1):
        sYear = '{:04}'.format(iYear)
        for iMonth in range(1,13,1):
            # convert month to string with padded zero
            sMonth = str(iMonth).zfill(2)
            sFilename = os.path.join(sWorkspace_data , sCase +'.mosart.h0.'+sYear+'-' + sMonth + '.nc' )
            ds = nc.Dataset(sFilename)
            var = ds.variables[sVariable]
            data_step = var[:]
            # Update clim with the minimum and maximum of the current data
            clim[0] = min(clim[0], data_step.min())
            clim[1] = max(clim[1], data_step.max())
            time = ds.variables["time"]
            dt_step = cftime.num2date(time[:], time.units, time.calendar)
            date_list.extend(dt_step)
            data_list.extend(data_step)
else:
    n_steps = 365 * (iYear_end - iYear_start + 1)
    for iYear in range(iYear_start,iYear_end+1,1):
        sYear = '{:04}'.format(iYear)
        sFilename_timeseries = os.path.join(sWorkspace_data , sCase +'.mosart.h1.'+sYear+'-01-02-00000.nc')
        if not os.path.exists(sFilename_timeseries):
            print(sFilename_timeseries)
            exit
        ds = nc.Dataset(sFilename_timeseries)
        var = ds.variables[sVariable]
        data_step = var[:]
        # Update clim with the minimum and maximum of the current data
        clim[0] = min(clim[0], data_step.min())
        clim[1] = max(clim[1], data_step.max())
        time = ds.variables["time"]
        dt_step = cftime.num2date(time[:], time.units, time.calendar)
        date_list.extend(dt_step)
        data_list.extend(data_step)

t = 0
mesh = geovista.Transform.from_unstructured(xv, yv, data=data_list[t])
scalars = "data"
plotter = geovista.GeoPlotter(off_screen=True)

plotter.open_movie(sFilename_animation)
text = date_list[t].strftime(fmt)
actor = plotter.add_text(
    text, position="upper_right", font_size=10, color="black", shadow=False
)

sargs = {
    "title": f"{var.long_name} [{var.units}]",
    "shadow": True,
    "title_font_size": 10,
    "label_font_size": 10,
    "fmt": "%.1f",
}
plotter.add_mesh(
    mesh,
    show_edges=True,
    cmap="deep",
    clim=clim,
    below_color="gray",
    above_color="red",
    scalar_bar_args=sargs,
    name=scalars,
)

center_lon = np.mean(xv[np.where(xv != -9999)])
center_lat = np.mean(yv[np.where(yv != -9999)])
center_lat = np.deg2rad(center_lat)
center_lon = np.deg2rad(center_lon)
x = np.cos(center_lat) * np.cos(center_lon)
y = np.cos(center_lat) * np.sin(center_lon)
z = np.sin(center_lat)
plotter.camera.focal_point = [-x,-y,-z]
plotter.camera.position =np.array([x,y,z]) * 2.6
plotter.camera.zoom(1.5)
plotter.add_axes()

plotter.show(auto_close=False)

for step in range(n_steps):
    #print(f"{step} [{n_steps}]")
    mesh[scalars] = np.ravel(data_list[step])
    mesh.active_scalars_name = scalars
    actor.SetText(3, date_list[step].strftime(fmt))
    plotter.write_frame()

plotter.close()
