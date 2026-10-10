"""Daten-Koordinator: pollt die lokale REST-API des Bordwächter-Geräts (/api/status)."""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class BordwaechterCoordinator(DataUpdateCoordinator):
    """Holt den Status vom Gerät (Basic-Auth mit dem UI-Passwort)."""

    def __init__(self, hass: HomeAssistant, host: str, port: int, password: str) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self._session = async_get_clientsession(hass)
        self._url = f"http://{host}:{port}/api/status"
        self._auth = aiohttp.BasicAuth("kai", password) if password else None

    async def _async_update_data(self) -> dict:
        try:
            async with asyncio.timeout(15):
                async with self._session.get(self._url, auth=self._auth) as resp:
                    if resp.status != 200:
                        raise UpdateFailed(f"HTTP {resp.status}")
                    return await resp.json()
        except UpdateFailed:
            raise
        except Exception as err:  # noqa: BLE001
            raise UpdateFailed(str(err)) from err
