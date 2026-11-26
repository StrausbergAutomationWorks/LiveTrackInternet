"""What ships: manifest, translations, the cause pictures, no BOM anywhere."""

import json
import re
import unittest

from _load import COMP, ROOT, load


class TestPackage(unittest.TestCase):
    def test_manifest(self):
        m = json.loads((COMP / "manifest.json").read_text(encoding="utf-8"))
        const = (COMP / "const.py").read_text(encoding="utf-8")
        self.assertEqual(m["domain"], "live_track_internet")
        self.assertIn('DOMAIN = "live_track_internet"', const)
        self.assertIn(f'VERSION = "{m["version"]}"', const)
        self.assertEqual(m["iot_class"], "cloud_polling")
        self.assertTrue(m["single_config_entry"])
        self.assertIn("http", m["dependencies"])

    def test_no_bom_anywhere(self):
        for p in ROOT.rglob("*"):
            if p.is_file() and ".git" not in p.parts and p.suffix in (".py", ".json", ".md", ".txt", ".svg"):
                self.assertFalse(p.read_bytes().startswith(b"\xef\xbb\xbf"), p)

    def test_translations(self):
        strings = (COMP / "strings.json").read_bytes()
        self.assertEqual(strings, (COMP / "translations" / "en.json").read_bytes())
        base = json.loads(strings)

        def keys(d, pre=""):
            out = set()
            for k, v in d.items():
                out |= keys(v, f"{pre}{k}.") if isinstance(v, dict) else {pre + k}
            return out

        want = keys(base)
        for f in (COMP / "translations").glob("*.json"):
            doc = json.loads(f.read_text(encoding="utf-8"))
            self.assertEqual(keys(doc), want, f.name)
            for k in want:
                v = doc
                for part in k.split("."):
                    v = v[part]
                b = base
                for part in k.split("."):
                    b = b[part]
                self.assertEqual(sorted(re.findall(r"\{\w+\}", v)), sorted(re.findall(r"\{\w+\}", b)), (f.name, k))
                self.assertNotIn("http", v, (f.name, k, "hassfest refuses a URL in strings"))

    def test_one_picture_per_class(self):
        const = load("const")
        icons = {p.stem for p in (COMP / "icons").glob("*.svg")}
        self.assertEqual(icons, {f"outage_{k}" for k in const.CLASSES})
        for p in (COMP / "icons").glob("*.svg"):
            self.assertTrue(p.read_text(encoding="utf-8").startswith("<svg"), p)

    def test_every_class_and_cause(self):
        const = load("const")
        self.assertEqual(set(const.CAUSE_CLASS.values()) - set(const.CLASSES), set())
        self.assertEqual(set(const.CAUSE_CLASS), set(const.CAUSE_WORDS))
        for c in const.CLASSES.values():
            self.assertRegex(c["color"], r"^#[0-9A-F]{6}$")
        self.assertEqual(sorted(c["order"] for c in const.CLASSES.values()), list(range(1, len(const.CLASSES) + 1)))

    def test_attribution_cut(self):
        """D4d: the box shows the part before the first full stop that is followed by white space or the end."""
        a = load("const").ATTRIBUTION
        head = re.split(r"\.(\s|$)", a, maxsplit=1)[0]
        self.assertEqual(head, "Outages: Cloudflare Radar, radar.cloudflare.com, CC BY-NC 4.0, placed on the map by "
                               "Live Track Internet")
        self.assertIn("creativecommons.org/licenses/by-nc/4.0", a)

    def test_terrestrial_links_wiring(self):
        """SSOT 7.4 and 7.6 item 6: the publisher's id set at first registration, its device, the option on by
        default, the view without sign-in, and every dialog naming the box."""
        src = (COMP / "sensor.py").read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r'^\s*self\.entity_id = f"sensor\.\{DOMAIN\}_terrestrial_links"$', src, re.M)), 1)
        self.assertIn('name="ITU Broadband Maps"', src)
        const = load("const")
        self.assertIs(const.DEFAULT_ITU_LINKS, True)
        self.assertEqual(const.CONF_ITU_LINKS, "itu_links")
        views = (COMP / "views.py").read_text(encoding="utf-8")
        self.assertRegex(views, r"class LinksView\(HomeAssistantView\):[\s\S]*?requires_auth = False")
        init = (COMP / "__init__.py").read_text(encoding="utf-8")
        self.assertIn('LINKS_UNIQUE_ID = f"{DOMAIN}_terrestrial_links"', init)
        self.assertIn('self._attr_unique_id = f"{DOMAIN}_terrestrial_links"', src)
        for f in [COMP / "strings.json", *(COMP / "translations").glob("*.json")]:
            d = json.loads(f.read_text(encoding="utf-8"))
            for step in ("user", "reconfigure"):
                self.assertIn("itu_links", d["config"]["step"][step]["data"], (f.name, step))
                self.assertIn("itu_links", d["config"]["step"][step]["data_description"], (f.name, step))
            self.assertIn("terrestrial_links", d["entity"]["sensor"], f.name)
        self.assertEqual(load("itu").CACHE_FILE, "saw_itu_bbmaps_links.json.gz")   # SAW-neutral (project rule)

    def test_count_sensor_entity_id(self):
        """SSOT 5.6: sensor.live_track_internet_outages, not built from the device name (measured 2026-11-24)."""
        src = (COMP / "sensor.py").read_text(encoding="utf-8")
        found = re.findall(r'^\s*self\.entity_id = f"sensor\.\{DOMAIN\}_outages"$', src, re.M)
        self.assertEqual(len(found), 1)
        self.assertEqual(f"sensor.{load('const').DOMAIN}_outages", "sensor.live_track_internet_outages")


if __name__ == "__main__":
    unittest.main()
