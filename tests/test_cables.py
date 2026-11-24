"""The cable build (SAW SSOT sections 0 items 7, 8, 13 and 2): the release-time builder on MADE-UP data, finding a
cable named in an outage description (section 1a), the three publishers, and the files as shipped.

The fixtures are invented (cable names and ids included): Hotham's data is CC BY-NC-SA 4.0 and lives only in
custom_components/live_track_internet/cables/, beside its licence, where the last tests read it as shipped."""

import gzip
import importlib.util
import json
import re
import unittest
from types import SimpleNamespace

from _load import COMP, ROOT, load

_spec = importlib.util.spec_from_file_location("build_cables", ROOT / "tools" / "build_cables.py")
bc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bc)
cables = load("cables")
radar = load("radar")

LINE = {"type": "MultiLineString", "coordinates": [[[10.0, 50.0], [11.5, 51.25]], [[-179.5, 0.0], [-170.0, 1.0]]]}


def feat(fid, geom=None):
    return {"type": "Feature", "properties": {"id": fid}, "geometry": geom or LINE}


def row(cid, name, status="in service", **kw):
    r = {"id": cid, "name": name, "status": status, "rfs": "", "length_km": "", "countries": "", "owners": "",
         "suppliers": ""}
    r.update(kw)
    return r


def lp(pid, lon, lat, live=1, planned=0, name=None, country="Atlantis"):
    return {"id": pid, "name": name or pid, "country": country, "lon": str(lon), "lat": str(lat),
            "cables_in_service": str(live), "cables_planned": str(planned)}


class TestBuilder(unittest.TestCase):
    def test_join_collapses_runs_of_hyphens_and_keeps_the_csv_id(self):
        out = bc.build([feat("north-phase-1"), feat("plain")],
                       [row("north---phase-1", "North - Phase 1"), row("plain", "Plain")], [])
        self.assertEqual(sorted(out["shape_file"]["shapes"]), ["north---phase-1", "plain"])
        self.assertEqual(out["catalog"]["cables"]["north---phase-1"], {"name": "North - Phase 1", "status": "in_service"})
        self.assertEqual(out["counts"]["cables"], 2)

    def test_refusals(self):
        cases = [
            ([feat("a"), feat("b")], [row("a", "A")], "joins no CSV row"),
            ([feat("a")], [row("a", "A"), row("b", "B")], "no feature"),
            ([feat("a-b"), feat("a--b")], [row("a-b", "AB")], "two features"),
            ([feat("a-b")], [row("a-b", "AB"), row("a--b", "AB2")], "two CSV rows"),
            ([feat("a")], [row("a", "A", status="retired")], "status"),
            ([feat("a")], [row("a", "  ")], "no name"),
            ([feat("a", {"type": "Point", "coordinates": [0, 0]})], [row("a", "A")], "not a line"),
            ([feat("a", {"type": "LineString", "coordinates": [[0, 0]]})], [row("a", "A")], "fewer than two"),
            ([feat("a", {"type": "LineString", "coordinates": [[0, 0], [181, 0]]})], [row("a", "A")], "finite"),
            ([feat("a", {"type": "LineString", "coordinates": [[0, 0], [True, 0]]})], [row("a", "A")], "finite"),
            ([{"properties": {}, "geometry": LINE}], [row("a", "A")], "no id"),
        ]
        for features, rows, words in cases:
            with self.subTest(words=words), self.assertRaisesRegex(bc.BuildError, words):
                bc.build(features, rows, [])

    def test_info_text(self):
        self.assertEqual(bc.info_for(row("x", "Xcable", rfs="1999", length_km="1234.6", countries="Atlantis, Mu",
                                         owners="Owner A, Owner B", suppliers="Maker")),
                         {"title": "Xcable", "text": "In service since 1999\nLength: 1,235 km\nLands in: Atlantis, Mu\n"
                                                     "Owners: Owner A, Owner B\nSupplier: Maker"})
        self.assertEqual(bc.info_for(row("y", "Ycable", status="planned", rfs="2028 Q3")),
                         {"title": "Ycable (planned)", "text": "Planned, ready for service 2028 Q3"})
        self.assertEqual(bc.info_for(row("z", "Zcable", status="planned", length_km="0")),
                         {"title": "Zcable (planned)", "text": "Planned"})
        self.assertEqual(bc.info_for(row("w", "Wcable", length_km="n/a"))["text"], "")
        with self.assertRaisesRegex(bc.BuildError, "longer than D12"):
            bc.info_for(row("v", "V", owners="o" * 4000))

    def test_planned_cables_are_their_own_event(self):
        out = bc.build([feat("a"), feat("b")], [row("a", "A"), row("b", "B", status="planned")], [])
        self.assertEqual(cables.zones_of(out["catalog"]["cables"]), {"a": "in_service", "b": "planned"})
        self.assertEqual((out["counts"]["in_service"], out["counts"]["planned"]), (1, 1))

    def test_landing_points(self):
        out = bc.build([], [], [lp("b", 1.234567, 2.345678, name="Bay"), lp("a", -10, 20, live=0, planned=2, name="Ash")])
        pf = out["point_file"]
        self.assertEqual([c["key"] for c in pf["columns"]], ["name", "country", "in_service", "planned"])
        self.assertEqual(pf["points"], [[-10.0, 20.0, "landing_planned", "Ash", "Atlantis", 0, 2],
                                        [1.2346, 2.3457, "landing", "Bay", "Atlantis", 1, 0]])
        for p in pf["points"]:
            self.assertIn(p[2], cables.POINT_STYLES)
        with self.assertRaisesRegex(bc.BuildError, "out of range"):
            bc.build([], [], [lp("c", 200, 0)])
        with self.assertRaisesRegex(bc.BuildError, "no coordinates"):
            bc.build([], [], [{"id": "d", "lon": "", "lat": "1"}])

    def test_deterministic_bytes(self):
        out = bc.build([feat("a")], [row("a", "Ä cable")], [])
        one, two = bc.gz(bc.dumps(out["shape_file"])), bc.gz(bc.dumps(out["shape_file"]))
        self.assertEqual(one, two)
        self.assertEqual(one[4:8], b"\0\0\0\0", "gzip mtime 0")
        self.assertIn("Ä cable".encode("utf-8"), gzip.decompress(one))

    def test_credit_names_source_licence_and_changes(self):
        md = bc.credit_md({"cables": 2, "in_service": 1, "planned": 1, "pairs": 4, "points": 3}, "abc1234")
        for s in ("10.5281/zenodo.23856607", "CC BY-NC-SA 4.0", "creativecommons.org/licenses/by-nc-sa/4.0",
                  "abc1234", "TeleGeography", "What Live Track Internet changed", "No warranty"):
            self.assertIn(s, md)


