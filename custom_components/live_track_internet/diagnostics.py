"""Diagnostics: the token is redacted; what the last poll found is summarised."""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_API_TOKEN, DOMAIN, LINKS_FETCHER, VERSION


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: ConfigEntry) -> dict[str, Any]:
    coordinator = hass.data.get(DOMAIN, {}).get(entry.entry_id)
    data = (coordinator.data if coordinator else None) or {}
    return {
        "version": VERSION,
        "entry": async_redact_data(dict(entry.data), {CONF_API_TOKEN}),
        "markers": [{"key": m["key"], "cause": m["attrs"].get("outage_cause"),
                     "place_kind": m["attrs"].get("place_kind"), "country_code": m["attrs"].get("country_code")}
                    for m in data.get("markers") or []],
        "not_on_map": len(data.get("not_on_map") or []),
        "open_records": data.get("open_records"),
        "expired": data.get("expired"),
        "reason": data.get("reason"),
        "last_success": data.get("last_success"),
        "poll_s": coordinator.update_interval.total_seconds() if coordinator and coordinator.update_interval else None,
        "terrestrial_links": fetcher.state() if (fetcher := hass.data.get(DOMAIN, {}).get(LINKS_FETCHER)) else None,
    }
