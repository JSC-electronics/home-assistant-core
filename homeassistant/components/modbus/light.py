"""Support for Modbus lights."""
from datetime import timedelta
import logging
from typing import Any, Dict, Optional

from homeassistant.components.light import LightEntity
from homeassistant.const import CONF_LIGHTS, CONF_NAME, CONF_SCAN_INTERVAL, STATE_ON
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
    HomeAssistantType,
)

from . import ModbusHub
from .const import (
    CALL_TYPE_COIL,
    CALL_TYPE_REGISTER_HOLDING,
    CONF_REGISTER,
    CONF_REGISTER_TYPE,
    MODBUS_DOMAIN,
)
from .switch import ModbusCoilSwitch, ModbusRegisterSwitch

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass: HomeAssistantType,
    config: ConfigType,
    async_add_entities,
    discovery_info: Optional[DiscoveryInfoType] = None,
):
    """Read configuration and create Modbus light."""
    if discovery_info is None:
        return

    lights = []
    for light in discovery_info[CONF_LIGHTS]:
        hub: ModbusHub = hass.data[MODBUS_DOMAIN][discovery_info[CONF_NAME]]

        if CALL_TYPE_COIL in light:
            lights.append(ModbusCoilLight(hub, light))

        if CONF_REGISTER in light:
            lights.append(ModbusRegisterLight(hub, light))

    async_add_entities(lights)


class ModbusCoilLight(ModbusCoilSwitch, LightEntity):
    """Representation of a Modbus coil light."""

    def __init__(self, hub: ModbusHub, config: Dict[str, Any]):
        """Initialize the coil fan."""
        super().__init__(hub, config)
        self._scan_interval = timedelta(seconds=config[CONF_SCAN_INTERVAL])

    async def async_added_to_hass(self):
        """Handle entity which will be added."""
        state = await self.async_get_last_state()
        if not state:
            return
        self._is_on = state.state == STATE_ON

        async_track_time_interval(
            self.hass, lambda arg: self._update(), self._scan_interval
        )

    @property
    def should_poll(self):
        """Return True if entity has to be polled for state.

        False if entity pushes its state to HA.
        """

        # Handle polling directly in this entity
        return False

    def turn_on(self, **kwargs):
        """Turn on the light."""
        super().turn_on(**kwargs)
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn off the light."""
        super().turn_off(**kwargs)
        self.schedule_update_ha_state()

    def _update(self):
        """Update the state of the light."""
        super().update()
        self.schedule_update_ha_state()


class ModbusRegisterLight(ModbusRegisterSwitch, LightEntity):
    """Representation of a Modbus register light."""

    def __init__(self, hub: ModbusHub, config: Dict[str, Any]):
        """Initialize the register fan."""
        config[CONF_REGISTER_TYPE] = CALL_TYPE_REGISTER_HOLDING
        super().__init__(hub, config)
        self._scan_interval = timedelta(seconds=config[CONF_SCAN_INTERVAL])

    async def async_added_to_hass(self):
        """Handle entity which will be added."""
        state = await self.async_get_last_state()
        if not state:
            return
        self._is_on = state.state == STATE_ON

        async_track_time_interval(
            self.hass, lambda arg: self._update(), self._scan_interval
        )

    @property
    def should_poll(self):
        """Return True if entity has to be polled for state.

        False if entity pushes its state to HA.
        """

        # Handle polling directly in this entity
        return False

    def turn_on(self, **kwargs):
        """Turn on the light."""
        super().turn_on(**kwargs)
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn off the light."""
        super().turn_off(**kwargs)
        self.schedule_update_ha_state()

    def _update(self):
        """Update the state of the light."""
        super().update()
        self.schedule_update_ha_state()
