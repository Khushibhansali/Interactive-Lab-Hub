#!/bin/bash

say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }
#say $*
say " Welcome to the Master Music Player, where you can transform any object into a musical instrument!"
say " Please listen carefully to the instructions:"
say "Say the keyword beats to press the individual touch sensors and play sounds. "
say " Sensor number one is empty on the touch sensor to allow you to record a sound. All other buttons are pre-recorded sounds. "
say " You can switch instruments by pressing 0 on the touch sensor and then saying guitar or beats"
say " Say the keyword guitar to play guitar notes on the individual touch sensors."
# say " Say the keyword piano to play piano notes on the individual touch sensors."
say "Say the keyword record and then press the green button to record a sound, "
# say "Say volume to press keyboard button and adjust volume with *, "
# say "Say tempo to press keyboard and have tempo adjusted by pressing numbers on the keypad followed by #, "
# say "Say layer to layer songs and press 3 sounds to layer on the touch sensors. "
say "Say instructions to hear the instructions again."