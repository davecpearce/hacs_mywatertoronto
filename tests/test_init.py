"""Test MyWaterToronto setup process."""
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.mywatertoronto import (
    MyWaterTorontoDataUpdateCoordinator,
    async_reload_entry,
    async_setup_entry,
    async_unload_entry,
)
from custom_components.mywatertoronto.const import DATA_COORDINATOR, DOMAIN

from .const import MOCK_CONFIG

pytestmark = pytest.mark.asyncio


async def test_setup_unload_and_reload_entry(
    hass, bypass_get_data
):  # pylint: disable=unused-argument
    """Test entry setup and unload."""
    # Create a mock entry so we don't have to go through config flow
    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")

    # Set up the entry and assert that the values set during setup are where we expect
    # them to be. Because we have patched the BlueprintDataUpdateCoordinator.async_get_data
    # call, no code from custom_components/integration_blueprint/api.py actually runs.
    assert await async_setup_entry(hass, config_entry)
    assert DOMAIN in hass.data and config_entry.entry_id in hass.data[DOMAIN]
    assert isinstance(
        hass.data[DOMAIN][config_entry.entry_id][DATA_COORDINATOR],
        MyWaterTorontoDataUpdateCoordinator,
    )

    # Reload the entry and assert that the data from above is still there
    assert await async_reload_entry(hass, config_entry) is None
    assert DOMAIN in hass.data and config_entry.entry_id in hass.data[DOMAIN]
    assert isinstance(
        hass.data[DOMAIN][config_entry.entry_id][DATA_COORDINATOR],
        MyWaterTorontoDataUpdateCoordinator,
    )

    # Unload the entry and verify that the data has been removed
    assert await async_unload_entry(hass, config_entry)
    assert config_entry.entry_id not in hass.data[DOMAIN]
