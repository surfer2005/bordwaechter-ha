"""Binärsensoren: Alarm, SIFA aktiv, Kamera-Hinweis, Position ok."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import BordwaechterEntity

DIAG = EntityCategory.DIAGNOSTIC

# (key, Name, device_class, Icon, entity_category)
BINARY = [
    ("alarm", "Alarm", BinarySensorDeviceClass.SAFETY, "mdi:alarm-light", None),
    ("sifa_deadman_active", "SIFA aktiv", BinarySensorDeviceClass.SAFETY, "mdi:account-alert", None),
    ("camera_hazard", "Kamera-Hinweis", BinarySensorDeviceClass.SAFETY, "mdi:cctv", None),
    ("pos_valid", "Position ok", BinarySensorDeviceClass.CONNECTIVITY, "mdi:crosshairs-gps", None),
    ("horn", "Hupe", BinarySensorDeviceClass.SOUND, "mdi:bullhorn", None),
    ("lamp", "Warnlampe", BinarySensorDeviceClass.LIGHT, "mdi:alarm-light-outline", None),
    ("hat_bordbuch", "Bordbuch vorhanden", None, "mdi:book-open-variant", DIAG),
    ("next_logbook_hint", "Nächstes Bordbuch fällig", None, "mdi:book-plus", None),
    ("cam_configured", "Kamera konfiguriert", None, "mdi:cctv", DIAG),
    ("stream_configured", "Livestream konfiguriert", None, "mdi:video", DIAG),
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([BwBinary(coordinator, entry, *b) for b in BINARY])


class BwBinary(BordwaechterEntity, BinarySensorEntity):
    def __init__(self, coordinator, entry, key, name, device_class, icon, category=None):
        super().__init__(coordinator, entry)
        self._key = key
        self._attr_name = name
        self._attr_device_class = device_class
        self._attr_icon = icon
        self._attr_entity_category = category
        self._attr_unique_id = f"{entry.entry_id}_{key}"

    @property
    def is_on(self) -> bool:
        return bool(self._data.get(self._key))
