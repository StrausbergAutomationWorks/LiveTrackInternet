"""The setup dialog (SAW SSOT 5.8, section 2 as decided 2026-11-24, and 7.6 item 6): the user's own Cloudflare API
token (Account > Radar > Read), OPTIONAL, and a box for the weekly fetch of ITU's terrestrial links, ON by default.
Without a token the cable layers and the links are shown; with one, checked with a real Radar call, the outage
markers and "cables in trouble" too. One entry only.

* Reconfigure: a new token is checked and replaces the old; an EMPTY field keeps what is there (so opening the
  dialog to look never removes a token). To drop the token, delete the entry and add it again without one. The box
  shows the current choice and saves whatever is ticked.
* Re-authenticate (Cloudflare refused the token): a token is required; the box is left as it was.
* An entry made before the box existed has no `itu_links` key and counts as ON (const.DEFAULT_ITU_LINKS).

! The token is stored in the entry's data and never logged; diagnostics redact it.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import BooleanSelector, TextSelector, TextSelectorConfig, TextSelectorType

from .api import check_token
from .const import CONF_API_TOKEN, CONF_ITU_LINKS, DEFAULT_ITU_LINKS, DOMAIN, ISSUES_URL, TOKEN_URL

_FIELD = TextSelector(TextSelectorConfig(type=TextSelectorType.PASSWORD))
_REQUIRED = vol.Schema({vol.Required(CONF_API_TOKEN): _FIELD})
_PLACEHOLDERS = {"token_url": TOKEN_URL, "issues_url": ISSUES_URL}

TITLE_WITH_TOKEN = "Cloudflare Radar"
TITLE_WITHOUT_TOKEN = "Submarine cables"


def _optional(itu_links: bool) -> vol.Schema:
    return vol.Schema({vol.Optional(CONF_API_TOKEN): _FIELD,
                       vol.Optional(CONF_ITU_LINKS, default=itu_links): BooleanSelector()})


class LiveTrackInternetFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def _check(self, token: str) -> dict[str, str]:
        result = await check_token(async_get_clientsession(self.hass), token)
        return {} if result == "ok" else {"base": result}

    @staticmethod
    def _token(user_input: dict[str, Any]) -> str:
        return (user_input.get(CONF_API_TOKEN) or "").strip()

    @staticmethod
    def _itu(user_input: dict[str, Any]) -> bool:
        return bool(user_input.get(CONF_ITU_LINKS, DEFAULT_ITU_LINKS))

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()
        errors: dict[str, str] = {}
        if user_input is not None:
            token, itu = self._token(user_input), self._itu(user_input)
            if not token:
                return self.async_create_entry(title=TITLE_WITHOUT_TOKEN, data={CONF_ITU_LINKS: itu})
            errors = await self._check(token)
            if not errors:
                return self.async_create_entry(title=TITLE_WITH_TOKEN, data={CONF_API_TOKEN: token, CONF_ITU_LINKS: itu})
        itu_default = self._itu(user_input) if user_input is not None else DEFAULT_ITU_LINKS
        return self.async_show_form(step_id="user", data_schema=_optional(itu_default), errors=errors,
                                    description_placeholders=_PLACEHOLDERS)

    async def async_step_reauth(self, entry_data: Mapping[str, Any]) -> ConfigFlowResult:
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            token = self._token(user_input)
            errors = await self._check(token) if token else {"base": "invalid_auth"}
            if not errors:
                return self.async_update_reload_and_abort(self._get_reauth_entry(),
                                                          data_updates={CONF_API_TOKEN: token})
        return self.async_show_form(step_id="reauth_confirm", data_schema=_REQUIRED, errors=errors,
                                    description_placeholders=_PLACEHOLDERS)

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        entry = self._get_reconfigure_entry()
        current = bool(entry.data.get(CONF_ITU_LINKS, DEFAULT_ITU_LINKS))
        if user_input is not None:
            token, itu = self._token(user_input), self._itu(user_input)
            if not token:
                return self.async_update_reload_and_abort(entry, data_updates={CONF_ITU_LINKS: itu})
            errors = await self._check(token)
            if not errors:
                return self.async_update_reload_and_abort(entry, data_updates={CONF_API_TOKEN: token,
                                                                               CONF_ITU_LINKS: itu})
            current = itu
        return self.async_show_form(step_id="reconfigure", data_schema=_optional(current), errors=errors,
                                    description_placeholders=_PLACEHOLDERS)
