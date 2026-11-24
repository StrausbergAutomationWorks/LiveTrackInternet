"""Submarine cables (SAW SSOT sections 0 items 7, 8, 13 and 2). NO Home Assistant here, so the tests run without it.

The data is Tristan Hotham's (CC BY-NC-SA 4.0, from TeleGeography), converted at release by tools/build_cables.py and
shipped in cables/ beside its licence and credit. Nothing is fetched at runtime.

Three publishers, each its own checkbox on the shared map:

* All cables: D12, `shapes_url` + one `zones` event per cable (`in_service` or `planned`), off by default.
* Cables in trouble: D12 `polygons` of the cables NAMED in an open outage record's description, bold red with a
  white casing, clickable, on by default. Only with a Cloudflare Radar token (no outages, no trouble).
* Landing points: D19, `points_url` under /api/, off by default.

Finding a cable in an outage description (SAW SSOT section 1a, measured 2026-11-23): the cause field cannot (the one
submarine fault in 30 days was filed UNKNOWN); the description can, compared on letters and digits only, lower case
(`SEA-ME-WE 5` = `SeaMeWe-5` = `seamewe5`). A name of fewer than 5 such characters (`Sol`, `Echo`, `AAE-1`) must be
whole words of the description. A name never matches inside a longer number (`seamewe5` is not in `seamewe55`), and
where one matched name lies inside another match (`2Africa` in `2Africa Pearls`), only the longer counts.

Names with brackets (191 of Hotham's 713, `Asia Africa Europe-1 (AAE-1)`, `West Africa Cable System (WACS)`) also match
by the name without the brackets, as above, and by each bracketed short form, but that only as WHOLE WORDS WITH ITS
OWN CAPITALS (`WACS`, `AAE-1`, never `Teams` for `TEAMS`). Measured over the year's 143 records (2026-11-24): names
alone found 1 cable (SEA-ME-WE 5, right); short forms as any other name added one right (WACS, a CABLE_CUT record
the names missed) and one wrong (`Teams` in a Microsoft 365 record); with their capitals, the right one only.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

CABLES_DIR = "cables"
WEB_DIR = "web"                       # the only folder served unauthenticated (D12)
SHAPE_FILE = "cables.json"            # requested name; shipped only as cables.json.gz (Home Assistant serves the .gz)
POINT_FILE = "landing_points.json.gz"
CATALOG_FILE = "catalog.json"
POINTS_PATH = "/api/live_track_internet/points"   # D19: under /api/, signed in
LANDING_LAYER = "landing"

SHORT = 5                             # names with fewer letters and digits must be whole words (section 1a)
TITLE_MAX, TEXT_MAX = 200, 4000       # D12's info limits

# One credit for all three publishers, so the card shows it once. No full stop: the whole line is the credit.
ATTRIBUTION = ("Cables: Hotham (2026), The internet's seabed, doi:10.5281/zenodo.23856607, from TeleGeography data, "
               "CC BY-NC-SA 4.0 (creativecommons.org/licenses/by-nc-sa/4.0), converted and joined by Live Track "
               "Internet")

# Colours (Lee 2026-11-24, from pictures): in-service cables blue, planned orange, trouble red with a white casing.
# The card draws lines from the file at its own thin, faint default (1 px at 0.5); weight and opacity are the card's.
ALL_STYLES = {"in_service": {"color": "#3F6E9A", "priority": 9},
              "planned": {"color": "#D9822B", "priority": 10}}
TROUBLE_EVENT = "trouble"
TROUBLE_STYLES = {TROUBLE_EVENT: {"color": "#C62828", "priority": 1, "casing": "#FFFFFF"}}
POINT_STYLES = {"landing": {"color": "#3F6E9A", "label": "Cable landing point", "radius": 3, "outline": "#FFFFFF"},
                "landing_planned": {"color": "#D9822B", "label": "Cable landing point (planned cables only)",
                                    "radius": 3, "outline": "#FFFFFF"}}
# D12 as amended for D16: a lower shape_order is drawn beneath. All cables under everything else; trouble on top.
ALL_SHAPE_ORDER = -10
TROUBLE_SHAPE_ORDER = 10
POINT_ORDER = 0
LAYER_DEFAULT_OFF = "off"


# ------------------------------------------------------------------ the shipped files


class CableData:
    """The shipped files, read once per Home Assistant run (blocking: call from an executor)."""

    def __init__(self, folder: Path) -> None:
        self.folder = folder
        shape_gz = (folder / WEB_DIR / (SHAPE_FILE + ".gz")).read_bytes()
        self.shape_digest = hashlib.sha256(shape_gz).hexdigest()[:12]
        doc = json.loads(gzip.decompress(shape_gz))
        self.shapes: dict[str, dict] = doc["shapes"]
        self.info: dict[str, dict] = doc.get("info") or {}
        self.point_gz = (folder / POINT_FILE).read_bytes()
        self.point_digest = hashlib.sha256(self.point_gz).hexdigest()[:12]
        self.point_count = len(json.loads(gzip.decompress(self.point_gz))["points"])
        self.catalog: dict[str, dict] = json.loads((folder / CATALOG_FILE).read_text(encoding="utf-8"))["cables"]
        self.matcher = build_matcher(self.catalog)

    @property
    def zones(self) -> dict[str, str]:
        return zones_of(self.catalog)

    def points_url(self) -> str:
        return f"{POINTS_PATH}/{LANDING_LAYER}/{self.point_digest}"


def zones_of(catalog: dict[str, dict]) -> dict[str, str]:
    """Every cable, one event each (D12 rule: one event per key)."""
    return {cid: ("planned" if c.get("status") == "planned" else "in_service") for cid, c in sorted(catalog.items())}


# ------------------------------------------------------------------ names in outage descriptions


def _norm_chars(text: str, fold: bool = True) -> str:
    t = unicodedata.normalize("NFKC", text)
    return "".join(ch for ch in (t.casefold() if fold else t) if ch.isalnum())


def normalize(text: str) -> str:
    """Letters and digits only, lower case (section 1a)."""
    return _norm_chars(text or "")


def _words(text: str, fold: bool = True) -> list[str]:
    return [w for w in (_norm_chars(t, fold) for t in re.split(r"[^\w]+|_", text or "")) if w]


def build_matcher(catalog: dict[str, dict]) -> list[tuple[str, tuple[str, ...], bool]]:
    """[(key, cable ids, exact)], longest key first. Two cables may share a key. `exact` marks a bracketed short
    form: letters and digits with their capitals, matched as whole words only."""
    keys: dict[tuple[str, bool], set[str]] = {}
    for cid, c in catalog.items():
        name = c.get("name", "") or ""
        n = normalize(name)
        if n:
            keys.setdefault((n, False), set()).add(cid)
        if "(" in name:
            base = normalize(re.sub(r"\([^)]*\)", " ", name))
            if base and base != n:
                keys.setdefault((base, False), set()).add(cid)
            for part in re.findall(r"\(([^)]*)\)", name):
                a = _norm_chars(part, fold=False)
                if a:
                    keys.setdefault((a, True), set()).add(cid)
    return sorted(((k, tuple(sorted(ids)), exact) for (k, exact), ids in keys.items()),
                  key=lambda x: (-len(x[0]), x[0], x[2]))


def _spans_long(name: str, text: str) -> list[tuple[int, int]]:
    out, start = [], 0
    while True:
        i = text.find(name, start)
        if i < 0:
            return out
        j = i + len(name)
        # never inside a longer number
        if not ((name[0].isdigit() and i > 0 and text[i - 1].isdigit())
                or (name[-1].isdigit() and j < len(text) and text[j].isdigit())):
            out.append((i, j))
        start = i + 1


def _spans_short(name: str, words: list[str], offsets: list[int]) -> list[tuple[int, int]]:
    """The name equal to one word or to several consecutive words joined (`AAE-1` = `aae` + `1`)."""
    out = []
    for i in range(len(words)):
        joined = ""
        for j in range(i, min(i + 4, len(words))):
            joined += words[j]
            if joined == name:
                out.append((offsets[i], offsets[i] + len(name)))
                break
            if len(joined) >= len(name):
                break
    return out


def match(description: str, matcher: list[tuple[str, tuple[str, ...], bool]]) -> list[str]:
    """The cable ids named in a description, sorted. Empty for no description."""
    if not description:
        return []
    text = normalize(description)
    words = _words(description)
    words_cs = _words(description, fold=False)   # the same words with their capitals, for the short forms
    offsets, pos = [], 0
    for w in words:   # each word's offset in the normalized text (the words concatenated ARE the text)
        offsets.append(pos)
        pos += len(w)
    found: list[tuple[int, int, tuple[str, ...]]] = []
    for name, ids, exact in matcher:
        if exact:
            spans = _spans_short(name, words_cs, offsets) if len(words_cs) == len(words) else []
        else:
            spans = _spans_short(name, words, offsets) if len(name) < SHORT else _spans_long(name, text)
        found.extend((a, b, ids) for a, b in spans)
    kept: set[str] = set()
    for a, b, ids in found:
        if any(a2 <= a and b <= b2 and (b2 - a2) > (b - a) for a2, b2, _ in found):
            continue  # inside a longer match
        kept.update(ids)
    return sorted(kept)


# ------------------------------------------------------------------ the three publishers


def all_cables_attrs(data: CableData, shapes_url: str) -> dict[str, Any]:
    return {"shapes_url": shapes_url, "zones": data.zones, "styles": ALL_STYLES, "shape_order": ALL_SHAPE_ORDER,
            "layer_default": LAYER_DEFAULT_OFF}


def landing_points_attrs(data: CableData) -> dict[str, Any]:
    return {"points_url": data.points_url(), "point_styles": POINT_STYLES, "point_order": POINT_ORDER,
            "layer_default": LAYER_DEFAULT_OFF}


def trouble_polygons(markers: list[dict[str, Any]], data: CableData) -> list[dict[str, Any]]:
    """One clickable line per cable named in an open outage's description; its text says which outage(s)."""
    named: dict[str, list[dict[str, Any]]] = {}
    seen_records: set[tuple[str, str]] = set()
    for m in markers:
        for cid in m.get("attrs", {}).get("cables_named") or []:
            rec_id = str(m["attrs"].get("identity", "")).split("/")[0]
            if (cid, rec_id) in seen_records or cid not in data.shapes:
                continue
            seen_records.add((cid, rec_id))
            named.setdefault(cid, []).append(m)
    out = []
    for cid in sorted(named):
        geom = data.shapes[cid]
        base = data.info.get(cid) or {"title": data.catalog.get(cid, {}).get("name", cid), "text": ""}
        parts = [base.get("text", "")] if base.get("text") else []
        for m in named[cid]:
            mi = m["attrs"].get("marker_info") or {}
            parts.append("Named in an open outage: " + (mi.get("title") or m.get("name", "")) + "\n" + (mi.get("text") or ""))
        text = "\n\n".join(p.strip() for p in parts if p.strip())
        out.append({"event": TROUBLE_EVENT, "type": geom["type"], "coordinates": geom["coordinates"],
                    "info": {"title": f"{base['title']}: in trouble"[:TITLE_MAX], "text": text[:TEXT_MAX]}})
    return out


def trouble_attrs(polygons: list[dict[str, Any]]) -> dict[str, Any]:
    return {"zones": {}, "polygons": polygons, "styles": TROUBLE_STYLES, "shape_order": TROUBLE_SHAPE_ORDER}
