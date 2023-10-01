#!/bin/bash

# Function to speak the instructions
say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }
#say $*
say " Welcome to the Master Music Player. Here are your options."
say "Say sounds to press the individual touch sensors and play sounds. 0-1 is empty on the touch sensor to allow you to record a sound. The rest will be pre-recorded sounds. "
say " Say guitar to play guitar notes on the individual touch sensors."
say " Say piano to play piano notes on the individual touch sensors."
say "Say record to press the green button and record a sound, "
# say "Say volume to press keyboard button and adjust volume with *, "
# say "Say tempo to press keyboard and have tempo adjusted by pressing numbers on the keypad followed by #, "
# say "Say layer to layer songs and press 3 sounds to layer on the touch sensors. "
say "Say instructions to hear the instructions again."