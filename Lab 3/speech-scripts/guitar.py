import time
import subprocess
import board
import busio
import adafruit_mpr121

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize MPR121
mpr121 = adafruit_mpr121.MPR121(i2c)

# Check if MPR121 is connected
if not mpr121:
    print("Error initializing MPR121. Check your wiring.")
    sys.exit(1)

print("Press Ctrl+C to exit.")

def play_sound(sound_file):
    subprocess.run(["aplay", sound_file])
a = True
try:
    while a == True:
        # Check each sensor
        for i in range(12):
            if mpr121[i].value:
                print(f"Sensor {i} is touched.")
                
                # Play different sounds based on the pressed sensor
                if i in [0]:
                    a = False
                    break
                if i in [1]:
                    play_sound("sounds/recording.wav")
                if i in [2, 3]:
                    play_sound("sounds/guitar/2_mixkit-cool-guitar-riff-2321.wav")
                if i in [4, 5]:
                    play_sound("sounds/guitar/3_mixkit-guitar-stroke-down-slow-2339.wav")
                if i in [6, 7]:
                    play_sound("sounds/guitar/4_mixkit-guitar-stroke-up-slow-2338.wav")
                if i in [8, 9]:
                    play_sound("sounds/guitar/5_mixkit-happy-guitar-chords-2319.wav")
                if i in [10, 11]:
                    play_sound("sounds/guitar/1_mixkit-bass-guitar-single-note-2331.wav")
                
        time.sleep(0.1)  # Adjust sleep duration as needed
except KeyboardInterrupt:
    print("\nExiting...")
