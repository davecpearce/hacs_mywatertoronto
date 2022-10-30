"""Tests for MyWaterToronto."""
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.mywatertoronto.const import DOMAIN

from .const import (
    TEST_ACCOUNT_NUMBER,
    TEST_CLIENT_NUMBER,
    TEST_LAST_NAME,
    TEST_LAST_PAYMENT_METHOD,
    TEST_POSTAL_CODE,
    TEST_TITLE,
    TEST_UNIQUE_ID,
)


def mock_config_entry() -> MockConfigEntry:
    """Return a MyWaterToronto mock config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        title=TEST_TITLE,
        unique_id=TEST_UNIQUE_ID,
        data={
            "account_nuber": TEST_ACCOUNT_NUMBER,
            "client_number": TEST_CLIENT_NUMBER,
            "last_name": TEST_LAST_NAME,
            "postal_code": TEST_POSTAL_CODE,
            "last_payment_method": TEST_LAST_PAYMENT_METHOD,
        },
        options=None,
    )
