"""Release-time builder: Tristan Hotham's submarine-cable dataset -> the files Live Track Internet ships.

    python tools/build_cables.py <Hotham's data/ folder> <commit of Tristan-Hotham/submarine-cables it came from>

Reads `cables.geojson`, `cables.csv` and `landing_points.csv` (Hotham, T. (2026), The internet's seabed, Zenodo,
https://doi.org/10.5281/zenodo.23856607, CC BY-NC-SA 4.0, from TeleGeography's Submarine Cable Map data) and writes,
into custom_components/live_track_internet/cables/:

* `web/cables.json.gz`: ONE D12 shape file (06_MAP_CONTRACT_OVERLAYS.md D12 as amended 2026-11-24):
  `{"meta", "shapes": {id: MultiLineString}, "info": {id: {"title", "text"}}}`. Lines exactly as Hotham published
  them (no simplification, SAW SSOT section 0 item 13). Served unauthenticated, as Live Track Weather's zones are.
* `landing_points.json.gz`: ONE D19 point file, served signed in under /api/.
* `catalog.json`: what the running integration needs that the map does not: each cable's name and status (to
  colour planned cables, and to find a cable named in an outage record).
* `CREDIT.md`: the credit, the licence, the source commit, and what this builder changed.

`LICENSE.txt` (CC BY-NC-SA 4.0, the licence's legal code) sits beside them and is checked, not written.

The join (SAW SSOT section 0 item 8): Hotham's GeoJSON collapses TeleGeography's runs of hyphens to one, his CSV
keeps TeleGeography's ids. Join with runs of `-` collapsed on BOTH sides; the CSV's id is the key. Every feature
must join exactly one row and every row exactly one feature, or nothing is written.

Deterministic: the same input gives byte-identical output (sorted keys, gzip mtime 0), so the content digest in the
served URL changes only when the data does. Standard library only.
"""

from __future__ import annotations

import csv
import gzip
import io
import json
import math
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "custom_components", "live_track_internet", "cables")

DOI = "10.5281/zenodo.23856607"
SOURCE_REPO = "Tristan-Hotham/submarine-cables"
LICENCE = "CC BY-NC-SA 4.0"
LICENCE_URL = "https://creativecommons.org/licenses/by-nc-sa/4.0/"
STATUS = {"in service": "in_service", "planned": "planned"}   # Hotham's words -> SAW's event keys
TITLE_MAX, TEXT_MAX = 200, 4000                                # D12's info limits
POINT_DECIMALS = 4                                             # D19: at most 4 decimals


class BuildError(Exception):
    """The input is not what this builder was written for. Nothing has been written."""


def collapse(cable_id: str) -> str:
    return re.sub(r"-+", "-", cable_id)


def read_csv(path: str) -> list[dict[str, str]]:
    with io.open(path, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def _check_geometry(cid: str, g: object) -> None:
    if not isinstance(g, dict) or g.get("type") not in ("LineString", "MultiLineString"):
        raise BuildError(f"{cid}: geometry is not a line")
    parts = [g["coordinates"]] if g["type"] == "LineString" else g["coordinates"]
    if not parts or not all(isinstance(p, list) and len(p) >= 2 for p in parts):
        raise BuildError(f"{cid}: a line part has fewer than two points")
    for p in parts:
        for pt in p:
            if (not isinstance(pt, list) or len(pt) != 2
                    or not all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in pt)
                    or not -180 <= pt[0] <= 180 or not -90 <= pt[1] <= 90):
                raise BuildError(f"{cid}: a coordinate is not a finite [lon, lat]")


def _km(v: str) -> str | None:
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return f"{x:,.0f} km" if x > 0 else None


