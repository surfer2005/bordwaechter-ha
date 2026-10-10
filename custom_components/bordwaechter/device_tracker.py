"""Device-Tracker: zeigt die Schiffsposition auf der HA-Karte (GPS übers Gerät)."""
from __future__ import annotations

from homeassistant.components.device_tracker import SourceType, TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import BordwaechterEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([BwTracker(coordinator, entry)])


class BwTracker(BordwaechterEntity, TrackerEntity):
    _attr_name = "Position"
    _attr_icon = "mdi:ferry"

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_tracker"

    @property
    def source_type(self) -> SourceType:
        return SourceType.GPS

    @property
    def latitude(self):
        if self._data.get("pos_valid"):
            return self._data.get("lat")
        return None

    @property
    def longitude(self):
        if self._data.get("pos_valid"):
            return self._data.get("lng")
        return None
