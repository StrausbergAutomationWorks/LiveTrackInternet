"""Terrestrial links (itu.py): the style rule, the builder, the all-or-nothing verdict, the file, the publisher, the
weekly slot and the retry waits. The pages here are MADE UP in the shape ITU's WFS answered on 2026-11-25; ITU's own
content stays out of the repository."""

import gzip
import json
import re
import unittest

from _load import load

itu = load("itu")


def feat(uid, a, b, type_inf="Fibre Operational", status="Operational", geom=True):
    g = {"type": "LineString", "coordinates": [list(a), list(b)]} if geom else None
    return {"type": "Feature", "id": f"trx_geocatalogue.{uid}", "geometry": g,
            "properties": {"uid": uid, "id": 0, "type_inf": type_inf, "status": status, "type_": 3}}


def page(features, number_matched):
    return {"type": "FeatureCollection", "features": features, "totalFeatures": number_matched,
            "numberMatched": number_matched, "numberReturned": len(features), "timeStamp": "2026-11-25T00:00:00Z",
            "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::4326"}}}


class TestStyleKey(unittest.TestCase):
    def test_every_pair_measured(self):
        """Every (type_inf, status) pair ITU served on 2026-11-25 (SAW SSOT 7.7)."""
        want = {
            ("Fibre Operational", "Operational"): "fibre_operational",
            ("Microwave Operational", "Operational"): "microwave_operational",
            ("Fibre Planned", "Planned"): "fibre_planned",
            ("Fibre Under Construction", "Under Construction"): "fibre_construction",
            ("Fibre Proposed", "Proposed"): "fibre_planned",
            ("Microwave Planned", "Planned"): "microwave_planned",
            ("Fibre Planned", "Fibre Planned"): "fibre_planned",
            (None, None): "fibre_unknown",
            ("Fibre Planned", "Proposed"): "fibre_planned",
            ("SCO OFC Network", "Operational"): "fibre_operational",
            ("Microwave Under Construction", "Under Construction"): "microwave_construction",
            ("Fibre Operational", "Planned"): "fibre_planned",              # the status decides
            ("Fibre Under Construction", "Under construction"): "fibre_construction",
            ("Fibre Under Construction", "Operational"): "fibre_operational",
            ("Fibre Under Construction", "Construction"): "fibre_construction",
            ("Fibre Planned", None): "fibre_planned",                       # no status: the type's own word
            ("Fibre Planned", "Under Construction"): "fibre_construction",
            ("Fibre Proposed", "Fibre Operational"): "fibre_operational",
        }
        for (t, s), k in want.items():
            self.assertEqual(itu.style_key({"type_inf": t, "status": s}), k, (t, s))

    def test_grey_only_with_neither(self):
        self.assertEqual(itu.style_key({}), "fibre_unknown")
        self.assertEqual(itu.style_key({"type_inf": "", "status": ""}), "fibre_unknown")
        self.assertEqual(itu.style_key({"type_inf": "Microwave", "status": None}), "microwave_unknown")
        self.assertEqual(itu.style_key({"type_inf": "SCO OFC Network", "status": None}), "fibre_unknown")

    def test_every_key_has_a_style(self):
        for kind in ("fibre", "microwave"):
            for st in ("operational", "construction", "planned", "unknown"):
                self.assertIn(f"{kind}_{st}", itu.STYLES)


class TestBuilder(unittest.TestCase):
    def test_kept_dropped_and_rounded(self):
        b = itu.LinksBuilder()
        n = b.add_page(page([
            feat(1, (10.123456, 50.987654), (11.0, 51.0)),
            feat(2, (11.0, 51.0), (10.12349, 50.98771)),        # the same two ends, reversed, after rounding
            feat(3, (11.0, 51.0), (10.12349, 50.98771), "Microwave Operational"),   # same ends, other style: kept
            feat(4, (5.00001, 5.00002), (5.00003, 5.00004)),    # zero length at 3 decimals
            feat(5, (0, 0), (1, 1), geom=False),
            feat(6, (200, 0), (1, 1)),                          # longitude out of range
            feat(7, (1, 1), (2, 2), None, None),
            feat(8, (0, 95), (1, 1)),                           # latitude out of range
        ], 8))
        self.assertEqual(n, 8)
        self.assertEqual(b.dropped, {"no_geometry": 1, "bad_geometry": 2, "zero_length": 1, "duplicate": 1})
        self.assertEqual(b.links_drawn, 3)
        self.assertEqual(b.groups["fibre_operational"], [[[10.123, 50.988], [11.0, 51.0]]])
        self.assertIn("microwave_operational", b.groups)
        self.assertIn("fibre_unknown", b.groups)
        self.assertIsNone(b.verdict())

    def test_multilinestring_parts(self):
        b = itu.LinksBuilder()
        f = feat(1, (0, 0), (1, 1))
        f["geometry"] = {"type": "MultiLineString", "coordinates": [[[0, 0], [1, 1]], [[2, 2], [3, 3]]]}
        b.add_page(page([f], 1))
        self.assertEqual(b.links_drawn, 2)

    def test_bytes_and_bad_pages(self):
        b = itu.LinksBuilder()
        self.assertEqual(b.add_page_bytes(json.dumps(page([feat(1, (0, 0), (1, 1))], 1)).encode()), 1)
        for bad in (b"<html>", b"[]", json.dumps({"features": []}).encode(),
                    json.dumps({"features": [], "numberMatched": "40358"}).encode()):
            with self.assertRaises(itu.PageError):
                itu.LinksBuilder().add_page_bytes(bad)


