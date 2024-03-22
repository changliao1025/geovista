
@lru_cache(maxsize=LRU_CACHE_SIZE)
def mosart(step: int | None = None) -> SampleUnstructuredXY:
    """Download and cache unstructured surface sample data.

    Load the MOSART unstructured hexagonal watershed mesh.

    Returns
    -------
    SampleUnstructuredXY
        The unstructured spatial coordinates and data payload.

    Notes
    -----
    .. versionadded:: 0.1.0

    """
    fname = "mosart_domain.nc"
    processor = pooch.Decompress(method="auto", name=fname)
    resource = CACHE.fetch(f"{PANTRY_DATA}/{fname}.bz2", processor=processor)
    dataset = nc.Dataset(resource)

    # load the lon/lat cell grid
    lons = dataset.variables["xv"][:]
    lats = dataset.variables["yv"][:]

    #reshape to remove the second dimension
    ni, nj, nv = lons.shape
    lons = lons.reshape(ni, nv)
    lats = lats.reshape(ni, nv)  
    connectivity = lons.shape   

    # load the mesh payload
    fname = "mosart_results.nc"
    processor = pooch.Decompress(method="auto", name=fname)
    resource = CACHE.fetch(f"{PANTRY_DATA}/{fname}.bz2", processor=processor)
    dataset = nc.Dataset(fname)
    data = dataset.variables["River_DISCHARGE"]
    steps = dataset.dimensions["time"].size
    idx = 0 if step is None else (step % steps)

    name = capitalise(data.standard_name)
    units = data.units

    return SampleUnstructuredXY(
        lons, lats, connectivity, data=data[idx], name=name, units=units, steps=steps
    )