import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import EntityCategory, SIGNAL_STRENGTH_DECIBELS_MILLIWATT, UnitOfInformation, UnitOfElectricCurrent
from .const import DOMAIN
from .entity import WledReviveEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    data = hass.data[DOMAIN][config_entry.entry_id]
    if data["coordinator"].data and "info" in data["coordinator"].data:
        async_add_entities([
            WLEDIPSensor(data, config_entry.entry_id),
            WLEDEstimatedCurrentSensor(data, config_entry.entry_id),
            WLEDMaxCurrentSensor(data, config_entry.entry_id),
            WLEDLedCountSensor(data, config_entry.entry_id),
            WLEDHeapSensor(data, config_entry.entry_id),
            WLEDUptimeSensor(data, config_entry.entry_id),
            WLEDWifiSignalSensor(data, config_entry.entry_id),
            WLEDWifiRSSISensor(data, config_entry.entry_id),
            WLEDWifiChannelSensor(data, config_entry.entry_id),
            WLEDWifiBSSIDSensor(data, config_entry.entry_id),
        ])

class WLEDDiagnosticSensor(WledReviveEntity, SensorEntity):
    def __init__(self, data, entry_id, key, name, icon, enabled_by_default):
        super().__init__(data)
        self._key = key
        self._attr_has_entity_name = True
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_sensor_{key}"
        self._attr_icon = icon
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_entity_registry_enabled_default = enabled_by_default

class WLEDIPSensor(WLEDDiagnosticSensor):
    def __init__(self, data, entry_id):
        super().__init__(data, entry_id, "ip", "IP Address", "mdi:ip-network", True)
    @property
    def native_value(self):
        return self.coordinator.data.get("info", {}).get("ip")

class WLEDEstimatedCurrentSensor(WLEDDiagnosticSensor):
    def __init__(self, data, entry_id):
        super().__init__(data, entry_id, "current", "Estimated Current", "mdi:current-ac", True)
        self._attr_device_class = "current"
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.MILLIAMPERE
    @property
    def native_value(self):
        return self.coordinator.data.get("info", {}).get("leds", {}).get("pwr")

class WLEDMaxCurrentSensor(WLEDDiagnosticSensor):
    def __init__(self, data, entry_id):
        super().__init__(data, entry_id, "max_current", "Max Current", "mdi:current-ac", True)
        self._attr_device_class = "current"
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.MILLIAMPERE
    @property
    def native_value(self):
        return self.coordinator.data.get("info", {}).get("leds", {}).get("maxpwr")

class WLEDLedCountSensor(WLEDDiagnosticSensor):
    def __init__(self, data, entry_id):
        super().__init__(data, entry_id, "led_count", "LED Count", "mdi:led-strip", True)
    @property
    def native_value(self):
        return self.coordinator.data.get("info", {}).get("leds", {}).get("count")

class WLEDHeapSensor(WLEDDiagnosticSensor):
    def __init__(self, data, entry_id):
        super().__init__(data, entry_id, "freeheap", "Free Memory", "mdi:memory", False)
        self._attr_device_class = "data_size"
        self._attr_native_unit_of_measurement = UnitOfInformation.BYTES
    @property
    def native_value(self):
        return self.coordinator.data.get("info", {}).get("freeheap")

class WLEDUptimeSensor(WLEDDiagnosticSensor):
    def __init__(self, data, entry_id):
        super().__init__(data, entry_id, "uptime", "Uptime", "mdi:clock-outline", False)
    @property
    def native_value(self):
        uptime_sec = self.coordinator.data.get("info", {}).get("uptime")
        if not uptime_sec: return None
        m, s = divmod(uptime_sec, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        y, d = divmod(d, 365)
        parts = []
        if y > 0: parts.append(f"{y}y")
        if d > 0: parts.append(f"{d}d")
        if h > 0: parts.append(f"{h}h")
        if m > 0: parts.append(f"{m}m")
        parts.append(f"{s}s")
        return " ".join(parts)

class WLEDWifiSignalSensor(WLEDDiagnosticSensor):
    def __init__(self, data, entry_id):
        super().__init__(data, entry_id, "wifi_signal", "Wi-Fi Signal", "mdi:wifi", False)
        self._attr_native_unit_of_measurement = "%"
    @property
    def native_value(self):
        return self.coordinator.data.get("info", {}).get("wifi", {}).get("signal")

class WLEDWifiRSSISensor(WLEDDiagnosticSensor):
    def __init__(self, data, entry_id):
        super().__init__(data, entry_id, "wifi_rssi", "Wi-Fi RSSI", "mdi:wifi-strength-outline", False)
        self._attr_device_class = "signal_strength"
        self._attr_native_unit_of_measurement = SIGNAL_STRENGTH_DECIBELS_MILLIWATT
    @property
    def native_value(self):
        return self.coordinator.data.get("info", {}).get("wifi", {}).get("rssi")

class WLEDWifiChannelSensor(WLEDDiagnosticSensor):
    def __init__(self, data, entry_id):
        super().__init__(data, entry_id, "wifi_channel", "Wi-Fi Channel", "mdi:router-wireless", False)
    @property
    def native_value(self):
        return self.coordinator.data.get("info", {}).get("wifi", {}).get("channel")

class WLEDWifiBSSIDSensor(WLEDDiagnosticSensor):
    def __init__(self, data, entry_id):
        super().__init__(data, entry_id, "wifi_bssid", "Wi-Fi BSSID", "mdi:router-network", False)
    @property
    def native_value(self):
        return self.coordinator.data.get("info", {}).get("wifi", {}).get("bssid")