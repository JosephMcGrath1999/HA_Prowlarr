import time
from datetime import datetime
from pytz import timezone
import requests
import json
import logging
from .parser import parse_data

from .const import DOMAIN


from homeassistant.core import HomeAssistant

LOGGER = logging.getLogger("custom_components." + DOMAIN)


def get_date(zone, offset=0):
    """Get date based on timezone and offset of days."""
    return datetime.date(datetime.fromtimestamp(
        time.time() + 86400 * offset, tz=zone))

class ProwlarrApi():
    def __init__(
        self,
        hass: HomeAssistant,
        api: str,
        host: str,
        port: int,
        ssl: bool,
    ):
        self._api = api
        self._hass = hass
        self._host = host
        self._port = port
        self._ssl = ssl

    def update(self):
        prowlarr = requests.Session()
        address = self.get_url()

        try:
            api = prowlarr.get(address, headers={'X-Api-Key': self._api}, timeout=10)
        except OSError:
            raise ProwlarrCannotBeReached

        if api.status_code == 200:
            LOGGER.info("Prowlarr connection successful")
            LOGGER.debug(f"Prowlarr response: {api.json()}")
            return {
                'online': True,
                'data': parse_data(api.json())
            }

        raise ProwlarrCannotBeReached

    def get_url(self):
        address = ""

        if self._ssl:
            address += "https://"
        else:
            address += "http://"
        address += f"{self._host}:{self._port}/api/v1/indexer"

        return address


class FailedToLogin(Exception):
    "Raised when the Prowlarr user fail to Log-in"
    pass

class ProwlarrCannotBeReached(Exception):
    "Raised when the Prowlarr cannot be reached"
    pass
