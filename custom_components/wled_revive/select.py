import logging
import async_timeout
import asyncio
from homeassistant.core import callback
from homeassistant.components.select import SelectEntity
from homeassistant.const import EntityCategory
from .const import DOMAIN
from .entity import WledReviveEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = data["coordinator"]
    known_segments = set()
    entities = []
    
    if data["presets_map"]:
        entities.append(WLEDPresetSelect(data, config_entry.entry_id))
        
    if data.get("playlists_map"):
        entities.append(WLEDPlaylistSelect(data, config_entry.entry_id))
        
    @callback
    def async_update_entities():
        new_entities = []
        state = coordinator.data.get("state", {})
        segs = state.get("seg", [])
        
        for segment in segs:
            seg_id = segment.get("id")
            if seg_id is not None and seg_id not in known_segments:
                pal_name = "Color Palette" if seg_id == 0 else f"Segment {seg_id} Color Palette"
                new_entities.append(WLEDPaletteSelect(data, config_entry.entry_id, seg_id, pal_name))
                known_segments.add(seg_id)
                
        if new_entities:
            async_add_entities(new_entities)

    config_entry.async_on_unload(coordinator.async_add_listener(async_update_entities))
    
    if entities:
        async_add_entities(entities)
    async_update_entities()


class WLEDPresetSelect(WledReviveEntity, SelectEntity):
    def __init__(self, data, entry_id):
        super().__init__(data)
        self._attr_has_entity_name = True
        self._attr_name = "Preset"
        self._attr_unique_id = f"{entry_id}_preset"
        self._attr_icon = "mdi:playlist-star"
        self._attr_options = list(self._data["presets_map"].keys())

    @property
    def current_option(self):
        current_ps = self.coordinator.data.get("state", {}).get("ps", -1)
        if current_ps == -1: return None
        return self._data["id_to_preset"].get(current_ps)

    async def async_select_option(self, option: str) -> None:
        preset_id = self._data["presets_map"].get(option)
        if preset_id is not None:
            self.coordinator.data["state"]["ps"] = preset_id
            self.coordinator.async_set_updated_data(self.coordinator.data)
            
            # TRAFFIC LIGHT LOCK
            async with self._data["lock"]:
                try:
                    async with async_timeout.timeout(5):
                        await self._data["session"].post(f"http://{self._data['ip_address']}/json/state", json={"ps": preset_id})
                    await self.coordinator.async_request_refresh()
                except Exception as e:
                    _LOGGER.error("Failed to set WLED preset: %s", e)
                finally:
                    await asyncio.sleep(0.5)


class WLEDPlaylistSelect(WledReviveEntity, SelectEntity):
    def __init__(self, data, entry_id):
        super().__init__(data)
        self._attr_has_entity_name = True
        self._attr_name = "Playlist"
        self._attr_unique_id = f"{entry_id}_playlist"
        self._attr_icon = "mdi:play-speed"
        self._attr_options = list(self._data["playlists_map"].keys())

    @property
    def current_option(self):
        current_pl = self.coordinator.data.get("state", {}).get("pl", -1)
        if current_pl == -1: return None
        return self._data["id_to_playlist"].get(current_pl)

    async def async_select_option(self, option: str) -> None:
        playlist_id = self._data["playlists_map"].get(option)
        if playlist_id is not None:
            self.coordinator.data["state"]["pl"] = playlist_id
            self.coordinator.async_set_updated_data(self.coordinator.data)
            
            # TRAFFIC LIGHT LOCK
            async with self._data["lock"]:
                try:
                    async with async_timeout.timeout(5):
                        await self._data["session"].post(f"http://{self._data['ip_address']}/json/state", json={"pl": playlist_id})
                    await self.coordinator.async_request_refresh()
                except Exception as e:
                    _LOGGER.error("Failed to set WLED playlist: %s", e)
                finally:
                    await asyncio.sleep(0.5)


class WLEDPaletteSelect(WledReviveEntity, SelectEntity):
    def __init__(self, data, entry_id, segment_id, name):
        super().__init__(data)
        self._segment_id = segment_id
        self._attr_has_entity_name = True
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_pal_seg_{segment_id}"
        self._attr_icon = "mdi:palette"
        self._attr_entity_category = EntityCategory.CONFIG  
        self._attr_options = list(self._data["palettes_map"].keys())

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
    def current_option(self):
        seg = self._get_segment()
        if seg and "pal" in seg:
            return self._data["id_to_palette"].get(seg["pal"], "Default")
        return "Default"

    async def async_select_option(self, option: str) -> None:
        pal_id = self._data["palettes_map"].get(option)
        if pal_id is not None:
            seg = self._get_segment()
            if seg: seg["pal"] = pal_id
            self.coordinator.async_set_updated_data(self.coordinator.data)
            
            payload = {"seg": [{"id": self._segment_id, "pal": pal_id}]}
            
            # TRAFFIC LIGHT LOCK
            async with self._data["lock"]:
                try:
                    async with async_timeout.timeout(5):
                        await self._data["session"].post(f"http://{self._data['ip_address']}/json/state", json=payload)
                except Exception as e:
                    _LOGGER.error("Failed to set WLED palette: %s", e)
                finally:
                    await asyncio.sleep(0.1)
