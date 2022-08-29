"""Config flow for mywatertoronto integration."""
import logging

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    TextSelector,
)

from pymywatertoronto.mywatertoronto import (
    MyWaterToronto,
)
from pymywatertoronto.enums import (
    LastPaymentMethod,
)
from pymywatertoronto.errors import (
    AccountDetailsError,
    ValidateAccountInfoError,
)
from pymywatertoronto.const import (
    KEY_ADDRESS,
    KEY_PREMISE_LIST,
)

import voluptuous as vol

from .const import (
    CONF_ACCOUNT_NUMBER,
    CONF_CLIENT_NUMBER,
    CONF_LAST_NAME,
    CONF_POSTAL_CODE,
    CONF_LAST_PAYMENT_METHOD,
    DOMAIN
)

_LOGGER = logging.getLogger(__name__)

LAST_PAYMENT_METHOD_TYPES = [
    SelectOptionDict(value="1", label="Pre-authorized"),
    SelectOptionDict(value="2", label="Mail in cheque"),
    SelectOptionDict(value="3", label="In person"),
    SelectOptionDict(value="4", label="Bank payment"),
    SelectOptionDict(value="5", label="Payment drop box"),
]

MYWATERTORONTO_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ACCOUNT_NUMBER): TextSelector(),
        vol.Required(CONF_CLIENT_NUMBER): TextSelector(),
        vol.Required(CONF_LAST_NAME): TextSelector(),
        vol.Required(CONF_POSTAL_CODE): TextSelector(),
        vol.Required(CONF_LAST_PAYMENT_METHOD, default='4'): SelectSelector(
            SelectSelectorConfig(
                options=LAST_PAYMENT_METHOD_TYPES,
                mode=SelectSelectorMode.DROPDOWN,
            )
        ),
    }
)

class MyWaterTorontoFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for mywatertoronto."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input=None
    ) -> FlowResult:

        """Handle the flow initialized by the user."""

        errors = {}
        if user_input:
            websession = async_get_clientsession(self.hass)
            mywatertoronto = MyWaterToronto(
                session = websession,
                account_number = user_input[CONF_ACCOUNT_NUMBER],
                client_number = user_input[CONF_CLIENT_NUMBER],
                last_name = user_input[CONF_LAST_NAME],
                postal_code = user_input[CONF_POSTAL_CODE],
                last_payment_method = LastPaymentMethod(user_input[CONF_LAST_PAYMENT_METHOD]),
            )

            try:
                await mywatertoronto.async_validate_account()
            except ValidateAccountInfoError:
                errors["base"] = "cannot_connect"
            else:
                try:
                    await mywatertoronto.async_get_account_details()
                except AccountDetailsError:
                    errors["base"] = "cannot_connect"
                else:
                    await self.async_set_unique_id(mywatertoronto.account_number_full)
                    title = f"{mywatertoronto.account_details[KEY_PREMISE_LIST][0][KEY_ADDRESS]} Water Meter"
                    return self.async_create_entry(title=title.title(), data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=MYWATERTORONTO_SCHEMA,
            errors=errors
        )