"""Live Track Internet for Home Assistant.

Internet outages and submarine cables on the shared Live Track map (SAW SSOT sections 2 and 5):

* Outages: Cloudflare Radar's outage records, read with the user's own API token, one marker per open outage per
  place. Only with a token.
* Cables: Tristan Hotham's dataset of TeleGeography's cable data (CC BY-NC-SA 4.0), converted at release and shipped
  in cables/ with its licence and credit. All cables and landing points always; cables named in an open outage
  ("cables in trouble") only with a token.

Original work, not affiliated with Cloudflare, Tristan Hotham or TeleGeography.

The cause pictures (icons/) and the cable shape file (cables/web/) are served at paths that change when they do, so a
browser caches them for a month and fetches new ones only after an update. ! Only cables/web/cables.json.gz ships: a
request for .../cables.json is answered with the .gz and Content-Encoding: gzip by aiohttp's FileResponse, as Live
Track Weather's zones are. The landing points are served signed in under /api/ (views.py, D19).
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from . import cables
from .const import CONF_API_TOKEN, DOMAIN, ICONS_DIR
from .coordinator import OutageCoordinator
from .shared_map_card import async_offer_map_card, async_withdraw_map_card
from .views import PointsView

# ! A new platform needs a FULL Home Assistant restart, not a reload (06_MAP_CONTRACT.md D6a-0c).
PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.GEO_LOCATION]

HERE = Path(__file__).parent


def _icons_digest() -> str:
    h = hashlib.sha256()
    for p in sorted((HERE / ICONS_DIR).glob("*.svg")):
        h.update(p.name.encode())
        h.update(p.read_bytes())
    return h.hexdigest()[:12]


async def _register_once(hass: HomeAssistant, data: dict) -> None:
    """Routes cannot be removed from HA's web server: register them once per run, not once per set-up."""
    if "icon_base" not in data:
        digest = await hass.async_add_executor_job(_icons_digest)
        base = f"/{DOMAIN}/icons/{digest}"
        await hass.http.async_register_static_paths([StaticPathConfig(base, str(HERE / ICONS_DIR), cache_headers=True)])
        data["icon_base"] = base
    if "cables" not in data:
        cd = await hass.async_add_executor_job(cables.CableData, HERE / cables.CABLES_DIR)
        base = f"/{DOMAIN}/cables/{cd.shape_digest}"
        await hass.http.async_register_static_paths(
            [StaticPathConfig(base, str(HERE / cables.CABLES_DIR / cables.WEB_DIR), cache_headers=True)])
        data["shapes_url"] = f"{base}/{cables.SHAPE_FILE}"
        hass.http.register_view(PointsView())
        data["cables"] = cd


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    data = hass.data.setdefault(DOMAIN, {})
    await _register_once(hass, data)
    # LiveTrackMapCard, shipped in frontend/ (backlog 291): served, offered, the one resource row reconciled.
    await async_offer_map_card(hass, DOMAIN, HERE / "frontend")
    coordinator: OutageCoordinator | None = None
    if (entry.data.get(CONF_API_TOKEN) or "").strip():
        matcher = data["cables"].matcher
        coordinator = OutageCoordinator(hass, entry, data["icon_base"],
                                        name_cables=lambda desc: cables.match(desc, matcher))
        # Raises ConfigEntryAuthFailed on a refused token (HA then asks for a new one); Radar being down does not raise.
        await coordinator.async_config_entry_first_refresh()
    # None without a token: the cable layers alone (SSOT section 2).
    data[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """The map card is NOT withdrawn here: a restart or reload unloads too, and that is not an uninstall."""
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    return unloaded


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """The entry was deleted. The domain's last entry withdraws the map card."""
    if not [e for e in hass.config_entries.async_entries(DOMAIN) if e.entry_id != entry.entry_id]:
        await async_withdraw_map_card(hass, DOMAIN)
