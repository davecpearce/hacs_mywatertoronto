"""Test sensor for MyWaterToronto integration."""
from unittest.mock import patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.mywatertoronto.const import DOMAIN
from homeassistant.components.sensor import ENTITY_ID_FORMAT
from homeassistant.config_entries import ConfigEntryState
from homeassistant.util import slugify

from .const import MOCK_CONFIG, TEST_TITLE, TEST_UNIQUE_ID

pytestmark = pytest.mark.asyncio


def generate_entity_id(
    name: str | None,
) -> str:
    """Generate an entity ID based on given name."""

    return ENTITY_ID_FORMAT.format(slugify(f"{TEST_TITLE} {name}"))


async def test_sensor(hass, account_details, consumption):
    """Test sensor."""
    with patch(
        "pymywatertoronto.mywatertoronto.MyWaterToronto.async_get_account_details",
        return_value=account_details,
    ), patch(
        "pymywatertoronto.mywatertoronto.MyWaterToronto.async_get_consumption",
        return_value=consumption,
    ):

        config_entry = MockConfigEntry(
            domain=DOMAIN, title=TEST_TITLE, data=MOCK_CONFIG, unique_id=TEST_UNIQUE_ID
        )

        config_entry.add_to_hass(hass)
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

        assert config_entry.state == ConfigEntryState.LOADED

        # Test First Read Date sensor
        name_frd = "First Read Date"
        sensor_frd = generate_entity_id(name_frd)
        state_frd = hass.states.get(sensor_frd)

        assert state_frd.state == "2019-01-01T00:00:00"
        assert state_frd.attributes.get("friendly_name") == f"{TEST_TITLE} {name_frd}"

        # Test Last Read Date sensor
        name_lrd = "Last Read Date"
        sensor_lrd = generate_entity_id(name_lrd)
        state_lrd = hass.states.get(sensor_lrd)

        assert state_lrd.state == "2019-12-31T00:00:00"
        assert state_lrd.attributes.get("friendly_name") == f"{TEST_TITLE} {name_lrd}"

        # Test Total Usage sensor
        name_tu = "Total Usage"
        sensor_tu = generate_entity_id(name_tu)
        state_tu = hass.states.get(sensor_tu)

        assert state_tu.state == "500.5"
        assert state_tu.attributes.get("friendly_name") == f"{TEST_TITLE} {name_tu}"

        # Test Daily Usage sensor
        name_du = "Daily Usage"
        sensor_du = generate_entity_id(name_du)
        state_du = hass.states.get(sensor_du)

        assert state_du.state == "0.5"
        assert state_du.attributes.get("friendly_name") == f"{TEST_TITLE} {name_du}"

        # Test Week To Date Usage sensor
        name_wtdu = "Week To Date Usage"
        sensor_wtdu = generate_entity_id(name_wtdu)
        state_wtdu = hass.states.get(sensor_wtdu)

        assert state_wtdu.state == "3.5"
        assert state_wtdu.attributes.get("friendly_name") == f"{TEST_TITLE} {name_wtdu}"

        # Test Month To Date Usage sensor
        name_mtdu = "Month To Date Usage"
        sensor_mtdu = generate_entity_id(name_mtdu)
        state_mtdu = hass.states.get(sensor_mtdu)

        assert state_mtdu.state == "8.5"
        assert state_mtdu.attributes.get("friendly_name") == f"{TEST_TITLE} {name_mtdu}"

        # Test Year To Date Usage sensor
        name_ytdu = "Year To Date Usage"
        sensor_ytdu = generate_entity_id(name_ytdu)
        state_ytdu = hass.states.get(sensor_ytdu)

        assert state_ytdu.state == "123.5"
        assert state_ytdu.attributes.get("friendly_name") == f"{TEST_TITLE} {name_ytdu}"
