from teachable_machine_lite import TeachableMachineLite
import cv2 as cv
import time
# from adafruit_servokit import ServoKit

# # Set channels to the number of servo channels on your kit.
# # There are 16 channels on the PCA9685 chip.
# kit = ServoKit(channels=16)

# # Name and set up the servo according to the channel you are using.
# servo = kit.servo[2]

# # Set the pulse width range of your servo for PWM control of rotating 0-180 degree (min_pulse, max_pulse)
# # Each servo might be different, you can normally find this information in the servo datasheet
# servo.set_pulse_width_range(500, 2500)

cap = cv.VideoCapture(0)


# Model 1: wjr83 selfmade dataset
# model_path = 'recycling_model_1/model.tflite'
# labels_path = "recycling_model_1/labels.txt"

# Model 2: Kaggle Dataset
model_path = 'recycling_model_2_kgldataset_v3/model.tflite'
labels_path = "recycling_model_2_kgldataset_v3/labels.txt"

image_file_name = "frame.jpg"


tm_model = TeachableMachineLite(model_path=model_path, labels_file_path=labels_path)

# # Initialize variables for object tracking
# tracking = True
# prev_x, prev_y, prev_w, prev_h = 0, 0, 0, 0

# text_color = (0, 0, 0)
# servo.angle = 0

while True:
    

    ret, frame = cap.read()
    results = tm_model.classify_frame(image_file_name)

    #  # Draw a bounding box and label on the frame
    # if results['confidence'] > 0.5 and results['label'] != 'background':  # You can adjust the confidence threshold as needed
        
    #     if results['id'] == 1: # plastic
    #         text_color = (255, 0, 255)
    #          # Set the servo to 180 degree position
    #         servo.angle = 36
    #         # time.sleep(1)
    #     elif results['id'] == 2 or results['id'] == 5: # paper (2) and cardboard (5)
    #         text_color = (0, 255, 255) 
    #         # Set the servo to 180 degree position
    #         servo.angle = 36*2
    #         # time.sleep(1)
    #     elif results['id'] == 3: # metal
    #         text_color = (255, 255, 0)
    #         # Set the servo to 180 degree position
    #         servo.angle = 36*3
    #         # time.sleep(1)
    #     elif results['id'] == 4: # glass
    #         text_color = (0, 0, 255)
    #         servo.angle = 36*4
    #         # time.sleep(1)
    #     elif results['id'] == 0: # trash
    #         text_color = (255, 0, 0)
    #         servo.angle = (36*5)-1
    #         # time.sleep(1)
            
    #     x, y, w, h = 100, 100, 200, 200  # Adjust the coordinates and size of the bounding box
        
    #     if tracking:
    #         # Adjust the bounding box position based on object movement
    #         x += int(0.2 * (x - prev_x))
    #         y += int(0.2 * (y - prev_y))
    #         w += int(0.2 * (w - prev_w))
    #         h += int(0.2 * (h - prev_h))
    #         # Draw a bounding box and label on the frame
    #         prev_x, prev_y, prev_w, prev_h = x, y, w, h
    #         # cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green rectangle
    #         #TODO: Adjust display of identified object, color code by type
    #         cv.putText(frame, results['label'], (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, text_color, 2)
    #     tracking = True
    # else:
    #     tracking = False

    

    cv.imshow('Cam', frame)
    cv.imwrite(image_file_name, frame)
    
    
    print("results:",results)
    
    k = cv.waitKey(1)
    if k% 255 == 27:
        # press ESC to close camera view.
        break

