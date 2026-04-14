import logging
import async_timeout
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, PLATFORMS, CONF_IP_ADDRESS, CONF_NAME, CONF_POLLING_INTERVAL, DEFAULT_POLLING_INTERVAL

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})

    ip_address = entry.options.get(CONF_IP_ADDRESS, entry.data.get(CONF_IP_ADDRESS))
    name = entry.data[CONF_NAME]
    polling_interval = entry.options.get(CONF_POLLING_INTERVAL, entry.data.get(CONF_POLLING_INTERVAL, DEFAULT_POLLING_INTERVAL))

    session = async_get_clientsession(hass)

    # Fetch Presets & Playlists dynamically
    presets_map = {}
    id_to_preset = {}
    playlists_map = {}
    id_to_playlist = {}
    try:
        async with async_timeout.timeout(5):
            async with session.get(f"http://{ip_address}/presets.json") as response:
                if response.status == 200:
                    presets_data = await response.json()
                    for p_id, p_data in presets_data.items():
                        if p_id != "0" and isinstance(p_data, dict) and "n" in p_data:
                            # If it contains a 'playlist' object, sort it into the playlist map
                            if "playlist" in p_data:
                                playlists_map[p_data["n"]] = int(p_id)
                                id_to_playlist[int(p_id)] = p_data["n"]
                            else:
                                presets_map[p_data["n"]] = int(p_id)
                                id_to_preset[int(p_id)] = p_data["n"]
    except Exception as err:
        _LOGGER.warning("Could not fetch presets from WLED: %s", err)

    async def async_update_data():
        try:
            async with async_timeout.timeout(10):
                async with session.get(f"http://{ip_address}/json") as response:
                    response.raise_for_status()
                    return await response.json()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with WLED API: {err}")

    coordinator = DataUpdateCoordinator(
        hass, _LOGGER, name=f"wled_{name}", update_method=async_update_data, update_interval=timedelta(seconds=polling_interval)
    )
    await coordinator.async_config_entry_first_refresh()

    effect_list = coordinator.data.get("effects", ["Solid"])
    effects_map = {eff_name: index for index, eff_name in enumerate(effect_list)}
    id_to_effect = {index: eff_name for index, eff_name in enumerate(effect_list)}

    palette_list = coordinator.data.get("palettes", ["Default"])
    palettes_map = {pal_name: index for index, pal_name in enumerate(palette_list)}
    id_to_palette = {index: pal_name for index, pal_name in enumerate(palette_list)}

    # Store everything
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "session": session,
        "ip_address": ip_address,
        "name": name,
        "effects_map": effects_map,
        "id_to_effect": id_to_effect,
        "palettes_map": palettes_map,
        "id_to_palette": id_to_palette,
        "presets_map": presets_map,
        "id_to_preset": id_to_preset,
        "playlists_map": playlists_map,
        "id_to_playlist": id_to_playlist,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(update_listener))
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)