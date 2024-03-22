import sys
from pathlib import Path
from os.path import realpath
import cftime
import netCDF4 as nc
import numpy as np

sPath_geovista = '/qfs/people/liao313/workspace/python/geovista/src'
#sPath_geovista = '/Users/liao313/workspace/python/geovista/src'

sVariable = 'FLOODED_FRACTION' #choose variable
clim = (0.0, 150.0) #change limit if needed

sys.path.append(sPath_geovista)
import geovista
import geovista.theme

sPath = str( Path().resolve(2) )
print(sPath)
sWorkspace_data = realpath( sPath +  '/data/mosart/amazon' )
# Load the sample data.

sFilename_domain = sWorkspace_data + '/mosart_amazon_domain.nc'
sFilename_animation = sWorkspace_data + '/mosart_amazon_animation_'+sVariable.lower()+'.mp4'

ds = nc.Dataset(sFilename_domain)
xv = ds.variables["xv"][:]
yv = ds.variables["yv"][:]
xv = xv[:, 0]
yv = yv[:, 0]

n_steps = 12
fmt = "%Y-%m-%d"
dt=list()
data=list()
for iMonth in range(1,13,1):
    # convert month to string with padded zero
    sMonth = str(iMonth).zfill(2)
    sFilename = sWorkspace_data + '/e3sm20240102001.mosart.h0.2019-' + sMonth + '.nc'
    ds = nc.Dataset(sFilename)
    var = ds.variables[sVariable]
    data_step = var[:]
    clim = data_step.min(), data_step.max()
    time = ds.variables["time"]
    dt_step = cftime.num2date(time[:], time.units, time.calendar)[0]
    #print(dt_step.strftime(fmt))
    dt.append(dt_step)
    data.append(data_step)

t = 0
mesh = geovista.Transform.from_unstructured(xv, yv, data=data[t])
scalars = "data"

plotter = geovista.GeoPlotter(off_screen=True)

plotter.open_movie(sFilename_animation)

text = dt[t].strftime(fmt)

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
plotter.view_xy()
plotter.camera.zoom(1.4)
plotter.add_axes()

plotter.show(auto_close=False)

for step in range(n_steps):
    print(f"{step} [{n_steps}]")
    mesh[scalars] = np.ravel(data[step])
    mesh.active_scalars_name = scalars
    actor.SetText(3, dt[step].strftime(fmt))
    plotter.write_frame()

plotter.close()
