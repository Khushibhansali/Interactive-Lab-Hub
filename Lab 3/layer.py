import subprocess
import time
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

# Define sound files for each sensor
sound_mapping = {
    2: "sounds/Sound 1.wav",
    3: "sounds/Sound 1.wav",
    4: "sounds/Sound 2.wav",
    5: "sounds/Sound 2.wav",
    6: "sounds/Sound 3.wav",
    7: "sounds/Sound 3.wav",
    8: "sounds/Sound 4.wav",
    9: "sounds/Sound 4.wav",
    10: "sounds/Sound 5.wav",
    11: "sounds/Sound 5.wav",
}

    
try:
    while True:
        # Check each sensor
        for i in range(12):
            if mpr121[i].value:
                print(f"Sensor {i} is touched.")

                # Get the sound file associated with the pressed sensor
                sound_file = sound_mapping.get(i)

                # Play the sound in the background
                if sound_file:
                    subprocess.Popen(["aplay", sound_file])

        time.sleep(0.1)  # Adjust sleep duration as needed

except KeyboardInterrupt:
    print("\nExiting...")
