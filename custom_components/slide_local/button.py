"""Button platform for Slide Local calibration."""
from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .hub import Curtain


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add calibration button entities for each curtain."""
    hub = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities(
        SlideLocalCalibrationButton(curtain) for curtain in hub.curtains
    )


class SlideLocalCalibrationButton(ButtonEntity):
    """Representation of a Slide calibration button."""

    _attr_has_entity_name = True
    _attr_translation_key = "calibrate"

    def __init__(self, curtain: Curtain) -> None:
        """Initialize the calibration button."""
        self._curtain = curtain
        self._attr_unique_id = f"{curtain.curtain_id}_calibrate"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for the curtain."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._curtain.curtain_id)},
            name="Slide",
            manufacturer=self._curtain.hub.manufacturer,
        )

    @property
    def available(self) -> bool:
        """Return True if the curtain and hub are online."""
        return self._curtain.online and self._curtain.hub.online

    async def async_press(self) -> None:
        """Trigger calibration."""
        await self._curtain.calibrate()
