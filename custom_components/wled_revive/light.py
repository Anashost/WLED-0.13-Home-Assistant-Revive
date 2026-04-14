import logging
import async_timeout
import asyncio
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
            
        for segment in segs:
            seg_id = segment.get("id")
            if seg_id is not None and seg_id not in known_segments:
                new_entities.append(WLEDSegmentLight(data, config_entry.entry_id, seg_id))
                known_segments.add(seg_id)
                
        if new_entities:
            async_add_entities(new_entities)

    config_entry.async_on_unload(coordinator.async_add_listener(async_update_entities))
    async_update_entities()


class WLEDMasterLight(WledReviveEntity, LightEntity):
    def __init__(self, data, entry_id):
        super().__init__(data)
        self._attr_has_entity_name = True
        self._attr_name = "Main" 
        self._attr_unique_id = f"{entry_id}_main"
        self._attr_icon = "mdi:led-strip-variant"
        self._attr_supported_color_modes = {ColorMode.BRIGHTNESS}
        self._attr_color_mode = ColorMode.BRIGHTNESS

    @property
    def available(self) -> bool:
        if not self.coordinator.last_update_success: return False
        segs = self.coordinator.data.get("state", {}).get("seg", [])
        return len(segs) > 1

    @property
    def is_on(self):
        return self.coordinator.data["state"].get("on", False)

    @property
    def brightness(self):
        return self.coordinator.data["state"].get("bri", 255)

    async def _send_command(self, payload):
        # TRAFFIC LIGHT LOCK
        async with self._data["lock"]:
            try:
                async with async_timeout.timeout(5):
                    await self._data["session"].post(f"http://{self._data['ip_address']}/json/state", json=payload)
                self.coordinator.async_set_updated_data(self.coordinator.data)
            except Exception as e:
                _LOGGER.error("Failed to send command to WLED master: %s", e)
            finally:
                await asyncio.sleep(0.1) # Protect ESP from spam

    async def async_turn_on(self, **kwargs):
        payload = {"on": True}
        try: self.coordinator.data["state"]["on"] = True
        except KeyError: pass
        
        if ATTR_BRIGHTNESS in kwargs:
            payload["bri"] = kwargs[ATTR_BRIGHTNESS]
            try: self.coordinator.data["state"]["bri"] = kwargs[ATTR_BRIGHTNESS]
            except KeyError: pass
                
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
        self._attr_name = None if segment_id == 0 else f"Segment {segment_id}"
        self._attr_unique_id = f"{entry_id}_seg_{segment_id}"
        self._attr_icon = "mdi:led-strip"
        self._attr_supported_color_modes = {ColorMode.RGB}
        self._attr_color_mode = ColorMode.RGB
        self._attr_supported_features = LightEntityFeature.EFFECT
        self._attr_effect_list = list(self._data["effects_map"].keys())

    def _get_segment(self):
        for seg in self.coordinator.data.get("state", {}).get("seg", []):
            if seg.get("id") == self._segment_id:
                return seg
        return None

    @property
    def available(self) -> bool:
        if not self.coordinator.last_update_success: return False
        return self._get_segment() is not None

    @property
    def is_on(self):
        seg = self._get_segment()
        return seg.get("on", False) if seg else False

    @property
    def brightness(self):
        seg = self._get_segment()
        return seg.get("bri", 255) if seg else 255

    @property
    def rgb_color(self):
        seg = self._get_segment()
        if seg and "col" in seg and len(seg["col"]) > 0:
            return tuple(seg["col"][0][:3])
        return (255, 255, 255)

    @property
    def effect(self):
        seg = self._get_segment()
        if seg and "fx" in seg:
            return self._data["id_to_effect"].get(seg["fx"], "Solid")
        return "Solid"

    async def _send_command(self, payload):
        # TRAFFIC LIGHT LOCK
        async with self._data["lock"]:
            try:
                async with async_timeout.timeout(5):
                    await self._data["session"].post(f"http://{self._data['ip_address']}/json/state", json=payload)
                self.coordinator.async_set_updated_data(self.coordinator.data)
            except Exception as e:
                _LOGGER.error("Failed to send command to WLED segment: %s", e)
            finally:
                await asyncio.sleep(0.1)

    async def async_turn_on(self, **kwargs):
        seg_update = {"id": self._segment_id, "on": True}
        seg = self._get_segment()
        
        if seg:
            seg["on"] = True
            if ATTR_BRIGHTNESS in kwargs:
                seg["bri"] = kwargs[ATTR_BRIGHTNESS]
                seg_update["bri"] = kwargs[ATTR_BRIGHTNESS]
                    
            if ATTR_RGB_COLOR in kwargs:
                rgb = kwargs[ATTR_RGB_COLOR]
                seg_update["col"] = [[rgb[0], rgb[1], rgb[2]]]
                try: seg["col"][0] = [rgb[0], rgb[1], rgb[2]]
                except KeyError: pass
                    
            if ATTR_EFFECT in kwargs:
                effect_id = self._data["effects_map"].get(kwargs[ATTR_EFFECT])
                if effect_id is not None:
                    seg_update["fx"] = effect_id
                    seg["fx"] = effect_id
        else:
            if ATTR_BRIGHTNESS in kwargs: seg_update["bri"] = kwargs[ATTR_BRIGHTNESS]
            if ATTR_EFFECT in kwargs:
                eff_id = self._data["effects_map"].get(kwargs[ATTR_EFFECT])
                if eff_id is not None: seg_update["fx"] = eff_id

        await self._send_command({"seg": [seg_update]})

    async def async_turn_off(self, **kwargs):
        seg = self._get_segment()
        if seg: seg["on"] = False
        await self._send_command({"seg": [{"id": self._segment_id, "on": False}]})
