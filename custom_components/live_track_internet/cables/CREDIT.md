# Submarine cable data: credit and licence

The files in this folder (`web/cables.json.gz`, `landing_points.json.gz`, `catalog.json`) are built from:

> Hotham, T. (2026) The internet's seabed: submarine cables, when they were laid, who owns them and where they crowd
> together. Zenodo. https://doi.org/10.5281/zenodo.23856607

Repository: https://github.com/Tristan-Hotham/submarine-cables, commit `8ddb44d`, files `data/cables.geojson`, `data/cables.csv`,
`data/landing_points.csv`. Hotham's data is derived from TeleGeography's Submarine Cable Map
(https://www.submarinecablemap.com/), credited to TeleGeography.

**Licence:** CC BY-NC-SA 4.0, https://creativecommons.org/licenses/by-nc-sa/4.0/ (the legal code is `LICENSE.txt` beside this file). These files are shared
under the same licence: non-commercial use only, with credit, and anything built from them under the same terms. The
rest of Live Track Internet is MIT; this licence covers only the files named above.

**What Live Track Internet changed:** joined Hotham's cable lines to his cable table by id (runs of hyphens
collapsed on both sides, his table's ids kept); converted the lines, unchanged, into a shape file for the Live Track
map, with a short text per cable built from the table's name, ready-for-service date, length, landing countries,
owners and supplier; converted the landing points into a point file (coordinates rounded to 4
decimals). Nothing was added to or corrected in the data.

**No warranty:** as the licence says, the data is offered as-is.

Built by `tools/build_cables.py`: 713 cables (608 in service, 105
planned), 13,350 coordinate pairs, 1,928 landing points.
