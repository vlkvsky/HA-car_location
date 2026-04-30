from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .coordinator import CarDataCoordinator

DOMAIN = "car_location"


async def async_setup(hass: HomeAssistant, config: dict):
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    coordinator = CarDataCoordinator(
        hass,
        entry.data,
        entry.options,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    entry.async_on_unload(
        entry.add_update_listener(update_listener)
    )

    await hass.config_entries.async_forward_entry_setups(
        entry, ["device_tracker"]
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    return await hass.config_entries.async_unload_platforms(
        entry, ["device_tracker"]
    )


async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_reload(entry.entry_id)