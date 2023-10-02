"""Unit-tests for :func:`geovista.cache.pooch_mute`."""
from __future__ import annotations

from pooch import get_logger

from geovista.cache import pooch_mute


def test():
    """Test all behaviours as one atomic test."""
    logger = get_logger()

    # default silent kwarg
    pooch_mute()
    assert logger.getEffectiveLevel() == 30
    from geovista.cache import GEOVISTA_POOCH_MUTE

    assert GEOVISTA_POOCH_MUTE is True

    # explicit verbose
    pooch_mute(silent=False)
    assert logger.getEffectiveLevel() == 0
    from geovista.cache import GEOVISTA_POOCH_MUTE

    assert GEOVISTA_POOCH_MUTE is False

    # explicit silence
    pooch_mute(silent=True)
    assert logger.getEffectiveLevel() == 30
    from geovista.cache import GEOVISTA_POOCH_MUTE

    assert GEOVISTA_POOCH_MUTE is True
