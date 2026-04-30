from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

DOMAIN = "car_location"


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        CarIgnitionBinarySensor(coordinator)
    ])


class CarIgnitionBinarySensor(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)

        self._attr_name = "Audi A4 Ignition"
        self._attr_unique_id = "audi_a4_ignition"
        self._attr_icon = "mdi:engine"

    @property
    def is_on(self):
        data = self.coordinator.data or {}
        return bool(data.get("engine", 0))