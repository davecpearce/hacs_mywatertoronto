"""pytest fixtures."""
import json
from unittest.mock import patch

from pymywatertoronto.errors import (
    AccountDetailsError,
    ApiError,
    ValidateAccountInfoError,
)
import pytest
from pytest_homeassistant_custom_component.common import load_fixture

pytest_plugins = "pytest_homeassistant_custom_component"


# This fixture enables loading custom integrations in all tests.
# Remove to enable selective use of this fixture
@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    yield


# This fixture is used to prevent HomeAssistant from attempting to create and dismiss persistent
# notifications. These calls would fail without this fixture since the persistent_notification
# integration is never loaded during a test.
@pytest.fixture(name="skip_notifications", autouse=True)
def skip_notifications_fixture():
    """Skip notification calls."""
    with patch("homeassistant.components.persistent_notification.async_create"), patch(
        "homeassistant.components.persistent_notification.async_dismiss"
    ):
        yield


# This fixture, when used, will result in calls to async_config_entry_first_refresh to return None.
@pytest.fixture(name="bypass_get_data")
def bypass_get_data_fixture():
    """Skip calls to get data."""
    with patch(
        "custom_components.mywatertoronto.MyWaterTorontoDataUpdateCoordinator.async_config_entry_first_refresh"
    ):
        yield


@pytest.fixture(name="account_details", scope="session")
def account_details_fixture():
    """Define account details data."""
    return json.loads(load_fixture("account_details.json"))


@pytest.fixture(name="consumption", scope="session")
def consumption_fixture():
    """Define consumption data."""
    return json.loads(load_fixture("consumption.json"))


@pytest.fixture(name="bypass_validate_account", autouse=True)
def bypass_validate_account_fixture():
    """Skip validate account calls."""
    with patch("pymywatertoronto.mywatertoronto.MyWaterToronto.async_validate_account"):
        yield


@pytest.fixture(name="bypass_get_account_details", autouse=True)
def bypass_get_account_details_fixture():
    """Skip validate account calls."""
    with patch(
        "pymywatertoronto.mywatertoronto.MyWaterToronto.async_get_account_details"
    ):
        yield


# In this fixture, we are forcing calls to async_validate_account to raise an Exception.
@pytest.fixture(name="api_error_on_async_validate_account")
def api_error_on_async_validate_account_fixture():
    """Simulate error when validating MyWaterToronto account."""
    with patch(
        "pymywatertoronto.mywatertoronto.MyWaterToronto.async_validate_account",
        side_effect=ApiError("Invalid response from MyWaterToronto API"),
    ):
        yield


# In this fixture, we are forcing calls to async_validate_account to raise an Exception.
@pytest.fixture(name="error_on_async_validate_account")
def error_on_async_validate_account_fixture():
    """Simulate error when validating MyWaterToronto account."""
    with patch(
        "pymywatertoronto.mywatertoronto.MyWaterToronto.async_validate_account",
        side_effect=ValidateAccountInfoError("Invalid account information"),
    ):
        yield


# In this fixture, we are forcing an API error async_get_account_details.
@pytest.fixture(name="api_error_on_async_get_account_details")
def api_error_on_async_get_account_details_fixture():
    """Simulate an API error when requesting MyWaterToronto account details."""
    with patch(
        "pymywatertoronto.mywatertoronto.MyWaterToronto.async_get_account_details",
        side_effect=ApiError("Error calling MyWaterToronto API"),
    ):
        yield


# In this fixture, we are forcing calls to async_get_account_details to raise an Exception.
@pytest.fixture(name="error_on_async_get_account_details")
def error_on_async_get_account_details_fixture():
    """Simulate error when requesting MyWaterToronto account details."""
    with patch(
        "pymywatertoronto.mywatertoronto.MyWaterToronto.async_get_account_details",
        side_effect=AccountDetailsError("Error getting account details"),
    ):
        yield


# In this fixture, we are forcing calls to async_get_account_details to raise an Exception.
@pytest.fixture(name="error_on_async_get_consumption")
def error_on_async_get_consumption_fixture():
    """Simulate error when requesting MyWaterToronto consumption data."""
    with patch(
        "pymywatertoronto.mywatertoronto.MyWaterToronto.async_get_consumption",
        side_effect=AccountDetailsError("Error getting consumption data"),
    ):
        yield
