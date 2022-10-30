"""Test MyWaterTorontoDataUpdateCoordinator."""
from unittest.mock import patch

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.mywatertoronto import MyWaterTorontoDataUpdateCoordinator
from custom_components.mywatertoronto.const import (
    DOMAIN,
    ERROR_API,
    ERROR_GET_ACCOUNT_DETAILS,
    ERROR_GET_CONSUMPTION,
    ERROR_VALIDATING_ACCOUNT,
)
from homeassistant.helpers.update_coordinator import UpdateFailed

from .const import MOCK_CONFIG


async def test_async_update_data(hass, account_details, consumption):
    """Test data update."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")

    coordinator = MyWaterTorontoDataUpdateCoordinator(hass=hass, entry=config_entry)

    with patch(
        "pymywatertoronto.mywatertoronto.MyWaterToronto.async_get_account_details",
        return_value=account_details,
    ), patch(
        "pymywatertoronto.mywatertoronto.MyWaterToronto.async_get_consumption",
        return_value=consumption,
    ):
        await coordinator._async_update_data()


# In this case, we want to simulate a data failure during validate account
async def test_async_update_data_validate_account_api_failure(
    hass, account_details, consumption, api_error_on_async_validate_account
):
    """Test data update with API error."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")

    coordinator = MyWaterTorontoDataUpdateCoordinator(hass=hass, entry=config_entry)

    with patch(
        "pymywatertoronto.mywatertoronto.MyWaterToronto.async_get_account_details",
        return_value=account_details,
    ), patch(
        "pymywatertoronto.mywatertoronto.MyWaterToronto.async_get_consumption",
        return_value=consumption,
    ):
        test_success = False
        try:
            await coordinator._async_update_data()
        except UpdateFailed as error:
            assert ERROR_API in str(error)
            test_success = True

    assert test_success is True


# In this case, we want to simulate a data failure during validate account
async def test_async_update_data_validate_account_failure(
    hass, account_details, consumption, error_on_async_validate_account
):
    """Test data update with invalid account."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")

    coordinator = MyWaterTorontoDataUpdateCoordinator(hass=hass, entry=config_entry)

    with patch(
        "pymywatertoronto.mywatertoronto.MyWaterToronto.async_get_account_details",
        return_value=account_details,
    ), patch(
        "pymywatertoronto.mywatertoronto.MyWaterToronto.async_get_consumption",
        return_value=consumption,
    ):
        test_success = False
        try:
            await coordinator._async_update_data()
        except UpdateFailed as error:
            assert ERROR_VALIDATING_ACCOUNT in str(error)
            test_success = True

    assert test_success is True


# In this case, we want to simulate an api failure during get account details
async def test_async_update_data_get_account_details_api_failure(
    hass, account_details, consumption, api_error_on_async_get_account_details
):
    """Test data update with API error."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")

    coordinator = MyWaterTorontoDataUpdateCoordinator(hass=hass, entry=config_entry)

    test_success = False
    try:
        await coordinator._async_update_data()
    except UpdateFailed as error:
        assert ERROR_API in str(error)
        test_success = True

    assert test_success is True


# In this case, we want to simulate a data failure during validate account
async def test_async_update_data_get_account_details_failure(
    hass, account_details, consumption, error_on_async_get_account_details
):
    """Test data update with error during get account details."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")

    coordinator = MyWaterTorontoDataUpdateCoordinator(hass=hass, entry=config_entry)

    with patch(
        "pymywatertoronto.mywatertoronto.MyWaterToronto.async_get_consumption",
        return_value=consumption,
    ):
        test_success = False
        try:
            await coordinator._async_update_data()
        except UpdateFailed as error:
            assert ERROR_GET_ACCOUNT_DETAILS in str(error)
            test_success = True

    assert test_success is True


# In this case, we want to simulate a data failure during validate account
async def test_async_update_data_get_consumption_failure(
    hass, account_details, consumption, error_on_async_get_consumption
):
    """Test data update with error during get consumption."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")

    coordinator = MyWaterTorontoDataUpdateCoordinator(hass=hass, entry=config_entry)

    with patch(
        "pymywatertoronto.mywatertoronto.MyWaterToronto.async_get_account_details",
        return_value=account_details,
    ):
        test_success = False
        try:
            await coordinator._async_update_data()
        except Exception as error:
            assert ERROR_GET_CONSUMPTION in str(error)
            test_success = True

    assert test_success is True
