# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
NeoSlider NeoPixel Rainbow Demo
"""
import board
from rainbowio import colorwheel
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.analoginput import AnalogInput
from adafruit_seesaw import neopixel
import time
import math

# NeoSlider Setup
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
neoslider = Seesaw(i2c, 0x30)
potentiometer = AnalogInput(neoslider, 18)
pixels = neopixel.NeoPixel(neoslider, 14, 4, pixel_order=neopixel.RGB)


def potentiometer_to_color(value):
    """Scale the potentiometer values (0-1023) to the colorwheel values (0-255)."""
    # print("Pixels:", pixels)
    return (value / 1023) * 255


# RED = (255, 0, 0)
# YELLOW = (255, 150, 0)
# GREEN = (0, 255, 0)
# CYAN = (0, 255, 255)
# BLUE = (0, 0, 255)
# PURPLE = (180, 0, 255)
while True:
    print(potentiometer.value)
    value2color = math.floor(((potentiometer.value - 32768)/(33792-32768))*255)
    print(value2color)
    if value2color < 0:
        value2color = 0 # = RED
    elif value2color > 255:
        value2color = 255 # = PURPLE
    # elif value2color >= 212:
    #     value2color = PURPLE
    # elif value2color < 212 and value2color >= 170:
    #     value2color = BLUE
    # elif value2color < 170 and value2color >= 127:
    #     value2color = CYAN
    # elif value2color < 127 and value2color >= 85:
    #     value2color = GREEN
    # elif  value2color < 85 and value2color >= 43:
    #     value2color = YELLOW
    # elif  value2color >=0 and value2color < 43:
    #     value2color = RED
    # list_values = math.round(((list(range(32768, 33792)))/33792)*255)
    time.sleep(0.5)
    # Fill the pixels a color based on the position of the potentiometer.
    pixels.fill(colorwheel(potentiometer_to_color(value2color)))