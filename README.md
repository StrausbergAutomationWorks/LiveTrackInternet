# Live Track Internet

**English** · [Deutsch](README.de.md) · [Français](README.fr.md) · [Nederlands](README.nl.md) · [简体中文](README.zh-Hans.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Українська](README.uk.md) · [العربية](README.ar.md) · [All languages](#languages)

**Internet outages, submarine cables and fibre links for Home Assistant, on one
map.** Live Track Internet puts the internet outages that Cloudflare Radar
records anywhere in the world on your Home Assistant map, with their cause. It
also draws every submarine cable and its landing points, and the fibre and
microwave links between towns that the ITU records. When an outage names a
cable, that cable is drawn in red.

> **Live Track Internet is one module of Live Track**, a family of Home
> Assistant integrations that draw everything that moves, and the weather it
> moves through, on one shared map: aircraft, ships, trains and weather.
> Install it on its own, or beside the other modules
> ([list below](#part-of-live-track-the-other-modules)).

> **Growing, and open to ideas.** Live Track Internet covers outages, cables
> and terrestrial links worldwide today, and we are adding more data sources
> (internet exchanges and data centres are planned). Is something missing?
> [Suggest it](#help-it-grow), or add it yourself: we will help you do it.

**Status: 0.3.0, the first release.** Added to the Marketplace by link
([below](#install-it-step-by-step)); it is not in the Marketplace's catalog
yet.

Original work by StrausbergAutomationWorks. Not affiliated with, or endorsed
by, Cloudflare, Tristan Hotham, TeleGeography, the International
Telecommunication Union (ITU), or any cable owner or network operator.

> ⚠ **Not a monitor of your own internet connection.** The outages are records
> that people at Cloudflare write, often hours after an outage begins, and
> only for outages large enough to see from Cloudflare's network. **An empty
> map does not mean that the internet works everywhere.** A cable or link on
> the map says nothing about whether it carries traffic today.

---

## Contents

1. [Everything it does](#everything-it-does)
2. [Where it works](#where-it-works)
3. [Part of Live Track: the other modules](#part-of-live-track-the-other-modules)
4. [Before you start](#before-you-start)
5. [Install it, step by step](#install-it-step-by-step)
6. [Set it up, step by step](#set-it-up-step-by-step)
7. [Free keys that switch on more, step by step](#free-keys-that-switch-on-more-step-by-step)
8. [Put the map on a dashboard](#put-the-map-on-a-dashboard)
9. [Use it in automations](#use-it-in-automations)
10. [Everything on the map, in detail](#everything-on-the-map-in-detail)
11. [All the entities it creates](#all-the-entities-it-creates)
12. [What it sends and downloads](#what-it-sends-and-downloads)
13. [Help it grow](#help-it-grow)
14. [Languages](#languages)
15. [Credits and licences](#credits-and-licences)
16. [Keywords](#keywords)

---

## Everything it does

### On the map, with nothing to set up

Each of these is a layer with its own box in the map's layer control. All of
them start **off**: tick a box to show it.

| What | Where | From |
|---|---|---|
| **All cables**: every submarine cable, 608 in service and 105 planned, as thin lines; click one for its name, owners, length and landing countries | the whole world | Tristan Hotham's dataset of TeleGeography's cable data, shipped with the integration |
| **Landing points**: the 1,928 places where cables come ashore, as small dots | the whole world | the same |
| **Terrestrial links**: fibre and microwave links between towns on land, drawn straight from one node to the next | the countries where the ITU has collected them ([where](#where-it-works)) | ITU Broadband Maps (BBmaps), fetched by your Home Assistant once a week |

### Switched on by your own free key or account

| Free key or account | What it adds |
|---|---|
| **Cloudflare** API token | **Outages**: one marker for each open internet outage that Cloudflare Radar records, in the country or region it names, coloured and drawn by its cause; on by default. **Cables in trouble**: any submarine cable that an open outage names, drawn bold and red; on by default |

It takes a few minutes to get: [step by step below](#free-keys-that-switch-on-more-step-by-step).

---

## Where it works

| Region | What you get | From | Needs |
|---|---|---|---|
| **The whole world** | internet outages, in the country or region each record names | Cloudflare Radar | a free token |
| **The whole world** | submarine cables in trouble | Cloudflare Radar, and the cable data | a free token |
| **The whole world** | all submarine cables and landing points | Tristan Hotham's dataset of TeleGeography's data | nothing |
| **Africa and the Middle East** | about 5,400 terrestrial links | ITU Broadband Maps | nothing |
| **Central and South America** | about 5,500 terrestrial links | ITU Broadband Maps | nothing |
| **Europe** | about 12,400 terrestrial links | ITU Broadband Maps | nothing |
| **North America** | about 4,700 terrestrial links | ITU Broadband Maps | nothing |
| **Oceania** | about 1,400 terrestrial links | ITU Broadband Maps | nothing |
| **Russia, North and East Asia** | about 1,500 terrestrial links | ITU Broadband Maps | nothing |
| **South and South-East Asia** | about 9,500 terrestrial links | ITU Broadband Maps | nothing |

The link counts were measured on 25 November 2026 and are rough: each link is
counted by its first end. ITU publishes about 40,000 links in all.

⚠ **Coverage of terrestrial links is uneven.** The ITU shows what operators and
regulators have given it. Some countries are drawn in detail (India, Brazil,
much of Europe); others have few links or none.

Not on the list? [Tell us](#help-it-grow). Where someone publishes the data
openly, we will look at adding it.

---

## Part of Live Track: the other modules

Live Track is a set of Home Assistant integrations, one per kind of moving
thing, all drawn on the same map card. Each works on its own; together they
make one live picture. They share the map card and a Python library
([saw-livetrack](https://github.com/StrausbergAutomationWorks/LiveTrackCore)),
so installing another one adds no requests to a source another already reads.

| Module | What it puts on the map | Status |
|---|---|---|
| [Live Track Aircraft](https://github.com/StrausbergAutomationWorks/LiveTrackAircraft) | aircraft overhead from ADS-B, with routes and type icons | released |
| [Live Track Ships](https://github.com/StrausbergAutomationWorks/LiveTrackShips) | ships and boats from AIS, near you or anywhere | released |
| [Live Track Commuter Rail](https://github.com/StrausbergAutomationWorks/LiveTrackCommuterRail) | commuter trains in North America, Europe and Australia | released |
| [Live Track Intercity Rail](https://github.com/StrausbergAutomationWorks/LiveTrackIntercityRail) | intercity and long-distance trains in North America, Europe and Australia | released |
| [Live Track SALT](https://github.com/StrausbergAutomationWorks/LiveTrackSALT) | immigration and federal law-enforcement aircraft and vessels, from public lists | released |
| [Live Track Weather](https://github.com/StrausbergAutomationWorks/LiveTrackWeather) | weather, storms and natural hazards | released |
| **Live Track Internet** | internet outages, submarine cables and terrestrial links (this module) | released |
| Live Track Stations | departure boards and "time to leave" alerts for every station | planned |
| Live Track Satellites | satellites passing overhead | planned |
| Live Track Freight Trains | freight and work trains where railways publish them | planned |
| Live Track Transit | city buses, trams, ferries and metro | planned |
| Live Track Intercity Buses | intercity and regional coaches | planned |
| Live Track Commuter Buses | commuter buses | planned |
| [LiveTrackMapCard](https://github.com/StrausbergAutomationWorks/LiveTrackMapCard) | the shared map card every module draws on | released, installed with each module |

Everything is free and open source. Nothing is held back for sponsors.

---

## Before you start

* **Home Assistant** 2026.11 or later.
* **The Marketplace** (HACS) in your Home Assistant, to install and update it
  the easy way. Without it you can copy the files by hand.
* **Internet access** for Home Assistant: the outages and the terrestrial links
  come from public services.
* **Optional: auto-entities** from the Marketplace, to put the outage markers
  on the map (see [Put the map on a dashboard](#put-the-map-on-a-dashboard)).
  The cable and link layers appear without it.
* Nothing to pay and no account needed for the cables and links. The free
  Cloudflare token above is optional.
* Home Assistant installs the Python package it needs (`saw-livetrack`) by
  itself the first time the integration loads.

---

## Install it, step by step

### From the Marketplace (recommended)

Live Track Internet is not in the Marketplace's catalog yet. Add it by its
link:

1. In Home Assistant, open **Settings → Marketplace** (HACS).
2. Choose the **Add from link** tab.
3. Under **GitHub link**, enter
   `https://github.com/StrausbergAutomationWorks/LiveTrackInternet`
   and, if asked for the **Type**, choose **Integration**.
4. Find **Live Track Internet** in the list and choose **Install**.
5. **Restart Home Assistant**: **Settings → System → Repairs** offers the
   restart, or use **Settings → System → Restart Home Assistant**.

The Marketplace then offers each new release as an update.

### By hand

1. Download the source code of the
   [latest release](https://github.com/StrausbergAutomationWorks/LiveTrackInternet/releases/latest).
2. Copy its `custom_components/live_track_internet` folder into the
   `custom_components` folder of your Home Assistant configuration folder
   (create `custom_components` if it is not there).
3. Restart Home Assistant.

To update by hand, replace the folder with the new release's and restart.

---

## Set it up, step by step

1. Open **Settings → Devices & services**.
2. Choose **Add integration** (bottom right) and search for **Live Track
   Internet**.
3. **Cloudflare API token**: paste your token if you have one
   ([how to get one](#free-keys-that-switch-on-more-step-by-step)). Leave it
   empty to show the cables and links only; you can add a token later.
4. **Terrestrial links from ITU**: keep it ticked. Untick it if you do not want
   your Home Assistant to fetch the links from the ITU once a week (about
   1 MB).
5. Choose **Submit**.

That is all. The entry is titled **Cloudflare Radar** with a token, or
**Submarine cables** without one. There is one entry only: a second entry would
draw every outage twice, so it is refused.

* The cable and landing-point layers are there at once.
* With a token, open outages appear within a minute.
* The terrestrial links appear a few minutes after setup, when the first
  fetch from the ITU has finished.

Every layer starts off. Tick it in the map's layer control to see it
([Put the map on a dashboard](#put-the-map-on-a-dashboard)).

### Change the token or the ITU box later

1. Open **Settings → Devices & services → Live Track Internet**.
2. Open the entry's three-dot menu and choose **Reconfigure**.
3. Paste a new token, or leave the field empty to keep the token you have.
   Tick or untick **Terrestrial links from ITU**.
4. Choose **Submit**.

To remove the token, delete the entry (**Delete** in the same menu) and add
Live Track Internet again without one. If Cloudflare refuses your token later
(it was deleted or has expired), the outage markers stop, and Home Assistant
asks you for a new token under **Settings → Devices & services**.

---

## Free keys that switch on more, step by step

The token is free and personal: each person who installs Live Track Internet
makes their own. You need a free Cloudflare account; you do not need a website
or a domain at Cloudflare.

### Cloudflare API token (internet outages, the whole world)

1. Sign in to Cloudflare, or create a free account, at
   <https://dash.cloudflare.com>.
2. Open <https://dash.cloudflare.com/profile/api-tokens> (**My Profile → API
   Tokens**) and choose **Create Token**.
3. Do not use a template: start from scratch, with a custom token. Give it a
   name, for example `Live Track Internet`.
4. Under the permissions, choose **Account**, then **Radar**, then **Read**.
   Nothing else is needed.
5. Choose **Continue to summary**, then **Create Token**.
6. Copy the token at once: Cloudflare shows it only once.
7. Paste it into **Cloudflare API token** when you
   [set up](#set-it-up-step-by-step) Live Track Internet, or later with
   **Reconfigure**.

Live Track Internet checks the token with one real request to Cloudflare Radar
before it saves it. The token is kept in your Home Assistant and sent only to
Cloudflare. No password and no secret other than the token is needed.

---

## Put the map on a dashboard

The map is [LiveTrackMapCard](https://github.com/StrausbergAutomationWorks/LiveTrackMapCard),
the card every Live Track module draws on. **It is installed with Live Track
Internet**: nothing to download, nothing to copy, no resource to add.

1. Open a dashboard, choose the pencil (**Edit dashboard**), then **Add card**.
2. Scroll to the bottom and choose **Manual**.
3. Paste this, and choose **Save**:

```yaml
type: custom:auto-entities
card:
  type: custom:live-track-map-card
filter:
  include:
    - domain: geo_location
      attributes:
        source: live_track_internet
      options:
        display: attribute
        attribute: marker_label
  exclude:
    - state: unavailable
```

The cable and link layers appear by themselves. The outage markers come
through the filter above, which needs
[auto-entities](https://github.com/thomasloven/lovelace-auto-entities) from
the Marketplace. With other Live Track modules installed, add one more
`- domain: geo_location` filter for each of their sources
(`live_track_aircraft`, `live_track_ships` and so on).

**Without auto-entities:** LiveTrackMapCard can choose what it shows by
itself, with `entity_filter`. Paste this instead; nothing more to install:

```yaml
type: custom:live-track-map-card
entity_filter:
  include:
    - domain: geo_location
      attributes:
        source: live_track_internet
      options:
        display: attribute
        attribute: marker_label
  exclude:
    - state: unavailable
```

Other Live Track modules go in `entity_filter` the same way: one more
`- domain: geo_location` rule for each source.

**On the map:**

* The **layer control** at the top right has a box for each layer: **Cables in
  trouble**, **All cables**, **Landing points** and **Terrestrial links**.
  Each viewer's choice is kept in their own browser.
* Each outage is a round picture of its cause with the country's two-letter
  code beside it. **Point at** it to see where and why; **click** it for
  Cloudflare's description and a link to the report.
* **Click** a cable for its name, owners, length and landing countries.
  Terrestrial links are not clickable.
* The **filter card** (`custom:live-track-map-filter-card`) can hide outages by
  cause.
* The credit of each source appears in the map's attribution line while its
  data is shown.

The card keeps exactly one dashboard resource row for every Live Track module
together: the newest card version any of them carries, never an older one. A
card you installed yourself through the Marketplace is left alone. If your
dashboards' resources are set in YAML (`lovelace: resource_mode: yaml`),
nothing can be registered for you: a **Repairs** issue then gives the exact
line to add, which looks like this, with the integration's own address in
place of the placeholders:

```yaml
lovelace:
  resource_mode: yaml
  resources:
    - url: /live_track_internet/map-card/<12 hex>/live-track-map-card.js?v=<version>&h=<12 hex>
      type: module
```

Deleting the Live Track Internet entry hands the row to another Live Track
module, or removes it when none is left. If the integration's files are removed
while its entry is still set up, and no other Live Track module is installed,
remove the card's row yourself in **Settings → Dashboards → Resources**. To
install the card by hand instead, follow the card's README. A row you made
yourself, for a copy under `/local/` or at any other address, is never changed
or removed. While it loads the card, every Live Track module leaves the card to
it, even when a module carries a newer release, and nothing in **Repairs** says
so. To go back to the module's copy, remove your row in
**Settings → Dashboards → Resources** and restart Home Assistant. If you delete
your copy's file, remove its row too: while a row whose file is gone stays, the
module adds no row of its own. Any other map card that shows `geo_location`
entities shows the outage markers too, but not the cables or links.

---

## Use it in automations

Everything is an ordinary Home Assistant entity, so the automation editor
works with it, no code needed.

**A phone notification when Cloudflare records a new internet outage** (this
needs the Cloudflare token):

1. **Settings → Automations & scenes → Create automation → Create new
   automation**.
2. **When**: **Add trigger**, type `numeric` in the search box, and choose
   **Numeric state crossed threshold**. Choose the **Entity** **Cloudflare
   Radar Internet outages**, and under **Above** enter `0`.
3. **Then do**: **Add action**, search for your phone's notification action
   (it carries your phone's name), and enter a message, for example:

   ```text
   Cloudflare Radar reports an internet outage
   ```

4. **Save**.

**Other ideas:** a notification when a submarine cable is named in an outage,
from **Submarine cables Cables in trouble** above 0; a dashboard tile with the
number of open outages, from **Cloudflare Radar Internet outages**.

---

## Everything on the map, in detail

### Outages

[Cloudflare Radar](https://radar.cloudflare.com) keeps an Outage Center:
records of internet outages around the world, written by people at Cloudflare,
each with a cause, a type (nationwide, regional or one network), the countries
or regions affected, a start time and usually a link to a news report.

Live Track Internet asks for the records of the last 24 hours every 15 minutes
and draws one marker for each open record in each place it names: in the
region when the record names one, otherwise in the country. A record that
ends leaves the map. Records about one online service rather than a place (a
cloud provider's outage, for example) are not drawn; the sensor
**Cloudflare Radar Internet outages** lists them in its `not_on_map`
attribute.

⚠ **A record that names only a network is placed at the centre of its
country**, which can be far from the outage in a large country. The click text
says so. For example, Cloudflare files two networks in Luhansk and Donetsk
(Ukraine) under Russia, so their outages are placed in central Siberia, and
networks in the United States are placed in Kansas.

⚠ Outage records are written by people, often hours after an outage begins.
When we measured a year of records (to 23 November 2026), there were 143, no
more than 4 were open at once, and none was open 43% of the time. Most of the
time the map shows no outage at all.

Each marker is drawn by its cause:

| Cause | Colour | Picture |
|---|---|---|
| Cable cut | red | open scissors |
| Power outage | amber | lightning bolt |
| Government-directed (a shutdown) | indigo | padlock |
| Military action | black | crosshair |
| Weather or natural disaster | blue | storm cloud |
| Cyberattack | teal | shield with `!` |
| Technical problem (network, software, DNS, maintenance) | blue-grey | wrench |
| Unknown cause | grey | `?` |

On each marker: `outage_cause` and `outage_type` (Cloudflare's own words, for
example `POWER_OUTAGE`, `NATIONWIDE`), `started_at`, `place_kind` (`region`,
`country` or `network`), `country_code`, `country_name`, `region_name`,
`asns` and `asn_names` when the record names networks, `description`,
`linked_url` (the report), `cables_named` when the description names a cable,
and `marker_group` (the cause, for the filter card).

### Cables in trouble

With the Cloudflare token, every submarine cable named in an open outage's
description is drawn bold and red with a white edge, on by default. Usually
there is none. The cable is found by its name, written in any of the usual
ways (`SEA-ME-WE 5`, `SeaMeWe-5`); short names are matched only as whole
words.

⚠ Cloudflare's cause field does not say whether a cut cable is a submarine
cable: in the year we measured, the one record filed as a cable cut was a cable
on land, and a fault on the SEA-ME-WE 5 cable was filed as an unknown cause.
So the cable is matched in the description, whatever the cause.

### All cables and landing points

Every submarine cable in Tristan Hotham's 2026 dataset of TeleGeography's
cable data: 713 cables, 608 in service (drawn in blue) and 105 planned (drawn
in orange), as thin, faint lines, and 1,928 landing points as small dots
(orange where only planned cables land). Click a cable for its name, the date
it entered service or will, its length, its landing countries, its owners and
its supplier. The data is shipped inside the integration and changes only
with a new release.

⚠ A cable laid after the dataset was made (November 2026) appears only after
a release that carries newer data.

### Terrestrial links

The fibre and microwave links on land that the ITU's Broadband Maps
(Infrastructure Connectivity Map) record, from operators and regulators. Each
link is drawn as ITU publishes it: a straight line from one node to the next,
not the route the cable takes on the ground.

| Line | What it is |
|---|---|
| plum | fibre, in operation |
| yellow with a black edge | microwave, in operation |
| orange | planned, proposed or under construction (microwave ones with a black edge) |
| grey | no status given (microwave ones with a black edge) |

⚠ At the map's thin, faint line width the microwave lines look olive or khaki
rather than yellow; the black edge is what tells them apart from fibre.

⚠ The ITU records no operator, name, capacity or date for a link, so a link is
not clickable, and no outage is tied to one.

Your Home Assistant fetches the whole layer from the ITU once a week, on its
own weekday and hour, and keeps it. If a fetch fails or comes back incomplete,
the last good copy stays, however old.

---

## All the entities it creates

| Entity | What it is |
|---|---|
| `sensor.live_track_internet_outages` | **Cloudflare Radar Internet outages**: how many outage markers are on the map (with the token only) |
| `sensor.live_track_internet_cables_in_trouble` | **Submarine cables Cables in trouble**: how many cables an open outage names (with the token only) |
| `sensor.live_track_internet_all_cables` | **Submarine cables All cables**: the number of cables, 713 |
| `sensor.live_track_internet_landing_points` | **Submarine cables Landing points**: the number of landing points, 1,928 |
| `sensor.live_track_internet_terrestrial_links` | **ITU Broadband Maps Terrestrial links**: how many links are drawn (only while **Terrestrial links from ITU** is ticked) |
| `geo_location.outage_…` | one per open outage and place, named from Cloudflare's record number (`geo_location.outage_1754`); it comes and goes with the record |

Each marker carries `source: live_track_internet`, and its state is its
distance from your home in kilometres. The sensors sit on three devices:
**Cloudflare Radar**, **Submarine cables** and **ITU Broadband Maps**.

The outage sensor's attributes: `open_records` (every open record, those not
on the map included), `not_on_map` and `last_success`.

⚠ **The markers have no unique ID, on purpose.** Outage records come and go,
and a registry row for each would stay forever. So they cannot be renamed,
hidden or given an area in the interface. The sensors have unique IDs and can
be renamed.

Attributes that change on every update, and the large lists the map reads,
are kept out of Home Assistant's history, so your database does not grow with
them.

---

## What it sends and downloads

**About your location.** Nothing. Your home's location is used only inside
your Home Assistant, to work out each marker's distance. Cloudflare receives
your token and the time window of the request; the ITU receives the request
for its links. The cable data is shipped with the integration and is not
downloaded. Each service sees your internet address, as any website does.

**How much.** Sizes measured on 25 November 2026, unless the table says
otherwise.

| Source | What and how often | Measured size | After an error |
|---|---|---|---|
| Cloudflare Radar, outages | one request every 15 minutes, with your token: the records of the last 24 hours | 447 bytes on the wire (one record) | a refused token stops the requests and asks you for a new one. HTTP 429: waits as long as Cloudflare asks, or 15 minutes, doubling up to 2 hours. Other errors: tried again after 15, 30 and 60 minutes, then every 2 hours. The last good answer is kept for 2 hours; after that the markers go |
| Cloudflare Radar, places | the countries' centre points once a day; a region's point the first time a record names it, then kept | the country list: 36,905 bytes (23 November 2026) | the copy you have stays in use |
| ITU Broadband Maps | the whole layer once a week, in 9 requests 3 seconds apart, about 36 seconds in all | about 0.9 MB on the wire (111,537 bytes for each 5,000 links) | HTTP 429: waits as long as the ITU asks, or an hour, doubling up to a day. Other errors: tried again the next day. The last good copy stays |
| Your browser | from your Home Assistant, not from the internet: the cable file when **All cables** is ticked, the landing points when **Landing points** is ticked, and the links file when **Terrestrial links** is ticked | cables 113,323 bytes; landing points 38,160 bytes; links 296,105 bytes | |

Untick **Terrestrial links from ITU** (**Reconfigure**) to stop the weekly
fetch. Delete the entry to stop everything.

The downloaded files are kept in Home Assistant's `.storage` folder under
names beginning `saw_` (`saw_radar_locations.json`,
`saw_radar_geolocations.json`, `saw_itu_bbmaps_links.json.gz`), so another
Live Track module could share them. If you remove Live Track Internet and no
other Live Track module uses them, you can delete them by hand.

---

## Help it grow

Live Track Internet is still growing. We add data sources as we find them,
and we want to know what you would like next.

### Suggest something

Is a data source missing? Is something wrong, or hard to understand? Tell us
whichever way is easier for you:

* [**Fill in a short form**](https://github.com/StrausbergAutomationWorks/LiveTrackInternet/issues/new?template=en.yml)
  in English. You need a free GitHub account.
* **Write an email** to
  [StrausbergAutomationWorks@recordwise.org](mailto:StrausbergAutomationWorks@recordwise.org).
  No account needed.

Either way, it helps to tell us:

* what you would like to see, and where in the world;
* a link to where the data is published, if you know one (an open-data page,
  a public feed, a service's website): not needed, but it helps;
* your Home Assistant language, if the problem is the wording or a
  translation.

Write in English or in your own language, whichever is easier for you.

### Add it yourself, with our help

If you would like to add something yourself, we will help you do it, from
the first question to the finished release. You do not need to be a
developer to start:

* **A translation.** The words in the setup dialog are a short list of
  phrases in one text file. We will show you which file and which lines.
* **A new source.** Tell us where the data is published. We can write the
  code together, or look over yours.
* **Testing where you live.** Install it, look at your part of the map, and
  tell us what is right and what is not.
* **A fix to this README.** If a step did not match what you saw, tell us
  what you saw.

[**Tell us what you have in mind**](https://github.com/StrausbergAutomationWorks/LiveTrackInternet/issues/new?template=en.yml)
or write to
[StrausbergAutomationWorks@recordwise.org](mailto:StrausbergAutomationWorks@recordwise.org),
and we will reply with the next steps.

---

## Languages

This README: **English**, [Deutsch](README.de.md), [Français](README.fr.md),
[Nederlands](README.nl.md), [简体中文](README.zh-Hans.md),
[Español](README.es.md), [Italiano](README.it.md),
[Українська](README.uk.md) and [العربية](README.ar.md). Each translated
README is complete. None has yet been read by a native speaker. If one of
these is your language, please tell us whether its README reads well: see
[Help it grow](#help-it-grow).

The setup dialog appears in your Home Assistant language when it is one of
these: English, Deutsch, Español, Français, Italiano, Nederlands, 简体中文,
Українська and العربية. Any other language shows English. The dialog's
translations were also written without a native speaker. The words on the
map (the outage names and click texts, the cause names in the filter card and
the credits) are in English in every language.

Found a mistake in a translation, or need another language? Tell us at
<https://github.com/StrausbergAutomationWorks/LiveTrackInternet/issues>, or
[translate it with our help](#add-it-yourself-with-our-help).

---

## Credits and licences

* **Cloudflare Radar** (Cloudflare, Inc., <https://radar.cloudflare.com>): the
  outage records, under
  [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/), read with
  each user's own token. This integration places each record on the map; it
  does not change the records. By installing this integration you use
  Cloudflare's API, and its terms apply to you.
* **Submarine cables and landing points**: Hotham, T. (2026), *The internet's
  seabed: submarine cables, when they were laid, who owns them and where they
  crowd together*, Zenodo, <https://doi.org/10.5281/zenodo.23856607>, derived
  from TeleGeography's
  [Submarine Cable Map](https://www.submarinecablemap.com/), under
  [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). This
  integration joined the cable lines to the cable table, converted both into
  map files and rounded the landing points to 4 decimals; nothing was added or
  corrected. The converted files in
  `custom_components/live_track_internet/cables/` are shared under the same
  licence, with its legal code and a credit file beside them
  ([CREDIT.md](custom_components/live_track_internet/cables/CREDIT.md)).
* **Terrestrial links**: ITU Broadband Maps (BBmaps), the Infrastructure
  Connectivity Map, <https://bbmaps.itu.int>, © ITU. Used under the ITU's terms
  of use for non-commercial use, with the source acknowledged. Nothing of the
  ITU's is shipped in this repository: each installation fetches the links for
  its own user. This integration draws them as ITU publishes them, rounded to
  3 decimals (about 110 m), with repeated links of the same kind drawn once.
* **The outage pictures** were drawn for StrausbergAutomationWorks, under the
  MIT licence.
* **The map card** is [LiveTrackMapCard](https://github.com/StrausbergAutomationWorks/LiveTrackMapCard),
  MIT, a copy of [ha-map-card](https://github.com/nathan-gs/ha-map-card) by
  nathan-gs, MIT. Its map tiles and their credits are in its README.

⚠ **Non-commercial use only.** All three data sources allow non-commercial use
only. The code is MIT, but the data it shows may not be used commercially.

None of these organisations made or endorsed this integration. Which licence
covers which part of this repository: [ATTRIBUTION.md](ATTRIBUTION.md).

**Code**: MIT, in [LICENSE](LICENSE).

**For developers:** the entities follow the shared Live Track map contract,
so every module renders on one map. `tools/build_cables.py` rebuilds the cable
files from Hotham's repository. The tests run with
`python -m unittest discover -s tests`.

---

## Keywords

Home Assistant internet outage · internet outage map · internet shutdown ·
internet blackout · network outage · ISP outage · Cloudflare Radar · Radar
Outage Center · submarine cables · undersea cables · subsea cables · submarine
cable map · cable cut · cable landing points · TeleGeography · Submarine Cable
Map · terrestrial fibre · fiber optic map · fibre backbone · microwave links ·
ITU · ITU Broadband Maps · BBmaps · Infrastructure Connectivity Map ·
Internetausfall · Seekabel · panne internet · câbles sous-marins ·
internetstoring · zeekabels · 断网 · 海底光缆 · corte de internet · cables
submarinos · interruzione internet · cavi sottomarini · відключення інтернету ·
підводні кабелі · انقطاع الإنترنت · كابلات بحرية · geo_location · map card ·
Lovelace · HACS · Marketplace · Live Track · LiveTrack ·
StrausbergAutomationWorks

---

**Acknowledgement.** StrausbergAutomationWorks acknowledges the Indigenous
peoples of every land and water on this map, all over the world, and pays its
respect to their Elders, past and present.
