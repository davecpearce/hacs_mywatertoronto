"""Coordinator for MyWaterToronto API."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any
from typing import cast

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.update_coordinator import UpdateFailed
from httpx import HTTPError
from httpx import HTTPStatusError
from httpx import TimeoutException
from pymywatertoronto.enums import (
    LastPaymentMethod,
)
from pymywatertoronto.errors import (
    ValidateAccountInfoError,
)
from pymywatertoronto.mywatertoronto import (
    MyWaterToronto,
)

from .const import CONF_ACCOUNT_NUMBER
from .const import CONF_CLIENT_NUMBER
from .const import CONF_LAST_NAME
from .const import CONF_LAST_PAYMENT_METHOD
from .const import CONF_POSTAL_CODE
from .const import DOMAIN

SCAN_INTERVAL = timedelta(minutes=60)

_LOGGER = logging.getLogger(__name__)


class MyWaterTorontoDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching MyWaterToronto data API."""

    def __init__(self, hass: HomeAssistant, *, entry: ConfigEntry) -> None:
        """Initialize."""

        self.websession = async_get_clientsession(hass)
        self.account_details: dict[str, Any] = None

        self.mywatertoronto = MyWaterToronto(
            session=self.websession,
            account_number=entry.data[CONF_ACCOUNT_NUMBER],
            client_number=entry.data[CONF_CLIENT_NUMBER],
            last_name=entry.data[CONF_LAST_NAME],
            postal_code=entry.data[CONF_POSTAL_CODE],
            last_payment_method=LastPaymentMethod(entry.data[CONF_LAST_PAYMENT_METHOD]),
        )

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}-{self.mywatertoronto.account_number_full}",
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self) -> dict[str, str]:
        """Fetch data from MyWaterToronto."""

        try:
            await self.mywatertoronto.async_validate_account()
        except ValidateAccountInfoError as err:
            raise UpdateFailed(
                f"Error validating account with MyWaterToronto API: {err}"
            ) from err

        try:
            self.account_details = (
                await self.mywatertoronto.async_get_account_details()
            )  # noqa: E501
        except (HTTPError, HTTPStatusError, TimeoutException) as err:
            raise UpdateFailed(
                f"Error communicating with MyWaterToronto API: {err}"
            ) from err

        try:
            return cast(
                dict[str, Any],
                await self.mywatertoronto.async_get_consumption(),
            )
        except (HTTPError, HTTPStatusError, TimeoutException) as err:
            raise UpdateFailed(
                f"Error communicating with MyWaterToronto API: {err}"
            ) from err
