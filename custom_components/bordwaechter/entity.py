"""Gemeinsame Basis: ein HA-Gerät je Bordwächter, Entitäten hängen daran."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import BordwaechterCoordinator


class BordwaechterEntity(CoordinatorEntity[BordwaechterCoordinator]):
    _attr_has_entity_name = True

    def __init__(self, coordinator: BordwaechterCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._entry = entry

    @property
    def _data(self) -> dict:
        return self.coordinator.data or {}

    def _get(self, path: str):
        """Wert über einen Punkt-Pfad lesen, z. B. 'info.weather.temp_c' oder 'system.cpu_pct'."""
        cur = self.coordinator.data or {}
        for part in path.split("."):
            if not isinstance(cur, dict):
                return None
            cur = cur.get(part)
        return cur

    @property
    def device_info(self) -> DeviceInfo:
        d = self.coordinator.data or {}
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name=d.get("ship") or "Bordwächter",
            manufacturer="KAI",
            model="Bordwächter",
            sw_version=str(d.get("version", "")) or None,
        )
