# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
from __future__ import print_function, division
import board
from adafruit_apds9960.apds9960 import APDS9960
import busio
import qwiic_oled_display
import time
from time import sleep
import math
import qwiic_proximity
from adafruit_apds9960.apds9960 import APDS9960
from adafruit_apds9960 import colorutility

i2c = board.I2C()
apds = APDS9960(i2c)
apds.enable_color = True
apds.enable_proximity = True
apds.enable_gesture = True

while True:
    # create some variables to store the color data in

    # wait for color data to be ready
    while not apds.color_data_ready:
        time.sleep(0.005)

    # get the data and print the different channels
    r, g, b, c = apds.color_data
    print("red: ", r)
    print("green: ", g)
    print("blue: ", b)
    print("clear: ", c)

    print("color temp {}".format(colorutility.calculate_color_temperature(r, g, b)))
    print("light lux {}".format(colorutility.calculate_lux(r, g, b)))
    time.sleep(0.5)



########### Initialize OLED Screen ###################################################

myOLED = qwiic_oled_display.QwiicOledDisplay()

if not myOLED.connected:
    print("The Qwiic OLED Display isn't connected to the system. Please check your connection", \
        file=sys.stderr)
    

myOLED.begin()
#  clear(ALL) will clear out the OLED's graphic memory.
#  clear(PAGE) will clear the Arduino's display buffer.
myOLED.clear(myOLED.ALL)  #  Clear the display's memory (gets rid of artifacts)
#  To actually draw anything on the display, you must call the
#  display() function.
myOLED.display()
time.sleep(1)

myOLED.clear(myOLED.PAGE)
###########################################################################################################

# Initialize Variables
p1_score = 0
p2_score = 0
seconds = 30    # Duration of 2-player game

def oled_update_score(p1_score, p2_score, countdown):
    
    myOLED.clear(myOLED.PAGE)            # Clear the display
    
    myOLED.set_cursor(32, 24)           # Set cursor to bottom-left
    myOLED.set_font_type(0)             # Smallest font
    myOLED.print("Timer: " + str(countdown))          
    
    if countdown == 0:
        # Player 1 Wins
        if p1_score > p2_score:
            myOLED.set_cursor(24, 24)        
            myOLED.set_font_type(0)         
            myOLED.print("Player 1 Wins!")  
        # Player 2 Wins
        if p1_score < p2_score:
            myOLED.set_cursor(24, 24)        
            myOLED.set_font_type(0)         
            myOLED.print("Player 2 Wins!") 
        # It's a tie!
        if p1_score == p2_score:
            myOLED.set_cursor(32, 24)        
            myOLED.set_font_type(0)         
            myOLED.print("It's a tie!")     

    myOLED.set_cursor(0, 0)        # Set cursor to top-left
    myOLED.set_font_type(0)         # Smallest font
    myOLED.print("P1: ")          # Print "P1"
    myOLED.set_font_type(2)         # 7-segment font
    myOLED.print("%.3d" % p1_score)

    # myOLED.set_cursor(0, 16)       # Set cursor to top-middle-left
    # myOLED.set_font_type(0)         # Repeat
    # myOLED.print("P2: ")
    # myOLED.set_font_type(2)

    # myOLED.print("%.3d" % hoops)
    myOLED.set_cursor(64, 0)
    myOLED.set_font_type(0)
    myOLED.print("P2: ")
    myOLED.set_font_type(2)
    myOLED.print("%.3d" % p2_score)

    myOLED.display()
    time.sleep(.1)



def start_2_player_game(seconds, p1_score, p2_score):
    ####### Initialize Distance Sensor #############################
    print("\nSparkFun Proximity Sensor VCN4040 Example 1\n")
    oProx = qwiic_proximity.QwiicProximity()

    if oProx.connected == False:
        print("The Qwiic Proximity device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
    oProx.begin()
    ################################################################
    start = time.time()
    while math.floor(time.time() - start) < seconds:
        countdown = seconds - math.floor(time.time() - start)
        oled_update_score(p1_score, p2_score, countdown)
        sleep(0.1)
        
        # Read Gesture Sensor Data
        gesture = apds.gesture() 
        if gesture == 0x02:
            # print("down")
            p1_score += 1
            print("Player 1\nHoops made:", p1_score)
            oled_update_score(p1_score, p2_score, countdown)
            sleep(0.1)

        # Read Distance Sensro Data
        proxValue = oProx.get_proximity()
        print("Proximity Value: %d" % proxValue) # For Troubleshooting
        if proxValue > 75: # Need to confirm optimal value after building prototype
            # TODO: need to ensure that hoop for player 2 is not double counted (the sleep function below doesn't work as well if the ball falls slowly past the distance sensor)
            sleep(0.1)
            p2_score += 1
            print("Player 2\nHoops made:", p1_score)
            oled_update_score(p1_score, p2_score, countdown)
            
    oled_update_score(p1_score, p2_score, 0)
            
    # return math.floor(time.time() - start)


# Initial Screen Set-Up
oled_update_score(p1_score, p2_score, seconds)
sleep(0.1)

# Start Game
start_2_player_game(seconds, p1_score, p2_score)

# Troubleshooting for Single Player Game
# while True:
#     gesture = apds.gesture()

#     if gesture == 0x02:
#         print("down")
#         p1_score += 1
#         print("Player 1\nHoops made:", p1_score)
#         oled_update_score(p1_score, p2_score)
         
