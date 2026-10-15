"""Sensoren: alle Werte, die das Bordgerät über /api/status liefert — Navigation/Pünktlichkeit,
Wetter, Pegel und der Zustand des Raspberry (CPU/Last/Speicher/Platte)."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import BordwaechterEntity

M = SensorStateClass.MEASUREMENT
DIAG = EntityCategory.DIAGNOSTIC

# (pfad, Anzeigename, Einheit, Icon, device_class, state_class, entity_category)
SENSORS = [
    # --- Fahrt / Pünktlichkeit ---
    ("phase", "Phase", None, "mdi:transit-connection-variant", None, None, None),
    ("verdict", "Empfehlung", None, "mdi:speedometer", None, None, None),
    ("off_state", "Kurszustand", None, "mdi:map-marker-path", None, None, None),
    ("alarm_state", "Alarm-Zustand", None, "mdi:alarm-light-outline", None, None, None),
    ("soll", "Soll-Ankunft", None, "mdi:clock-outline", None, None, None),
    ("abfahrt", "Abfahrt", None, "mdi:clock-start", None, None, None),
    ("remain_km", "Reststrecke", "km", "mdi:map-marker-distance", None, M, None),
    ("today_km", "Tageskilometer", "km", "mdi:map-marker-distance", None, SensorStateClass.TOTAL_INCREASING, None),
    ("ist_kmh", "Ist-Tempo", "km/h", "mdi:speedometer", None, M, None),
    ("soll_kmh", "Soll-Tempo", "km/h", "mdi:speedometer-medium", None, M, None),
    ("diff_kmh", "Tempo-Differenz", "km/h", "mdi:speedometer-slow", None, M, None),
    ("max_kmh", "Höchstgeschwindigkeit", "km/h", "mdi:car-speed-limiter", None, M, None),
    ("heading", "Kurs über Grund", "°", "mdi:compass", None, M, None),
    ("off_course_m", "Kursabweichung", "m", "mdi:map-marker-alert", None, M, None),
    ("off_course_limit_m", "Kursgrenze", "m", "mdi:map-marker-radius", None, None, DIAG),
    ("rest_min", "Restzeit", "min", "mdi:timer-sand", None, None, None),
    ("warten_min", "Wartezeit", "min", "mdi:timer-pause", None, None, None),
    ("delay_min", "Verspätung", "min", "mdi:timer-alert", None, None, None),
    ("pos_age_sec", "Position Alter", "s", "mdi:crosshairs-question", None, None, DIAG),
    ("bundle_age_sec", "KAI-Daten Alter", "s", "mdi:cloud-clock-outline", None, None, DIAG),
    ("hint", "Hinweis", None, "mdi:information-outline", None, None, DIAG),
    ("sifa_countdown_sec", "Totmann-Countdown", "s", "mdi:timer-alert-outline", SensorDeviceClass.DURATION, None, None),
    ("registration_number", "Kennzeichen", None, "mdi:ferry", None, None, DIAG),
    # --- Wetter (info.weather) ---
    ("info.weather.temp_c", "Lufttemperatur", "°C", "mdi:thermometer", SensorDeviceClass.TEMPERATURE, M, None),
    ("info.weather.wind_kmh", "Wind", "km/h", "mdi:weather-windy", None, M, None),
    ("info.weather.wind_dir_deg", "Windrichtung", "°", "mdi:compass-outline", None, M, None),
    ("info.weather.precip_mm", "Niederschlag", "mm", "mdi:weather-rainy", None, M, None),
    # --- Pegel (info.pegel) ---
    ("info.pegel.cm", "Pegel", "cm", "mdi:waves", None, M, None),
    ("info.pegel.rate_cm_per_h", "Pegeländerung", "cm/h", "mdi:trending-up", None, M, None),
    ("info.pegel.station", "Pegel-Station", None, "mdi:map-marker", None, None, DIAG),
    # --- Pi-Zustand (system) ---
    ("system.cpu_temp_c", "CPU-Temperatur", "°C", "mdi:thermometer", SensorDeviceClass.TEMPERATURE, M, DIAG),
    ("system.cpu_pct", "CPU-Auslastung", "%", "mdi:cpu-64-bit", None, M, DIAG),
    ("system.load1", "Systemlast", None, "mdi:chart-line", None, M, DIAG),
    ("system.mem_pct", "Speicher belegt", "%", "mdi:memory", None, M, DIAG),
    ("system.mem_total_mb", "RAM gesamt", "MB", "mdi:memory", None, None, DIAG),
    ("system.disk_pct", "Platte belegt", "%", "mdi:harddisk", None, M, DIAG),
    ("system.uptime_sec", "Laufzeit", "s", "mdi:timer-outline", SensorDeviceClass.DURATION, None, DIAG),
]

# Ein Nachkommastelle in der Anzeige für diese Gleitkomma-Messwerte.
_PRECISION1 = {
    "info.weather.temp_c", "info.weather.wind_kmh", "info.pegel.cm", "info.pegel.rate_cm_per_h",
    "system.cpu_temp_c", "system.cpu_pct", "system.load1", "system.mem_pct", "system.disk_pct",
    "ist_kmh", "soll_kmh", "diff_kmh", "max_kmh", "remain_km", "off_course_m", "heading", "today_km",
}
_TREND = {-1: "fallend", 0: "stabil", 1: "steigend"}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[SensorEntity] = [BwSensor(coordinator, entry, *s) for s in SENSORS]
    entities.append(BwNextStop(coordinator, entry))
    entities.append(BwPegelTrend(coordinator, entry))
    async_add_entities(entities)


class BwSensor(BordwaechterEntity, SensorEntity):
    def __init__(self, coordinator, entry, path, name, unit, icon, device_class, state_class, category):
        super().__init__(coordinator, entry)
        self._path = path
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._attr_entity_category = category
        if path in _PRECISION1:
            self._attr_suggested_display_precision = 1
        self._attr_unique_id = f"{entry.entry_id}_{path.replace('.', '_')}"

    @property
    def native_value(self):
        v = self._get(self._path)
        # Negative Rest-/Wartezeit heißt „nicht zutreffend".
        if self._path in ("rest_min", "warten_min", "delay_min") and isinstance(v, (int, float)) and v < 0:
            return None
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


class BwPegelTrend(BordwaechterEntity, SensorEntity):
    """Pegeltrend als Text (steigend/stabil/fallend) aus der Zahl -1/0/1."""
    _attr_icon = "mdi:swap-vertical"

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)
        self._attr_name = "Pegeltrend"
        self._attr_unique_id = f"{entry.entry_id}_pegel_trend"

    @property
    def native_value(self):
        if self._get("info.pegel.cm") is None:
            return None
        return _TREND.get(self._get("info.pegel.trend"))
