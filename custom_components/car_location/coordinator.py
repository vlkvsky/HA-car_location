import asyncio
import json
import logging
from datetime import timedelta

import aiohttp

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

REQUEST_TIMEOUT = 20  # секунд


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

        # Мережа: таймаут і помилки з'єднання -> UpdateFailed
        # (HA пише зрозуміле повідомлення в лог і повторює на наступному інтервалі)
        try:
            async with self.session.get(
                url, timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
            ) as resp:
                if resp.status != 200:
                    raise UpdateFailed(f"livegpstracks HTTP {resp.status}")
                text = await resp.text()
        except asyncio.TimeoutError as err:
            raise UpdateFailed(f"livegpstracks timeout ({REQUEST_TIMEOUT}s)") from err
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"livegpstracks connection error: {err}") from err

        # Відповідь: невалідний JSON або порожній список -> UpdateFailed
        try:
            data = json.loads(text)
        except ValueError as err:
            raise UpdateFailed(f"Bad response: {text[:200]}") from err

        if not data:
            raise UpdateFailed("Empty response from livegpstracks")

        d = data[0]

        try:
            bigdata = _parse_bigdata(d.get("bigdata", ""))
            engine = int(bigdata.get("engine", 0))
            speed = float(d.get("speed", 0))
#            if d.get("gpslbs") != "A":
#                speed = 0

            return {
                "lat": float(d["lat"]),
                "lon": float(d["lng"]),
                "speed": speed,
                "timestamp": f'{d["d"]} {d["t"]}',
                "diff_time": int(d.get("diff_time", 0)),
                "engine": engine,
            }
        except (KeyError, TypeError, ValueError) as err:
            raise UpdateFailed(f"Unexpected data format: {err}; raw: {str(d)[:200]}") from err
