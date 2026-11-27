"""radar.py against records shaped as Cloudflare Radar sends them (field names and forms measured 2026-11-23,
SAW research note MEASURE_outage_build_20261123.md). The descriptions and names here are made up."""

import unittest
from datetime import datetime, timezone

from _load import load

radar = load("radar")
const = load("const")

COUNTRIES = {"CI": {"name": "Côte d'Ivoire", "lat": 7.539989, "lon": -5.54708},
             "UA": {"name": "Ukraine", "lat": 48.379433, "lon": 31.16558},
             "CH": {"name": "Switzerland", "lat": 46.818188, "lon": 8.227512},
             "RU": {"name": "Russian Federation", "lat": 61.52401, "lon": 105.318756},
             "PE": {"name": "Peru", "lat": -9.189967, "lon": -75.015152}}
REGIONS = {"686966": {"name": "Zhytomyr", "lat": 50.5, "lon": 28.5, "country_code": "UA", "country_name": "Ukraine"},
           "111": {"name": "Region A", "lat": -5.0, "lon": -80.5, "country_code": "PE", "country_name": "Peru"},
           "222": {"name": "Region B", "lat": -6.0, "lon": -79.0, "country_code": "PE", "country_name": "Peru"}}
ICONS = "/live_track_internet/icons/abc123def456"


def rec(rid, cause="POWER_OUTAGE", otype="NATIONWIDE", locations=(), asns=(), geo=(), end=None,
        desc="A made-up outage.", link="https://example.org/post/1"):
    return {"id": rid, "dataSource": "ALL", "description": desc, "scope": None, "startDate": "2026-11-23T15:30:00Z",
            "endDate": end, "locations": list(locations), "asns": [int(a[0]) for a in asns],
            "asnsDetails": [{"asn": a[0], "name": a[1], "location": {"code": a[2], "name": "x"}} for a in asns],
            "geoIds": list(geo), "linkedUrl": link, "eventType": "OUTAGE",
            "outage": {"outageCause": cause, "outageType": otype}, "locationsDetails": [], "origins": [],
            "originsDetails": [], "entities": [], "tags": []}


class TestPlacement(unittest.TestCase):
    def test_country(self):
        m, n = radar.build_markers([rec("1", locations=["CI"])], COUNTRIES, REGIONS, ICONS)
        self.assertEqual(n, [])
        self.assertEqual(len(m), 1)
        self.assertEqual(m[0]["key"], "1")
        self.assertEqual((m[0]["lat"], m[0]["lon"]), (7.53999, -5.54708))
        self.assertEqual(m[0]["name"], "Côte d'Ivoire: power outage")
        self.assertEqual(m[0]["attrs"]["place_kind"], "country")

    def test_region_wins_over_country_and_network(self):
        r = rec("2", cause="CABLE_CUT", otype="REGIONAL", locations=["UA"], asns=[("15796", "X-NET", "CH")],
                geo=["686966"])
        m, _ = radar.build_markers([r], COUNTRIES, REGIONS, ICONS)
        self.assertEqual(len(m), 1)
        self.assertEqual(m[0]["attrs"]["place_kind"], "region")
        self.assertEqual(m[0]["name"], "Zhytomyr, Ukraine: cable cut")
        self.assertEqual(m[0]["attrs"]["region_geoid"], "686966")
        self.assertEqual(m[0]["attrs"]["marker_label"], "UA")

    def test_several_regions_several_markers(self):
        m, _ = radar.build_markers([rec("3", otype="REGIONAL", locations=["PE"], geo=["111", "222"])],
                                   COUNTRIES, REGIONS, ICONS)
        self.assertEqual([x["key"] for x in m], ["3_111", "3_222"])
        self.assertEqual([x["attrs"]["identity"] for x in m], ["3/111", "3/222"])

    def test_unresolved_region_falls_back_to_country(self):
        m, n = radar.build_markers([rec("4", otype="REGIONAL", locations=["UA"], geo=["999"])], COUNTRIES, REGIONS,
                                   ICONS)
        self.assertEqual((len(m), n), (1, []))
        self.assertEqual(m[0]["attrs"]["place_kind"], "country")

    def test_network_only_is_placed_at_its_country_with_a_note(self):
        """2026-11-23: at the country's centre point, with a note; RU networks included."""
        m, _ = radar.build_markers([rec("5", cause="MILITARY_ACTION", otype="NETWORK",
                                        asns=[("29031", "LTC", "RU")])], COUNTRIES, REGIONS, ICONS)
        a = m[0]["attrs"]
        self.assertEqual(a["place_kind"], "network")
        self.assertEqual(a["country_code"], "RU")
        self.assertEqual(m[0]["name"], "LTC (AS29031), Russian Federation: military action")
        self.assertIn("Placed at the centre of Russian Federation: Cloudflare names only the network.",
                      a["marker_info"]["text"])
        self.assertEqual(a["asns"], [29031])

    def test_platform_never_drawn(self):
        r = rec("6", cause="TECHNICAL_PROBLEM", otype="PLATFORM", asns=[("32934", "META", "CH")])
        m, n = radar.build_markers([r], COUNTRIES, REGIONS, ICONS)
        self.assertEqual(m, [])
        self.assertEqual(n[0]["id"], "6")
        self.assertEqual(n[0]["type"], "PLATFORM")

    def test_nothing_known_goes_to_not_on_map(self):
        m, n = radar.build_markers([rec("7", locations=["ZZ"])], COUNTRIES, REGIONS, ICONS)
        self.assertEqual((m, len(n)), ([], 1))

    def test_needed_geoids_skips_platform(self):
        rs = [rec("8", geo=["1", "2"]), rec("9", otype="PLATFORM", geo=["3"]), rec("10", geo=["2"])]
        self.assertEqual(radar.needed_geoids(rs), ["1", "2"])

    def test_open_records_only(self):
        doc = {"result": {"annotations": [rec("11"), rec("12", end="2026-11-23T18:00:00Z")]}}
        self.assertEqual([r["id"] for r in radar.open_records(doc)], ["11"])


