import logging
import json
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)


def _parse_bigdata(bigdata: str):
    result = {}

    if not bigdata:
        return result

    parts = bigdata.split(",")
    for part in parts:
        if ":" in part:
            key_parts = part.split(":")
            if len(key_parts) >= 3:
                key = key_parts[0]
                value = key_parts[-1]
                result[key] = value

    return result


class CarDataCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        self.hass = hass
        self.entry = entry

        self.username = entry.data["username"]
        self.client_id = entry.data["client_id"]

        self.session = async_get_clientsession(hass)

        super().__init__(
            hass,
            _LOGGER,
            name="car_location",
            update_interval=timedelta(seconds=self._get_interval()),
        )

    def _get_interval(self):
        return self.entry.options.get(
            "scan_interval",
            self.entry.data.get("scan_interval", 60),
        )

    def get_current_interval(self):
        return self._get_interval()

    async def set_interval(self, value: int):
        _LOGGER.debug(f"Set interval to {value}")

        self.update_interval = timedelta(seconds=value)

        await self.async_request_refresh()

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

            bigdata_raw = d.get("bigdata", "")
            bigdata = _parse_bigdata(bigdata_raw)

            engine = int(bigdata.get("engine", 0))

            speed = float(d.get("speed", 0))
            if d.get("gpslbs") != "A":
                speed = 0

            return {
                "lat": float(d["lat"]),
                "lon": float(d["lng"]),
                "speed": speed,
                "timestamp": f'{d["d"]} {d["t"]}',
                "diff_time": int(d.get("diff_time", 0)),
                "engine": engine,
            }