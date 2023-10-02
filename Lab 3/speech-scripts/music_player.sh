#!/bin/bash

# Function to speak the instructions
say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }
#say $*
say " Welcome to the Master Music Player. Here are your options."
say "Say sounds to press the individual touch sensors and play sounds. "
say " Sensor number one is empty on the touch sensor to allow you to record a sound. All other buttons are pre-recorded sounds. "
say " You can switch instruments by pressing 0 on the touch sensor and then saying guitar, piano, or sounds"
say " Say guitar to play guitar notes on the individual touch sensors."
say " Say piano to play piano notes on the individual touch sensors."
say "Say record and then press the green button to record a sound, "
# say "Say volume to press keyboard button and adjust volume with *, "
# say "Say tempo to press keyboard and have tempo adjusted by pressing numbers on the keypad followed by #, "
# say "Say layer to layer songs and press 3 sounds to layer on the touch sensors. "
say "Say instructions to hear the instructions again."

# speak_instructions() {
#         espeak -ven+f2 -k5 -s150 --stdout "$(cat instructions.txt)" | aplay
# }

# Function to capture user speech and implement the action
capture_and_process() {
    python3 player.py # Replace with the actual name of your Python script
}

# Execute functions
# speak_instructions
capture_and_process