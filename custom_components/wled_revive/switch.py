import logging
import async_timeout
from homeassistant.core import callback
from homeassistant.components.switch import SwitchEntity
from homeassistant.const import EntityCategory
from .const import DOMAIN
from .entity import WledReviveEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = data["coordinator"]
    known_segments = set()
    
    entities = [
        WLEDSyncSwitch(data, config_entry.entry_id, "send", "Sync Send", "mdi:upload-network"),
        WLEDSyncSwitch(data, config_entry.entry_id, "recv", "Sync Receive", "mdi:download-network"),
        WLEDNightlightSwitch(data, config_entry.entry_id)
    ]
    
    @callback
    def async_update_entities():
        new_entities = []
        state = coordinator.data.get("state", {})
        segs = state.get("seg", [])
        
        for index, segment in enumerate(segs):
            if index not in known_segments:
                rev_name = "Reverse" if index == 0 else f"Segment {index} Reverse"
                new_entities.append(WLEDSegmentReverseSwitch(data, config_entry.entry_id, index, rev_name))
                known_segments.add(index)
                
        if new_entities:
            async_add_entities(new_entities)

    config_entry.async_on_unload(coordinator.async_add_listener(async_update_entities))
    
    if entities:
        async_add_entities(entities)
    async_update_entities()


class WLEDSyncSwitch(WledReviveEntity, SwitchEntity):
    def __init__(self, data, entry_id, key, name, icon):
        super().__init__(data)
        self._key = key
        self._attr_has_entity_name = True
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_sync_{key}"
        self._attr_icon = icon
        self._attr_entity_category = EntityCategory.CONFIG

    @property
    def is_on(self):
        return self.coordinator.data.get("state", {}).get("udpn", {}).get(self._key, False)

    async def _send_command(self, is_on):
        try:
            self.coordinator.data["state"]["udpn"][self._key] = is_on
            self.coordinator.async_set_updated_data(self.coordinator.data)
        except KeyError: pass

        payload = {"udpn": {self._key: is_on}}
        try:
            async with async_timeout.timeout(5):
                await self._data["session"].post(f"http://{self._data['ip_address']}/json/state", json=payload)
        except Exception as e:
            _LOGGER.error("Failed to toggle WLED sync: %s", e)

    async def async_turn_on(self, **kwargs):
        await self._send_command(True)

    async def async_turn_off(self, **kwargs):
        await self._send_command(False)


class WLEDNightlightSwitch(WledReviveEntity, SwitchEntity):
    def __init__(self, data, entry_id):
        super().__init__(data)
        self._attr_has_entity_name = True
        self._attr_name = "Nightlight"
        self._attr_unique_id = f"{entry_id}_nightlight"
        self._attr_icon = "mdi:weather-night"
        self._attr_entity_category = EntityCategory.CONFIG

    @property
    def is_on(self):
        return self.coordinator.data.get("state", {}).get("nl", {}).get("on", False)

    async def _send_command(self, is_on):
        try:
            self.coordinator.data["state"]["nl"]["on"] = is_on
            self.coordinator.async_set_updated_data(self.coordinator.data)
        except KeyError: pass

        payload = {"nl": {"on": is_on}}
        try:
            async with async_timeout.timeout(5):
                await self._data["session"].post(f"http://{self._data['ip_address']}/json/state", json=payload)
        except Exception as e:
            _LOGGER.error("Failed to toggle WLED nightlight: %s", e)

    async def async_turn_on(self, **kwargs):
        await self._send_command(True)

    async def async_turn_off(self, **kwargs):
        await self._send_command(False)


class WLEDSegmentReverseSwitch(WledReviveEntity, SwitchEntity):
    def __init__(self, data, entry_id, segment_id, name):
        super().__init__(data)
        self._segment_id = segment_id
        self._attr_has_entity_name = True
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_rev_seg_{segment_id}"
        self._attr_icon = "mdi:swap-horizontal"
        self._attr_entity_category = EntityCategory.CONFIG

    @property
    def available(self) -> bool:
        if not self.coordinator.last_update_success: return False
        return self._segment_id < len(self.coordinator.data.get("state", {}).get("seg", []))

    @property
    def is_on(self):
        try: return self.coordinator.data["state"]["seg"][self._segment_id].get("rev", False)
        except (KeyError, IndexError): return False

    async def _send_command(self, is_on):
        try:
            self.coordinator.data["state"]["seg"][self._segment_id]["rev"] = is_on
            self.coordinator.async_set_updated_data(self.coordinator.data)
        except KeyError: pass

        payload = {"seg": [{"id": self._segment_id, "rev": is_on}]}
        try:
            async with async_timeout.timeout(5):
                await self._data["session"].post(f"http://{self._data['ip_address']}/json/state", json=payload)
        except Exception as e:
            _LOGGER.error("Failed to toggle WLED reverse: %s", e)

    async def async_turn_on(self, **kwargs):
        await self._send_command(True)

    async def async_turn_off(self, **kwargs):
        await self._send_command(False)