import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789


# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# Define different scenes and fish for different times of day
scenes = {
    "morning": "./Images/morning.jpeg",
    "afternoon": "./Images/afternoon.jpeg",
    "night": "./Images/night.jpeg",
}

while True:
    current_time = time.strftime("%H:%M")

    # Determine the time of day based on the current hour
    current_hour = int(time.strftime("%H"))
    if 6 <= current_hour < 12:
        time_of_day = "morning"
    elif 12 <= current_hour < 18:
        time_of_day = "afternoon"
    else:
        time_of_day = "night"

    # Load the appropriate scenery and fish image based on the time of day
    scenery_and_fish_image = Image.open(scenes[time_of_day])

    # Resize the image to match the display's dimensions (135x240)
    scenery_and_fish_image = scenery_and_fish_image.resize((135, 240))

    # Create an image to overlay the text on
    image_with_text = scenery_and_fish_image.copy()
    draw = ImageDraw.Draw(image_with_text)

    # Draw the current time on the overlay
    draw.text((5, 5), "Time:", font=font, fill=(255, 255, 255))
    draw.text((10, 40), current_time, font=font, fill=(255, 255, 255))

    # Display the image with the overlay
    disp.image(image_with_text)

    # Update the display every minute
    time.sleep(60)
