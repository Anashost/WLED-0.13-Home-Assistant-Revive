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
        
        for index, segment in enumerate(segs):
            if index not in known_segments:
                speed_name = "Speed" if index == 0 else f"Segment {index} Speed"
                int_name = "Intensity" if index == 0 else f"Segment {index} Intensity"
                
                new_entities.append(WLEDNumber(data, config_entry.entry_id, index, "sx", speed_name, "mdi:speedometer"))
                new_entities.append(WLEDNumber(data, config_entry.entry_id, index, "ix", int_name, "mdi:creation"))
                known_segments.add(index)
                
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

    @property
    def available(self) -> bool:
        if not self.coordinator.last_update_success: return False
        return self._segment_id < len(self.coordinator.data.get("state", {}).get("seg", []))

    @property
    def native_value(self):
        try: return self.coordinator.data["state"]["seg"][self._segment_id][self._key]
        except (KeyError, IndexError): return 128

    async def async_set_native_value(self, value: float) -> None:
        val = int(value)
        try: self.coordinator.data["state"]["seg"][self._segment_id][self._key] = val
        except KeyError: pass
        self.coordinator.async_set_updated_data(self.coordinator.data)

        payload = {"seg": [{"id": self._segment_id, self._key: val}]}
        try:
            async with async_timeout.timeout(5):
                await self._data["session"].post(f"http://{self._data['ip_address']}/json/state", json=payload)
        except Exception as e:
            _LOGGER.error("Failed to update WLED parameter: %s", e)