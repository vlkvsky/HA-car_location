from homeassistant.components.device_tracker import SourceType, TrackerEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

DOMAIN = "car_location"


def format_diff_time(seconds: int) -> str:
    if seconds is None:
        return "unknown"

    seconds = int(seconds)

    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)

    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if seconds and not days:
        parts.append(f"{seconds}s")

    return " ".join(parts) if parts else "0s"


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([CarTracker(coordinator)])


class CarTracker(CoordinatorEntity, TrackerEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Audi A4"
        self._attr_unique_id = "audi_a4_tracker"
        self._attr_icon = "mdi:car"

    @property
    def should_poll(self):
        return False

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
        data = self.coordinator.data or {}

        engine = int(data.get("engine", 0))
        diff_time = int(data.get("diff_time", 0))

        return {
            "speed": float(data.get("speed", 0)),
            "ignition": bool(engine),
            "ignition_status": "Заведен" if engine else "Заглушен",
            "last_update": format_diff_time(diff_time),
        }