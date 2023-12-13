
from adafruit_servokit import ServoKit
import time

class Feedback360Servo:
    def __init__(self, kit, servo_channel, feedback_pin):
        self.kit = kit
        self.servo_channel = servo_channel
        self.feedback_pin = feedback_pin

        # Calibration setup
        self.angle_min = 0
        self.angle_max = 360
        self.feedback_min = 0
        self.feedback_max = 4095  # This value depends on the resolution of your feedback pin

        # Helper function to convert feedback value to angle
        self.scale_factor = (self.angle_max - self.angle_min) / (self.feedback_max - self.feedback_min)

    def set_angle(self, target_angle):
        # Ensure target angle is within valid range
        target_angle = self.normalize_angle(target_angle)

        # Convert target angle to PWM value
        pwm_value = int(self.angle_to_pwm(target_angle))
        self.kit.servo[self.servo_channel].angle = pwm_value

        # Wait for the servo to reach the target angle
        self.wait_for_angle(target_angle)

    def angle_to_pwm(self, angle):
        # Convert angle to PWM value based on calibration
        return ((angle - self.angle_min) / self.scale_factor) + self.feedback_min

    def wait_for_angle(self, target_angle, tolerance=5, timeout=10):
        # Wait for the servo to reach the target angle within a specified tolerance
        start_time = time.time()

        while True:
            current_angle = self.feedback_to_angle(self.kit._pca.channels[self.feedback_pin].duty_cycle)

            if abs(current_angle - target_angle) <= tolerance:
                break

            if time.time() - start_time > timeout:
                print("Timeout reached. Servo did not reach the target angle.")
                break

            time.sleep(0.1)

    def feedback_to_angle(self, feedback_value):
        # Convert feedback value to angle based on calibration
        return (feedback_value - self.feedback_min) * self.scale_factor + self.angle_min

    def normalize_angle(self, angle):
        # Normalize the angle to be within the valid range and handle multiple revolutions
        revolutions = angle // 360
        normalized_angle = angle - revolutions * 360
        return normalized_angle

# Example usage:
# kit = ServoKit(channels=16)
# servo = Feedback360Servo(kit=kit, servo_channel=2, feedback_pin=YOUR_FEEDBACK_PIN)
# servo.set_angle(180)
