"""Sensor for displaying the number of result from MyWaterToronto."""
from datetime import timedelta
import logging
from typing import Any, Final

from pymywatertoronto.enums import (
    ConsumptionBuckets,
)
from pymywatertoronto.const import (
    KEY_ADDRESS,
    KEY_METER_FIRST_READ_DATE,
    KEY_METER_LAST_READ_DATE,
    KEY_METER_LIST,
    KEY_METER_MANUFACTURER_TYPE,
    KEY_METER_NUMBER,
    KEY_PREMISE_ID,
    KEY_PREMISE_LIST,
)

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import (
    HomeAssistant,
    callback
)
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from homeassistant.const import (
    VOLUME_CUBIC_METERS,
)

from .const import (
    DATA_COORDINATOR,
    DOMAIN
)
from .coordinator import MyWaterTorontoDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=1)

SENSORS: Final[tuple[SensorEntityDescription, ...]] = (
    SensorEntityDescription(
        key=KEY_METER_LAST_READ_DATE,
        name="Last Read Date",
        icon="mdi:update",
        #native_unit_of_measurement=SensorDeviceClass.TIMESTAMP,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key=KEY_METER_FIRST_READ_DATE,
        name="First Read Date",
        icon="mdi:update",
        #native_unit_of_measurement=SensorDeviceClass..TIMESTAMP,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key=ConsumptionBuckets.TOTAL_USAGE.value,
        name="Total Usage",
        icon="mdi:gauge",
        native_unit_of_measurement=VOLUME_CUBIC_METERS,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key=ConsumptionBuckets.TODAY_USAGE.value,
        name="Daily Usage",
        icon="mdi:gauge",
        native_unit_of_measurement=VOLUME_CUBIC_METERS,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key=ConsumptionBuckets.WEEK_TO_DATE_USAGE.value,
        name="Week To Date Usage",
        icon="mdi:gauge",
        native_unit_of_measurement=VOLUME_CUBIC_METERS,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key=ConsumptionBuckets.MONTH_TO_DATE_USAGE.value,
        name="Month To Date Usage",
        icon="mdi:gauge",
        native_unit_of_measurement=VOLUME_CUBIC_METERS,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key=ConsumptionBuckets.YEAR_TO_DATE_USAGE.value,
        name="Year To Date Usage",
        icon="mdi:gauge",
        native_unit_of_measurement=VOLUME_CUBIC_METERS,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the MyWaterToronto sensors."""

    coordinator: MyWaterTorontoDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]

    entities = []
    account_details = coordinator.account_details

    if account_details is not None:
        for premise in account_details[KEY_PREMISE_LIST]:
            address = premise[KEY_ADDRESS]
            _LOGGER.debug("Premise found: %s", address)

            for meter in premise[KEY_METER_LIST]:
                meter_number = meter[KEY_METER_NUMBER]
                _LOGGER.debug("Meter %s found at %s", meter_number, address)

                for description in SENSORS:
                    entities.append(MyWaterTorontoSensor(coordinator, entry, description, premise, meter))

    async_add_entities(entities)

class MyWaterTorontoSensor(CoordinatorEntity[MyWaterTorontoDataUpdateCoordinator], SensorEntity):
    """Representation of the MyWaterToronto sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MyWaterTorontoDataUpdateCoordinator,
        entry: ConfigEntry,
        description: SensorEntityDescription,
        premise: dict[str, Any],
        meter: dict[str, Any],
    ) -> None:
        """Initialize the MyWaterToronto Meter sensor."""

        super().__init__(coordinator)

        self.entity_description = description
        self.entry = entry

        self.data_type = description.key
        self._attr_unique_id = f"{entry.unique_id}_{premise[KEY_PREMISE_ID]}_{meter[KEY_METER_NUMBER]}_{description.key}"

        self.premise = premise
        self.meter = meter
        self._attr_native_value = None

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return {
            "name": self.entry.title,
            "manufacturer": self.meter[KEY_METER_MANUFACTURER_TYPE],
            "identifiers": {(DOMAIN, str(self.meter[KEY_METER_NUMBER]))},
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""

        _LOGGER.debug("_handle_coordinator_update: %s", self.data_type)

        meter_consumption = self.coordinator.data[KEY_PREMISE_LIST][self.premise[KEY_PREMISE_ID]][KEY_METER_LIST][self.meter[KEY_METER_NUMBER]]

        if self.data_type == KEY_METER_FIRST_READ_DATE:
            self._attr_native_value = meter_consumption[KEY_METER_FIRST_READ_DATE]
        elif self.data_type == KEY_METER_LAST_READ_DATE:
            self._attr_native_value = meter_consumption[KEY_METER_LAST_READ_DATE]
        else:
            self._attr_native_value = meter_consumption["consumption_data"][self.data_type]["consumption"]

        super()._handle_coordinator_update()

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""

        _LOGGER.debug("async_added_to_hass: %s", self.data_type)

        await super().async_added_to_hass()
        self._handle_coordinator_update()