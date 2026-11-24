"""Cloudflare Radar outage records -> marker records (SAW SSOT section 5). No Home Assistant here, so it is tested
without it.

* Only OPEN records (no endDate) are drawn; PLATFORM records never are (5.1): they name a service, not a place.
* Placement, first that applies (5.2): GeoNames ids -> one marker per region, at the point Radar's own
  /radar/geolocations gives; a country -> Radar's country point; networks only -> each network's country, with a note
  that it is placed at the country's centre (Lee 2026-11-23 20:54); nothing -> not drawn.
* The record shape is Live Track Weather's (key, name, lat, lon, attrs), contract D20. D0: anything unknown is
  OMITTED, never sent as a placeholder; no last_seen, observed_at or previous_* (a record has no update time and
  does not move).
"""

from __future__ import annotations

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from collections.abc import Callable
from typing import Any

from .const import (ATTRIBUTION, BACKOFF_S, CAUSE_CLASS, CAUSE_WORDS, CLASSES, RATE_LIMIT_MAX_S, TYPE_WORDS)

TITLE_MAX = 200
TEXT_MAX = 4000


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        t = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return t if t.tzinfo else t.replace(tzinfo=timezone.utc)


def _num(value: Any) -> float | None:
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None
    return f if f == f else None


def cause_class(cause: Any) -> str:
    return CAUSE_CLASS.get(cause if isinstance(cause, str) else "", "unknown")


def cause_words(cause: Any) -> str:
    if not isinstance(cause, str) or not cause:
        return CAUSE_WORDS["UNKNOWN"]
    return CAUSE_WORDS.get(cause, cause.replace("_", " ").lower())


def type_words(otype: Any) -> str | None:
    if not isinstance(otype, str) or not otype:
        return None
    return TYPE_WORDS.get(otype, otype.replace("_", " ").lower())


# ---------------------------------------------------------------- lookups Radar answers

def parse_locations(doc: Any) -> dict[str, dict[str, Any]]:
    """GET /radar/entities/locations -> {alpha2: {name, lat, lon}}; entries without a point are dropped."""
    out: dict[str, dict[str, Any]] = {}
    for loc in ((doc or {}).get("result") or {}).get("locations") or []:
        code, lat, lon = loc.get("alpha2"), _num(loc.get("latitude")), _num(loc.get("longitude"))
        if isinstance(code, str) and len(code) == 2 and lat is not None and lon is not None:
            out[code.upper()] = {"name": loc.get("name") or code.upper(), "lat": lat, "lon": lon}
    return out


def parse_geolocation(doc: Any) -> dict[str, Any] | None:
    """GET /radar/geolocations/{id} -> {name, lat, lon, country_code, country_name}, or None without a point."""
    g = ((doc or {}).get("result") or {}).get("geolocation") or {}
    lat, lon = _num(g.get("latitude")), _num(g.get("longitude"))
    if lat is None or lon is None:
        return None
    out: dict[str, Any] = {"name": g.get("name") or str(g.get("geoId")), "lat": lat, "lon": lon}
    p = g.get("parent")
    while isinstance(p, dict):
        if p.get("type") == "COUNTRY":
            if isinstance(p.get("code"), str):
                out["country_code"] = p["code"].upper()
            if p.get("name"):
                out["country_name"] = p["name"]
            break
        p = p.get("parent")
    return out


def open_records(doc: Any) -> list[dict[str, Any]]:
    """The outage records with no end date."""
    recs = ((doc or {}).get("result") or {}).get("annotations") or []
    return [r for r in recs if isinstance(r, dict) and not r.get("endDate")]


def needed_geoids(records: list[dict[str, Any]]) -> list[str]:
    seen: list[str] = []
    for r in records:
        if (r.get("outage") or {}).get("outageType") == "PLATFORM":
            continue
        for g in r.get("geoIds") or []:
            g = str(g)
            if g.isdigit() and g not in seen:
                seen.append(g)
    return seen


# ---------------------------------------------------------------- placement (SSOT 5.2)

