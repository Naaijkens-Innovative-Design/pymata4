"""
 Copyright (c) 2020 Alan Yorinks All rights reserved.

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

import sys
import time
from pymata4 import pymata4

"""
Setup a pin for digital output and output
and toggle the pin using the digital_pin_output as opposed to digital_output
pin mode.
"""

def eeprom_callback(data):
    """
    A callback function to report raw data changes.

    :param data: [pin, current reported value, pin_mode, timestamp]
    """
    print('read eeprom callback:')
    print(data) 

def isotest_callback(data):
    """
    A callback function to report raw data changes.

    :param data: [pin, current reported value, pin_mode, timestamp]
    """
    print('read isotest callback:')
    print(data) 

def blink(my_board, pin):
    """
    This function will to toggle a digital pin.

    :param my_board: an PymataExpress instance
    :param pin: pin to be controlled
    """

    # set the pin mode
    my_board.set_pin_mode_digital_output(pin)

    print(my_board.get_firmware_version())
    print(f'Protocol Version: {my_board.get_protocol_version()}')
    print(my_board.get_pymata_version())

    # toggle the pin 4 times and exit
    for x in range(1):
        print('ON')
        my_board.digital_pin_write(pin, 1)
        time.sleep(1)
        print('OFF')
        my_board.digital_pin_write(pin, 0)

board = pymata4.Pymata4(com_port='COM10',baud_rate=57600)

# test eeprom
print('write eeprom')
board.eeprom_write(300, [56, 65, 78, 98])
time.sleep(5);
print('read eeprom')
board.eeprom_read(300, 4, eeprom_callback)
time.sleep(5);

# test isotest
print('start isotest type 1')
board.isotest_start(1)
time.sleep(10);
print('read isotest')
board.isotest_read(isotest_callback)

# print('start isotest type 2')
# board.isotest_start(2)
# time.sleep(10);
# print('read isotest')
# board.isotest_read(isotest_callback)

while True:
    try:
        print("led on")
        board.digital_pin_write(13, 1)
        time.sleep(1)
        print("led off")
        board.digital_pin_write(13, 0)
        time.sleep(1)
    except KeyboardInterrupt:
        board.shutdown()
        sys.exit(0)