CAT = {"sea5": {"name": "SeaMeWe-5", "status": "in_service"},
       "sea55": {"name": "SeaMeWe-55", "status": "planned"},
       "sol": {"name": "Sol", "status": "in_service"},
       "aae": {"name": "AAE-1", "status": "in_service"},
       "two": {"name": "2Africa", "status": "in_service"},
       "twop": {"name": "2Africa Pearls", "status": "in_service"},
       "echo1": {"name": "Echo", "status": "in_service"},
       "echo2": {"name": "Echo", "status": "planned"},
       "ronne": {"name": "Rønne-Rødvig", "status": "in_service"}}
M = cables.build_matcher(CAT)


class TestMatch(unittest.TestCase):
    def test_letters_and_digits_only(self):
        self.assertEqual(cables.match("Fault on SEA-ME-WE 5 off Pakistan", M), ["sea5"])
        self.assertEqual(cables.match("the seamewe5 system", M), ["sea5"])

    def test_never_inside_a_longer_number(self):
        self.assertEqual(cables.match("SeaMeWe-55 delayed", M), ["sea55"])
        self.assertEqual(cables.match("SeaMeWe-5 and SeaMeWe-55", M), ["sea5", "sea55"])
        # a longer number that is no cable's name: only the digit rule stops these (not "the longer match wins")
        self.assertEqual(cables.match("SeaMeWe-56 survey", M), [])
        self.assertEqual(cables.match("route 32Africa", M), [])
        self.assertEqual(cables.match("route 2Africa", M), ["two"])

    def test_short_names_must_be_whole_words(self):
        self.assertEqual(cables.match("consolidated outage near Solway", M), [])
        self.assertEqual(cables.match("the SOL cable was cut", M), ["sol"])
        self.assertEqual(cables.match("AAE-1 damaged", M), ["aae"])
        self.assertEqual(cables.match("AAE-10 damaged", M), [])
        self.assertEqual(cables.match("the echoing hall", M), [])

    def test_the_longer_match_wins(self):
        self.assertEqual(cables.match("2Africa Pearls segment down", M), ["twop"])
        self.assertEqual(cables.match("2Africa, and later 2Africa Pearls", M), ["two", "twop"])

    def test_shared_names_and_letters_beyond_ascii(self):
        self.assertEqual(cables.match("Echo repair", M), ["echo1", "echo2"])
        self.assertEqual(cables.match("RØNNE–RØDVIG cable", M), ["ronne"])

    def test_nothing_to_match(self):
        self.assertEqual(cables.match("", M), [])
        self.assertEqual(cables.match(None, M), [])
        self.assertEqual(cables.match("power outage in the capital", M), [])

    def test_matcher_is_longest_first(self):
        lens = [len(n) for n, *_ in M]
        self.assertEqual(lens, sorted(lens, reverse=True))


