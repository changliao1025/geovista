"""pytest fixture infra-structure for :mod:`geovista.geodesic` unit-tests."""
import numpy as np
import pytest

from geovista.pantry import lam_uk as pantry_lam_uk
from geovista.samples import lam_uk as sample_lam_uk
from geovista.samples import lfric as sample_lfric
from geovista.samples import lfric_sst as sample_lfric_sst


@pytest.fixture(scope="session")
def lam_uk():
    """Fixture generates a Local Area Model mesh with indexed faces and points."""
    mesh = sample_lam_uk()
    mesh.cell_data["ids"] = np.arange(mesh.n_cells)
    mesh.point_data["ids"] = np.arange(mesh.n_points)
    return mesh


@pytest.fixture(scope="session")
def lam_uk_sample():
    """Fixture generates a Local Area Model data sample for the UK."""
    sample = pantry_lam_uk()
    return sample.lons, sample.lats


@pytest.fixture
def lfric(request):
    """Fixture to provide a cube-sphere mesh."""
    # support indirect parameters for fixtures and also
    # calling the fixture with no parameter
    resolution = request.param if hasattr(request, "param") else "c48"
    mesh = sample_lfric(resolution=resolution)
    return mesh


@pytest.fixture(scope="session")
def lfric_sst():
    """Fixture to provide a cube-sphere mesh with SST face data."""
    mesh = sample_lfric_sst()
    return mesh