import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import os
import random 
from datetime import datetime, timedelta, timezone 
from gpiozero import Button

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

# Function to get the country name from the background image file name
def get_country_name(filename):
    return os.path.splitext(filename)[0]

dinosaur = Image.open("dino.png")  # Replace with the path to your dinosaur image
dinosaur_width, dinosaur_height = 50, 40  # Set the size of the dinosaur image
dinosaur = dinosaur.resize((dinosaur_width, dinosaur_height))
dinosaur_x = 0
dinosaur_y = height // 2
dinosaur_updated = False  # Track if the dinosaur was updated in this frame

# Set up button input
button_pin = digitalio.DigitalInOut(board.D24)
button_pin.switch_to_input(pull=digitalio.Pull.UP)
button = Button(24)

# Load the cactus image
cactus = Image.open("cactus.png")  # Replace with the path to your cactus image
cactus_width, cactus_height = 20, 40  # Set the size of the cactus image
cactus = cactus.resize((cactus_width, cactus_height))

cactus_x = width - cactus_width
cactus_y = height // 2

buffer = Image.new("RGB", (width, height), (0, 0, 0))
buffer_draw = ImageDraw.Draw(buffer)

background = Image.open("TimeZones/1.jpeg")  # Replace with the path to your background image
background = background.resize((width, height))

background_folder = "TimeZones"
background_images = [f for f in os.listdir(background_folder) if f.endswith(".jpeg") or f.endswith(".png")]
background_images.sort()  # Ensure images are sorted alphabetically
background_index = 0  # Initialize the index for the current background image
cactus_counter = 0  # Initialize a counter for the cactuses

# Load the cactus image
cactus = Image.open("cactus.png")  # Replace with the path to your cactus image
cactus_width, cactus_height = 20, 40  # Set the size of the cactus image
cactus = cactus.resize((cactus_width, cactus_height))

# Set the initial position of the dot and the cactus
cactus_x = width - cactus_width
cactus_y = height // 2

# Store the original position of the cactus
original_cactus_x = width - cactus_width
cactus_x = original_cactus_x
cactus_y = height // 2

jump_count = 0
collision = False
gravity = 1

while True:
    if button.is_pressed:
        # Button is pressed, move the dinosaur up 
        dinosaur_y -= 14  # Adjust the value to control the speed of the dinosaur's upward movement
    else:
        # Apply gravity to the dinosaur's position to make it descend slowly
        dinosaur_y += gravity
        if dinosaur_y > height // 2:
            dinosaur_y = height // 2  # Ensure the dinosaur doesn't fall below its initial position
    
    if cactus_counter >=3 and cactus_counter % 3 == 0:
        #Change the background image
        background_index = (background_index + 1) % len(background_images)
        background = Image.open(os.path.join(background_folder, background_images[background_index]))
        background = background.resize((width, height))
        cactus_counter = 0 
       
    # Update the position of the cactus based on its distance from the dinosaur
    cactus_x -= 1  # Move the cactus left
    if cactus_x < -cactus_width:
        cactus_x = width  # Reset the cactus to the right of the screent
        cactus_counter +=1
    
    if (
        dinosaur_x < cactus_x + cactus_width
        and dinosaur_x + dinosaur_width > cactus_x
        and cactus_y + cactus_height > dinosaur_y  # Check if the cactus is below the dinosaur
        and dinosaur_y + dinosaur_height > cactus_y  # Check if the dinosaur is below the cactus
        and cactus_x > dinosaur_x  # Check if the cactus is ahead of the dinosaur
    ):
        # Collision occurred, reset the cactus to its original position
        cactus_x = original_cactus_x
        # Reset the collision flag
        collision = True
        # Reset the jump count to 0
        jump_count = 0
    else:
        collision = False


    if not collision :
        # Increment the jump count when the cactus is ahead of the dinosaur and the dinosaur is above the threshold
        if cactus_x <= dinosaur_x and dinosaur_y <= cactus_y:
            jump_count += 1
    

    # Determine if you should display the black screen with information
    if jump_count == 0 and cactus_counter > 0:

        dict = {
            "1":"\nPrecambrian Era: About\n 4.5 billion years ago\n it created multicelled \nlife-forms.", 
            "2":"\nPaleozic Era: About \n251.9 million years ago. \nFish diversified, shallow \nseas formed, and collisions \nformed the Appalachian \nMountains.", 
            "3":"\nMesozoic Era: About \n66 million years ago.\n Pangaea separated, and dinosaurs,\ncrocodiles, and pterosaurs ruled \nthe land and air."
        }

        info_text = "You lost in the " + dict[str(background_index+1)]
        draw.rectangle((0, 0, width, height), outline=0, fill=400)
        draw.text((10, 10), info_text, font=font, fill=(255, 255, 255))

    elif jump_count >=441 or jump_count//21 == 21 :
        
        congrats_message = "Congrats! You won the\n game! Your dinosaur reached\n modern day new york.\n Year 2023."
        draw.rectangle((0, 0, width, height), outline=0, fill=400)
        draw.text((10, 10), congrats_message, font=font, fill=(255, 255, 255))

    else:
        # Paste the background image onto the screen
        image.paste(background, (0, 0))

        # Draw the dinosaur at the updated position
        image.paste(dinosaur, (dinosaur_x, dinosaur_y))

        # Paste the cactus image on the screen
        image.paste(cactus, (cactus_x, cactus_y))

        # Display the jump count on the screen
        text = f"Jumps: {jump_count//21}"
        draw.text((10, 10), text, font=font, fill=(255, 255, 255))

    # Display image.
    disp.image(image, rotation)
    time.sleep(0.03)  # Adjust the delay as needed
