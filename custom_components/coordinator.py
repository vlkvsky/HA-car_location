import logging
import json
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=120)


class CarDataCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, config):
        self.username = config["username"]
        self.client_id = config["client_id"]
        self.session = async_get_clientsession(hass)

        super().__init__(
            hass,
            _LOGGER,
            name="car_location",
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self):
        url = (
            "https://livegpstracks.com/viewer_coos_s.php"
            f"?username={self.username}&ctp=one&code={self.client_id}"
        )

        async with self.session.get(url) as resp:
            text = await resp.text()

            try:
                data = json.loads(text)
            except Exception:
                _LOGGER.error(f"Bad response: {text[:200]}")
                return None

            if not data:
                return None

            d = data[0]

            return {
                "lat": float(d["lat"]),
                "lon": float(d["lng"]),
                "speed": float(d.get("speed", 0)),
                "timestamp": f'{d["d"]} {d["t"]}',
                "diff_time": int(d.get("diff_time", 0)),
            }