def places(rec: dict[str, Any], countries: dict[str, dict[str, Any]],
           regions: dict[str, dict[str, Any] | None]) -> list[dict[str, Any]]:
    """Where a record goes on the map: a list of {kind, lat, lon, country_code, country_name, region_*}.

    A region id Radar has not resolved (not looked up yet, or no point) falls back to the record's country, so a
    lookup failure never hides an outage that names one."""
    if (rec.get("outage") or {}).get("outageType") == "PLATFORM":
        return []
    out: list[dict[str, Any]] = []
    for g in rec.get("geoIds") or []:
        reg = regions.get(str(g))
        if not reg:
            continue
        cc = reg.get("country_code")
        p = {"kind": "region", "lat": reg["lat"], "lon": reg["lon"], "region_name": reg["name"],
             "region_geoid": str(g)}
        if cc:
            p["country_code"] = cc
            p["country_name"] = reg.get("country_name") or (countries.get(cc) or {}).get("name") or cc
        out.append(p)
    if out:
        return out
    codes = [c.upper() for c in rec.get("locations") or [] if isinstance(c, str)]
    kind = "country"
    if not codes:
        kind = "network"
        for a in rec.get("asnsDetails") or []:
            c = ((a or {}).get("location") or {}).get("code")
            if isinstance(c, str) and c.upper() not in codes:
                codes.append(c.upper())
    for cc in dict.fromkeys(codes):
        pt = countries.get(cc)
        if pt:
            out.append({"kind": kind, "lat": pt["lat"], "lon": pt["lon"], "country_code": cc,
                        "country_name": pt["name"]})
    return out


def _asns(rec: dict[str, Any]) -> tuple[list[int], list[str]]:
    nums, names = [], []
    for a in rec.get("asnsDetails") or []:
        try:
            n = int((a or {}).get("asn"))
        except (TypeError, ValueError):
            continue
        nums.append(n)
        names.append((a or {}).get("name") or f"AS{n}")
    if not nums:
        for a in rec.get("asns") or []:
            try:
                nums.append(int(a))
            except (TypeError, ValueError):
                continue
    return nums, names


def _place_words(p: dict[str, Any], rec: dict[str, Any]) -> str:
    if p["kind"] == "region":
        return f"{p['region_name']}, {p['country_name']}" if p.get("country_name") else p["region_name"]
    if p["kind"] == "network":
        nums, names = _asns(rec)
        net = ", ".join(f"{nm} (AS{n})" for n, nm in zip(nums, names)) if names else ", ".join(f"AS{n}" for n in nums)
        return f"{net}, {p['country_name']}" if net else p["country_name"]
    return p["country_name"]


def _since(t: datetime) -> str:
    """'Since 15:30 UTC 3 Nov 2026': the hour zero-padded, the day not."""
    u = t.astimezone(timezone.utc)
    return f"Since {u:%H:%M} UTC {u.day} {u:%b %Y}"


def _https(url: Any) -> str | None:
    return url if isinstance(url, str) and url.startswith("https://") and len(url) < 2000 else None


