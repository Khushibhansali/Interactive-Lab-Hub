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

dinosaur = Image.open("dinosaur.png")  # Replace with the path to your dinosaur image
dinosaur_width, dinosaur_height = 20, 40  # Set the size of the dinosaur image
dinosaur = dinosaur.resize((dinosaur_width, dinosaur_height))
dinosaur_x = 0
dinosaur_y = height // 2
dinosaur_updated = False  # Track if the dinosaur was updated in this frame

# Set up button input
button_pin = digitalio.DigitalInOut(board.D23)
button_pin.switch_to_input(pull=digitalio.Pull.UP)

# Load the cactus image
cactus = Image.open("cactus.png")  # Replace with the path to your cactus image
cactus_width, cactus_height = 20, 40  # Set the size of the cactus image
cactus = cactus.resize((cactus_width, cactus_height))

# Set the initial position of the dot and the cactus
dot_x = 0
dot_y = height // 2
dot_updated = False  # Track if the dot was updated in this frame

cactus_x = width - cactus_width
cactus_y = height // 2

buffer = Image.new("RGB", (width, height), (0, 0, 0))
buffer_draw = ImageDraw.Draw(buffer)

background = Image.open("background.jpeg")  # Replace with the path to your background image
background = background.resize((width, height))


while True:
    # Check for button press to move the dot (ball) up
    if not button_pin.value:
        dot_y -= 10  # Adjust the speed by changing the value

    # Clear the buffer image.
    # buffer_draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    buffer_draw.rectangle((dinosaur_x, dinosaur_y, dinosaur_x + dinosaur_width, dinosaur_y + dinosaur_height), outline=0, fill=(0, 0, 0))

    #buffer_draw.rectangle((dot_x, height // 2 - 2, dot_x + 4, height // 2 + 2), outline=0, fill=(0, 0, 0))

    # Paste the background image on the buffer
    buffer.paste(background, (0, 0))

    # Update the position of the dot if necessary
    if dot_updated:
        dot_x += 1  # Adjust the speed by changing the value
        dot_updated = False

    # Ensure the dot stays within the screen width
    if dot_x >= width:
        dot_x = 0  # Reset the dot to the left edge

    if dinosaur_x >= width:
        dinosaur_x = 0  # Reset the dinosaur to the left edge

    # Move the cactus towards the dot
    cactus_x -= 1  # Adjust the speed by changing the value

    # Reset the cactus position when it goes off-screen
    if cactus_x < -cactus_width:
        cactus_x = width

    # Check for collision between the dot and the cactus
    if (
        dot_x < cactus_x + cactus_width
        and dot_x + 4 > cactus_x
        and height // 2 + 2 > cactus_y
        and height // 2 - 2 < cactus_y + cactus_height
    ):
        # Collision occurred, reset the dot to its original position
        dot_x = 0

    # Draw the dot at the updated position on the buffer
    buffer_draw.rectangle((dot_x, height // 2 - 2, dot_x + 4, height // 2 + 2), fill=(255, 255, 255))

    # Check for collision between the dinosaur and the cactus
    if (
        dinosaur_x < cactus_x + cactus_width
        and dinosaur_x + dinosaur_width > cactus_x
        and dinosaur_y + dinosaur_height > cactus_y
        and dinosaur_y < cactus_y + cactus_height
    ):
        # Collision occurred, reset the dinosaur to its original position
        dinosaur_x = 0

    # Draw the dinosaur at the updated position on the buffer
    buffer.paste(dinosaur, (dinosaur_x, dinosaur_y))

    # Paste the cactus image on the buffer
    buffer.paste(cactus, (cactus_x, cactus_y))

    # Display the buffer image on the screen.
    disp.image(buffer, rotation)
    time.sleep(0.05)  # Adjust the delay as needed
