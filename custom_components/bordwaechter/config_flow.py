"""Config-Flow: Host + Port + UI-Passwort eintippen, Verbindung testen."""
from __future__ import annotations

import asyncio

import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PASSWORD, CONF_PORT
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DEFAULT_PORT, DOMAIN


class BordwaechterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Einrichtung über die Oberfläche."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors: dict[str, str] = {}
        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input.get(CONF_PORT, DEFAULT_PORT)
            pw = user_input.get(CONF_PASSWORD, "")
            session = async_get_clientsession(self.hass)
            auth = aiohttp.BasicAuth("kai", pw) if pw else None
            try:
                async with asyncio.timeout(15):
                    async with session.get(f"http://{host}:{port}/api/status", auth=auth) as resp:
                        if resp.status != 200:
                            raise RuntimeError(f"HTTP {resp.status}")
                        data = await resp.json()
                await self.async_set_unique_id(f"{host}:{port}")
                self._abort_if_unique_id_configured()
                title = user_input.get(CONF_NAME) or data.get("ship") or f"Bordwächter {host}"
                return self.async_create_entry(title=title, data=user_input)
            except Exception:  # noqa: BLE001
                errors["base"] = "cannot_connect"

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST): str,
                vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
                vol.Optional(CONF_PASSWORD, default=""): str,
                vol.Optional(CONF_NAME): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
