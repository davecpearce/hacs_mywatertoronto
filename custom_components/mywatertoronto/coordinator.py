"""Coordinator for MyWaterToronto API."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any, cast

from pymywatertoronto.enums import LastPaymentMethod
from pymywatertoronto.errors import (
    AccountDetailsError,
    ApiError,
    ValidateAccountInfoError,
)
from pymywatertoronto.mywatertoronto import MyWaterToronto

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_ACCOUNT_NUMBER,
    CONF_CLIENT_NUMBER,
    CONF_LAST_NAME,
    CONF_LAST_PAYMENT_METHOD,
    CONF_POSTAL_CODE,
    DOMAIN,
    ERROR_API,
    ERROR_GET_ACCOUNT_DETAILS,
    ERROR_GET_CONSUMPTION,
    ERROR_VALIDATING_ACCOUNT,
)

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
        except ApiError as err:
            raise UpdateFailed(f"{ERROR_API}: {err}") from err
        except ValidateAccountInfoError as err:
            raise UpdateFailed(f"{ERROR_VALIDATING_ACCOUNT}: {err}") from err

        try:
            self.account_details = await self.mywatertoronto.async_get_account_details()
        except ApiError as err:
            raise UpdateFailed(f"{ERROR_API}: {err}") from err
        except AccountDetailsError as err:
            raise UpdateFailed(f"{ERROR_GET_ACCOUNT_DETAILS}: {err}") from err

        try:
            return cast(
                dict[str, Any],
                await self.mywatertoronto.async_get_consumption(),
            )
        except Exception as err:
            raise UpdateFailed(f"{ERROR_GET_CONSUMPTION}: {err}") from err

    async def async_update_data(self) -> dict[str, str]:
        """Fetch data from MyWaterToronto."""

        await self._async_update_data()
