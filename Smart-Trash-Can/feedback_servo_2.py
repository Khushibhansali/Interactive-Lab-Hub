from adafruit_servokit import ServoKit
import time
import board
from analogio import AnalogIn

# Set channels to the number of servo channels on your kit.
# There are 16 channels on the PCA9685 chip.
kit = ServoKit(channels=16)

# Assuming the servo is connected to channel 2 on the PCA9685
servo_channel = 2

# GPIO pin connected to the feedback pin of the Parallax Feedback 360° High-Speed Servo
feedback_pin = board.D21  # Change this to the actual GPIO pin you are using

# Dictionary to map label to servo rotation
servo_rotation = {
    'paper': 60,
    'cardboard': 60,
    'trash': 120,
    'plastic': 180,
    'metal': 240,
    'glass': 300,
    'batteries': 360
}

# Helper function to read feedback value from the analog pin
def read_feedback(analog_pin, samples=10, delay=0.01):
    reading = 0
    for _ in range(samples):
        reading += analog_pin.value
        time.sleep(delay)
    return int(reading / samples)

# Helper function to set servo angle and wait for stabilization
def set_servo_angle(angle, stabilization_time=2):
    kit.servo[servo_channel].angle = angle
    time.sleep(stabilization_time)

# Function to convert feedback value to angle
def feedback_to_angle(feedback_value):
    # Duty cycle range of the feedback signal
    duty_cycle_min = 2.9
    duty_cycle_max = 97.1

    # Map the feedback value to the duty cycle range
    duty_cycle = (feedback_value / 65535.0) * 100.0

    # Map the duty cycle to the angle range (0 to 360 degrees)
    angle = 360.0 * (duty_cycle - duty_cycle_min) / (duty_cycle_max - duty_cycle_min)

    # Ensure the angle is within the valid range
    angle = max(0, min(360, angle))

    return angle

# Function to move back to the north position (0 degrees)
def move_to_north_position():
    print("Moving back to the north position...")
    set_servo_angle(0)
    print("Returned to the north position.")

# Function to set servo angle based on the label
def set_servo_angle_by_label(label, feedback_pin):
    if label in servo_rotation:
        target_angle = servo_rotation[label]
        print("Moving to {} degrees for label: {}...".format(target_angle, label))
        current_angle = 0  # Assume the current angle is 0 (north position)

        while True:
            # Read the current feedback value
            feedback_value = read_feedback(feedback_pin)
            
            # Convert the feedback value to an angle
            current_angle = feedback_to_angle(feedback_value)

            # Set the servo angle
            set_servo_angle(target_angle)

            # Print the current angle
            print("Current Angle: {:.2f} degrees".format(current_angle))

            # Check if the servo has reached the target angle
            if abs(current_angle - target_angle) < 1:
                print("Reached target angle. Stopping the servo.")
                break

        # Move back to the north position after reaching the target angle
        move_to_north_position()
    else:
        print("Label {} not found in servo_rotation dictionary.".format(label))

# Example usage:
# Assuming 'paper' is the identified label
set_servo_angle_by_label('paper', AnalogIn(feedback_pin))