ALIAS_CAT = {"wacs": {"name": "West Africa Cable System (WACS)", "status": "in_service"},
             "teams": {"name": "The East African Marine System (TEAMS)", "status": "in_service"},
             "aae": {"name": "Asia Africa Europe-1 (AAE-1)", "status": "in_service"},
             "ase": {"name": "Asia Submarine-cable Express (ASE)/Cahaya Malaysia", "status": "in_service"}}
AM = cables.build_matcher(ALIAS_CAT)


class TestAliases(unittest.TestCase):
    """Bracketed short forms: whole words with their own capitals (measured over the year's records, 2026-11-24)."""

    def test_short_form_with_its_capitals(self):
        self.assertEqual(cables.match("Incident on the WACS subsea cable", AM), ["wacs"])
        self.assertEqual(cables.match("AAE-1 repair ship on site", AM), ["aae"])
        self.assertEqual(cables.match("TEAMS cable fault", AM), ["teams"])

    def test_not_in_another_case_or_inside_a_word(self):
        self.assertEqual(cables.match("Copilot and Teams calendar features", AM), [])
        self.assertEqual(cables.match("the wacs system", AM), [])
        self.assertEqual(cables.match("AAE-10 and BASE stations", AM), [])

    def test_the_name_without_brackets_matches_as_any_name(self):
        self.assertEqual(cables.match("west africa cable system outage", AM), ["wacs"])
        self.assertEqual(cables.match("Asia Africa Europe-1 cut", AM), ["aae"])

    def test_full_name_still_one_cable(self):
        self.assertEqual(cables.match("Asia Africa Europe-1 (AAE-1) and nothing else", AM), ["aae"])

    def test_matcher_marks_short_forms_exact(self):
        exact = {k for k, _, e in AM if e}
        self.assertEqual(exact, {"WACS", "TEAMS", "AAE1", "ASE"})


def fake_data():
    shapes = {k: LINE for k in CAT}
    info = {k: {"title": v["name"], "text": "In service since 2000"} for k, v in CAT.items()}
    return SimpleNamespace(shapes=shapes, info=info, catalog=CAT, zones=cables.zones_of(CAT), point_digest="abcdef012345",
                           points_url=lambda: f"{cables.POINTS_PATH}/{cables.LANDING_LAYER}/abcdef012345")


def marker(key, rid, named, title="Pakistan: unknown cause"):
    return {"key": key, "name": title, "attrs": {"identity": rid, "cables_named": named,
                                                 "marker_info": {"title": title, "text": "Unknown cause\nCloudflare Radar"}}}


