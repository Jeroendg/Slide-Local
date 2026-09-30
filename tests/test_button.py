"""Tests for the Slide Local button platform."""
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.slide_local.button import (
    SlideLocalCalibrationButton,
    async_setup_entry,
)
from custom_components.slide_local.const import DOMAIN


@pytest.fixture
def mock_curtain():
    """Create a mock curtain."""
    return SimpleNamespace(
        curtain_id="test_curtain_1",
        name="Test Curtain",
        calibrate=AsyncMock(),
        hub=SimpleNamespace(online=True, manufacturer="Slide"),
        online=True,
    )


@pytest.fixture
def button(mock_curtain):
    """Create a calibration button entity."""
    return SlideLocalCalibrationButton(mock_curtain)


@pytest.mark.asyncio
async def test_setup_adds_a_button_for_each_curtain(mock_curtain):
    """Test platform setup creates one button per curtain."""
    second_curtain = SimpleNamespace(
        curtain_id="test_curtain_2",
        name="Second Curtain",
        calibrate=AsyncMock(),
        hub=mock_curtain.hub,
        online=True,
    )
    entry = SimpleNamespace(entry_id="entry-id")
    hass = SimpleNamespace(
        data={
            DOMAIN: {
                entry.entry_id: SimpleNamespace(
                    curtains=[mock_curtain, second_curtain]
                )
            }
        }
    )
    async_add_entities = MagicMock()

    await async_setup_entry(hass, entry, async_add_entities)

    entities = list(async_add_entities.call_args.args[0])
    assert [entity.unique_id for entity in entities] == [
        "test_curtain_1_calibrate",
        "test_curtain_2_calibrate",
    ]


def test_button_identity_and_translation(button, mock_curtain):
    """Test the entity identity and translated-name key."""
    assert button.unique_id == f"{mock_curtain.curtain_id}_calibrate"
    assert button.translation_key == "calibrate"
    assert button.has_entity_name is True


def test_button_assigned_to_cover_device(button, mock_curtain):
    """Test the button is associated with the same device as the cover."""
    assert button.device_info["identifiers"] == {(DOMAIN, mock_curtain.curtain_id)}
    assert button.device_info["name"] == "Slide"
    assert button.device_info["manufacturer"] == "Slide"


@pytest.mark.parametrize(
    ("curtain_online", "hub_online", "expected"),
    [
        (True, True, True),
        (False, True, False),
        (True, False, False),
    ],
)
def test_button_availability(
    button, mock_curtain, curtain_online, hub_online, expected
):
    """Test button availability follows the curtain and hub."""
    mock_curtain.online = curtain_online
    mock_curtain.hub.online = hub_online
    assert button.available is expected


@pytest.mark.asyncio
async def test_button_press_calls_calibrate(button, mock_curtain):
    """Test pressing the button starts calibration."""
    await button.async_press()

    mock_curtain.calibrate.assert_awaited_once_with()


def test_button_should_poll_is_true(button):
    """Regression test: button must participate in HA polling so its
    available property is periodically re-evaluated from shared Curtain.online.

    Before the fix, ButtonEntity.should_poll defaults to False and the button
    stays unavailable forever after HA writes the initial state — even though
    the cover's polling has already updated Curtain.online to True.
    """
    assert button.should_poll is True
