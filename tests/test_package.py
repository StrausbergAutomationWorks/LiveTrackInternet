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

    def test_count_sensor_entity_id(self):
        """SSOT 5.6: sensor.live_track_internet_outages, not built from the device name (measured 2026-11-24)."""
        src = (COMP / "sensor.py").read_text(encoding="utf-8")
        found = re.findall(r'^\s*self\.entity_id = f"sensor\.\{DOMAIN\}_outages"$', src, re.M)
        self.assertEqual(len(found), 1)
        self.assertEqual(f"sensor.{load('const').DOMAIN}_outages", "sensor.live_track_internet_outages")


if __name__ == "__main__":
    unittest.main()
