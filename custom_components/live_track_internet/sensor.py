"""The sensors: the outage count (SAW SSOT 5.6) and the three cable publishers (SSOT section 2; contract D12, D19).

Each is one per entry, so each KEEPS a unique_id and a device (06_MAP_CONTRACT.md D1). The entity ids are set before
the entities are added, which Home Assistant takes as the suggested id at FIRST registration only (Home Assistant
2026.11.2 entity_platform.py, read on the box 2026-11-24); after that the registry owns the id.

! PERMANENT from first install: the unique_ids below, and so the entity ids.
"""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import cables
from .const import ATTRIBUTION, DOMAIN, VERSION
from .coordinator import OutageCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    data = hass.data[DOMAIN]
    coordinator: OutageCoordinator | None = data[entry.entry_id]
    cd: cables.CableData = data["cables"]
    entities: list[SensorEntity] = [AllCables(cd, data["shapes_url"], entry), LandingPoints(cd, entry)]
    if coordinator is not None:
        entities += [OutageCount(coordinator, entry), CablesInTrouble(coordinator, cd, entry)]
    async_add_entities(entities)


def _radar_device(entry: ConfigEntry) -> DeviceInfo:
    return DeviceInfo(identifiers={(DOMAIN, entry.entry_id)}, name="Cloudflare Radar", manufacturer="Cloudflare",
                      model="Radar outage records", sw_version=VERSION, entry_type=DeviceEntryType.SERVICE,
                      configuration_url="https://radar.cloudflare.com")


def _cables_device(entry: ConfigEntry) -> DeviceInfo:
    return DeviceInfo(identifiers={(DOMAIN, f"{entry.entry_id}_cables")}, name="Submarine cables",
                      manufacturer="Tristan Hotham, from TeleGeography data", model="The internet's seabed (2026)",
                      sw_version=VERSION, entry_type=DeviceEntryType.SERVICE,
                      configuration_url="https://doi.org/10.5281/zenodo.23856607")


class OutageCount(CoordinatorEntity[OutageCoordinator], SensorEntity):
    """Open outages drawn as markers (SSOT 5.6)."""

    _attr_has_entity_name = True
    _attr_translation_key = "outages"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_attribution = ATTRIBUTION
    _attr_icon = "mdi:web-off"
    _unrecorded_attributes = frozenset({"not_on_map", "last_success"})

    def __init__(self, coordinator: OutageCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_outages"
        # SSOT 5.6 names this sensor.live_track_internet_outages; without this line Home Assistant built
        # sensor.cloudflare_radar_internet_outages from the device name (measured on the box 2026-11-24).
        self.entity_id = f"sensor.{DOMAIN}_outages"
        self._attr_device_info = _radar_device(entry)

    @property
    def available(self) -> bool:
        return super().available and not (self.coordinator.data or {}).get("expired", True)

    @property
    def native_value(self) -> int | None:
        data = self.coordinator.data or {}
        return len(data.get("markers") or [])

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        data = self.coordinator.data or {}
        out: dict[str, Any] = {"open_records": data.get("open_records", 0),
                               "not_on_map": data.get("not_on_map") or []}
        if data.get("last_success"):
            out["last_success"] = data["last_success"]
        return out


class _CableSensor(SensorEntity):
    """A static cable publisher: its attributes change only with a release."""

    _attr_has_entity_name = True
    _attr_should_poll = False
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_attribution = cables.ATTRIBUTION
    _KEY = ""

    def __init__(self, entry: ConfigEntry) -> None:
        self._attr_unique_id = f"{DOMAIN}_{self._KEY}"
        self._attr_translation_key = self._KEY
        self.entity_id = f"sensor.{DOMAIN}_{self._KEY}"
        self._attr_device_info = _cables_device(entry)


class AllCables(_CableSensor):
    """Every cable as a line from the shipped shape file (D12), off until ticked."""

    _KEY = "all_cables"
    _attr_icon = "mdi:transit-connection-variant"
    # D12: zones and styles unrecorded (A7); the rest is static and adds nothing to the history.
    _unrecorded_attributes = frozenset({"shapes_url", "zones", "styles", "shape_order", "layer_default"})

    def __init__(self, cd: cables.CableData, shapes_url: str, entry: ConfigEntry) -> None:
        super().__init__(entry)
        self._attr_native_value = len(cd.catalog)
        self._attrs = cables.all_cables_attrs(cd, shapes_url)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return self._attrs


class LandingPoints(_CableSensor):
    """Every landing point as a dot from the shipped point file (D19), off until ticked."""

    _KEY = "landing_points"
    _attr_icon = "mdi:map-marker-radius-outline"
    _unrecorded_attributes = frozenset({"points_url", "point_styles", "point_order", "layer_default"})

    def __init__(self, cd: cables.CableData, entry: ConfigEntry) -> None:
        super().__init__(entry)
        self._attr_native_value = cd.point_count
        self._attrs = cables.landing_points_attrs(cd)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return self._attrs


class CablesInTrouble(CoordinatorEntity[OutageCoordinator], SensorEntity):
    """Cables named in an open outage record's description (SSOT section 2): bold red lines, clickable, on."""

    _attr_has_entity_name = True
    _attr_translation_key = "cables_in_trouble"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_attribution = cables.ATTRIBUTION
    _attr_icon = "mdi:transit-connection-variant"
    _unrecorded_attributes = frozenset({"zones", "polygons", "styles", "shape_order"})

    def __init__(self, coordinator: OutageCoordinator, cd: cables.CableData, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._cd = cd
        self._attr_unique_id = f"{DOMAIN}_cables_in_trouble"
        self.entity_id = f"sensor.{DOMAIN}_cables_in_trouble"
        self._attr_device_info = _cables_device(entry)

    @property
    def available(self) -> bool:
        # The same 2-hour rule as the outages: an old "in trouble" is a wrong map, and an unavailable publisher
        # has its lines cleared by the card (D12 rule 9).
        return super().available and not (self.coordinator.data or {}).get("expired", True)

    def _polygons(self) -> list[dict[str, Any]]:
        return cables.trouble_polygons((self.coordinator.data or {}).get("markers") or [], self._cd)

    @property
    def native_value(self) -> int | None:
        return len(self._polygons())

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return cables.trouble_attrs(self._polygons())
