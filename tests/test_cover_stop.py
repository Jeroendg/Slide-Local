"""Regression test for LocalSlide.async_stop_cover — proves missing Curtain.stop delegation."""
import asyncio
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

from custom_components.slide_local.cover import LocalSlide
from custom_components.slide_local.hub import Curtain, Hub


@pytest.fixture
def mock_hub():
    """A minimal Hub scaffold for building a real Curtain."""
    hub = Hub.__new__(Hub)
    hub._host = "127.0.0.1"
    hub._id = "test-id"
    hub._name = "Slide Test"
    hub.online = True
    return hub


@pytest_asyncio.fixture
async def curtain(mock_hub):
    """A real Curtain instance with a mocked SlideLocal backing."""
    # parse_to_cover expects a float; pass 50.0 not "50".
    # Ensure an event loop exists for Curtain.__init__'s get_event_loop() call.
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    curtain = Curtain("test_curtain_1", "Test Curtain", 50.0, mock_hub)
    # Patch the real SlideLocal so slide_stop is a controllable async mock.
    curtain._cover.slide_stop = AsyncMock(return_value=True)
    return curtain


@pytest.fixture
def cover(curtain):
    """LocalSlide wrapping the real Curtain."""
    return LocalSlide(curtain)


@pytest.mark.asyncio
async def test_async_stop_cover_delegates_to_curtain_stop(cover, curtain):
    """LocalSlide.async_stop_cover must call self._cover.stop().

    Prior to the fix Curtain has no stop() method, so this call raises
    AttributeError.  After the fix Curtain.stop delegates to
    self._cover.slide_stop() and the mocked API is exercised.
    """
    await cover.async_stop_cover()

    curtain._cover.slide_stop.assert_awaited_once_with()
