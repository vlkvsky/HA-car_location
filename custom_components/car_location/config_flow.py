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

    @staticmethod
    def async_get_options_flow(config_entry):
        return CarLocationOptionsFlow(config_entry)


class CarLocationOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_interval = self.config_entry.options.get(
            "scan_interval",
            self.config_entry.data.get("scan_interval", 60)
        )

        schema = vol.Schema({
            vol.Optional("scan_interval", default=current_interval): int,
        })

        return self.async_show_form(step_id="init", data_schema=schema)