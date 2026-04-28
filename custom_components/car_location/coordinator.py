import logging
import json
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=120)


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

            bigdata_raw = d.get("bigdata", "")
            bigdata = _parse_bigdata(bigdata_raw)

            acc = int(bigdata.get("ACC", 0))

            # фильтр мусорной скорости при LBS
            speed = float(d.get("speed", 0))
            if d.get("gpslbs") != "A":
                speed = 0

            return {
                "lat": float(d["lat"]),
                "lon": float(d["lng"]),
                "speed": speed,
                "timestamp": f'{d["d"]} {d["t"]}',
                "diff_time": int(d.get("diff_time", 0)),
                "acc": acc,
            }
