# Attribution

Live Track Internet ships one dataset of its own, converted from published
data, and reads two sources at runtime: one with each user's own token, one
with no key. Every entity carries an `attribution` with the credit line for its
source, which Home Assistant shows in the entity's details, and the Live Track
map card shows each source's credit in its attribution line while that
source's data are on screen. If you show this data to others, for example on a
public dashboard, keep the credit with it and read the source's own terms.

**All three data sources allow non-commercial use only.** The code in this
repository is MIT; the data it ships or shows is not, and may not be used
commercially.

None of these organisations made or endorsed this integration.

## Which licence covers which part

| Part | Licence |
|---|---|
| The code: every `.py` file, `custom_components/live_track_internet/strings.json` and `translations/`, `tools/`, `tests/` | MIT, in [LICENSE](LICENSE) |
| The outage pictures, `custom_components/live_track_internet/icons/*.svg`, drawn for StrausbergAutomationWorks | MIT, in [LICENSE](LICENSE) |
| The cable data, `custom_components/live_track_internet/cables/` (`web/cables.json.gz`, `landing_points.json.gz`, `catalog.json`) | CC BY-NC-SA 4.0, legal code in `cables/LICENSE.txt`, credit in [`cables/CREDIT.md`](custom_components/live_track_internet/cables/CREDIT.md) |
| The map card, `custom_components/live_track_internet/frontend/live-track-map-card.js` | MIT; the bundle keeps the licence notices of the code it includes (Leaflet and others) |
| Outage records, read at runtime and never stored in this repository | CC BY-NC 4.0, Cloudflare's |
| Terrestrial links, read at runtime and never stored in this repository | the ITU's terms of use |

## Shipped in this repository

| File | From | Licence |
|---|---|---|
| `custom_components/live_track_internet/cables/web/cables.json.gz`, `landing_points.json.gz`, `catalog.json` | Hotham, T. (2026), *The internet's seabed: submarine cables, when they were laid, who owns them and where they crowd together*, Zenodo, <https://doi.org/10.5281/zenodo.23856607>; repository <https://github.com/Tristan-Hotham/submarine-cables>, commit `8ddb44d`. Hotham's data is derived from TeleGeography's [Submarine Cable Map](https://www.submarinecablemap.com/) and credited to TeleGeography | CC BY-NC-SA 4.0 |
| `custom_components/live_track_internet/frontend/live-track-map-card.js` | [LiveTrackMapCard](https://github.com/StrausbergAutomationWorks/LiveTrackMapCard) release, vendored byte for byte; derived from [nathan-gs/ha-map-card](https://github.com/nathan-gs/ha-map-card) | MIT |

**What Live Track Internet changed in the cable data:** joined Hotham's cable
lines to his cable table by id (runs of hyphens collapsed on both sides, his
table's ids kept); converted the lines, unchanged, into a shape file for the
map, with a short text per cable built from the table's name, ready-for-service
date, length, landing countries, owners and supplier; converted the landing
points into a point file, coordinates rounded to 4 decimals. Nothing was added
to or corrected in the data. The converted files are shared under the same
licence, CC BY-NC-SA 4.0: non-commercial use only, with credit, and anything
built from them under the same terms. As the licence says, the data is offered
as-is. `tools/build_cables.py` rebuilds them from Hotham's files.

The credit line on the map:

> Cables: Hotham (2026), The internet's seabed, doi:10.5281/zenodo.23856607, from TeleGeography data, CC BY-NC-SA 4.0 (creativecommons.org/licenses/by-nc-sa/4.0), converted and joined by Live Track Internet

## Read at runtime with the user's own token

**Cloudflare Radar** (Cloudflare, Inc., <https://radar.cloudflare.com>): the
outage records of the Radar Outage Center, under Creative Commons
Attribution-NonCommercial 4.0
(<https://creativecommons.org/licenses/by-nc/4.0/>). Each person who installs
Live Track Internet makes their own token; none is shipped. Live Track Internet
does not change the records: it places each on the map, at the point of the
region or country it names, and says so in the credit, as the licence asks for
changes to be indicated:

> Outages: Cloudflare Radar, radar.cloudflare.com, CC BY-NC 4.0, placed on the map by Live Track Internet. Licence: creativecommons.org/licenses/by-nc/4.0

## Read at runtime with no key

**ITU Broadband Maps** (BBmaps), the Infrastructure Connectivity Map of the
International Telecommunication Union, <https://bbmaps.itu.int>, © ITU. Used
under the ITU's terms of use, which allow personal, educational or
non-commercial use with the source acknowledged. Nothing of the ITU's is
shipped in this repository: each installation fetches the links for its own
user, once a week, and keeps them in its own Home Assistant. Live Track
Internet draws the links as ITU publishes them (from node to node), rounded to
3 decimals (about 110 m), with repeated links of the same kind drawn once and
links of zero length left out, and keeps ITU's notice in the credit:

> Terrestrial links: ITU Broadband Maps (BBmaps), bbmaps.itu.int, © ITU, schematic links from node to node, placed on the map by Live Track Internet

## Drawn by the map card

The base map tiles, and any overlay the dashboard turns on, come from the
LiveTrackMapCard bundle, which credits each in the map's attribution line while
it is shown. See that card's README.
