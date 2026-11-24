"""Import the component's HA-free modules without Home Assistant.

The package __init__ imports Home Assistant, so it must never run here. This registers the component folder as a bare
package named `lti` whose __init__ is skipped; `lti.radar` then imports normally.

Run from the repo root:  python -m unittest discover -s tests -v
"""

import importlib
import importlib.machinery
import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
COMP = ROOT / "custom_components" / "live_track_internet"

if "lti" not in sys.modules:
    spec = importlib.machinery.ModuleSpec("lti", None, is_package=True)
    pkg = importlib.util.module_from_spec(spec)
    pkg.__path__ = [str(COMP)]
    sys.modules["lti"] = pkg


def load(name: str):
    return importlib.import_module(f"lti.{name}")