def info_for(row: dict[str, str]) -> dict[str, str]:
    """The popup of one cable (D12 `info`): plain text, English, from Hotham's columns as published."""
    planned = row["status"] == "planned"
    rfs = (row.get("rfs") or "").strip()
    lines = []
    if planned:
        lines.append(f"Planned, ready for service {rfs}" if rfs else "Planned")
    elif rfs:
        lines.append(f"In service since {rfs}")
    km = _km(row.get("length_km", ""))
    if km:
        lines.append(f"Length: {km}")
    for label, col in (("Lands in", "countries"), ("Owners", "owners"), ("Supplier", "suppliers")):
        v = (row.get(col) or "").strip()
        if v:
            lines.append(f"{label}: {v}")
    title = row["name"].strip() + (" (planned)" if planned else "")
    text = "\n".join(lines)
    if len(title) > TITLE_MAX or len(text) > TEXT_MAX:
        raise BuildError(f"{row['id']}: info longer than D12 allows ({len(title)}, {len(text)})")
    return {"title": title, "text": text}


def _pairs(g: dict) -> int:
    return len(g["coordinates"]) if g["type"] == "LineString" else sum(len(p) for p in g["coordinates"])


def build(features: list[dict], rows: list[dict[str, str]], landing: list[dict[str, str]]) -> dict[str, object]:
    """Pure: the parsed inputs in, the documents out. Raises BuildError on anything unexpected."""
    by_norm: dict[str, dict[str, str]] = {}
    for r in rows:
        if r.get("status") not in STATUS:
            raise BuildError(f"{r.get('id')}: status {r.get('status')!r} is neither 'in service' nor 'planned'")
        if not (r.get("name") or "").strip():
            raise BuildError(f"{r.get('id')}: no name")
        n = collapse(r["id"])
        if n in by_norm:
            raise BuildError(f"two CSV rows collapse to {n}")
        by_norm[n] = r
    shapes: dict[str, dict] = {}
    seen: set[str] = set()
    for f in features:
        fid = (f.get("properties") or {}).get("id")
        if not isinstance(fid, str):
            raise BuildError("a feature has no id")
        n = collapse(fid)
        if n in seen:
            raise BuildError(f"two features collapse to {n}")
        seen.add(n)
        row = by_norm.get(n)
        if row is None:
            raise BuildError(f"feature {fid} joins no CSV row")
        _check_geometry(row["id"], f.get("geometry"))
        shapes[row["id"]] = f["geometry"]
    missing = sorted(r["id"] for n, r in by_norm.items() if n not in seen)
    if missing:
        raise BuildError(f"CSV rows with no feature: {missing[:5]}")
    ids = sorted(shapes)
    info = {cid: info_for(by_norm[collapse(cid)]) for cid in ids}
    catalog = {cid: {"name": by_norm[collapse(cid)]["name"].strip(), "status": STATUS[by_norm[collapse(cid)]["status"]]}
               for cid in ids}
    points = []
    for r in landing:
        try:
            lon, lat = float(r["lon"]), float(r["lat"])
        except (KeyError, TypeError, ValueError):
            raise BuildError(f"landing point {r.get('id')}: no coordinates") from None
        if not (math.isfinite(lon) and math.isfinite(lat) and -180 <= lon <= 180 and -90 <= lat <= 90):
            raise BuildError(f"landing point {r.get('id')}: coordinates out of range")
        live = int(r.get("cables_in_service") or 0)
        planned = int(r.get("cables_planned") or 0)
        points.append([round(lon, POINT_DECIMALS), round(lat, POINT_DECIMALS),
                       "landing" if live > 0 else "landing_planned",
                       (r.get("name") or "").strip() or None, (r.get("country") or "").strip() or None, live, planned])
    points.sort(key=lambda p: (p[3] or "", p[0], p[1]))
    counts = Counter(c["status"] for c in catalog.values())
    meta = {"source": f"Hotham (2026), doi:{DOI}, from TeleGeography data", "licence": LICENCE,
            "changes": "joined to the CSV by id, converted to D12 by Live Track Internet", "cables": len(ids)}
    return {
        "shape_file": {"meta": meta, "shapes": shapes, "info": info},
        "point_file": {"meta": {**meta, "changes": "converted to D19 by Live Track Internet", "points": len(points)},
                       "columns": [{"key": "name", "label": "Landing point"}, {"key": "country", "label": "Country"},
                                   {"key": "in_service", "label": "Cables in service"},
                                   {"key": "planned", "label": "Cables planned"}],
                       "points": points},
        "catalog": {"meta": meta, "cables": catalog},
        "counts": {"cables": len(ids), "in_service": counts["in_service"], "planned": counts["planned"],
                   "points": len(points), "pairs": sum(_pairs(g) for g in shapes.values())},
    }


