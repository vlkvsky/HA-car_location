from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

DOMAIN = "car_location"


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        CarSpeedSensor(coordinator),
        CarDiffTimeSensor(coordinator),
    ])


class CarSpeedSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)

        self._attr_name = "Audi A4 Speed"
        self._attr_unique_id = "audi_a4_speed"
        self._attr_native_unit_of_measurement = "km/h"
        self._attr_icon = "mdi:speedometer"

    @property
    def native_value(self):
        data = self.coordinator.data or {}
        return data.get("speed", 0)


class CarDiffTimeSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)

        self._attr_name = "Audi A4 Last Update"
        self._attr_unique_id = "audi_a4_diff_time"
        self._attr_icon = "mdi:clock"

    @property
    def native_value(self):
        data = self.coordinator.data or {}
        return data.get("diff_time", 0)