class TestVerdict(unittest.TestCase):
    def built(self, n, matched=None, uids=None):
        b = itu.LinksBuilder()
        uids = uids or list(range(1, n + 1))
        b.add_page(page([feat(u, (i * 0.01, 0), (i * 0.01, 1)) for i, u in enumerate(uids)], matched or n))
        return b

    def test_whole(self):
        self.assertIsNone(self.built(10).verdict(last_good_total=10))

    def test_incomplete(self):
        self.assertEqual(self.built(9, matched=10).verdict(), "incomplete")

    def test_uid_repeated(self):
        self.assertEqual(self.built(3, uids=[1, 2, 2]).verdict(), "uid_repeated")

    def test_number_matched_changed_between_pages(self):
        b = itu.LinksBuilder()
        b.add_page(page([feat(1, (0, 0), (1, 1))], 2))
        b.add_page(page([feat(2, (0, 0), (2, 2))], 3))
        self.assertEqual(b.verdict(), "number_matched_changed")

    def test_shrunk(self):
        self.assertEqual(self.built(49).verdict(last_good_total=100), "shrunk")
        self.assertIsNone(self.built(50).verdict(last_good_total=100))       # exactly half is accepted
        self.assertIsNone(self.built(49).verdict(last_good_total=None))      # no last file: nothing to compare

    def test_empty_and_none(self):
        self.assertEqual(itu.LinksBuilder().verdict(), "no_pages")
        b = itu.LinksBuilder()
        b.add_page(page([feat(1, (0, 0), (0, 0))], 1))
        self.assertEqual(b.verdict(), "empty")

    def test_too_many(self):
        b = self.built(2)
        b.number_matched = b.features = itu.MAX_FEATURES + 1
        self.assertEqual(b.verdict(), "too_many")


class TestFile(unittest.TestCase):
    def build(self):
        b = itu.LinksBuilder()
        b.add_page(page([feat(1, (0, 0), (1, 1)), feat(2, (1, 1), (2, 2), "Microwave Operational"),
                         feat(3, (2, 2), (3, 3), "Fibre Planned", "Planned")], 3))
        return b.build("2026-11-25T12:00:00+00:00")

    def test_d12_shape_and_meta(self):
        links = self.build()
        doc = json.loads(gzip.decompress(links.gz))
        self.assertEqual(set(doc), {"meta", "shapes"})
        self.assertEqual(list(doc["shapes"]), sorted(doc["shapes"]))
        for g in doc["shapes"].values():
            self.assertEqual(g["type"], "MultiLineString")
        m = doc["meta"]
        self.assertEqual((m["fetched_at"], m["number_matched"], m["links_drawn"]), ("2026-11-25T12:00:00+00:00", 3, 3))
        self.assertEqual(m["credit"], itu.ATTRIBUTION)
        self.assertEqual(links.keys, ("fibre_operational", "fibre_planned", "microwave_operational"))
        self.assertRegex(links.digest, r"^[0-9a-f]{12}$")
        self.assertEqual(links.url, f"/live_track_internet/links/{links.digest}/links.json")

    def test_same_input_same_bytes(self):
        """The digest is the URL: the same layer must give the same bytes on any day (gzip's mtime field zero)."""
        gz = self.build().gz
        self.assertEqual(gz, self.build().gz)
        self.assertEqual(gz[4:8], b"\x00\x00\x00\x00")

    def test_cache_round_trip_and_junk(self):
        links = self.build()
        again = itu.Links.from_gz(links.gz)
        self.assertEqual((again.digest, again.keys, again.links_drawn, again.number_matched, again.fetched_at),
                         (links.digest, links.keys, 3, 3, "2026-11-25T12:00:00+00:00"))
        for junk in (b"", b"not gzip", gzip.compress(b"{}"), gzip.compress(b'{"meta": {}, "shapes": {"x": {}}}')):
            with self.assertRaises(ValueError):
                itu.Links.from_gz(junk)


