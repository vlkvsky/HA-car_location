import voluptuous as vol
from homeassistant import config_entries

DOMAIN = "car_location"


class CarLocationFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            user_input.setdefault("scan_interval", 60)

            return self.async_create_entry(
                title="Car Location",
                data=user_input,
            )

        schema = vol.Schema({
            vol.Required("username"): str,
            vol.Required("client_id"): str,
            vol.Optional("scan_interval", default=60): int,
        })

        return self.async_show_form(step_id="user", data_schema=schema)