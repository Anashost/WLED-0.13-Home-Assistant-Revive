import logging
import async_timeout
from homeassistant.core import callback
from homeassistant.components.number import NumberEntity
from homeassistant.const import EntityCategory
from .const import DOMAIN
from .entity import WledReviveEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = data["coordinator"]
    known_segments = set()
    
    @callback
    def async_update_entities():
        new_entities = []
        state = coordinator.data.get("state", {})
        segs = state.get("seg", [])
        
        for segment in segs:
            seg_id = segment.get("id")
            if seg_id is not None and seg_id not in known_segments:
                speed_name = "Speed" if seg_id == 0 else f"Segment {seg_id} Speed"
                int_name = "Intensity" if seg_id == 0 else f"Segment {seg_id} Intensity"
                
                new_entities.append(WLEDNumber(data, config_entry.entry_id, seg_id, "sx", speed_name, "mdi:speedometer"))
                new_entities.append(WLEDNumber(data, config_entry.entry_id, seg_id, "ix", int_name, "mdi:creation"))
                known_segments.add(seg_id)
                
        if new_entities:
            async_add_entities(new_entities)

    config_entry.async_on_unload(coordinator.async_add_listener(async_update_entities))
    async_update_entities()


class WLEDNumber(WledReviveEntity, NumberEntity):
    def __init__(self, data, entry_id, segment_id, key, name, icon):
        super().__init__(data)
        self._segment_id = segment_id
        self._key = key
        self._attr_has_entity_name = True
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_seg_{segment_id}_{key}"
        self._attr_icon = icon
        self._attr_native_min_value = 0
        self._attr_native_max_value = 255
        self._attr_native_step = 1
        self._attr_entity_category = EntityCategory.CONFIG

    def _get_segment(self):
        for seg in self.coordinator.data.get("state", {}).get("seg", []):
            if seg.get("id") == self._segment_id:
                return seg
        return None

    @property
    def available(self) -> bool:
        if not self.coordinator.last_update_success: return False
        
        if self._segment_id == 0:
            segs = self.coordinator.data.get("state", {}).get("seg", [])
            if len(segs) <= 1:
                return False
                
        return self._get_segment() is not None

    @property
    def native_value(self):
        seg = self._get_segment()
        return seg.get(self._key, 128) if seg else 128

    async def async_set_native_value(self, value: float) -> None:
        val = int(value)
        seg = self._get_segment()
        if seg: seg[self._key] = val
        self.coordinator.async_set_updated_data(self.coordinator.data)

        payload = {"seg": [{"id": self._segment_id, self._key: val}]}
        try:
            async with async_timeout.timeout(5):
                await self._data["session"].post(f"http://{self._data['ip_address']}/json/state", json=payload)
        except Exception as e:
            _LOGGER.error("Failed to update WLED parameter: %s", e)
