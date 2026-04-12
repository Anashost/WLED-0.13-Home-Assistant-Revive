import logging
import async_timeout
from datetime import timedelta

from homeassistant.components.light import (
    LightEntity,
    ColorMode,
    LightEntityFeature,
    ATTR_BRIGHTNESS,
    ATTR_RGB_COLOR,
    ATTR_EFFECT,
)
from homeassistant.const import CONF_NAME, CONF_IP_ADDRESS
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from .const import DOMAIN, CONF_POLLING_INTERVAL, DEFAULT_POLLING_INTERVAL

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the WLED Revive light."""
    # Check options first (in case it was updated via the cog), fallback to original data
    ip_address = config_entry.options.get(
        CONF_IP_ADDRESS, 
        config_entry.data.get(CONF_IP_ADDRESS)
    )
    name = config_entry.data[CONF_NAME] # Name rarely changes, so data is fine
    
    polling_interval = config_entry.options.get(
        CONF_POLLING_INTERVAL,
        config_entry.data.get(CONF_POLLING_INTERVAL, DEFAULT_POLLING_INTERVAL)
    )

    session = async_get_clientsession(hass)


    # Dynamically fetch the list of effects from the controller
    effect_list = []
    try:
        async with async_timeout.timeout(5):
            async with session.get(f"http://{ip_address}/json/eff") as response:
                response.raise_for_status()
                effect_list = await response.json()
    except Exception as err:
        _LOGGER.warning("Could not fetch effects list from WLED: %s. Using basic fallback.", err)
        # Fallback just in case the endpoint fails
        effect_list = ["Solid", "Blink", "Breathe", "Wipe", "Random Colors"]

    # In WLED, the array index corresponds to the effect ID
    effects_map = {name: index for index, name in enumerate(effect_list)}
    id_to_effect = {index: name for index, name in enumerate(effect_list)}

    async def async_update_data():
        """Fetch data from WLED API."""
        try:
            async with async_timeout.timeout(10):
                async with session.get(f"http://{ip_address}/json/state") as response:
                    response.raise_for_status()
                    return await response.json()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with WLED API: {err}")

    coordinator = DataUpdateCoordinator(
        hass, 
        _LOGGER, 
        name=f"wled_poll_{name}", 
        update_method=async_update_data, 
        update_interval=timedelta(seconds=polling_interval),
    )

    await coordinator.async_config_entry_first_refresh()
    
    # Pass our dynamically generated effect maps into the light entity
    async_add_entities([WLEDReviveLight(coordinator, name, ip_address, config_entry.entry_id, session, effects_map, id_to_effect)])


class WLEDReviveLight(CoordinatorEntity, LightEntity):
    """Representation of a WLED Revive Light."""

    def __init__(self, coordinator, name, ip_address, entry_id, session, effects_map, id_to_effect):
        super().__init__(coordinator)
        self._name = name
        self._ip_address = ip_address
        self._session = session
        self._effects_map = effects_map
        self._id_to_effect = id_to_effect
        
        self._attr_icon = "mdi:led-strip-variant"
        self._attr_unique_id = entry_id
        self._attr_supported_color_modes = {ColorMode.RGB}
        self._attr_color_mode = ColorMode.RGB
        self._attr_supported_features = LightEntityFeature.EFFECT
        self._attr_effect_list = list(self._effects_map.keys())

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        if self.coordinator.data and "on" in self.coordinator.data:
            return self.coordinator.data["on"]
        return False

    @property
    def brightness(self):
        if self.coordinator.data and "bri" in self.coordinator.data:
            return self.coordinator.data["bri"]
        return 255

    @property
    def rgb_color(self):
        if self.coordinator.data and "seg" in self.coordinator.data:
            try:
                col = self.coordinator.data["seg"][0]["col"][0]
                return (col[0], col[1], col[2])
            except (IndexError, KeyError):
                pass
        return (255, 255, 255)

    @property
    def effect(self):
        if self.coordinator.data and "seg" in self.coordinator.data:
            try:
                fx_id = self.coordinator.data["seg"][0]["fx"]
                return self._id_to_effect.get(fx_id, "Solid")
            except (IndexError, KeyError):
                pass
        return "Solid"

    async def _send_json_command(self, payload):
        """Send JSON command to WLED in the background."""
        url = f"http://{self._ip_address}/json/state"
        try:
            async with async_timeout.timeout(5):
                async with self._session.post(url, json=payload) as response:
                    response.raise_for_status()
                    
            await self.coordinator.async_request_refresh()
            
        except Exception as e:
            _LOGGER.error("Failed to send command to WLED: %s", e)

    async def async_turn_on(self, **kwargs):
        """Turn the light on with optimistic UI updates."""
        payload = {"on": True}
        
        if self.coordinator.data:
            self.coordinator.data["on"] = True
            
        if ATTR_BRIGHTNESS in kwargs:
            bri = kwargs[ATTR_BRIGHTNESS]
            payload["bri"] = bri
            if self.coordinator.data:
                self.coordinator.data["bri"] = bri
                
        seg_update = {}
        if ATTR_RGB_COLOR in kwargs:
            rgb = kwargs[ATTR_RGB_COLOR]
            seg_update["col"] = [[rgb[0], rgb[1], rgb[2]]]
            try:
                self.coordinator.data["seg"][0]["col"][0] = [rgb[0], rgb[1], rgb[2]]
            except (KeyError, IndexError, TypeError):
                pass
                
        if ATTR_EFFECT in kwargs:
            effect_name = kwargs[ATTR_EFFECT]
            effect_id = self._effects_map.get(effect_name)
            if effect_id is not None:
                seg_update["fx"] = effect_id
                try:
                    self.coordinator.data["seg"][0]["fx"] = effect_id
                except (KeyError, IndexError, TypeError):
                    pass
                
        if seg_update:
            payload["seg"] = [seg_update]

        self.async_write_ha_state()
        await self._send_json_command(payload)

    async def async_turn_off(self, **kwargs):
        """Turn the light off with optimistic UI updates."""
        if self.coordinator.data:
            self.coordinator.data["on"] = False
        self.async_write_ha_state()
        
        await self._send_json_command({"on": False})