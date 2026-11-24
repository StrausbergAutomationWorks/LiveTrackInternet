"""Polls Cloudflare Radar's outage records and turns them into marker records (SAW SSOT 5.5).

* One outage call every POLL_S; country points once a day; a region id only the first time it is seen.
* 401/403: every marker cleared and Home Assistant's re-authentication dialog raised (ConfigEntryAuthFailed).
* 429: wait Retry-After, else the t= of `ratelimit`, else the backoff. 5xx, timeouts, no network: 15, 30, 60, then
  every 120 minutes. The last good answer is kept KEEP_S, then every marker goes and the count sensor turns
  unavailable: an old "open" outage is a wrong map.
* 400 is a bug of ours, not the token's: logged once, last good answer kept.
* Country points and region points are kept in .storage under SAW-neutral names, so a restart while Radar is down
  can still place, and any SAW module reading Radar finds them.
"""

from __future__ import annotations

import json
import logging
import os
import time
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from . import radar
from .api import outage_params, radar_get
from .const import (CONF_API_TOKEN, DOMAIN, GEO_LOOKUPS_PER_POLL, GEOLOCATIONS_CACHE, KEEP_S, LOCATIONS_CACHE,
                    LOCATIONS_EVERY_S, POLL_S)

_LOGGER = logging.getLogger(__name__)


def _read_json(path: str) -> Any:
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def _write_json(path: str, doc: Any) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, separators=(",", ":"))
    os.replace(tmp, path)


class OutageCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, icon_base: str) -> None:
        super().__init__(hass, _LOGGER, config_entry=entry, name=f"{DOMAIN}_outages",
                         update_interval=timedelta(seconds=POLL_S))
        self._session = async_get_clientsession(hass)
        self._token: str = entry.data.get(CONF_API_TOKEN, "")
        self._icon_base = icon_base
        self._countries: dict[str, dict[str, Any]] = {}
        self._countries_at = 0.0
        self._regions: dict[str, dict[str, Any] | None] = {}
        self._loaded = False
        self._good: dict[str, Any] | None = None
        self._good_at = 0.0
        self._failures = 0
        self._logged_400 = False
        self.reason: str | None = None

    # ------------------------------------------------------------ caches

    async def _load_caches(self) -> None:
        loc = await self.hass.async_add_executor_job(_read_json, self.hass.config.path(".storage", LOCATIONS_CACHE))
        if isinstance(loc, dict) and isinstance(loc.get("countries"), dict):
            self._countries = loc["countries"]
            self._countries_at = float(loc.get("fetched_at") or 0)
        geo = await self.hass.async_add_executor_job(_read_json, self.hass.config.path(".storage", GEOLOCATIONS_CACHE))
        if isinstance(geo, dict) and isinstance(geo.get("regions"), dict):
            self._regions = {k: v for k, v in geo["regions"].items() if isinstance(v, dict)}
        self._loaded = True

    async def _save(self, name: str, doc: Any) -> None:
        try:
            await self.hass.async_add_executor_job(_write_json, self.hass.config.path(".storage", name), doc)
        except OSError as err:
            _LOGGER.debug("could not write %s: %s", name, err)

    async def _refresh_countries(self) -> None:
        if self._countries and time.time() - self._countries_at < LOCATIONS_EVERY_S:
            return
        ans = await radar_get(self._session, self._token, "entities/locations", {"limit": 300, "format": "json"})
        if ans.status in (401, 403):
            raise ConfigEntryAuthFailed("Cloudflare refused the API token")
        countries = radar.parse_locations(ans.data) if ans.status == 200 else {}
        if countries:
            self._countries, self._countries_at = countries, time.time()
            await self._save(LOCATIONS_CACHE, {"source": "Cloudflare Radar, CC BY-NC 4.0",
                                               "fetched_at": self._countries_at, "countries": countries})

    async def _refresh_regions(self, records: list[dict[str, Any]]) -> None:
        todo = [g for g in radar.needed_geoids(records) if g not in self._regions][:GEO_LOOKUPS_PER_POLL]
        changed = False
        for g in todo:
            ans = await radar_get(self._session, self._token, f"geolocations/{g}", {"format": "json"})
            if ans.status in (401, 403):
                raise ConfigEntryAuthFailed("Cloudflare refused the API token")
            if ans.status == 200:
                self._regions[g] = radar.parse_geolocation(ans.data)
                changed = True
            # any other answer: not cached, asked again next poll; the record falls back to its country
        if changed:
            await self._save(GEOLOCATIONS_CACHE, {"source": "Cloudflare Radar, CC BY-NC 4.0",
                                                  "regions": {k: v for k, v in self._regions.items() if v}})

    # ------------------------------------------------------------ the poll

    def _empty(self, reason: str) -> dict[str, Any]:
        self.reason = reason
        return {"markers": [], "not_on_map": [], "open_records": 0, "expired": True, "reason": reason,
                "last_success": self._good.get("last_success") if self._good else None}

    def _failed(self, reason: str, wait_s: int) -> dict[str, Any]:
        """Keep the last good answer KEEP_S, then clear. Never raises."""
        self._failures += 1
        self.update_interval = timedelta(seconds=wait_s)
        self.reason = reason
        if self._good is not None and time.time() - self._good_at < KEEP_S:
            return {**self._good, "reason": reason}
        return self._empty(reason)

    async def _async_update_data(self) -> dict[str, Any]:
        if not self._loaded:
            await self._load_caches()
        if not self._token:
            raise ConfigEntryAuthFailed("No Cloudflare API token")
        await self._refresh_countries()
        ans = await radar_get(self._session, self._token, "annotations/outages", outage_params(dt_util.utcnow()))
        if ans.status in (401, 403):
            self._good = None
            raise ConfigEntryAuthFailed("Cloudflare refused the API token")
        if ans.status == 429:
            return self._failed("rate_limited", radar.rate_limit_wait_s(ans.headers, self._failures + 1))
        if ans.status == 400:
            if not self._logged_400:
                _LOGGER.warning("Cloudflare Radar answered 400 to the outage query; keeping the last answer")
                self._logged_400 = True
            return self._failed("bad_request", POLL_S)
        if ans.status != 200 or not isinstance(ans.data, dict) or ans.data.get("success") is False:
            return self._failed("no_answer" if ans.status == 0 else f"http_{ans.status}",
                                radar.backoff_s(self._failures + 1))
        records = radar.open_records(ans.data)
        await self._refresh_regions(records)
        markers, not_on_map = radar.build_markers(records, self._countries, self._regions, self._icon_base)
        self._failures = 0
        self.update_interval = timedelta(seconds=POLL_S)
        self.reason = None
        self._good_at = time.time()
        self._good = {"markers": markers, "not_on_map": not_on_map, "open_records": len(records),
                      "expired": False, "reason": None, "last_success": dt_util.utcnow().isoformat()}
        return self._good
