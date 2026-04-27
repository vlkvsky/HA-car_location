from homeassistant.components.device_tracker import SourceType, TrackerEntity

DOMAIN = "car_location"


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([CarTracker(coordinator)])


class CarTracker(TrackerEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "Audi A4"
        self._attr_unique_id = "audi_a4_tracker"

    @property
    def source_type(self):
        return SourceType.GPS

    @property
    def latitude(self):
        if not self.coordinator.data:
            return None
        return float(self.coordinator.data.get("lat"))

    @property
    def longitude(self):
        if not self.coordinator.data:
            return None
        return float(self.coordinator.data.get("lon"))

    @property
    def available(self):
        return self.coordinator.data is not None

    @property
    def extra_state_attributes(self):
        return self.coordinator.data or {}