"""Binary sensor platform for Waterkotte Heatpump."""
import logging
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.helpers.typing import ConfigType, HomeAssistantType
# from homeassistant.const import ATTR_FRIENDLY_NAME

# from .const import DOMAIN
from pywaterkotte.ecotouch import EcotouchTag
from .entity import WaterkotteHeatpumpEntity

# from pywaterkotte.ecotouch import EcotouchTag
from .const import DOMAIN  # , NAME, CONF_FW, CONF_BIOS, CONF_IP

_LOGGER = logging.getLogger(__name__)


# Sensor types are defined as:
#   variable -> [0]title, [1] EcoTouchTag, [2]device_class, [3]units, [4]icon, [5]enabled_by_default, [6]options, [7]entity_category #pylint: disable=line-too-long
SENSOR_TYPES = {
    "state_sourcepump": [
        "Sourcepump",
        EcotouchTag.STATE_SOURCEPUMP,
        BinarySensorDeviceClass.RUNNING,
        None,
        None,
        True,
        None,
        None,
    ],
    "state_heatingpump": [
        "Heatingpump",
        EcotouchTag.STATE_HEATINGPUMP,
        BinarySensorDeviceClass.RUNNING,
        None,
        None,
        True,
        None,
        None,
    ],
    "state_evd": [
        "EVD",
        EcotouchTag.STATE_EVD,
        BinarySensorDeviceClass.RUNNING,
        None,
        None,
        False,
        None,
        None,
    ],
    "state_compressor": [
        "Compressor",
        EcotouchTag.STATE_COMPRESSOR,
        BinarySensorDeviceClass.RUNNING,
        None,
        None,
        False,
        None,
        None,
    ],
    "state_compressor2": [
        "Compressor2",
        EcotouchTag.STATE_COMPRESSOR2,
        BinarySensorDeviceClass.RUNNING,
        None,
        None,
        False,
        None,
        None,
    ],
    "state_external_heater": [
        "External Heater",
        EcotouchTag.STATE_EXTERNAL_HEATER,
        BinarySensorDeviceClass.RUNNING,
        None,
        None,
        False,
        None,
        None,
    ],
    "state_alarm": [
        "Alarm",
        EcotouchTag.STATE_ALARM,
        BinarySensorDeviceClass.RUNNING,
        None,
        None,
        False,
        None,
        None,
    ],
    "state_cooling": [
        "Cooling",
        EcotouchTag.STATE_COOLING,
        BinarySensorDeviceClass.RUNNING,
        None,
        None,
        False,
        None,
        None,
    ],
    "state_water": [
        "Water",
        EcotouchTag.STATE_WATER,
        BinarySensorDeviceClass.RUNNING,
        None,
        None,
        False,
        None,
        None,
    ],
    "state_pool": [
        "Pool",
        EcotouchTag.STATE_POOL,
        BinarySensorDeviceClass.RUNNING,
        None,
        None,
        True,
        None,
        None,
    ],
    "state_solar": [
        "Solar",
        EcotouchTag.STATE_SOLAR,
        BinarySensorDeviceClass.RUNNING,
        None,
        "mdi:weather-partly-cloudy",
        False,
        None,
        None,
    ],
    "state_cooling4way": [
        "Cooling4way",
        EcotouchTag.STATE_COOLING4WAY,
        BinarySensorDeviceClass.RUNNING,
        None,
        None,
        False,
        None,
        None,
    ],
    "heatingmode_mixing1": [
        "Heating mode Mixing 1",
        EcotouchTag.HEATINGMODE_MIXING1,
        BinarySensorDeviceClass.RUNNING,
        None,
        None,
        False,
        None,
        None,
    ],
    "heatingmode_mixing2": [
        "Heating mode Mixing 2",
        EcotouchTag.HEATINGMODE_MIXING2,
        BinarySensorDeviceClass.RUNNING,
        None,
        None,
        False,
        None,
        None,
    ],
    "heatingmode_mixing3": [
        "Heating mode Mixing 3",
        EcotouchTag.HEATINGMODE_MIXING3,
        BinarySensorDeviceClass.RUNNING,
        None,
        None,
        False,
        None,
        None,
    ],
    # "holiday_enabled": [
    #     "Holiday Mode",
    #     EcotouchTag.HOLIDAY_ENABLED,
    #     BinarySensorDeviceClass.RUNNING,
    #     None,
    #     None,
    #     True,
    #     None,
    #     None,
    # ],


}

