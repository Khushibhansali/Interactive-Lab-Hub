#!/bin/bash

# Function to speak the instructions
speak_instructions() {
        espeak -ven+f2 -k5 -s150 --stdout "$(cat instructions.txt)" | aplay
}

# Function to capture user speech and implement the action
capture_and_process() {
    python3 player.py # Replace with the actual name of your Python script
}

# Execute functions
speak_instructions
capture_and_process