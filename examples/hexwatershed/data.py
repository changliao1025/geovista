
@lru_cache(maxsize=LRU_CACHE_SIZE)
def hexwatershed(step: int | None = None) -> SampleUnstructuredXY:
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
    fname = "hexwatershed.json"
    processor = pooch.Decompress(method="auto", name=fname)
    resource = CACHE.fetch(f"{PANTRY_DATA}/{fname}.bz2", processor=processor)
    
    #load the json file, the structure can be found from the pyhexwatershed python package
    

    #reshape to remove the second dimension
   
    connectivity = lons.shape   

    

    name = ''
    units = ''

    return SampleUnstructuredXY(
        lons, lats, connectivity, data=data, name=name, units=units
    )