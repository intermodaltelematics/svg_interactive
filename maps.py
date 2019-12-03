i2c_bus = 0x01  # I2C bus to the board
i2c_firmware_address = 0x1  # Slave Address of the Arduino Board
i2c_flags = 0  # no flags

############# REGISTERS #################
# R/W - register of the relay that can turn things on and off
register_power_state = 0x01
# R/W - 0x01 - Led Blue / 0x02 - Led Red  /  0x03 - Led Green
register_tester_state = 0x02
# W - accepts 3 bytes (RGB) Custom colours - red (0-255), green(0-255),  blue(0-255) Decimal
register_set_led_colour = 0x03
# R - uint8_t milli amperes, something greaqter than ZERO
register_hct_power_consumption = 0x04
# Get Fw version
register_firmware_version = 0x05

############# OPTIONS ###############
IGNORE_LOCATIONS_IN_TESTS = ["D5"]
#
test_state = {
    "idle": 0x00,  # blue solid
    "assign": 0x01,  # blue blinky 1 Hz - fast
    "progress": 0x02,  # yellow
    "pass": 0x03,  # green
    "fail": 0x04,  # red
    "error": 0x05,
}

inverse_test_state = {
    0x00: "idle",  # blue solid
    0x01: "assign",  # blue blinky 1 Hz - fast
    0x02: "progress",  # yellow
    0x03: "pass",  # green
    0x04: "fail",  # red
    0x05: "error",
}

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

COLOUR_MAP = {
    "p1": Qt.cyan,
    "p2": Qt.red,
    "p3": Qt.green,
    "p4": Qt.red,
    "p5": Qt.green,
    "default": Qt.blue,
}

STATES = {
    "p1": "p1 state changed",
    "p2": "p2 state changed",
    "p3": "p3 state changed",
    "p4": "p4 state changed",
    "p5": "p5 state changed",
}


SLAVE_ADDRESSES = {
    "A1": 0x01,
    "A2": 0x02,
    "A3": 0x03,
    "A4": 0x04,
    "A5": 0x05,
    "B1": 0x06,
    "B2": 0x07,
    "B3": 0x08,
    "B4": 0x09,
    "B5": 0x0A,
    "C1": 0x0B,
    "C2": 0x0C,
    "C3": 0x0D,
    "C4": 0x0E,
    "C5": 0x0F,
    "D1": 0x10,
    "D2": 0x11,
    "D3": 0x12,
    "D4": 0x13,
    "D5": 0x14,
}
