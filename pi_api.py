# from smbus2 import SMBus
from time import sleep
import logging as log

from maps import *

DELAY = 0.5


def execute_and_check_pi_command(
    command_string,
    expected,
    set_command,
    set_command_args,
    get_command,
    get_command_args,
    location,
    check_only=False,
    delay=0.1,
):
    """Execute a commmand to the pi and check that the state is set as expected
    
    Arguments:
        command_string {string} -- informatino for logging and debugging.
        expected {int} -- Expected state after setting the pi
        set_command {funcion} -- function that executes the setting of the pi
        set_command_args {tuple} -- tuple of arguments to send to the set command
        get_command {function} -- function that reads the currrent state from the pi
        get_command_args {tuple} -- tuple of arguments to send with the read command
        location {string} -- string version of the location address for debugging and logging.
    
    Keyword Arguments:
        check_only {bool} -- skip the setting and only read the stae (default: {False})
        delay {float} -- delay to send between actions (default: {0.1})
    
    Returns:
        Bool -- True if all is good, False if any OS or Assertion Errors
    """

    log.debug(f"Operation ::  {command_string}")

    if not check_only:
        try:
            set_command(*set_command_args, delay=delay)
        except OSError as e:
            log.error(f"OSError ::  {e}  ::  location  ::  {location}")

    try:
        res = get_command(*get_command_args, delay=delay)
        try:
            assert expected == res
            log.debug(f"Success  ::  {expected} == {res} ::  {expected == res}")
        except AssertionError:
            log.error(
                f"AssertionError  ::  {expected} == {res} ::  {expected == res}  ::  Location  ::  {location}"
            )
            return False
    except OSError as e:
        log.error(
            f"OSError ::  {e}  ::  location  ::  {location}  ::  Location  ::  {location}"
        )
        return False

    return True


def change_state_and_power_and_check(*args, **kwargs):

    on_off = 0
    switch = turn_power_off

    if power_on:
        on_off = 1
        switch = turn_power_on

    log.debug(
        f"INSIDE change state  ::  on_off  ::  {on_off}  ::  switch  ::  {switch}  ::  {location}"
    )

    state_res = execute_and_check_pi_command(*args, **kwargs)

    log.debug(f"state_res ::  {state_res}  :: ")

    if state_res:
        power = execute_and_check_pi_command(*args, **kwargs)
        log.debug(f"power ::  {power}")


def turn_power_on(address, register, force=None, delay=0.1):
    with SMBus(1) as bus:
        bus.write_byte_data(address, register_power_state, 1, force=force)


def turn_power_off(address, force=None, delay=0.1):
    with SMBus(1) as bus:
        bus.write_byte_data(address, register_power_state, 0, force=force)


def change_state(address, state, force=None, delay=0.1):
    try:
        with SMBus(1) as bus:
            bus.write_byte_data(address, register_tester_state, state, force=force)

    except OSError:
        return None


def get_firmware_version(address, force=None, delay=0.1):
    with SMBus(1) as bus:
        return bus.read_byte_data(address, register_firmware_version, force=force)


def get_state(address, force=None, delay=0.1):
    with SMBus(1) as bus:
        return bus.read_byte_data(address, register_tester_state, force=force)


def get_power_status(address, force=None, delay=0.1):
    with SMBus(1) as bus:
        return bus.read_byte_data(address, register_power_state, force=force)


def reset_all_to_idle(delay):
    log.debug("resetting to Idle")
    for k, v in SLAVE_ADDRESSES.items():
        change_state(v, test_state["idle"], delay=0.5)


def turn_off_all(delay):
    log.debug("Turning power off")
    for k, v in SLAVE_ADDRESSES.items():
        turn_power_off(v, delay=0.5)


def turn_on_all(delay):
    log.debug("Turning power on")
    for k, v in SLAVE_ADDRESSES.items():
        power = get_power_status(v)
        log.debug(f"Current Power  ::  {k}  ::   {power}")
        turn_power_on(v, delay=0.5)


#############################################


if __name__ == "__main__":
    # turn_on_all(0.5)
    pass
