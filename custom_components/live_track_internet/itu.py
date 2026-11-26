"""Terrestrial links from ITU Broadband Maps (BBmaps), SAW SSOT section 7. NO Home Assistant here, so the tests run
without it.

ITU's GeoServer serves the Infrastructure Connectivity Map's links as a keyless WFS layer, `trx_geocatalogue`: about
40,000 fibre and microwave links, each ONE straight segment from node to node, with a kind and a status and no
operator, name, capacity or date (measured 2026-11-25, section 7.1). Used under ITU's terms for non-commercial use,
the source acknowledged (section 0 item 16). Each install fetches the layer for itself once a week (item 17).

The fetch (section 7.3, approved 2026-11-25):

* Pages of PAGE features sorted by `uid`, PAGE_GAP_S apart, gzip. ITU allows up to 1,000,000 a request (its
  capabilities' CountDefault); 5,000 keeps one page about 1.5 MB decoded. About 111 KB a page on the wire.
* All or nothing: accepted only when the features add up to `numberMatched`, every `uid` is unique, every page agrees
  on `numberMatched`, and the total is not under half the last good file's. Otherwise the last good file stays.
* No ETag, Last-Modified or Cache-Control on ITU's answers (measured twice), so every fetch is the whole layer.
* One fixed slot a week per install, from its entry id; the first fetch FIRST_DELAY_S after setup when there is no
  file; a restart fetches only when the slot has passed.

The file (contract D12): one key per STYLE, not per link (section 7.2): `{kind}_{status}`, one MultiLineString each,
the same two ends within a style kept once, 3 decimals. 7 keys, a 285-byte `zones`, about 295 KB gzipped.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import math
import time
from dataclasses import dataclass
from email.utils import parsedate_to_datetime
from typing import Any

WFS_URL = "https://bbmaps.itu.int/geoserver/ows"
LAYER = "itu-geocatalogue:trx_geocatalogue"
PAGE = 5000
PAGE_GAP_S = 3
PAGE_TIMEOUT_S = 120
MAX_FEATURES = 250_000          # measured 40,358: anything past this is not the layer we know
MAX_PAGES = MAX_FEATURES // PAGE + 1
DECIMALS = 3                    # about 110 m
SHRINK_FLOOR = 0.5              # a total under half the last good one is refused

CACHE_FILE = "saw_itu_bbmaps_links.json.gz"     # in .storage; SAW-neutral (project rule)
LINKS_PATH = "/live_track_internet/links"        # + /<digest>/links.json, served without sign-in (D12)
LINKS_FILE = "links.json"

WEEK_S = 7 * 86400
DAY_S = 86400
FIRST_DELAY_S = 300             # the first fetch after setup, or after a start that finds the slot passed
MIN_GAP_S = DAY_S               # never two good fetches closer than this (a first fetch just before the slot)
RATE_FIRST_S = 3600             # 429 without Retry-After: 1 h, doubling, at most a day
SLOT_ANCHOR = 345600            # 1970-01-05 00:00 UTC, a Monday

# D4d: one line, no full stop, so the box shows all of it (section 7.4, decided).
ATTRIBUTION = ("Terrestrial links: ITU Broadband Maps (BBmaps), bbmaps.itu.int, © ITU, schematic links from node "
               "to node, placed on the map by Live Track Internet")
SOURCE = f"ITU Broadband Maps (BBmaps), WFS {LAYER}"

# Section 7.4, set M (2026-11-25): fibre plum, microwave yellow cased black at every status, planned,
# proposed and under construction orange (the planned cables' orange), status not given grey.
ORANGE, GREY = "#D9822B", "#808080"
STYLES: dict[str, dict[str, Any]] = {
    "fibre_operational": {"color": "#861360", "priority": 9},
    "fibre_construction": {"color": ORANGE, "priority": 10},
    "fibre_planned": {"color": ORANGE, "priority": 10},
    "fibre_unknown": {"color": GREY, "priority": 11},
    "microwave_operational": {"color": "#FFD633", "priority": 9, "casing": "#000000"},
    "microwave_construction": {"color": ORANGE, "priority": 10, "casing": "#000000"},
    "microwave_planned": {"color": ORANGE, "priority": 10, "casing": "#000000"},
    "microwave_unknown": {"color": GREY, "priority": 11, "casing": "#000000"},
}
SHAPE_ORDER = -12               # beneath All cables (-10)
LAYER_DEFAULT_OFF = "off"


# ------------------------------------------------------------------ the request


def wfs_params(start: int) -> dict[str, Any]:
    return {"service": "WFS", "version": "2.0.0", "request": "GetFeature", "typeNames": LAYER,
            "outputFormat": "application/json", "count": PAGE, "startIndex": start, "sortBy": "uid"}


# ------------------------------------------------------------------ which style a link takes


def _word(text: Any) -> str | None:
    s = str(text or "").lower()
    if "operational" in s:
        return "operational"
    if "construction" in s:
        return "construction"
    if "planned" in s or "proposed" in s:
        return "planned"
    return None


def style_key(props: dict[str, Any]) -> str:
    """`{kind}_{status}`. The status decides; an empty status falls back to the type's own word (`Fibre Planned`);
    neither gives `unknown`, grey (section 7.6 item 7: the 33 links with no type and no status)."""
    t = props.get("type_inf")
    kind = "microwave" if "microwave" in str(t or "").lower() else "fibre"
    return f"{kind}_{_word(props.get('status')) or _word(t) or 'unknown'}"


# ------------------------------------------------------------------ building the file


class PageError(ValueError):
    """An answer that is not one page of this layer."""


def _point(c: Any) -> list[float] | None:
    if not isinstance(c, (list, tuple)) or len(c) < 2:
        return None
    try:
        lon, lat = float(c[0]), float(c[1])
    except (TypeError, ValueError):
        return None
    if not (math.isfinite(lon) and math.isfinite(lat) and -180 <= lon <= 180 and -90 <= lat <= 90):
        return None
    return [round(lon, DECIMALS), round(lat, DECIMALS)]


def _parts(geom: Any) -> list[Any] | None:
    if not isinstance(geom, dict):
        return None
    t, c = geom.get("type"), geom.get("coordinates")
    if t == "LineString" and isinstance(c, list):
        return [c]
    if t == "MultiLineString" and isinstance(c, list):
        return c
    return None


class LinksBuilder:
    """Pages in, one D12 file out. Feed pages in order with add_page; then verdict(); then build()."""

    def __init__(self) -> None:
        self.groups: dict[str, list[list[list[float]]]] = {}
        self._seen: dict[str, set] = {}
        self._uids: set = set()
        self.features = 0
        self.number_matched: int | None = None
        self.dropped = {"no_geometry": 0, "bad_geometry": 0, "zero_length": 0, "duplicate": 0}
        self.problem: str | None = None

    def add_page_bytes(self, raw: bytes) -> int:
        try:
            doc = json.loads(raw)
        except ValueError as err:
            raise PageError("not JSON") from err
        return self.add_page(doc)

    def add_page(self, doc: Any) -> int:
        """Returns how many features the page held."""
        if not isinstance(doc, dict) or not isinstance(doc.get("features"), list):
            raise PageError("not a feature collection")
        nm = doc.get("numberMatched")
        if not isinstance(nm, int) or isinstance(nm, bool) or nm < 0:
            raise PageError("no numberMatched")
        if self.number_matched is None:
            self.number_matched = nm
        elif nm != self.number_matched:
            self.problem = self.problem or "number_matched_changed"
        for f in doc["features"]:
            self._add(f)
        return len(doc["features"])

    def _add(self, f: Any) -> None:
        self.features += 1
        props = f.get("properties") if isinstance(f, dict) else None
        props = props if isinstance(props, dict) else {}
        uid = props.get("uid")
        if uid is None or uid in self._uids:
            self.problem = self.problem or ("uid_missing" if uid is None else "uid_repeated")
        else:
            self._uids.add(uid)
        geom = f.get("geometry") if isinstance(f, dict) else None
        if geom is None:
            self.dropped["no_geometry"] += 1
            return
        parts = _parts(geom)
        if parts is None:
            self.dropped["bad_geometry"] += 1
            return
        key = style_key(props)
        seen = self._seen.setdefault(key, set())
        group = self.groups.setdefault(key, [])
        for part in parts:
            pts = [_point(c) for c in part] if isinstance(part, list) else [None]
            if len(pts) < 2 or any(p is None for p in pts):
                self.dropped["bad_geometry"] += 1
                continue
            if all(p == pts[0] for p in pts):
                self.dropped["zero_length"] += 1
                continue
            sig = tuple(sorted(tuple(p) for p in pts))
            if sig in seen:
                self.dropped["duplicate"] += 1
                continue
            seen.add(sig)
            group.append(pts)

    @property
    def links_drawn(self) -> int:
        return sum(len(v) for v in self.groups.values())

    def verdict(self, last_good_total: int | None = None) -> str | None:
        """None when the fetch is whole and believable; otherwise why not (the last good file then stays)."""
        if self.problem:
            return self.problem
        if self.number_matched is None:
            return "no_pages"
        if self.features != self.number_matched:
            return "incomplete"
        if self.number_matched > MAX_FEATURES:
            return "too_many"
        if not self.links_drawn:
            return "empty"
        if last_good_total and self.number_matched < last_good_total * SHRINK_FLOOR:
            return "shrunk"
        return None

    def build(self, fetched_at: str) -> "Links":
        meta = {"source": SOURCE, "credit": ATTRIBUTION, "fetched_at": fetched_at,
                "number_matched": self.number_matched, "links_drawn": self.links_drawn,
                "dropped": dict(self.dropped), "decimals": DECIMALS}
        doc = {"meta": meta,
               "shapes": {k: {"type": "MultiLineString", "coordinates": v} for k, v in sorted(self.groups.items()) if v}}
        body = json.dumps(doc, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        return Links.from_gz(gzip.compress(body, 9, mtime=0))


# ------------------------------------------------------------------ the file as kept and served


@dataclass(frozen=True)
class Links:
    gz: bytes
    digest: str
    meta: dict[str, Any]
    keys: tuple[str, ...]

    @classmethod
    def from_gz(cls, gz: bytes) -> "Links":
        """Reads a file this module wrote (the cache); raises ValueError on anything else."""
        try:
            doc = json.loads(gzip.decompress(gz))
        except (OSError, EOFError, ValueError) as err:
            raise ValueError("not a links file") from err
        if not isinstance(doc, dict) or not isinstance(doc.get("shapes"), dict) or not isinstance(doc.get("meta"), dict):
            raise ValueError("not a links file")
        keys = tuple(sorted(k for k in doc["shapes"] if k in STYLES))
        if not keys:
            raise ValueError("no known keys")
        return cls(gz=gz, digest=hashlib.sha256(gz).hexdigest()[:12], meta=doc["meta"], keys=keys)

    @property
    def url(self) -> str:
        return f"{LINKS_PATH}/{self.digest}/{LINKS_FILE}"

    @property
    def links_drawn(self) -> int:
        n = self.meta.get("links_drawn")
        return n if isinstance(n, int) else 0

    @property
    def number_matched(self) -> int | None:
        n = self.meta.get("number_matched")
        return n if isinstance(n, int) else None

    @property
    def fetched_at(self) -> str | None:
        v = self.meta.get("fetched_at")
        return v if isinstance(v, str) else None


def publisher_attrs(links: Links) -> dict[str, Any]:
    """The Terrestrial links sensor's attributes (section 7.4). Not clickable: no `info`."""
    out: dict[str, Any] = {"shapes_url": links.url, "zones": {k: k for k in links.keys},
                           "styles": {k: STYLES[k] for k in links.keys}, "layer_default": LAYER_DEFAULT_OFF,
                           "shape_order": SHAPE_ORDER}
    if links.number_matched is not None:
        out["links_total"] = links.number_matched
    if links.fetched_at:
        out["last_success"] = links.fetched_at
    return out


