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
import qwiic_twist
import sys
import arcade_game_1 # Game #1: Arcade
import hoops_game_2
import hoops_game_3

def set_up():
    i2c = board.I2C()
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

    ############# Qwiic Twist ############################################################################################# 
    myTwist = qwiic_twist.QwiicTwist()

    if myTwist.connected == False:
        print("The Qwiic twist device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
    return myOLED, myTwist

def game_options(myOLED, myTwist):
    myOLED.clear(myOLED.PAGE)            # Clear the display
    
    # Initialize Rotary Encoder Value
    myTwist.begin()
    time.sleep(1)
    myTwist.count = 1

    while not myTwist.pressed:
        myOLED.set_cursor(0, 0)           # Set cursor to bottom-left
        myOLED.set_font_type(0)             # Smallest font
        myOLED.print("1: Arcade")          

        myOLED.set_cursor(0, 12)           # Set cursor to bottom-left
        myOLED.set_font_type(0)             # Smallest font
        myOLED.print("2: Horse")  

        myOLED.set_cursor(0, 24)           # Set cursor to bottom-left
        myOLED.set_font_type(0)             # Smallest font
        myOLED.print("3: Knockout")  

        myOLED.set_cursor(77, 0)           # Set cursor to bottom-left
        myOLED.set_font_type(0) 
        myOLED.print("Play:")
        myOLED.set_cursor(77, 10)           # Set cursor to bottom-left
        myOLED.set_font_type(0)
        myOLED.print("Game:")
        myOLED.set_cursor(110, 0) 
        myOLED.set_font_type(2)
        
        # Don't exceed Number of Games Available
        if myTwist.count > 3:
            myTwist.count = 3
        elif myTwist.count < 1:
             myTwist.count = 1
            
        myOLED.print("%1d" % myTwist.count)
        # # myOLED.set_cursor(0, 16)       # Set cursor to top-middle-left
        # # myOLED.set_font_type(0)         # Repeat
        # # myOLED.print("P2: ")
        # # myOLED.set_font_type(2)
        # if countdown == 0:
        # # Player 1 Wins
        # if p1_score > p2_score:
        #     myOLED.set_cursor(24, 24)        
        #     myOLED.set_font_type(0)         
        #     myOLED.print("Player 1 Wins!")  
        # # Player 2 Wins
        # if p1_score < p2_score:
        #     myOLED.set_cursor(24, 24)        
        #     myOLED.set_font_type(0)         
        #     myOLED.print("Player 2 Wins!") 
        # # It's a tie!
        # if p1_score == p2_score:
        #     myOLED.set_cursor(32, 24)        
        #     myOLED.set_font_type(0)         
        #     myOLED.print("It's a tie!")     

        # myOLED.set_cursor(0, 0)        # Set cursor to top-left
        # myOLED.set_font_type(0)         # Smallest font
        # myOLED.print("P1: ")          # Print "P1"
        # myOLED.set_font_type(2)         # 7-segment font
        # myOLED.print("%.3d" % p1_score)

        # # myOLED.set_cursor(0, 16)       # Set cursor to top-middle-left
        # # myOLED.set_font_type(0)         # Repeat
        # # myOLED.print("P2: ")
        # # myOLED.set_font_type(2)

        # # myOLED.print("%.3d" % hoops)
        # myOLED.set_cursor(64, 0)
        # myOLED.set_font_type(0)
        # myOLED.print("P2: ")
        # myOLED.set_font_type(2)
        # myOLED.print("%.3d" % p2_score)

        myOLED.display()
        time.sleep(.1)
    return myTwist.count

def main_menu():
    myOLED, myTwist = set_up()
    game_number = 0
    game_number = game_options(myOLED, myTwist)

    if game_number == 1:
        arcade_game_1.game_1_main()
    if game_number == 2:
        hoops_game_2.game_2_main()
    if game_number == 3:
        hoops_game_3.game_3_main()
    time.sleep(3)
    main_menu()

main_menu()