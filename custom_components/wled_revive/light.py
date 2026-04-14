import logging
import async_timeout
from homeassistant.core import callback
from homeassistant.components.light import LightEntity, ColorMode, LightEntityFeature, ATTR_BRIGHTNESS, ATTR_RGB_COLOR, ATTR_EFFECT
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
        
        if "master" not in known_segments:
            new_entities.append(WLEDMasterLight(data, config_entry.entry_id))
            known_segments.add("master")
            
        for index, segment in enumerate(segs):
            if index not in known_segments:
                new_entities.append(WLEDSegmentLight(data, config_entry.entry_id, index))
                known_segments.add(index)
                
        if new_entities:
            async_add_entities(new_entities)

    config_entry.async_on_unload(coordinator.async_add_listener(async_update_entities))
    async_update_entities()


class WLEDMasterLight(WledReviveEntity, LightEntity):
    def __init__(self, data, entry_id):
        super().__init__(data)
        self._attr_has_entity_name = True
        self._attr_name = None 
        self._attr_unique_id = f"{entry_id}_master"
        self._attr_icon = "mdi:led-strip-variant"
        self._attr_supported_color_modes = {ColorMode.RGB}
        self._attr_color_mode = ColorMode.RGB
        self._attr_supported_features = LightEntityFeature.EFFECT
        self._attr_effect_list = list(self._data["effects_map"].keys())

    @property
    def is_on(self):
        return self.coordinator.data["state"].get("on", False)

    @property
    def brightness(self):
        return self.coordinator.data["state"].get("bri", 255)

    @property
    def rgb_color(self):
        try: return tuple(self.coordinator.data["state"]["seg"][0]["col"][0][:3])
        except (IndexError, KeyError): return (255, 255, 255)

    @property
    def effect(self):
        try:
            fx_id = self.coordinator.data["state"]["seg"][0]["fx"]
            return self._data["id_to_effect"].get(fx_id, "Solid")
        except (IndexError, KeyError): return "Solid"

    async def _send_command(self, payload):
        try:
            async with async_timeout.timeout(5):
                await self._data["session"].post(f"http://{self._data['ip_address']}/json/state", json=payload)
            self.coordinator.async_set_updated_data(self.coordinator.data)
        except Exception as e:
            _LOGGER.error("Failed to send command to WLED master: %s", e)

    async def async_turn_on(self, **kwargs):
        payload = {"on": True}
        seg_payload = {"id": 0}
        update_seg = False
        
        try: self.coordinator.data["state"]["on"] = True
        except KeyError: pass
        
        if ATTR_BRIGHTNESS in kwargs:
            payload["bri"] = kwargs[ATTR_BRIGHTNESS]
            try: self.coordinator.data["state"]["bri"] = kwargs[ATTR_BRIGHTNESS]
            except KeyError: pass
                
        if ATTR_RGB_COLOR in kwargs:
            rgb = kwargs[ATTR_RGB_COLOR]
            seg_payload["col"] = [[rgb[0], rgb[1], rgb[2]]]
            update_seg = True
            try: self.coordinator.data["state"]["seg"][0]["col"][0] = [rgb[0], rgb[1], rgb[2]]
            except (KeyError, IndexError): pass
                
        if ATTR_EFFECT in kwargs:
            effect_id = self._data["effects_map"].get(kwargs[ATTR_EFFECT])
            if effect_id is not None:
                seg_payload["fx"] = effect_id
                update_seg = True
                try: self.coordinator.data["state"]["seg"][0]["fx"] = effect_id
                except (KeyError, IndexError): pass

        if update_seg: payload["seg"] = [seg_payload]
        await self._send_command(payload)

    async def async_turn_off(self, **kwargs):
        try: self.coordinator.data["state"]["on"] = False
        except KeyError: pass
        await self._send_command({"on": False})


class WLEDSegmentLight(WledReviveEntity, LightEntity):
    def __init__(self, data, entry_id, segment_id):
        super().__init__(data)
        self._segment_id = segment_id
        self._attr_has_entity_name = True
        self._attr_name = "Main" if segment_id == 0 else f"Segment {segment_id}"
        self._attr_unique_id = f"{entry_id}_seg_{segment_id}"
        self._attr_icon = "mdi:led-strip"
        self._attr_supported_color_modes = {ColorMode.RGB}
        self._attr_color_mode = ColorMode.RGB
        self._attr_supported_features = LightEntityFeature.EFFECT
        self._attr_effect_list = list(self._data["effects_map"].keys())

    @property
    def available(self) -> bool:
        if not self.coordinator.last_update_success: return False
        return self._segment_id < len(self.coordinator.data.get("state", {}).get("seg", []))

    @property
    def is_on(self):
        try: return self.coordinator.data["state"]["seg"][self._segment_id]["on"]
        except (KeyError, IndexError): return False

    @property
    def brightness(self):
        try: return self.coordinator.data["state"]["seg"][self._segment_id]["bri"]
        except (KeyError, IndexError): return 255

    @property
    def rgb_color(self):
        try: return tuple(self.coordinator.data["state"]["seg"][self._segment_id]["col"][0][:3])
        except (IndexError, KeyError): return (255, 255, 255)

    @property
    def effect(self):
        try:
            fx_id = self.coordinator.data["state"]["seg"][self._segment_id]["fx"]
            return self._data["id_to_effect"].get(fx_id, "Solid")
        except (IndexError, KeyError): return "Solid"

    async def _send_command(self, payload):
        try:
            async with async_timeout.timeout(5):
                await self._data["session"].post(f"http://{self._data['ip_address']}/json/state", json=payload)
            self.coordinator.async_set_updated_data(self.coordinator.data)
        except Exception as e:
            _LOGGER.error("Failed to send command to WLED segment: %s", e)

    async def async_turn_on(self, **kwargs):
        seg_update = {"id": self._segment_id, "on": True}
        try: self.coordinator.data["state"]["seg"][self._segment_id]["on"] = True
        except KeyError: pass
        
        if ATTR_BRIGHTNESS in kwargs:
            seg_update["bri"] = kwargs[ATTR_BRIGHTNESS]
            try: self.coordinator.data["state"]["seg"][self._segment_id]["bri"] = kwargs[ATTR_BRIGHTNESS]
            except KeyError: pass
                
        if ATTR_RGB_COLOR in kwargs:
            rgb = kwargs[ATTR_RGB_COLOR]
            seg_update["col"] = [[rgb[0], rgb[1], rgb[2]]]
            try: self.coordinator.data["state"]["seg"][self._segment_id]["col"][0] = [rgb[0], rgb[1], rgb[2]]
            except KeyError: pass
                
        if ATTR_EFFECT in kwargs:
            effect_id = self._data["effects_map"].get(kwargs[ATTR_EFFECT])
            if effect_id is not None:
                seg_update["fx"] = effect_id
                try: self.coordinator.data["state"]["seg"][self._segment_id]["fx"] = effect_id
                except KeyError: pass

        await self._send_command({"seg": [seg_update]})

    async def async_turn_off(self, **kwargs):
        try: self.coordinator.data["state"]["seg"][self._segment_id]["on"] = False
        except KeyError: pass
        await self._send_command({"seg": [{"id": self._segment_id, "on": False}]})