class TestAttributes(unittest.TestCase):
    def test_contract_fields(self):
        m, _ = radar.build_markers([rec("20", locations=["CI"])], COUNTRIES, REGIONS, ICONS)
        a = m[0]["attrs"]
        self.assertEqual(a["entity_picture"], f"{ICONS}/outage_power.svg")
        self.assertEqual(a["marker_color"], "#F9A825")
        self.assertEqual(a["marker_label"], "CI")
        self.assertEqual(a["marker_label_placement"], "heading")
        self.assertEqual(a["map_layer"], "fixed")
        self.assertEqual((a["marker_group"], a["marker_group_label"], a["marker_group_order"]),
                         ("power", "Power outage", 2))
        self.assertEqual(a["started_at"], "2026-11-23T15:30:00+00:00")
        self.assertEqual(a["outage_type"], "NATIONWIDE")
        self.assertEqual(a["marker_links"], [{"label": "Report", "url": "https://example.org/post/1"},
                                             {"label": "Radar: Côte d'Ivoire",
                                              "url": "https://radar.cloudflare.com/traffic/ci?dateStart=2026-11-22"}])
        self.assertEqual(a["attribution"], const.ATTRIBUTION)
        self.assertEqual(a["marker_info"]["title"], "Côte d'Ivoire: power outage")
        self.assertEqual(a["marker_info"]["text"].split("\n"),
                         ["Power outage, nationwide", "Since 15:30 UTC 23 Nov 2026", "A made-up outage.",
                          "Cloudflare Radar"])

    def test_d0_omissions(self):
        """Nothing unknown is sent: no empty description, no non-https link, and never a fetch time."""
        r = rec("21", locations=["CI"], desc="", link="http://example.org/x")
        r["startDate"] = None
        a = radar.build_markers([r], COUNTRIES, REGIONS, ICONS)[0][0]["attrs"]
        self.assertEqual(a["marker_links"], [{"label": "Radar: Côte d'Ivoire",
                                             "url": "https://radar.cloudflare.com/traffic/ci"}])
        for k in ("description", "linked_url", "started_at", "last_seen", "observed_at",
                  "previous_latitude", "icon_rotation_deg", "asns"):
            self.assertNotIn(k, a)
        self.assertNotIn(None, a.values())
        self.assertNotIn("", a.values())

    def test_every_cause_has_a_class_and_picture(self):
        for cause, cls in const.CAUSE_CLASS.items():
            a = radar.build_markers([rec("22", cause=cause, locations=["CI"])], COUNTRIES, REGIONS, ICONS)[0][0]["attrs"]
            self.assertEqual(a["marker_group"], cls)
            self.assertEqual(a["marker_color"], const.CLASSES[cls]["color"])

    def test_unlisted_cause_is_unknown_but_named(self):
        m, _ = radar.build_markers([rec("23", cause="SOLAR_FLARE", locations=["CI"])], COUNTRIES, REGIONS, ICONS)
        self.assertEqual(m[0]["attrs"]["marker_group"], "unknown")
        self.assertEqual(m[0]["name"], "Côte d'Ivoire: solar flare")
        self.assertEqual(m[0]["attrs"]["outage_cause"], "SOLAR_FLARE")



