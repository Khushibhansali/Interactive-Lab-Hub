import time
import subprocess
import random
import board
import busio
import displayio
import adafruit_mpr121
import adafruit_ssd1306

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize MPR121
mpr121 = adafruit_mpr121.MPR121(i2c)

# Check if MPR121 is connected
if not mpr121:
    print("Error initializing MPR121. Check your wiring.")
    sys.exit(1)

# Create the SSD1306 OLED class
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Function to play sound
def play_sound(sound_file):
    subprocess.run(["aplay", sound_file])

# Function to create a random animation at a specific position
def create_random_animation(x, y):
    animation_size = 5
    oled.fill_rect(x, y, animation_size, animation_size, 1)

try:
    while True:
        # Check each sensor
        for i in range(12):
            if mpr121[i].value:
                print(f"Sensor {i} is touched.")
                
                # Play different sounds based on the pressed sensor
                if i < 9:
                    song_name = f"Sound {i}.wav"
                    play_sound(f"sound/{song_name}")
                   
                    # Create and animate random symbols bouncing around for 2 seconds
                    start_time = time.time()
                    while time.time() - start_time < 2:
                        symbol_x = random.randint(0, oled.width - 1)
                        symbol_y = random.randint(0, oled.height - 1)
                        create_random_animation(symbol_x, symbol_y)
                        oled.show()
                        time.sleep(0.05)  # Adjust the delay as needed
                    
                    # Clear the screen after 2 seconds
                    oled.fill(0)
                    oled.show()

except KeyboardInterrupt:
    print("\nExiting...")
