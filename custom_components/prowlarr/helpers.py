from homeassistant.core import HomeAssistant
from .prowlarr_api import ProwlarrApi

def setup_client(
    hass: HomeAssistant,
    api: str,
    host: str,
    port: int,
    ssl: bool,
) -> ProwlarrApi:
    client = ProwlarrApi(hass, api, host, port, ssl)

    client.update()
    return client