class TestRadarLinks(unittest.TestCase):
    """SSOT 5.3, decided 2026-11-26: one link per place; network, else region, else country; Radar's padding."""
    T = "https://radar.cloudflare.com/traffic/"

    def links(self, r):
        return [x["marker_links"] if "marker_links" in x else None for x in
                [m["attrs"] for m in radar.build_markers([r], COUNTRIES, REGIONS, ICONS)[0]]]

    def test_network_page_when_the_outage_names_one(self):
        r = rec("30", otype="REGIONAL", locations=["UA"], asns=[("15796", "X-NET", "CH")], geo=["686966"], link=None)
        self.assertEqual(self.links(r), [[{"label": "Radar: AS15796 X-NET",
                                           "url": self.T + "as15796?dateStart=2026-11-22"}]])

    def test_network_only_each_marker_its_own_networks(self):
        r = rec("31", otype="NETWORK", asns=[("1", "A", "CH"), ("2", "B", "RU"), ("3", "C", "CH")], link=None)
        self.assertEqual(self.links(r), [
            [{"label": "Radar: AS1 A", "url": self.T + "as1?dateStart=2026-11-22"},
             {"label": "Radar: AS3 C", "url": self.T + "as3?dateStart=2026-11-22"}],
            [{"label": "Radar: AS2 B", "url": self.T + "as2?dateStart=2026-11-22"}]])

    def test_region_page_otherwise(self):
        r = rec("32", otype="REGIONAL", locations=["PE"], geo=["111", "222"], link=None)
        self.assertEqual(self.links(r), [[{"label": "Radar: Region A", "url": self.T + "111?dateStart=2026-11-22"}],
                                         [{"label": "Radar: Region B", "url": self.T + "222?dateStart=2026-11-22"}]])

    def test_country_page_otherwise_report_first(self):
        self.assertEqual(self.links(rec("33", locations=["CI"])),
                         [[{"label": "Report", "url": "https://example.org/post/1"},
                           {"label": "Radar: Côte d'Ivoire", "url": self.T + "ci?dateStart=2026-11-22"}]])

    def test_at_most_four_links_report_kept(self):
        nets = [(str(n), f"N{n}", "CI") for n in range(10, 16)]
        out = self.links(rec("34", locations=["CI"], asns=nets))[0]
        self.assertEqual(len(out), 4)
        self.assertEqual(out[0]["label"], "Report")
        self.assertEqual([x["url"] for x in out[1:]],
                         [self.T + f"as{n}?dateStart=2026-11-22" for n in (10, 11, 12)])

    def test_padding_is_the_utc_day_before(self):
        for start, day in (("2026-11-23T00:15:00Z", "2026-11-22"), ("2026-11-01T05:00:00Z", "2026-10-31"),
                           ("2026-01-01T23:59:00+00:00", "2025-12-31"), ("2026-11-23T01:00:00+05:00", "2026-11-21")):
            r = rec("35", locations=["CI"], link=None)
            r["startDate"] = start
            self.assertEqual(self.links(r)[0][0]["url"], self.T + f"ci?dateStart={day}")

    def test_never_a_date_end_and_all_https(self):
        for r in (rec("36", locations=["CI"]), rec("37", otype="NETWORK", asns=[("9", "Z", "RU")])):
            for links in self.links(r):
                for x in links:
                    self.assertTrue(x["url"].startswith("https://"))
                    self.assertNotIn("dateEnd", x["url"])


class TestLookups(unittest.TestCase):
    def test_parse_locations(self):
        doc = {"result": {"locations": [{"alpha2": "CI", "name": "Côte d'Ivoire", "latitude": "7.539989",
                                         "longitude": "-5.54708"}, {"alpha2": "XX", "name": "No point"}]}}
        self.assertEqual(radar.parse_locations(doc), {"CI": {"name": "Côte d'Ivoire", "lat": 7.539989,
                                                             "lon": -5.54708}})

    def test_parse_geolocation(self):
        doc = {"result": {"geolocation": {"geoId": "12095449", "name": "Bagmati Province", "type": "ADM1",
                                          "latitude": "27.65249", "longitude": "85.39536",
                                          "parent": {"geoId": "1282988", "name": "Nepal", "type": "COUNTRY",
                                                     "code": "NP", "parent": {"type": "CONTINENT"}}}}}
        self.assertEqual(radar.parse_geolocation(doc), {"name": "Bagmati Province", "lat": 27.65249, "lon": 85.39536,
                                                        "country_code": "NP", "country_name": "Nepal"})
        self.assertIsNone(radar.parse_geolocation({"result": {"geolocation": {"name": "x"}}}))


class TestBackoff(unittest.TestCase):
    def test_steps(self):
        self.assertEqual([radar.backoff_s(n) for n in range(0, 7)], [900, 900, 1800, 3600, 7200, 7200, 7200])

    def test_rate_limit(self):
        self.assertEqual(radar.rate_limit_wait_s({"Retry-After": "120"}, 1), 120)
        self.assertEqual(radar.rate_limit_wait_s({"ratelimit": '"default";r=0;t=240'}, 1), 240)
        self.assertEqual(radar.rate_limit_wait_s({}, 2), 1800)
        self.assertEqual(radar.rate_limit_wait_s({"Retry-After": "99999"}, 1), const.RATE_LIMIT_MAX_S)
        self.assertEqual(radar.rate_limit_wait_s({"Retry-After": "5"}, 1), 60)
        now = datetime(2026, 11, 24, 7, 0, tzinfo=timezone.utc)
        self.assertEqual(radar.rate_limit_wait_s({"Retry-After": "Tue, 24 Nov 2026 07:10:00 GMT"}, 1, now), 600)


if __name__ == "__main__":
    unittest.main()
