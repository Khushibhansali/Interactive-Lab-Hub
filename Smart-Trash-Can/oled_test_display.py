import qwiic_oled_display
import board
import sys
import time

def disp_message_oled(myOLED, message):
    myOLED.clear(myOLED.PAGE)            # Clear the display
    # print("TEST")
    myOLED.set_cursor(16, 0)           # Set cursor to bottom-left
    myOLED.set_font_type(3)             # Largest font
    myOLED.print(message)
    myOLED.display()

i2c = board.I2C()
myOLED = qwiic_oled_display.QwiicOledDisplay()

# Initialize OLED
def initialize_OLED():
    myOLED.begin()
    myOLED.clear(myOLED.ALL)  #  Clear the display's memory (gets rid of artifacts)
    myOLED.clear(myOLED.PAGE)
    myOLED.display()
    time.sleep(1)

def disp_message_oled(myOLED, label):
    myOLED.clear(myOLED.ALL)  #  Clear the display's memory (gets rid of artifacts)
    myOLED.clear(myOLED.PAGE)
    # Center display on OLED Screen
    if label == 'plastic':
        myOLED.set_cursor(38, 12)           
    elif label == 'cardboard':
        myOLED.set_cursor(23, 12)
    elif label == 'trash' or 'paper' or 'glass' or 'metal':
        myOLED.set_cursor(43, 12)    
    elif label == 'battery':
        myOLED.set_cursor(26, 12)    
    myOLED.set_font_type(1)             # Set font size
    myOLED.print(label.upper())
    myOLED.display()


initialize_OLED()
label = 'battery'
disp_message_oled(myOLED, label)