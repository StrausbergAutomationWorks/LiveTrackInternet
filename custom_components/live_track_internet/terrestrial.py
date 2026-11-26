"""Fetches ITU's terrestrial links once a week and keeps the built file (SAW SSOT section 7.3, approved by Lee
2026-11-25). The rules live in itu.py, which has no Home Assistant; this is the timer, the HTTP and the disk.

* At start the last good file is read from .storage (SAW-neutral name), so a restart while ITU is down still draws.
* One fetch at a time, page by page, each page parsed in an executor. A fetch that is not whole, or is under half the
  last good total, changes nothing: the last good file stays, however old (reference data, not news).
* A good fetch writes the file atomically, then tells the sensor; the next fetch is this install's slot a week on.
* Never raises into Home Assistant; failures are logged at debug and kept in `reason`.
"""

from __future__ import annotations

import asyncio
import logging
import os
import time
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any

import aiohttp

from homeassistant.core import CALLBACK_TYPE, HomeAssistant, callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_point_in_utc_time

from . import itu
from .const import USER_AGENT

_LOGGER = logging.getLogger(__name__)


def _read(path: str) -> itu.Links | None:
    try:
        with open(path, "rb") as fh:
            return itu.Links.from_gz(fh.read())
    except (OSError, ValueError):
        return None


def _write(path: str, data: bytes) -> None:
    tmp = path + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, path)


def _ts(iso: str | None) -> float | None:
    if not iso:
        return None
    try:
        return datetime.fromisoformat(iso).timestamp()
    except ValueError:
        return None


class LinksFetcher:
    def __init__(self, hass: HomeAssistant, entry_id: str) -> None:
        self.hass = hass
        self.entry_id = entry_id
        self.links: itu.Links | None = None
        self.reason: str | None = None
        self.next_at: float | None = None
        self._path = hass.config.path(".storage", itu.CACHE_FILE)
        self._unsub: CALLBACK_TYPE | None = None
        self._task: asyncio.Task | None = None
        self._listeners: list[Callable[[], None]] = []
        self._failures = 0
        self._stopped = False

    # ------------------------------------------------------------ life

    async def async_start(self) -> None:
        self.links = await self.hass.async_add_executor_job(_read, self._path)
        last = _ts(self.links.fetched_at) if self.links else None
        self._schedule(itu.next_due(self.entry_id, last, time.time()))

    async def async_stop(self) -> None:
        self._stopped = True
        if self._unsub:
            self._unsub()
            self._unsub = None
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        self._listeners.clear()

    @callback
    def add_listener(self, cb: Callable[[], None]) -> Callable[[], None]:
        self._listeners.append(cb)

        def remove() -> None:
            if cb in self._listeners:
                self._listeners.remove(cb)
        return remove

    def _schedule(self, when: float) -> None:
        if self._stopped:
            return
        if self._unsub:
            self._unsub()
        self.next_at = when
        self._unsub = async_track_point_in_utc_time(
            self.hass, self._fire, datetime.fromtimestamp(when, tz=timezone.utc))

    @callback
    def _fire(self, _now: datetime) -> None:
        self._unsub = None
        if self._task is None or self._task.done():
            self._task = self.hass.async_create_background_task(self._run(), f"{itu.CACHE_FILE} fetch")

    # ------------------------------------------------------------ one fetch

    async def _run(self) -> None:
        reason, retry_after, built = await self._fetch()
        if built is None:
            self._failures += 1
            self.reason = reason
            wait = itu.retry_s(reason, self._failures, retry_after)
            _LOGGER.debug("ITU links: %s; the last good file stays; again in %d s", reason, wait)
            self._schedule(time.time() + wait)
            return
        try:
            await self.hass.async_add_executor_job(_write, self._path, built.gz)
        except OSError as err:
            # Still served from memory until a restart; the next good fetch writes again.
            _LOGGER.debug("ITU links: could not write %s: %s", itu.CACHE_FILE, err)
        self.links = built
        self._failures = 0
        self.reason = None
        for cb in list(self._listeners):
            cb()
        self._schedule(itu.next_due(self.entry_id, time.time(), time.time()))

    async def _fetch(self) -> tuple[str | None, str | None, itu.Links | None]:
        session = async_get_clientsession(self.hass)
        headers = {"User-Agent": USER_AGENT, "Accept": "application/json", "Accept-Encoding": "gzip"}
        builder = itu.LinksBuilder()
        start = 0
        for page in range(itu.MAX_PAGES):
            if page:
                await asyncio.sleep(itu.PAGE_GAP_S)
            try:
                async with session.get(itu.WFS_URL, params=itu.wfs_params(start), headers=headers,
                                       timeout=aiohttp.ClientTimeout(total=itu.PAGE_TIMEOUT_S)) as resp:
                    status = resp.status
                    retry_after = resp.headers.get("Retry-After")
                    raw = await resp.read() if status == 200 else b""
            except (aiohttp.ClientError, TimeoutError):
                return "no_answer", None, None
            if status == 429:
                return "rate_limited", retry_after, None
            if status != 200:
                return f"http_{status}", None, None
            try:
                n = await self.hass.async_add_executor_job(builder.add_page_bytes, raw)
            except itu.PageError:
                return "bad_answer", None, None
            start += n
            if n < itu.PAGE or (builder.number_matched is not None and start >= builder.number_matched):
                break
        else:
            return "too_many", None, None
        last_total = self.links.number_matched if self.links else None
        verdict = builder.verdict(last_total)
        if verdict:
            return verdict, None, None
        fetched_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        built = await self.hass.async_add_executor_job(builder.build, fetched_at)
        return None, None, built

    # ------------------------------------------------------------ for diagnostics

    def state(self) -> dict[str, Any]:
        return {"has_file": self.links is not None, "digest": self.links.digest if self.links else None,
                "meta": self.links.meta if self.links else None, "reason": self.reason,
                "failures": self._failures,
                "next_at": datetime.fromtimestamp(self.next_at, tz=timezone.utc).isoformat() if self.next_at else None,
                "slot_offset_s": itu.slot_offset_s(self.entry_id)}
