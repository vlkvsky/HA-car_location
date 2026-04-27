import voluptuous as vol

from homeassistant import config_entries

DOMAIN = "car_location"


class CarLocationFlow(config_entries.ConfigFlow, domain=DOMAIN):

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="Car Location",
                data=user_input,
            )

        schema = vol.Schema({
            vol.Required("username"): str,
            vol.Required("client_id"): str,
        })

        return self.async_show_form(step_id="user", data_schema=schema)