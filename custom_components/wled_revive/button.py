import logging
import async_timeout
from homeassistant.components.button import ButtonEntity
from homeassistant.const import EntityCategory
from .const import DOMAIN
from .entity import WledReviveEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    data = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([WLEDRestartButton(data, config_entry.entry_id)])

class WLEDRestartButton(WledReviveEntity, ButtonEntity):
    def __init__(self, data, entry_id):
        super().__init__(data)
        self._attr_has_entity_name = True
        self._attr_name = "Restart"
        self._attr_unique_id = f"{entry_id}_restart"
        self._attr_icon = "mdi:restart"
        self._attr_entity_category = EntityCategory.CONFIG

    async def async_press(self) -> None:
        try:
            async with async_timeout.timeout(5):
                await self._data["session"].post(f"http://{self._data['ip_address']}/json/state", json={"rb": True})
        except Exception as e:
            _LOGGER.error("Failed to restart WLED: %s", e)