# async def async_setup_entry(hass, entry, async_add_devices):
#     """Setup binary_sensor platform."""
#     coordinator = hass.data[DOMAIN][entry.entry_id]
#     async_add_devices([WaterkotteHeatpumpBinarySensor(coordinator, entry)])


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigType, async_add_devices) -> None:
    """Set up the Waterkotte sensor platform."""
    # hass_data = hass.data[DOMAIN][entry.entry_id]
    _LOGGER.debug("Sensor async_setup_entry")
    coordinator = hass.data[DOMAIN][entry.entry_id]
    # async_add_devices([WaterkotteHeatpumpSensor(entry, coordinator, "temperature_condensation")])
    # async_add_devices([WaterkotteHeatpumpSensor(entry, coordinator, "temperature_evaporation")])
    async_add_devices([WaterkotteHeatpumpBinarySensor(entry, coordinator, sensor_type)
                       for sensor_type in SENSOR_TYPES])


class WaterkotteHeatpumpBinarySensor(WaterkotteHeatpumpEntity, BinarySensorEntity):
    """waterkotte_heatpump binary_sensor class."""
    # _attr_has_entity_name = True

    def __init__(self, entry, hass_data, sensor_type):  # pylint: disable=unused-argument
        """Initialize the sensor."""
        self._coordinator = hass_data

        self._type = sensor_type
        # self._name = f"{SENSOR_TYPES[self._type][0]} {DOMAIN}"
        self._name = f"{SENSOR_TYPES[self._type][0]}"
        # self._unique_id = f"{SENSOR_TYPES[self._type][0]}_{DOMAIN}"
        # self._unique_id = f"{self._type}_{DOMAIN}"
        self._unique_id = self._type
        self._entry_data = entry.data
        self._device_id = entry.entry_id
        hass_data.alltags.update({self._unique_id: SENSOR_TYPES[self._type][1]})
        super().__init__(hass_data, entry)
        # self._attr_capability_attributes[ATTR_FRIENDLY_NAME] = self._name

    @property
    def tag(self):
        """Return a tag to use for this entity."""
        return SENSOR_TYPES[self._type][1]

    @ property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary_sensor is on."""
        # return self.coordinator.data.get("title", "") == "foo"
        try:
            sensor = SENSOR_TYPES[self._type]
            value = self._coordinator.data[sensor[1]]["value"]
            if value is None or value == "":
                value = None
        except KeyError:
            value = None
            #print(value)
        except TypeError:
            return None
        return value

    @ property
    def icon(self):
        """Return the icon of the sensor."""
        if SENSOR_TYPES[self._type][4] is None:
            sensor = SENSOR_TYPES[self._type]
            try:
                if self._type == "holiday_enabled" and 'value' in self._coordinator.data[sensor[1]]:
                    if self._coordinator.data[sensor[1]]["value"] is True:
                        return "mdi:calendar-check"
                    else:
                        return "mdi:calendar-blank"
                else:
                    return None
            except KeyError:
                print(f"KeyError in Binary_sensor.icon: should have value? data:{self._coordinator.data[sensor[1]]}")  # pylint: disable=line-too-long
        return SENSOR_TYPES[self._type][4]
        # return ICON

    @ property
    def device_class(self):
        """Return the device class of the sensor."""
        return SENSOR_TYPES[self._type][2]

    @ property
    def entity_registry_enabled_default(self):
        """Return the entity_registry_enabled_default of the sensor."""
        return SENSOR_TYPES[self._type][5]

    @ property
    def entity_category(self):
        """Return the unit of measurement."""
        try:
            return SENSOR_TYPES[self._type][7]
        except IndexError:
            return None

    @ property
    def unique_id(self):
        """Return the unique of the sensor."""
        return self._unique_id
