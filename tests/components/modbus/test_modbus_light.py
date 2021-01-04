"""The tests for the Modbus light component."""
from datetime import timedelta

import pytest

from homeassistant.components.light import DOMAIN as LIGHT_DOMAIN
from homeassistant.components.modbus.const import (
    CALL_TYPE_COIL,
    CALL_TYPE_REGISTER_HOLDING,
    CONF_COILS,
    CONF_REGISTER,
    CONF_REGISTERS,
)
from homeassistant.const import (
    CONF_COMMAND_OFF,
    CONF_COMMAND_ON,
    CONF_NAME,
    CONF_SLAVE,
    STATE_OFF,
    STATE_ON,
)

from .conftest import run_base_read_test, setup_base_test


@pytest.mark.parametrize(
    "regs,expected",
    [
        (
            [0x00],
            STATE_OFF,
        ),
        (
            [0x80],
            STATE_OFF,
        ),
        (
            [0xFE],
            STATE_OFF,
        ),
        (
            [0xFF],
            STATE_ON,
        ),
        (
            [0x01],
            STATE_ON,
        ),
    ],
)
async def test_coil_light(hass, mock_hub, regs, expected):
    """Run test for given config."""
    light_name = "modbus_test_light"
    scan_interval = 5
    entity_id, now, device = await setup_base_test(
        light_name,
        hass,
        mock_hub,
        {
            CONF_COILS: [
                {CONF_NAME: light_name, CALL_TYPE_COIL: 1234, CONF_SLAVE: 1},
            ]
        },
        LIGHT_DOMAIN,
        scan_interval,
    )

    await run_base_read_test(
        entity_id,
        hass,
        mock_hub,
        CALL_TYPE_COIL,
        regs,
        expected,
        now + timedelta(seconds=scan_interval + 1),
    )


@pytest.mark.parametrize(
    "regs,expected",
    [
        (
            [0x00],
            STATE_OFF,
        ),
        (
            [0x80],
            STATE_OFF,
        ),
        (
            [0xFE],
            STATE_OFF,
        ),
        (
            [0xFF],
            STATE_OFF,
        ),
        (
            [0x01],
            STATE_ON,
        ),
    ],
)
async def test_register_light(hass, mock_hub, regs, expected):
    """Run test for given config."""
    light_name = "modbus_test_light"
    scan_interval = 5
    entity_id, now, device = await setup_base_test(
        light_name,
        hass,
        mock_hub,
        {
            CONF_REGISTERS: [
                {
                    CONF_NAME: light_name,
                    CONF_REGISTER: 1234,
                    CONF_SLAVE: 1,
                    CONF_COMMAND_OFF: 0x00,
                    CONF_COMMAND_ON: 0x01,
                },
            ]
        },
        LIGHT_DOMAIN,
        scan_interval,
    )

    await run_base_read_test(
        entity_id,
        hass,
        mock_hub,
        CALL_TYPE_REGISTER_HOLDING,
        regs,
        expected,
        now + timedelta(seconds=scan_interval + 1),
    )