class TestPublishers(unittest.TestCase):
    def test_trouble_one_line_per_cable_with_its_outages(self):
        d = fake_data()
        polys = cables.trouble_polygons([marker("1754_PK", "1754", ["sea5"]), marker("1754_AE", "1754", ["sea5"]),
                                         marker("1800", "1800", ["sea5", "two"], title="Egypt: cable cut"),
                                         marker("1900", "1900", ["unknown-id"])], d)
        self.assertEqual([p["info"]["title"] for p in polys], ["SeaMeWe-5: in trouble", "2Africa: in trouble"],
                         "one per cable, in id order (sea5, two)")
        sea = polys[0]
        self.assertEqual((sea["event"], sea["type"], sea["coordinates"]), ("trouble", LINE["type"], LINE["coordinates"]))
        self.assertEqual(sea["info"]["text"].count("Named in an open outage:"), 2, "record 1754 once, 1800 once")
        self.assertIn("Egypt: cable cut", sea["info"]["text"])
        self.assertTrue(sea["info"]["text"].startswith("In service since 2000"))
        self.assertEqual(len(polys), 2, "an id not in the shape file is skipped")

    def test_trouble_text_within_d12_limits(self):
        d = fake_data()
        many = [marker(str(i), str(i), ["sea5"], title="x" * 300) for i in range(40)]
        p = cables.trouble_polygons(many, d)[0]
        self.assertLessEqual(len(p["info"]["title"]), cables.TITLE_MAX)
        self.assertLessEqual(len(p["info"]["text"]), cables.TEXT_MAX)

    def test_no_trouble(self):
        self.assertEqual(cables.trouble_polygons([], fake_data()), [])
        self.assertEqual(cables.trouble_polygons([{"key": "1", "attrs": {"identity": "1"}}], fake_data()), [])
        a = cables.trouble_attrs([])
        self.assertEqual((a["zones"], a["polygons"]), ({}, []), "zones must be a mapping for the card to find it (D12)")

    def test_all_cables_attrs(self):
        a = cables.all_cables_attrs(fake_data(), "/live_track_internet/cables/abcdef012345/cables.json")
        self.assertEqual(a["layer_default"], "off")
        self.assertEqual(set(a["zones"].values()) - set(a["styles"]), set())
        self.assertEqual(a["styles"]["planned"]["color"], "#D9822B")
        self.assertLess(a["shape_order"], cables.TROUBLE_SHAPE_ORDER)
        for s in a["styles"].values():
            self.assertRegex(s["color"], r"^#[0-9A-F]{6}$")
            self.assertIsInstance(s["priority"], int)

    def test_trouble_styles_cased_and_on_top(self):
        s = cables.TROUBLE_STYLES[cables.TROUBLE_EVENT]
        self.assertEqual((s["color"], s["casing"], s["priority"]), ("#C62828", "#FFFFFF", 1))
        self.assertNotIn("layer_default", cables.trouble_attrs([]), "on by default (SSOT section 2)")

    def test_landing_points_attrs_follow_d19(self):
        a = cables.landing_points_attrs(fake_data())
        url = a["points_url"]
        self.assertRegex(url, r"^/api/[A-Za-z0-9_\-/]+$")
        self.assertNotIn("//", url)
        self.assertLessEqual(len(url), 200)
        self.assertEqual(a["layer_default"], "off")
        for s in a["point_styles"].values():
            self.assertTrue(2 <= s["radius"] <= 10)
            self.assertRegex(s["outline"], r"^#[0-9A-F]{6}$")

    def test_attribution_has_no_full_stop_and_names_the_licence(self):
        a = cables.ATTRIBUTION
        self.assertIsNone(re.search(r"\.(\s|$)", a), "the whole credit shows in the box (D4d)")
        for s in ("Hotham (2026)", "doi:10.5281/zenodo.23856607", "TeleGeography", "CC BY-NC-SA 4.0",
                  "creativecommons.org/licenses/by-nc-sa/4.0", "converted and joined by Live Track Internet"):
            self.assertIn(s, a)


class TestRadarNamesCables(unittest.TestCase):
    REC = {"id": 1754, "description": "Fault on SEA-ME-WE 5", "startDate": "2026-11-23T15:30:00Z",
           "outage": {"outageCause": "UNKNOWN", "outageType": "NATIONWIDE"}, "locations": ["PK"],
           "locationsDetails": [{"code": "PK", "name": "Pakistan"}]}
    COUNTRIES = {"PK": {"name": "Pakistan", "lat": 30.0, "lon": 70.0}}

    def test_cables_named_set_only_when_a_cable_is_named(self):
        m, _ = radar.build_markers([self.REC], self.COUNTRIES, {}, "/i", lambda d: cables.match(d, M))
        self.assertEqual(m[0]["attrs"]["cables_named"], ["sea5"])
        m, _ = radar.build_markers([{**self.REC, "description": "power cut"}], self.COUNTRIES, {}, "/i",
                                   lambda d: cables.match(d, M))
        self.assertNotIn("cables_named", m[0]["attrs"])
        m, _ = radar.build_markers([self.REC], self.COUNTRIES, {}, "/i")
        self.assertNotIn("cables_named", m[0]["attrs"], "no matcher, no attribute")

    def test_no_description_never_asks(self):
        calls = []
        radar.build_markers([{**self.REC, "description": ""}], self.COUNTRIES, {}, "/i", lambda d: calls.append(d) or [])
        self.assertEqual(calls, [])