class TestPublisher(unittest.TestCase):
    def test_attrs(self):
        b = itu.LinksBuilder()
        b.add_page(page([feat(1, (0, 0), (1, 1)), feat(2, (1, 1), (2, 2), "Microwave Planned", "Planned")], 2))
        a = itu.publisher_attrs(b.build("2026-11-25T12:00:00+00:00"))
        self.assertEqual(a["zones"], {"fibre_operational": "fibre_operational", "microwave_planned": "microwave_planned"})
        self.assertEqual(set(a["styles"]), set(a["zones"]))       # drawn events only
        self.assertEqual(a["layer_default"], "off")
        self.assertEqual(a["shape_order"], -12)
        self.assertEqual((a["links_total"], a["last_success"]), (2, "2026-11-25T12:00:00+00:00"))
        self.assertNotIn("polygons", a)                           # not clickable, nothing live
        self.assertNotIn("info", json.dumps(a))

    def test_set_m(self):
        """SSOT 7.4, set M (2026-11-25)."""
        s = itu.STYLES
        self.assertEqual(s["fibre_operational"], {"color": "#861360", "priority": 9})
        self.assertEqual(s["microwave_operational"], {"color": "#FFD633", "priority": 9, "casing": "#000000"})
        for k in ("fibre_planned", "fibre_construction", "microwave_planned", "microwave_construction"):
            self.assertEqual((s[k]["color"], s[k]["priority"]), ("#D9822B", 10), k)
        self.assertEqual((s["fibre_unknown"]["color"], s["fibre_unknown"]["priority"]), ("#808080", 11))
        for k, v in s.items():
            self.assertEqual("casing" in v, k.startswith("microwave"), k)
            self.assertRegex(v["color"], r"^#[0-9A-F]{6}$")

    def test_attribution_is_one_line(self):
        """D4d: the box shows the part before the first full stop followed by white space or the end: all of it."""
        a = itu.ATTRIBUTION
        self.assertEqual(re.split(r"\.(\s|$)", a, maxsplit=1)[0], a)
        self.assertEqual(a, "Terrestrial links: ITU Broadband Maps (BBmaps), bbmaps.itu.int, © ITU, schematic "
                            "links from node to node, placed on the map by Live Track Internet")

    def test_request(self):
        p = itu.wfs_params(15000)
        self.assertEqual((p["count"], p["startIndex"], p["sortBy"], p["typeNames"], p["outputFormat"]),
                         (5000, 15000, "uid", "itu-geocatalogue:trx_geocatalogue", "application/json"))


class TestWhen(unittest.TestCase):
    NOW = 1795600000.0   # 2026-11-25

    def test_slot_is_fixed_per_install(self):
        off = itu.slot_offset_s("01KAB")
        self.assertEqual(off, itu.slot_offset_s("01KAB"))
        self.assertTrue(0 <= off < itu.WEEK_S)
        t1 = itu.next_slot("01KAB", self.NOW)
        t2 = itu.next_slot("01KAB", t1)
        self.assertTrue(self.NOW < t1 <= self.NOW + itu.WEEK_S)
        self.assertEqual(t2 - t1, itu.WEEK_S)
        self.assertEqual((t1 - itu.SLOT_ANCHOR) % itu.WEEK_S, off)

    def test_spread_over_the_week(self):
        days = [0] * 7
        for i in range(7000):
            days[itu.slot_offset_s(f"entry{i}") // itu.DAY_S] += 1
        self.assertTrue(all(850 < d < 1150 for d in days), days)

    def test_first_and_missed(self):
        self.assertEqual(itu.next_due("x", None, self.NOW), self.NOW + itu.FIRST_DELAY_S)
        self.assertEqual(itu.next_due("x", self.NOW - 30 * itu.DAY_S, self.NOW), self.NOW + itu.FIRST_DELAY_S)

    def test_after_a_good_fetch(self):
        due = itu.next_due("x", self.NOW, self.NOW)
        self.assertTrue(self.NOW + itu.MIN_GAP_S <= due <= self.NOW + itu.MIN_GAP_S + itu.WEEK_S)
        # a first fetch minutes before the slot does not fetch again minutes later
        slot = itu.next_slot("x", self.NOW)
        due = itu.next_due("x", slot - 60, slot - 60)
        self.assertEqual(due, slot + itu.WEEK_S)

    def test_retry(self):
        self.assertEqual(itu.retry_s("no_answer", 1), itu.DAY_S)
        self.assertEqual(itu.retry_s("http_503", 4), itu.DAY_S)
        self.assertEqual(itu.retry_s("shrunk", 1), itu.DAY_S)
        self.assertEqual([itu.retry_s("rate_limited", a) for a in range(1, 8)],
                         [3600, 7200, 14400, 28800, 57600, 86400, 86400])
        self.assertEqual(itu.retry_s("rate_limited", 1, "120"), 120)
        self.assertEqual(itu.retry_s("rate_limited", 1, "0"), 60)
        self.assertEqual(itu.retry_s("rate_limited", 1, "999999"), itu.DAY_S)
        self.assertEqual(itu.retry_s("rate_limited", 2, "soon"), 7200)

    def test_retry_after_date(self):
        # 12:10:00 GMT is 1795608600; ten minutes before it
        self.assertAlmostEqual(itu._retry_after_s("Wed, 25 Nov 2026 12:10:00 GMT", now=1795608000.0), 600, delta=1)


if __name__ == "__main__":
    unittest.main()
