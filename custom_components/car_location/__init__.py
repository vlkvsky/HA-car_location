from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .coordinator import CarDataCoordinator

DOMAIN = "car_location"


async def async_setup(hass: HomeAssistant, config: dict):
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    coordinator = CarDataCoordinator(hass, entry)

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry, ["device_tracker", "number", "sensor", "binary_sensor"]
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    return await hass.config_entries.async_unload_platforms(
        entry, ["device_tracker", "number", "sensor", "binary_sensor"]
    )