"""Sensoren: Phase, Empfehlung, Soll/Reststrecke/Tempo, Kursabweichung, nächster Halt."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import BordwaechterEntity

# (key, Anzeigename, Einheit, Icon)
SENSORS = [
    ("phase", "Phase", None, "mdi:transit-connection-variant"),
    ("verdict", "Empfehlung", None, "mdi:speedometer"),
    ("off_state", "Kurszustand", None, "mdi:map-marker-path"),
    ("soll", "Soll-Ankunft", None, "mdi:clock-outline"),
    ("abfahrt", "Abfahrt", None, "mdi:clock-start"),
    ("remain_km", "Reststrecke", "km", "mdi:map-marker-distance"),
    ("ist_kmh", "Ist-Tempo", "km/h", "mdi:speedometer"),
    ("soll_kmh", "Soll-Tempo", "km/h", "mdi:speedometer-medium"),
    ("off_course_m", "Kursabweichung", "m", "mdi:map-marker-alert"),
    ("rest_min", "Restzeit", "min", "mdi:timer-sand"),
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[SensorEntity] = [BwSensor(coordinator, entry, *s) for s in SENSORS]
    entities.append(BwNextStop(coordinator, entry))
    async_add_entities(entities)


class BwSensor(BordwaechterEntity, SensorEntity):
    def __init__(self, coordinator, entry, key, name, unit, icon):
        super().__init__(coordinator, entry)
        self._key = key
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon
        self._attr_unique_id = f"{entry.entry_id}_{key}"

    @property
    def native_value(self):
        v = self._data.get(self._key)
        if self._key in ("rest_min", "warten_min") and isinstance(v, (int, float)) and v < 0:
            return None
        if self._key in ("remain_km", "ist_kmh", "soll_kmh", "off_course_m") and v == 0:
            return v
        if v in ("", None):
            return None
        return v


class BwNextStop(BordwaechterEntity, SensorEntity):
    _attr_icon = "mdi:map-marker"

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)
        self._attr_name = "Nächster Halt"
        self._attr_unique_id = f"{entry.entry_id}_next_stop"

    @property
    def native_value(self):
        d = self._data
        f, t = d.get("from"), d.get("to")
        if f and t:
            return f"{f} → {t}"
        return None
