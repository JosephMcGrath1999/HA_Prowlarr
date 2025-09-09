from typing import Any
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow
from homeassistant.const import (
    CONF_API_KEY, 
    CONF_HOST, 
    CONF_PORT, 
    CONF_SSL
    )

from .const import (
    DOMAIN
    )
from .helpers import setup_client
from .prowlarr_api import (
    FailedToLogin,
    ProwlarrCannotBeReached
)

PROWLARR_SCHEMA = vol.Schema({
    vol.Optional(CONF_HOST, default='localhost'): vol.All(str),
    vol.Optional(CONF_PORT, default=7878): vol.All(vol.Coerce(int), vol.Range(min=0)),
    vol.Required(CONF_API_KEY): vol.All(str),
    vol.Optional(CONF_SSL, default=False): vol.All(bool),
})

class ProwlarrConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for the Prowlarr integration."""

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ):
        errors = {}

        if user_input is not None:
            self._async_abort_entries_match({CONF_API_KEY: user_input[CONF_API_KEY]})
            try:
                await self.hass.async_add_executor_job(
                    setup_client,
                    self.hass,
                    user_input[CONF_API_KEY],
                    user_input[CONF_HOST],
                    user_input[CONF_PORT],
                    user_input[CONF_SSL]
                )
            except FailedToLogin as err:
                errors = {'base': 'failed_to_login'}
            except ProwlarrCannotBeReached as err:
                errors = {'base': 'cannot_be_reached'}
            else:
                return self.async_create_entry(title="Prowlarr", data=user_input)

        schema = self.add_suggested_values_to_schema(PROWLARR_SCHEMA, user_input)
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)