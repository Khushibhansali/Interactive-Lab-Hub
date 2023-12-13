import time
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# There are 16 channels on the PCA9685 chip.
kit = ServoKit(channels=16)

# Name and set up the servos according to the channels you are using.
servo_180 = kit.servo[1]  # 180 degree servo
continuous_servo = kit.servo[2]  # Continuous servo

# Set the pulse width range of your 180 degree servo for PWM control of rotating 0-180 degrees
servo_180.set_pulse_width_range(500, 2500)

# Set the continuous servo to the mid position to stop it initially
continuous_servo.angle = 90

continuous_servo.angle = 95 # spin slowly in one direction
continuous_servo.angle = 85 # spin slowly in the other direction
continuous_servo.angle = 90 # stop

while True:
    try:
        # Spin the continuous servo 90 degrees
        continuous_servo.angle = 180
        time.sleep(3)

        # Stop the continuous servo by setting it to the mid position (90 degrees)
        continuous_servo.angle = 90

        time.sleep(3)

        # Spin the continuous servo in the opposite direction for 90 degrees
        continuous_servo.angle = 0
        time.sleep(3)

        # Stop the continuous servo by setting it to the mid position (90 degrees)
        continuous_servo.angle = 90

        time.sleep(3)

    except KeyboardInterrupt:
        # Once interrupted, set the continuous servo back to the mid position to stop it
        continuous_servo.angle = 90
        time.sleep(0.5)
        break
