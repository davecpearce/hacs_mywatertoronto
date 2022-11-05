"""The MyWaterToronto component."""
from __future__ import annotations

from homeassistant.const import Platform

DOMAIN = "mywatertoronto"

PLATFORMS = [Platform.SENSOR]

DEFAULT_NAME = "MyWaterToronto Meter"

MYWATERTORONTO = "mywatertoronto"

CONF_ACCOUNT_NUMBER = "account_number"
CONF_CLIENT_NUMBER = "client_number"
CONF_ACCOUNT_NUMBER_FULL = "account_number_full"
CONF_LAST_NAME = "last_name"
CONF_POSTAL_CODE = "postal_code"
CONF_LAST_PAYMENT_METHOD = "last_payment_method"

DATA_COORDINATOR = "coordinator"
DATA_UNDO_UPDATE_LISTENER = "undo_update_listener"

ERROR_API = "Error calling MyWaterToronto API"
ERROR_VALIDATING_ACCOUNT = "Error validating account with MyWaterToronto API"
ERROR_GET_ACCOUNT_DETAILS = "Error getting account details"
ERROR_GET_CONSUMPTION = "Error getting consumption data"
