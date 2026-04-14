from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
from .const import DOMAIN

class WledReviveEntity(CoordinatorEntity):
    """Master base entity for all WLED Revive platforms."""
    
    def __init__(self, data):
        super().__init__(data["coordinator"])
        self._data = data

    @property
    def device_info(self):
        info = self.coordinator.data.get("info", {})
        
        raw_mac = info.get("mac", "")
        formatted_mac = ":".join(raw_mac[i:i+2] for i in range(0, len(raw_mac), 2)) if len(raw_mac) == 12 else raw_mac

        device_info = {
            "identifiers": {(DOMAIN, self._data["ip_address"])},
            "name": self._data["name"],
            "manufacturer": "AnasBox", 
            "model": "WLED Revive", 
            "sw_version": info.get("ver", "Unknown"),
            "hw_version": info.get("arch", "Unknown"), # This forces Hardware onto its own line!
            "configuration_url": f"http://{self._data['ip_address']}",
        }
        
        if formatted_mac:
            device_info["connections"] = {(CONNECTION_NETWORK_MAC, formatted_mac)}
            
        return device_info