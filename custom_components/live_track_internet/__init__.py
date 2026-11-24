"""Live Track Internet for Home Assistant.

Internet outages on the shared Live Track map: Cloudflare Radar's outage records, read with the user's own API
token, one marker per open outage per place (SAW SSOT section 5). Submarine cables come in a later release.
Original work, not affiliated with Cloudflare.

The cause pictures ship in icons/ and are served at a path that changes when they do, so a browser caches them for
a month and fetches new ones only after an update.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN, ICONS_DIR
from .coordinator import OutageCoordinator
from .shared_map_card import async_offer_map_card, async_withdraw_map_card

# ! A new platform needs a FULL Home Assistant restart, not a reload (06_MAP_CONTRACT.md D6a-0c).
PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.GEO_LOCATION]

HERE = Path(__file__).parent


def _icons_digest() -> str:
    h = hashlib.sha256()
    for p in sorted((HERE / ICONS_DIR).glob("*.svg")):
        h.update(p.name.encode())
        h.update(p.read_bytes())
    return h.hexdigest()[:12]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    data = hass.data.setdefault(DOMAIN, {})
    if "icon_base" not in data:
        # A route cannot be removed from HA's web server: register it once per run, not once per set-up.
        digest = await hass.async_add_executor_job(_icons_digest)
        base = f"/{DOMAIN}/icons/{digest}"
        await hass.http.async_register_static_paths([StaticPathConfig(base, str(HERE / ICONS_DIR), cache_headers=True)])
        data["icon_base"] = base
    # LiveTrackMapCard, shipped in frontend/ (backlog 291): served, offered, the one resource row reconciled.
    await async_offer_map_card(hass, DOMAIN, HERE / "frontend")
    coordinator = OutageCoordinator(hass, entry, data["icon_base"])
    # Raises ConfigEntryAuthFailed on a refused token (HA then asks for a new one); Radar being down does not raise.
    await coordinator.async_config_entry_first_refresh()
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
