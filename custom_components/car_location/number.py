from homeassistant.components.number import NumberEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

DOMAIN = "car_location"


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        CarScanIntervalNumber(coordinator, entry)
    ])


class CarScanIntervalNumber(CoordinatorEntity, NumberEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)

        self.entry = entry

        self._attr_name = "Car Scan Interval"
        self._attr_unique_id = f"{entry.entry_id}_scan_interval"
        self._attr_native_min_value = 30
        self._attr_native_max_value = 3600
        self._attr_native_step = 30
        self._attr_native_unit_of_measurement = "s"
        self._attr_icon = "mdi:timer"

    @property
    def native_value(self):
        return self.coordinator.get_current_interval()

    async def async_set_native_value(self, value):
        value = int(value)

        new_options = dict(self.entry.options)
        new_options["scan_interval"] = value

        self.hass.config_entries.async_update_entry(
            self.entry,
            options=new_options,
        )

        await self.coordinator.set_interval(value)