class TestShippedFiles(unittest.TestCase):
    """The files as built from Hotham's commit 8ddb44d (cables/CREDIT.md)."""

    @classmethod
    def setUpClass(cls):
        cls.d = cables.CableData(COMP / cables.CABLES_DIR)

    def test_counts_measured_2026_11_24(self):
        self.assertEqual(len(self.d.catalog), 713)
        self.assertEqual(sum(c["status"] == "planned" for c in self.d.catalog.values()), 105)
        self.assertEqual(self.d.point_count, 1928)
        self.assertEqual(set(self.d.shapes), set(self.d.catalog))
        self.assertEqual(set(self.d.info), set(self.d.catalog))

    def test_digests_and_paths(self):
        self.assertRegex(self.d.shape_digest, r"^[0-9a-f]{12}$")
        self.assertRegex(self.d.points_url(), r"^/api/live_track_internet/points/landing/[0-9a-f]{12}$")
        self.assertFalse((COMP / "cables" / "web" / "cables.json").exists(), "only the .gz ships")
        self.assertEqual(sorted(p.name for p in (COMP / "cables" / "web").iterdir()), ["cables.json.gz"])

    def test_every_geometry_is_a_line_and_every_info_fits(self):
        for cid, g in self.d.shapes.items():
            self.assertIn(g["type"], ("LineString", "MultiLineString"), cid)
        for cid, i in self.d.info.items():
            self.assertTrue(0 < len(i["title"]) <= 200 and len(i["text"]) <= 4000, cid)

    def test_the_measured_submarine_fault_is_found(self):
        """Section 1a: the one submarine fault in 30 days, SEA-ME-WE 5 off Pakistan, filed UNKNOWN."""
        found = cables.match("Damage to the SEA-ME-WE 5 submarine cable off Pakistan", self.d.matcher)
        self.assertEqual([self.d.catalog[c]["name"] for c in found], ["SeaMeWe-5"])

    def test_the_years_two_real_texts(self):
        """The year's 143 records (2026-11-24): WACS found by its short form; Microsoft 365's "Teams" not a cable."""
        wacs = cables.match("Incident on the WACS subsea cable", self.d.matcher)
        self.assertEqual([self.d.catalog[c]["name"] for c in wacs], ["West Africa Cable System (WACS)"])
        self.assertEqual(cables.match("A global Microsoft 365 disruption impacted Exchange Online and dependent "
                                      "services, including Outlook, Copilot and Teams calendar features.", self.d.matcher), [])

    def test_names_are_clean_text(self):
        for c in self.d.catalog.values():
            self.assertNotIn("\ufffd", c["name"])

    def test_point_file_follows_d19(self):
        doc = json.loads(gzip.decompress(self.d.point_gz))
        n = len(doc["columns"])
        for p in doc["points"]:
            self.assertEqual(len(p), 3 + n)
            self.assertIn(p[2], cables.POINT_STYLES)
            self.assertTrue(-180 <= p[0] <= 180 and -90 <= p[1] <= 90)

    def test_licence_and_credit_beside_the_data(self):
        lic = (COMP / "cables" / "LICENSE.txt").read_text(encoding="utf-8")
        self.assertTrue(lic.startswith("Attribution-NonCommercial-ShareAlike 4.0 International"))
        credit = (COMP / "cables" / "CREDIT.md").read_text(encoding="utf-8")
        for s in ("10.5281/zenodo.23856607", "8ddb44d", "CC BY-NC-SA 4.0", "713 cables", "1,928 landing points"):
            self.assertIn(s, credit)


if __name__ == "__main__":
    unittest.main()
