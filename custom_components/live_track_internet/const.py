"""Constants for Live Track Internet (SAW SSOT section 5)."""

from __future__ import annotations

DOMAIN = "live_track_internet"
NAME = "Live Track Internet"
VERSION = "0.2.0"

CONF_API_TOKEN = "api_token"

RADAR_BASE = "https://api.cloudflare.com/client/v4/radar/"
TOKEN_URL = "https://dash.cloudflare.com/profile/api-tokens"
ISSUES_URL = "https://github.com/StrausbergAutomationWorks/LiveTrackInternet/issues"
USER_AGENT = f"LiveTrackInternet/{VERSION} (+https://github.com/StrausbergAutomationWorks/LiveTrackInternet)"
REQUEST_TIMEOUT = 30

# Polling (SSOT 5.5). Radar caches the outage answer 10 minutes (max-age=600, measured 2026-11-23).
POLL_S = 900
WINDOW_H = 24                      # dateStart = now - 24 h: a window returns every record that OVERLAPS it
BACKOFF_S = (900, 1800, 3600, 7200)
RATE_LIMIT_MAX_S = 7200
KEEP_S = 7200                      # the last good answer is kept 2 h, then every marker goes
LOCATIONS_EVERY_S = 86400          # country points once a day
GEO_LOOKUPS_PER_POLL = 20

# SAW-neutral caches in .storage (project rule: never named after an integration)
LOCATIONS_CACHE = "saw_radar_locations.json"
GEOLOCATIONS_CACHE = "saw_radar_geolocations.json"

ICONS_DIR = "icons"

# D4d. The box shows the part before the first full stop; the licence link is on hover (SSOT 5.7).
ATTRIBUTION = ("Outages: Cloudflare Radar, radar.cloudflare.com, CC BY-NC 4.0, placed on the map by Live Track "
               "Internet. Licence: creativecommons.org/licenses/by-nc/4.0")

# Cause classes (SSOT 5.4): key (marker_group, permanent once shipped), colour, group label, order.
CLASSES: dict[str, dict] = {
    "cable":       {"color": "#C62828", "label": "Cable cut", "order": 1},
    "power":       {"color": "#F9A825", "label": "Power outage", "order": 2},
    "government":  {"color": "#283593", "label": "Government-directed", "order": 3},
    "military":    {"color": "#212121", "label": "Military action", "order": 4},
    "weather":     {"color": "#0277BD", "label": "Weather or natural disaster", "order": 5},
    "cyberattack": {"color": "#00897B", "label": "Cyberattack", "order": 6},
    "technical":   {"color": "#546E7A", "label": "Technical problem", "order": 7},
    "unknown":     {"color": "#757575", "label": "Unknown cause", "order": 8},
}

CAUSE_CLASS: dict[str, str] = {
    "CABLE_CUT": "cable",
    "POWER_OUTAGE": "power",
    "GOVERNMENT_DIRECTED": "government",
    "MILITARY_ACTION": "military",
    "WEATHER": "weather",
    "NATURAL_DISASTER": "weather",
    "CYBERATTACK": "cyberattack",
    "TECHNICAL_PROBLEM": "technical",
    "NETWORK_PROBLEM": "technical",
    "MECHANICAL": "technical",
    "SOFTWARE": "technical",
    "DNS": "technical",
    "MAINTENANCE": "technical",
    "UNKNOWN": "unknown",
}

# Radar's cause and type in words, for names and the click text. A cause not listed is written from its code.
CAUSE_WORDS: dict[str, str] = {
    "CABLE_CUT": "cable cut",
    "POWER_OUTAGE": "power outage",
    "GOVERNMENT_DIRECTED": "government-directed shutdown",
    "MILITARY_ACTION": "military action",
    "WEATHER": "weather",
    "NATURAL_DISASTER": "natural disaster",
    "CYBERATTACK": "cyberattack",
    "TECHNICAL_PROBLEM": "technical problem",
    "NETWORK_PROBLEM": "network problem",
    "MECHANICAL": "mechanical failure",
    "SOFTWARE": "software problem",
    "DNS": "DNS problem",
    "MAINTENANCE": "maintenance",
    "UNKNOWN": "unknown cause",
}
TYPE_WORDS: dict[str, str] = {
    "NATIONWIDE": "nationwide",
    "REGIONAL": "regional",
    "NETWORK": "one network",
    "PLATFORM": "a platform",
}
