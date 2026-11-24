"""One geo_location entity per open outage per place (SAW SSOT 5.3; contract D20's event markers).

! NO unique_id, by design (06_MAP_CONTRACT.md D1): records come and go, and anything WITH a unique_id stays in the
entity registry for good. So no device_info either (05_SHARED_LESSONS.md A9). The entity id comes from
`suggested_object_id`: `outage_<Radar id>`, or `outage_<Radar id>_<GeoNames id>` when a record names several regions.
A record that ends, or leaves Radar's answer, is removed.
"""

from __future__ import annotations

from typing import Any

from homeassistant.components.geo_location import GeolocationEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfLength
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util.location import distance as ha_distance

from .const import DOMAIN
from .coordinator import OutageCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator: OutageCoordinator = hass.data[DOMAIN][entry.entry_id]
    manager = _Outages(hass, coordinator, async_add_entities)
    entry.async_on_unload(coordinator.async_add_listener(manager.update))
    entry.async_on_unload(manager.remove_all)
    manager.update()


class _Outages:
    def __init__(self, hass: HomeAssistant, coordinator: OutageCoordinator, add: AddEntitiesCallback) -> None:
        self.hass = hass
        self.coordinator = coordinator
        self.add = add
        self.entities: dict[str, OutageEvent] = {}

    @callback
    def update(self) -> None:
        records = {r["key"]: r for r in (self.coordinator.data or {}).get("markers", [])}
        for key in [k for k in self.entities if k not in records]:
            entity = self.entities.pop(key)
            if entity.hass is not None:
                self.hass.async_create_task(entity.async_remove(force_remove=True))
        new = []
        for key, rec in records.items():
            if key in self.entities:
                self.entities[key].set_record(rec)
            else:
                entity = OutageEvent(rec)
                self.entities[key] = entity
                new.append(entity)
        if new:
            self.add(new)

    @callback
    def remove_all(self) -> None:
        self.entities.clear()


class OutageEvent(GeolocationEvent):
    _attr_should_poll = False
    _attr_source = DOMAIN
    _attr_unit_of_measurement = UnitOfLength.KILOMETERS
    # ! No `icon`: the card draws an icon in preference to the picture and the label.
    _unrecorded_attributes = frozenset({"marker_info", "marker_links", "description"})

    def __init__(self, rec: dict[str, Any]) -> None:
        self._key = rec["key"]
        self._rec = rec

    @callback
    def set_record(self, rec: dict[str, Any]) -> None:
        self._rec = rec
        if self.hass is not None:
            self.async_write_ha_state()

    @property
    def suggested_object_id(self) -> str:
        return f"outage_{self._key}"

    @property
    def name(self) -> str:
        return self._rec["name"]

    @property
    def latitude(self) -> float | None:
        return self._rec["lat"]

    @property
    def longitude(self) -> float | None:
        return self._rec["lon"]

    @property
    def distance(self) -> float | None:
        """The entity STATE, km from home (D1). Never also an attribute."""
        if self.hass is None:
            return None
        return round(ha_distance(self.hass.config.latitude, self.hass.config.longitude,
                                 self._rec["lat"], self._rec["lon"]) / 1000, 1)

    @property
    def entity_picture(self) -> str | None:
        return self._rec["attrs"].get("entity_picture")

    @property
    def attribution(self) -> str | None:
        return self._rec["attrs"].get("attribution")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {k: v for k, v in self._rec["attrs"].items() if k not in ("attribution", "entity_picture")}
