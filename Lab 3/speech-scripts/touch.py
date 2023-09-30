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

try:
    while True:
        # Check each sensor
        for i in range(12):
            if mpr121[i].value:
                print(f"Sensor {i} is touched.")
                
                # Play different sounds based on the pressed sensor
                if i in [2, 3]:
                    play_sound("sounds/Sound 1.wav")
                elif i in [4, 5]:
                    play_sound("sounds/Sound 2.wav")
                elif i in [6, 7]:
                    play_sound("sounds/Sound 3.wav")
                elif i in [8, 9]:
                    play_sound("sounds/Sound 4.wav")
                elif i in [10, 11]:
                    play_sound("sounds/Sound 5.wav")
                
        time.sleep(0.1)  # Adjust sleep duration as needed
except KeyboardInterrupt:
    print("\nExiting...")
