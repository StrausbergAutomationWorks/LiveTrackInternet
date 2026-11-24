"""The setup dialog (SAW SSOT 5.8): one field, the user's own Cloudflare API token (Account > Radar > Read), checked
with a real Radar call. One entry only. Re-authenticate and reconfigure take a new token.

! The token is stored in the entry's data and never logged; diagnostics redact it.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import TextSelector, TextSelectorConfig, TextSelectorType

from .api import check_token
from .const import CONF_API_TOKEN, DOMAIN, ISSUES_URL, TOKEN_URL

_SCHEMA = vol.Schema({vol.Required(CONF_API_TOKEN): TextSelector(TextSelectorConfig(type=TextSelectorType.PASSWORD))})
_PLACEHOLDERS = {"token_url": TOKEN_URL, "issues_url": ISSUES_URL}


class LiveTrackInternetFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def _check(self, user_input: dict[str, Any]) -> tuple[str, dict[str, str]]:
        token = (user_input.get(CONF_API_TOKEN) or "").strip()
        result = await check_token(async_get_clientsession(self.hass), token)
        return token, ({} if result == "ok" else {"base": result})

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()
        errors: dict[str, str] = {}
        if user_input is not None:
            token, errors = await self._check(user_input)
            if not errors:
                return self.async_create_entry(title="Cloudflare Radar", data={CONF_API_TOKEN: token})
        return self.async_show_form(step_id="user", data_schema=_SCHEMA, errors=errors,
                                    description_placeholders=_PLACEHOLDERS)

    async def async_step_reauth(self, entry_data: Mapping[str, Any]) -> ConfigFlowResult:
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            token, errors = await self._check(user_input)
            if not errors:
                return self.async_update_reload_and_abort(self._get_reauth_entry(), data={CONF_API_TOKEN: token})
        return self.async_show_form(step_id="reauth_confirm", data_schema=_SCHEMA, errors=errors,
                                    description_placeholders=_PLACEHOLDERS)

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            token, errors = await self._check(user_input)
            if not errors:
                return self.async_update_reload_and_abort(self._get_reconfigure_entry(), data={CONF_API_TOKEN: token})
        return self.async_show_form(step_id="reconfigure", data_schema=_SCHEMA, errors=errors,
                                    description_placeholders=_PLACEHOLDERS)
