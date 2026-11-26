"""Live Track Internet for Home Assistant.

Internet outages, submarine cables and terrestrial links on the shared Live Track map (SAW SSOT sections 2, 5, 7):

* Outages: Cloudflare Radar's outage records, read with the user's own API token, one marker per open outage per
  place. Only with a token.
* Cables: Tristan Hotham's dataset of TeleGeography's cable data (CC BY-NC-SA 4.0), converted at release and shipped
  in cables/ with its licence and credit. All cables and landing points always; cables named in an open outage
  ("cables in trouble") only with a token.
* Terrestrial links: ITU Broadband Maps' fibre and microwave links, fetched by this install once a week (terrestrial.py,
  itu.py) unless the setup option is off; served without sign-in at the file's digest (views.py, D12).

Original work, not affiliated with Cloudflare, Tristan Hotham, TeleGeography or ITU.

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
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er

from . import cables
from .const import CONF_API_TOKEN, CONF_ITU_LINKS, DEFAULT_ITU_LINKS, DOMAIN, ICONS_DIR, LINKS_FETCHER
from .coordinator import OutageCoordinator
from .shared_map_card import async_offer_map_card, async_withdraw_map_card
from .terrestrial import LinksFetcher
from .views import LinksView, PointsView

LINKS_UNIQUE_ID = f"{DOMAIN}_terrestrial_links"   # sensor.py's; here to remove the row when the option is off

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
    if "links_view" not in data:
        hass.http.register_view(LinksView())   # 404 until a fetcher holds a file
        data["links_view"] = True


def itu_links_on(entry: ConfigEntry) -> bool:
    return bool(entry.data.get(CONF_ITU_LINKS, DEFAULT_ITU_LINKS))


def _remove_links_entity(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Option off: no publisher at all, so the map shows no dead checkbox (D12 rule 10). The cache file stays in
    .storage (SAW-neutral; Lee 2026-11-25)."""
    ent = er.async_get(hass)
    if eid := ent.async_get_entity_id("sensor", DOMAIN, LINKS_UNIQUE_ID):
        ent.async_remove(eid)
    dev = dr.async_get(hass)
    if device := dev.async_get_device(identifiers={(DOMAIN, f"{entry.entry_id}_itu")}):
        dev.async_update_device(device.id, remove_config_entry_id=entry.entry_id)


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
    # After the refresh that may raise, so a refused token never leaves a fetcher's timer running.
    if itu_links_on(entry):
        fetcher = LinksFetcher(hass, entry.entry_id)
        await fetcher.async_start()     # reads the last good file; the fetch itself runs later, in the background
        data[LINKS_FETCHER] = fetcher
    else:
        _remove_links_entity(hass, entry)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """The map card is NOT withdrawn here: a restart or reload unloads too, and that is not an uninstall."""
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        data = hass.data.get(DOMAIN, {})
        data.pop(entry.entry_id, None)
        if (fetcher := data.pop(LINKS_FETCHER, None)) is not None:
            await fetcher.async_stop()
    return unloaded


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """The entry was deleted. The domain's last entry withdraws the map card."""
    if not [e for e in hass.config_entries.async_entries(DOMAIN) if e.entry_id != entry.entry_id]:
        await async_withdraw_map_card(hass, DOMAIN)
