import pyvista as pv
import numpy as np

# generate random plane
rng = np.random.default_rng()
center, direction = rng.uniform(size=(2, 3)) * 2 - 1
plane = pv.Plane(center=center, direction=direction)

plotter = pv.Plotter()
plotter.add_mesh(plane)

# find the plane's center and normal from scratch
center = plane.center
normal = plane.compute_normals()['Normals'].mean(axis=0)

# align camera: focus on center, position at center + normal
plotter.camera.focal_point = center
p = center + normal
plotter.camera.position = center + normal

# reset camera to put entire mesh in view
plotter.reset_camera()

plotter.show()