def build_markers(records: list[dict[str, Any]], countries: dict[str, dict[str, Any]],
                  regions: dict[str, dict[str, Any] | None], icon_base: str,
                  name_cables: Callable[[str], list[str]] | None = None,
                  ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """(markers, not_on_map). `records` are OPEN records; `icon_base` is the served icons path with no slash at the
    end. A record that cannot be placed (PLATFORM, or no country point known) goes to not_on_map. `name_cables`, when
    given, returns the cable ids a description names; a marker then carries them as `cables_named` (SSOT 5.3), which
    drives "cables in trouble"."""
    markers: list[dict[str, Any]] = []
    not_on_map: list[dict[str, Any]] = []
    for rec in records:
        rid = str(rec.get("id") or "")
        if not rid:
            continue
        outage = rec.get("outage") or {}
        cause, otype = outage.get("outageCause"), outage.get("outageType")
        cls = cause_class(cause)
        where = places(rec, countries, regions)
        desc = (rec.get("description") or "").strip()
        link = _https(rec.get("linkedUrl"))
        named = name_cables(desc) if (name_cables and desc) else []
        if not where:
            item = {"id": rid, "cause": cause or "UNKNOWN"}
            if otype:
                item["type"] = otype
            if desc:
                item["description"] = desc
            if link:
                item["linked_url"] = link
            not_on_map.append(item)
            continue
        started = parse_time(rec.get("startDate"))
        nums, names = _asns(rec)
        many = len(where) > 1
        for p in where:
            suffix = p.get("region_geoid") or p.get("country_code") or ""
            key = f"{rid}_{suffix}" if many else rid
            name = f"{_place_words(p, rec)}: {cause_words(cause)}"
            words = cause_words(cause)
            head = words[:1].upper() + words[1:]
            tw = type_words(otype)
            lines = [f"{head}, {tw}" if tw else head]
            if started:
                lines.append(_since(started))
            if desc:
                lines.append(desc)
            if p["kind"] == "network":
                lines.append(f"Placed at the centre of {p['country_name']}: Cloudflare names only the network.")
            lines.append("Cloudflare Radar")
            attrs: dict[str, Any] = {
                "identity": f"{rid}/{p['region_geoid']}" if p.get("region_geoid") and many else rid,
                "marker_label": p.get("country_code") or "",
                "marker_label_placement": "heading",
                "entity_picture": f"{icon_base}/outage_{cls}.svg",
                "marker_color": CLASSES[cls]["color"],
                "map_layer": "fixed",
                "marker_group": cls,
                "marker_group_label": CLASSES[cls]["label"],
                "marker_group_order": CLASSES[cls]["order"],
                "outage_cause": cause or "UNKNOWN",
                "place_kind": p["kind"],
                "marker_info": {"title": name[:TITLE_MAX], "text": "\n".join(lines)[:TEXT_MAX]},
                "attribution": ATTRIBUTION,
            }
            if not attrs["marker_label"]:
                del attrs["marker_label"], attrs["marker_label_placement"]
            if otype:
                attrs["outage_type"] = otype
            if started:
                attrs["started_at"] = started.astimezone(timezone.utc).isoformat()
            for k in ("country_code", "country_name", "region_name", "region_geoid"):
                if p.get(k):
                    attrs[k] = p[k]
            if nums:
                attrs["asns"] = nums
            if names:
                attrs["asn_names"] = names
            if desc:
                attrs["description"] = desc
            if link:
                attrs["linked_url"] = link
                attrs["marker_links"] = [{"label": "Report", "url": link}]
            if named:
                attrs["cables_named"] = list(named)
            markers.append({"key": key, "name": name, "lat": round(p["lat"], 5), "lon": round(p["lon"], 5),
                            "attrs": attrs})
    return markers, not_on_map


# ---------------------------------------------------------------- backoff (SSOT 5.5)

def backoff_s(failures: int) -> int:
    """Seconds until the next try after `failures` failures in a row (1 -> 15 min, 2 -> 30, 3 -> 60, then 120)."""
    if failures <= 0:
        return BACKOFF_S[0]
    return BACKOFF_S[min(failures, len(BACKOFF_S)) - 1]


def rate_limit_wait_s(headers: dict[str, str], failures: int, now: datetime | None = None) -> int:
    """After HTTP 429: Retry-After (seconds or a date), else the t= of `ratelimit`, else the backoff; capped."""
    h = {k.lower(): v for k, v in (headers or {}).items()}
    wait: float | None = None
    ra = h.get("retry-after")
    if ra:
        try:
            wait = float(ra)
        except ValueError:
            try:
                when = parsedate_to_datetime(ra)
                wait = (when - (now or datetime.now(timezone.utc))).total_seconds()
            except (TypeError, ValueError):
                wait = None
    if wait is None and h.get("ratelimit"):
        for part in h["ratelimit"].split(";"):
            part = part.strip()
            if part.startswith("t="):
                try:
                    wait = float(part[2:])
                except ValueError:
                    pass
    if wait is None or wait <= 0:
        wait = backoff_s(failures)
    return int(min(max(wait, 60), RATE_LIMIT_MAX_S))
