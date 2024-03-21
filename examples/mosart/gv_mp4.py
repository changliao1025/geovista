import sys
import cftime
import netCDF4 as nc
import numpy as np

sPath_geovista = '/Users/liao313/workspace/python/geovista/src'
sys.path.append(sPath_geovista)
import geovista
import geovista.theme


ds = nc.Dataset("/Users/liao313/workspace/python/geovista/data/mosart/mosart_sag_domain.nc")
xv = ds.variables["xv"][:]
yv = ds.variables["yv"][:]
xv = xv[:, 0]
yv = yv[:, 0]

ds = nc.Dataset("/Users/liao313/workspace/python/geovista/data/mosart/e3sm20240103001.mosart.h1.2019-01-02-00000.nc")
name = "RIVER_DISCHARGE_OVER_LAND_LIQ"
var = ds.variables[name]
data = var[:]
n_steps = data.shape[0]

clim = data.min(), data.max()
clim = (1.0, 150.0)

time = ds.variables["time"]
fmt = "%Y-%m-%d"
dt = cftime.num2date(time[:], time.units, time.calendar)

t = 0
mesh = geovista.Transform.from_unstructured(xv, yv, data=data[t])
scalars = "data"

plotter = geovista.GeoPlotter(off_screen=True)

plotter.open_movie("movie.mp4")

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
