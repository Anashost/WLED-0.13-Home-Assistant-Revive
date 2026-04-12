import voluptuous as vol
import async_timeout
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_NAME, CONF_IP_ADDRESS
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN, CONF_POLLING_INTERVAL, DEFAULT_POLLING_INTERVAL

class WledReviveConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for WLED Revive."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        
        if user_input is not None:
            ip_address = user_input[CONF_IP_ADDRESS]
            session = async_get_clientsession(self.hass)
            
            try:
                async with async_timeout.timeout(5):
                    async with session.get(f"http://{ip_address}/json/state") as response:
                        response.raise_for_status()
            except Exception:
                errors["base"] = "cannot_connect"

            if not errors:
                return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME, default="WLED Light"): str,
                vol.Required(CONF_IP_ADDRESS): str,
                vol.Required(CONF_POLLING_INTERVAL, default=DEFAULT_POLLING_INTERVAL): int,
            }),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return WledReviveOptionsFlowHandler(config_entry)


class WledReviveOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for WLED Revive."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        errors = {}

        if user_input is not None:
            ip_address = user_input[CONF_IP_ADDRESS]
            session = async_get_clientsession(self.hass)
            
            # Test the connection to the new IP before saving
            try:
                async with async_timeout.timeout(5):
                    async with session.get(f"http://{ip_address}/json/state") as response:
                        response.raise_for_status()
            except Exception:
                errors["base"] = "cannot_connect"

            if not errors:
                return self.async_create_entry(title="", data=user_input)

        # Get current values, preferring 'options' over 'data' in case they were updated before
        current_ip = self._config_entry.options.get(
            CONF_IP_ADDRESS,
            self._config_entry.data.get(CONF_IP_ADDRESS)
        )
        current_interval = self._config_entry.options.get(
            CONF_POLLING_INTERVAL,
            self._config_entry.data.get(CONF_POLLING_INTERVAL, DEFAULT_POLLING_INTERVAL)
        )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_IP_ADDRESS, default=current_ip): str,
                vol.Required(CONF_POLLING_INTERVAL, default=current_interval): int,
            }),
            errors=errors
        )