"""Binärsensoren: Alarm, SIFA aktiv, Kamera-Hinweis, Position ok."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import BordwaechterEntity

# (key, Name, device_class, Icon)
BINARY = [
    ("alarm", "Alarm", BinarySensorDeviceClass.SAFETY, "mdi:alarm-light"),
    ("sifa_deadman_active", "SIFA aktiv", BinarySensorDeviceClass.SAFETY, "mdi:account-alert"),
    ("camera_hazard", "Kamera-Hinweis", BinarySensorDeviceClass.SAFETY, "mdi:cctv"),
    ("pos_valid", "Position ok", BinarySensorDeviceClass.CONNECTIVITY, "mdi:crosshairs-gps"),
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([BwBinary(coordinator, entry, *b) for b in BINARY])


class BwBinary(BordwaechterEntity, BinarySensorEntity):
    def __init__(self, coordinator, entry, key, name, device_class, icon):
        super().__init__(coordinator, entry)
        self._key = key
        self._attr_name = name
        self._attr_device_class = device_class
        self._attr_icon = icon
        self._attr_unique_id = f"{entry.entry_id}_{key}"

    @property
    def is_on(self) -> bool:
        return bool(self._data.get(self._key))