# ------------------------------------------------------------------ when


def slot_offset_s(entry_id: str) -> int:
    """This install's place in the week, from its entry id, so installs do not arrive together."""
    return int(hashlib.sha256(entry_id.encode("utf-8")).hexdigest()[:12], 16) % WEEK_S


def next_slot(entry_id: str, after: float) -> float:
    """The first slot strictly after `after` (seconds since the epoch, UTC)."""
    base = SLOT_ANCHOR + slot_offset_s(entry_id)
    k = math.floor((after - base) / WEEK_S) + 1
    t = base + k * WEEK_S
    return t if t > after else t + WEEK_S


def next_due(entry_id: str, last_success: float | None, now: float) -> float:
    """When to fetch next after a good fetch, or at start. No file: soon. Slot passed while down: soon."""
    if last_success is None:
        return now + FIRST_DELAY_S
    due = next_slot(entry_id, last_success + MIN_GAP_S)
    return due if due > now else now + FIRST_DELAY_S


def retry_s(reason: str, attempt: int, retry_after: str | None = None) -> int:
    """After a failed fetch. 429: Retry-After (seconds or a date), else 1 h doubling, at most a day. Anything else:
    the next day. `attempt` counts this failure, from 1."""
    if reason == "rate_limited":
        wait = _retry_after_s(retry_after)
        if wait is None:
            wait = RATE_FIRST_S * 2 ** max(0, attempt - 1)
        return int(min(max(wait, 60), DAY_S))
    return DAY_S


def _retry_after_s(value: str | None, now: float | None = None) -> float | None:
    if not value:
        return None
    v = value.strip()
    if v.isdigit():
        return float(v)
    try:
        when = parsedate_to_datetime(v)
    except (TypeError, ValueError):
        return None
    if when is None:
        return None
    return max(0.0, when.timestamp() - (time.time() if now is None else now))
