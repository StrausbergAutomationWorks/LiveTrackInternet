"""The count sensor (SAW SSOT 5.6): open outages drawn as markers. One per entry, so it KEEPS a unique_id and the
entry's device (06_MAP_CONTRACT.md D1)."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN, VERSION
from .coordinator import OutageCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    async_add_entities([OutageCount(hass.data[DOMAIN][entry.entry_id], entry)])


class OutageCount(CoordinatorEntity[OutageCoordinator], SensorEntity):
    _attr_has_entity_name = True
    _attr_translation_key = "outages"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_attribution = ATTRIBUTION
    _attr_icon = "mdi:web-off"
    _unrecorded_attributes = frozenset({"not_on_map", "last_success"})

    def __init__(self, coordinator: OutageCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_outages"
        self._attr_device_info = DeviceInfo(identifiers={(DOMAIN, entry.entry_id)}, name="Cloudflare Radar",
                                            manufacturer="Cloudflare", model="Radar outage records",
                                            sw_version=VERSION, entry_type=DeviceEntryType.SERVICE,
                                            configuration_url="https://radar.cloudflare.com")

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