def dumps(doc: object) -> bytes:
    return json.dumps(doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def gz(data: bytes) -> bytes:
    return gzip.compress(data, compresslevel=9, mtime=0)


def credit_md(counts: dict, commit: str) -> str:
    return f"""# Submarine cable data: credit and licence

The files in this folder (`web/cables.json.gz`, `landing_points.json.gz`, `catalog.json`) are built from:

> Hotham, T. (2026) The internet's seabed: submarine cables, when they were laid, who owns them and where they crowd
> together. Zenodo. https://doi.org/{DOI}

Repository: https://github.com/{SOURCE_REPO}, commit `{commit}`, files `data/cables.geojson`, `data/cables.csv`,
`data/landing_points.csv`. Hotham's data is derived from TeleGeography's Submarine Cable Map
(https://www.submarinecablemap.com/), credited to TeleGeography.

**Licence:** {LICENCE}, {LICENCE_URL} (the legal code is `LICENSE.txt` beside this file). These files are shared
under the same licence: non-commercial use only, with credit, and anything built from them under the same terms. The
rest of Live Track Internet is MIT; this licence covers only the files named above.

**What Live Track Internet changed:** joined Hotham's cable lines to his cable table by id (runs of hyphens
collapsed on both sides, his table's ids kept); converted the lines, unchanged, into a shape file for the Live Track
map, with a short text per cable built from the table's name, ready-for-service date, length, landing countries,
owners and supplier; converted the landing points into a point file (coordinates rounded to {POINT_DECIMALS}
decimals). Nothing was added to or corrected in the data.

**No warranty:** as the licence says, the data is offered as-is.

Built by `tools/build_cables.py`: {counts['cables']} cables ({counts['in_service']} in service, {counts['planned']}
planned), {counts['pairs']:,} coordinate pairs, {counts['points']:,} landing points.
"""


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__.split("\n\n")[1])
        return 2
    src, commit = argv[1], argv[2]
    if not re.fullmatch(r"[0-9a-f]{7,40}", commit):
        raise BuildError("the commit must be a hex SHA")
    with open(os.path.join(src, "cables.geojson"), encoding="utf-8") as fh:
        features = json.load(fh)["features"]
    docs = build(features, read_csv(os.path.join(src, "cables.csv")), read_csv(os.path.join(src, "landing_points.csv")))
    if not os.path.isfile(os.path.join(OUT, "LICENSE.txt")):
        raise BuildError("cables/LICENSE.txt (CC BY-NC-SA 4.0 legal code) is missing")
    os.makedirs(os.path.join(OUT, "web"), exist_ok=True)
    files = {
        os.path.join(OUT, "web", "cables.json.gz"): gz(dumps(docs["shape_file"])),
        os.path.join(OUT, "landing_points.json.gz"): gz(dumps(docs["point_file"])),
        os.path.join(OUT, "catalog.json"): dumps(docs["catalog"]) + b"\n",
        os.path.join(OUT, "CREDIT.md"): credit_md(docs["counts"], commit).encode("utf-8"),
    }
    for path, data in files.items():
        with open(path, "wb") as fh:
            fh.write(data)
        with open(path, "rb") as fh:
            if fh.read() != data:
                raise BuildError(f"{path} did not read back equal")
    for path, data in files.items():
        print(f"{os.path.relpath(path, OUT)} {len(data):,} b")
    print(json.dumps(docs["counts"]))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except BuildError as err:
        print(f"REFUSED: {err}")
        sys.exit(1)
