"""Cloudflare Radar over HTTP, with the user's own token. aiohttp only, no Home Assistant.

! The token is sent in the Authorization header and never logged, never put in a URL or an error message.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Any

import aiohttp

from .const import RADAR_BASE, REQUEST_TIMEOUT, USER_AGENT, WINDOW_H

_LOGGER = logging.getLogger(__name__)


class RadarAnswer:
    """status 0 = no answer (network, timeout, a body that is not JSON)."""

    __slots__ = ("status", "data", "headers")

    def __init__(self, status: int, data: Any = None, headers: dict[str, str] | None = None) -> None:
        self.status = status
        self.data = data
        self.headers = headers or {}


async def radar_get(session: aiohttp.ClientSession, token: str, path: str,
                    params: dict[str, Any] | None = None) -> RadarAnswer:
    headers = {"Authorization": f"Bearer {token}", "User-Agent": USER_AGENT, "Accept": "application/json"}
    try:
        async with session.get(RADAR_BASE + path, params=params, headers=headers,
                               timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)) as resp:
            hdrs = {k.lower(): v for k, v in resp.headers.items()}
            raw = await resp.read()
            status = resp.status
    except (aiohttp.ClientError, TimeoutError) as err:
        _LOGGER.debug("Radar %s: no answer (%s)", path.split("/")[0], type(err).__name__)
        return RadarAnswer(0)
    if status != 200:
        return RadarAnswer(status, None, hdrs)
    try:
        return RadarAnswer(200, json.loads(raw), hdrs)
    except ValueError:
        return RadarAnswer(0, None, hdrs)


def outage_params(now: datetime | None = None) -> dict[str, Any]:
    """The poll's window: the last WINDOW_H hours. Radar returns every record that OVERLAPS a window (measured
    2026-11-23: LTC's 13-day outage came back from a 6 h window in its middle), so an outage open for weeks is
    returned too."""
    now = (now or datetime.now(timezone.utc)).replace(second=0, microsecond=0)
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    return {"dateStart": (now - timedelta(hours=WINDOW_H)).strftime(fmt), "dateEnd": now.strftime(fmt),
            "limit": 100, "format": "json"}


async def check_token(session: aiohttp.ClientSession, token: str) -> str:
    """For the setup dialog: one real outage call. 'ok', 'invalid_auth' (400/401/403: Radar answers 400 with no
    token at all, measured 2026-11-23), 'cannot_connect' or 'unknown'."""
    if not token:
        return "invalid_auth"
    ans = await radar_get(session, token, "annotations/outages", {"dateRange": "1d", "limit": 1, "format": "json"})
    if ans.status == 200 and isinstance(ans.data, dict) and ans.data.get("success") is not False:
        return "ok"
    if ans.status in (400, 401, 403):
        return "invalid_auth"
    if ans.status == 0 or ans.status >= 500 or ans.status == 429:
        return "cannot_connect"
    return "unknown"
