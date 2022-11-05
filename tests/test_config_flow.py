"""Tests for the config flow."""
from unittest.mock import PropertyMock, patch

from custom_components.mywatertoronto.const import (
    CONF_ACCOUNT_NUMBER,
    CONF_CLIENT_NUMBER,
    CONF_LAST_NAME,
    CONF_LAST_PAYMENT_METHOD,
    CONF_POSTAL_CODE,
    DOMAIN,
)
from homeassistant import config_entries, data_entry_flow

from .const import (
    MOCK_CONFIG,
    TEST_ACCOUNT_NUMBER,
    TEST_CLIENT_NUMBER,
    TEST_LAST_NAME,
    TEST_LAST_PAYMENT_METHOD,
    TEST_POSTAL_CODE,
    TEST_TITLE,
)

INTEGRATION = "custom_components.mywatertoronto"
PATCH_CONNECTION = f"{INTEGRATION}.config_flow.Connection.test_connection"
PATCH_ASYNC_SETUP_ENTRY = f"{INTEGRATION}.async_setup_entry"


async def test_form(hass, account_details, bypass_validate_account):
    """Test we get the form."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == "form"
    assert result["errors"] == {}

    with patch(
        "custom_components.mywatertoronto.async_setup_entry", return_value=True
    ), patch(
        "pymywatertoronto.mywatertoronto.MyWaterToronto.account_details",
        new_callable=PropertyMock,
        return_value=account_details,
    ) as mock_setup_entry:
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_ACCOUNT_NUMBER: TEST_ACCOUNT_NUMBER,
                CONF_CLIENT_NUMBER: TEST_CLIENT_NUMBER,
                CONF_LAST_NAME: TEST_LAST_NAME,
                CONF_LAST_PAYMENT_METHOD: TEST_LAST_PAYMENT_METHOD,
                CONF_POSTAL_CODE: TEST_POSTAL_CODE,
            },
        )

        assert result2["type"] == "create_entry"
        assert result2["title"] == TEST_TITLE
        assert result2["data"] == {
            CONF_ACCOUNT_NUMBER: TEST_ACCOUNT_NUMBER,
            CONF_CLIENT_NUMBER: TEST_CLIENT_NUMBER,
            CONF_LAST_NAME: TEST_LAST_NAME,
            CONF_LAST_PAYMENT_METHOD: TEST_LAST_PAYMENT_METHOD,
            CONF_POSTAL_CODE: TEST_POSTAL_CODE,
        }
        await hass.async_block_till_done()
        assert len(mock_setup_entry.mock_calls) == 1


# In this case, we want to simulate a failure during validate account
async def test_validate_account_failure(hass, error_on_async_validate_account):
    """Test a failed config flow due to validate account failure."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=MOCK_CONFIG
    )

    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["errors"] == {"base": "cannot_connect"}


# In this case, we want to simulate a failure during validate account
async def test_get_accounts_details_failure(hass, error_on_async_get_account_details):
    """Test a failed config flow due to get account details failure."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=MOCK_CONFIG
    )

    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["errors"] == {"base": "cannot_connect"}
