"""The landing-point file (D19): served signed in, under /api/, at a path carrying its content digest.

The file ships in cables/ and never changes while Home Assistant runs, so one view answers it from memory: the
current digest gives the gzipped bytes with Content-Encoding: gzip and a day's private cache; anything else is 404.
"""

from __future__ import annotations

from aiohttp import web

from homeassistant.components.http import KEY_HASS, HomeAssistantView

from .cables import LANDING_LAYER, POINTS_PATH
from .const import DOMAIN


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
