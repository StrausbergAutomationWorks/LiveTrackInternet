"""Two files the card fetches, each at a path carrying its content digest:

* The landing points (D19): served signed in, under /api/. The file ships in cables/ and never changes while Home
  Assistant runs, so one view answers it from memory: the current digest gives the gzipped bytes with
  Content-Encoding: gzip and a day's private cache; anything else is 404.
* The terrestrial links (D12, SSOT section 7.3): served WITHOUT sign-in, as every D12 shape file is (the card fetches
  it with plain fetch()). Built on this install once a week, so it changes while Home Assistant runs: a view, not a
  static path (routes cannot be removed). The current digest gives the bytes with a month's public cache; an old or
  unknown digest is 404, and the sensor already points at the new one.
"""

from __future__ import annotations

from aiohttp import web

from homeassistant.components.http import KEY_HASS, HomeAssistantView

from .cables import LANDING_LAYER, POINTS_PATH
from .const import DOMAIN, LINKS_FETCHER
from .itu import LINKS_FILE, LINKS_PATH


class PointsView(HomeAssistantView):
    url = POINTS_PATH + "/{layer}/{digest}"
    name = f"api:{DOMAIN}:points"
    requires_auth = True

    async def get(self, request: web.Request, layer: str, digest: str) -> web.Response:
        data = request.app[KEY_HASS].data.get(DOMAIN, {}).get("cables")
        if data is None or layer != LANDING_LAYER or digest != data.point_digest:
            return web.Response(status=404)
        return web.Response(body=data.point_gz, content_type="application/json",
                            headers={"Content-Encoding": "gzip", "Cache-Control": "private, max-age=86400"})


class LinksView(HomeAssistantView):
    url = LINKS_PATH + "/{digest}/" + LINKS_FILE
    name = f"{DOMAIN}:links"
    requires_auth = False

    async def get(self, request: web.Request, digest: str) -> web.Response:
        fetcher = request.app[KEY_HASS].data.get(DOMAIN, {}).get(LINKS_FETCHER)
        links = fetcher.links if fetcher is not None else None
        if links is None or digest != links.digest:
            return web.Response(status=404)
        return web.Response(body=links.gz, content_type="application/json",
                            headers={"Content-Encoding": "gzip", "Cache-Control": "public, max-age=2678400"})
