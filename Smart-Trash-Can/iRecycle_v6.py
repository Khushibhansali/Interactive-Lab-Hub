from teachable_machine_lite import TeachableMachineLite
import os
import shutil
import sys
from datetime import datetime
import cv2 as cv
import time
from adafruit_servokit import ServoKit
import qwiic_led_stick
from word_counter import WordCounter # custom class to validate reading from camera
import walking_rainbow_LED_stick
import qwiic_button
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import paho.mqtt.client as mqtt
import uuid
import ssl
import qwiic_proximity
import qwiic_tca9548a
import qwiic_oled_display

##############################################################################
# Check if the camera opened successfully
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
# Set the frame width and height (optional)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

##############################################################################
# Configure client to send notifications through MQTT about bin status and count 
client = mqtt.Client(str(uuid.uuid1()))
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Set the SSL context
client.tls_set_context(ssl_context)

# this is the username and pw we have set up for the class
client.username_pw_set('idd', 'device@theFarm')

# connect to the broker
client.connect('farlab.infosci.cornell.edu', port=8883)

##############################################################################
label_counter = WordCounter()

walking_rainbow_LED_stick.run_example()
my_stick = qwiic_led_stick.QwiicLEDStick()
my_stick.set_all_LED_color(0,50,0)
my_stick.set_all_LED_brightness(1)
# Turn on all the LEDs to white
my_stick.LED_off()

bin_lid = 'closed'  # Closed bin, dummy variable to check whether any bin is open.
last_saved_label = None

if my_stick.begin() == False:
    print("\nThe Qwiic LED Stick isn't connected to the sytsem. Please check your connection", \
        file=sys.stderr)

print("\nLED Stick ready!")

# Dictionary to map classifications to colors
colors_dict = {
    'background': (0,0,0),          # Off
    'paper': (0, 0, 255),           # Blue
    'cardboard': (0, 0, 255),       # Blue      # (128, 0, 128),       # Purple
    'trash': (255, 255, 255),       # White
    'plastic': (255, 0, 0),         # Red
    'metal': (255, 255, 0),         # Yellow             
    'glass': (0, 255, 0),           # Green
    'battery': (255, 13, 0)         # Orange
}

# Dictionary to store file paths for misclassified items
misclassified_items = {
    'paper': 'new_training_items/paper',
    'cardboard': 'new_training_items/cardboard',
    'trash': 'new_training_items/trash',
    'plastic': 'new_training_items/plastic',
    'metal': 'new_training_items/metal',
    'glass': 'new_training_items/glass',
    'battery': 'new_training_items/battery'
}

# Dictionary to map label to servo rotation
servo_index = {
    'paper': 0,
    'cardboard': 0,
    'trash': 7,
    'plastic': 8,
    'metal': 15,
    'glass': 10,
    'battery': 12
}

# Dictionary to map label to qwiic button
qwiic_button_address = {
    'paper': 0x6b,      # Soldered: A2 -> Green Button
    'cardboard': 0x6b,  # Soldered: A2 -> Green Button
    'trash': 0x6c,      # Soldered: A0 & A1 -> Green Button
    'plastic': 0x6e,    # Soldered: A0 -> Green Button
    'metal': 0x69,      # Soldered: A1 & A2 -> Green Button
    'glass': 0x67,      # Soldered: A3 -> Green Button 
    'battery': 0x63   # Soldered: A2 & A3 -> Green Button
}

# Dictionary with item counts
item_counts = {
    'paper': 0,
    'cardboard': 0,
    'trash': 0,
    'plastic': 0,
    'metal': 0,
    'glass': 0,
    'batteries': 0
}

# Mux Port Correspondances 
dist_port = {
    'paper': 0,
    'cardboard': 0,
    'trash': 1,
    'plastic': 2,
    'metal': 3,
    'glass': 4,
    'battery': 5
}

##############################################################################
# Set channels to the number of servo channels on your kit.
# There are 16 channels on the PCA9685 chip.
kit = ServoKit(channels=16)

# Name and set up the servo according to channel using for physical prototype.
servo_paper_cardboard = kit.servo[servo_index['paper']]
servo_trash = kit.servo[servo_index['trash']]
servo_plastic = kit.servo[servo_index['plastic']]
servo_metal = kit.servo[servo_index['metal']]
servo_glass = kit.servo[servo_index['glass']]
servo_battery = kit.servo[servo_index['battery']]


# Set the pulse width range of your servo for PWM control of rotating 0-180 degree (min_pulse, max_pulse)
# Each servo might be different, you can normally find this information in the servo datasheet
servo_paper_cardboard.set_pulse_width_range(525, 2500)
servo_trash.set_pulse_width_range(525, 2500)
servo_plastic.set_pulse_width_range(525, 2500)
servo_metal.set_pulse_width_range(525, 2500)
servo_glass.set_pulse_width_range(525, 2500)
servo_battery.set_pulse_width_range(525, 2500)
#############################################################################################################
# Initialize buttons for each class
red_button = qwiic_button.QwiicButton(0x6f) # Soldered: None (Set -> Red Button)
paper_button = qwiic_button.QwiicButton(qwiic_button_address['paper']) # Soldered: A2 -> Green Button
trash_button = qwiic_button.QwiicButton(qwiic_button_address['trash']) # Soldered: A0 & A1 -> Green Button
plastic_button = qwiic_button.QwiicButton(qwiic_button_address['plastic']) # Soldered: A0 -> Green Button
metal_button = qwiic_button.QwiicButton(qwiic_button_address['metal']) # Soldered: A1 & A2 -> Green Button
glass_button = qwiic_button.QwiicButton(qwiic_button_address['glass']) # Soldered: A3 -> Green Button 
battery_button = qwiic_button.QwiicButton(qwiic_button_address['battery']) # Soldered: A2 & A3 -> Green Button

def turn_off_all_buttons(brightness=0):
    # Turn off all buttons
    red_button.LED_off()
    paper_button.LED_off()
    trash_button.LED_off()
    plastic_button.LED_off()
    metal_button.LED_off()
    glass_button.LED_off()
    battery_button.LED_off()

turn_off_all_buttons()
##############################################################################################################
# Model 1: wjr83 selfmade dataset
# model_path = 'recycling_model_1/model.tflite'
# labels_path = "recycling_model_1/labels.txt"

# Model
model_path = 'iRecycle_cornell_background/model.tflite' #'smart_trashcan_model_v1/model.tflite'
labels_path = 'iRecycle_cornell_background/labels.txt' #'smart_trashcan_model_v1/labels.txt'

image_file_name = "frame.jpg"


tm_model = TeachableMachineLite(model_path=model_path, labels_file_path=labels_path)


text_color = (0, 0, 0)
# Close all bins
def close_all_bins():
    servo_paper_cardboard.angle = 90
    servo_trash.angle = 90
    servo_plastic.angle = 90
    servo_metal.angle = 97  # Correction based on testing
    servo_glass.angle = 90
    servo_battery.angle = 90
    bin_lid = 'closed'
close_all_bins()

def open_all_bins():
    servo_paper_cardboard.angle = 00
    servo_trash.angle = 0
    servo_plastic.angle = 0
    servo_metal.angle = 0  # Correction based on testing
    servo_glass.angle = 0
    servo_battery.angle = 0
    bin_lid = 'open'

def count_files_in_folders(folder_paths):
    file_counts = {}
    for label, folder_path in folder_paths.items():
        file_counts[label] = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
    return file_counts


def plot_bar_chart(file_counts):
    # Convert the file_counts dictionary to a DataFrame
    data = {'Item Categories': list(file_counts.keys()), 'Quantity': list(file_counts.values())}
    df = pd.DataFrame(data)

    # Sort DataFrame by 'Item Categories' column
    df = df.sort_values(by='Item Categories')

    # Set a color palette
    colors = sns.color_palette("viridis", n_colors=len(df))

    # Set the background color to black
    sns.set(style="darkgrid")

    # Create a bar chart using seaborn
    plt.figure(figsize=(11, 12), dpi=80)
    ax = sns.barplot(x='Item Categories', y='Quantity', data=df, palette=colors, edgecolor='w')

    # Set background color
    ax.set_facecolor('#1E1E1E')

    # Set text color to white and capitalize x-axis labels
    plt.xticks(ticks=range(len(df['Item Categories'])), labels=df['Item Categories'].str.capitalize(), color='yellow', fontsize=16, rotation=0, ha='center')
    plt.yticks(color='yellow', fontsize=16)
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')

    # Remove x-axis label
    ax.set(xlabel=None)

    # Set title and labels
    plt.ylabel('Quantity', fontsize=16, color='white')
    plt.title('Quantity of Items Disposed', fontsize=16, color='white')

    # Remove empty space between bars
    plt.tight_layout()

    # Set the face color of the entire figure to black
    fig = plt.gcf()
    fig.set_facecolor('#1E1E1E')

    # Save the plot
    plt.savefig('statistics_plot.png')
    plt.close()


def display_statistics_window():
    statistics_image = cv.imread('statistics_plot.png')
    cv.imshow('Statistics', statistics_image)
    # cv.moveWindow('Statistics', 0, 0)  # Move the window to the top left corner
    cv.waitKey(1)  # Required to update the window

# Initialize statistics window
cv.namedWindow('Statistics', cv.WINDOW_NORMAL)
cv.resizeWindow('Statistics', 950, 1050)  # Set the size of the statistics window


def save_item(label, frame): # Increase dataset of objects by saving a picture to folder
    folder_path = misclassified_items.get(label)
    if folder_path:
        # Use the class name and timestamp to create a unique file name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_name = f"{label}_{timestamp}.jpg"
        image_path = os.path.join(folder_path, image_name)

        cv.imwrite(image_path, frame)
        print(f"Saved classified item ({label}) image to: {image_path}")
    else:
        print(f"Error: No folder path defined for misclassified item ({label})")

# If item was misclassified, user inputs correct label by pressing the red button followed by the corrected green button associated with the class.
def move_item_to_correct_folder(label, corrected_label, r, g, b, frame):
    close_bin(label) # Close incorrectly opened bin due to misclassification
    # Get the folder paths for misclassified and correct labels
    misclassified_folder = misclassified_items.get(label)
    correct_folder = misclassified_items.get(corrected_label)

    if misclassified_folder and correct_folder:
        # Get the list of files in the misclassified folder
        misclassified_files = os.listdir(misclassified_folder)

        if misclassified_files:
            # Move the last item to the correct folder
            last_item = misclassified_files[-1]
            misclassified_item_path = os.path.join(misclassified_folder, last_item)
            correct_item_path = os.path.join(correct_folder, last_item)

            # Move the item
            shutil.move(misclassified_item_path, correct_item_path)

            # Rename the file in the correct folder
            base_name, extension = os.path.splitext(last_item)
            new_name = f"{base_name}_corrected{extension}"
            new_item_path = os.path.join(correct_folder, new_name)
            os.rename(correct_item_path, new_item_path)

            print(f"Moved {last_item} from '{misclassified_folder}' to '{correct_folder}'.")
            print(f"Renamed to {new_name} in '{correct_folder}'.")
            file_counts = count_files_in_folders(misclassified_items)
            plot_bar_chart(file_counts)
            display_statistics_window()

            # Open correct bin per user input
            turn_off_all_buttons()
            turn_on_button(corrected_label)
            if corrected_label == 'paper' or corrected_label == 'cardboard': # paper (1) and cardboard (2)
                servo_paper_cardboard.angle = 0
            elif corrected_label == 'trash': # trash
                servo_trash.angle = 0
            elif corrected_label == 'plastic': # plastic
                servo_plastic.angle = 0
            elif corrected_label == 'metal': # metal
                servo_metal.angle = 0
            elif corrected_label == 'glass': # glass
                servo_glass.angle = 0
            elif corrected_label == 'battery': # battery
                servo_battery.angle = 0
            
            # Display corrected label
            # Create a solid color image
            if corrected_label == 'trash':
                r, g, b = 0, 0, 0
            if corrected_label == 'battery':
                r, g, b = 255, 127, 0

            # if label == 'trash':
            #     r, g, b = 255, 255, 255
            if corrected_label == 'trash':
                my_stick.LED_off()
                time.sleep(0.1)
                my_stick.set_all_LED_color(255, 255, 255)
                time.sleep(0.1)
            elif corrected_label == 'battery':
                my_stick.LED_off()
                time.sleep(0.1)
                my_stick.set_all_LED_color(255, 13, 0)
                time.sleep(0.1)
            else: 
                my_stick.LED_off()
                time.sleep(0.1)
                r, g, b = colors_dict[corrected_label][0], colors_dict[corrected_label][1], colors_dict[corrected_label][2]
                my_stick.set_all_LED_color(r, g, b)
                time.sleep(0.1)
            # Determine text color based on class
            text_color = (255, 255, 255) if corrected_label in ['paper', 'plastic', 'trash'] else (0, 0, 0)

            # Create a solid color window
            window = np.ones((1000, 1000, 3), dtype=np.uint8) * np.array([b, g, r], dtype=np.uint8)

            # Display the class label in text, centered and large
            font = cv.FONT_HERSHEY_SIMPLEX
            text_size = cv.getTextSize(corrected_label, font, 5, 10)[0]
            text_x = (1000 - text_size[0]) // 2
            text_y = (1000 + text_size[1]) // 2
            cv.putText(window, corrected_label.capitalize(), (text_x, text_y), font, 5, text_color, 10, cv.LINE_AA)

            cv.imshow('Object Classification', window)
            cv.waitKey(1) # Necessary in order for window to update.

            # Timer for corrected label (to remain lid open)
            new_start_time = time.time()
            while True:
                elapsed_time = time.time() - new_start_time

                if elapsed_time >= 30:
                    close_bin(corrected_label)
                    # close_all_bins()
                    break

           
            
            # time.sleep(1)  # Adjust sleep time as needed
        else:
            print(f"No items found in '{misclassified_folder}'.")
    else:
        print("Error: Invalid labels or folder paths.")


def turn_on_button(label,brightness=150):
    if label == 'paper' or label == 'cardboard': # paper (1) and cardboard (2)
        paper_button.LED_on(brightness)
    elif label == 'trash': # trash
        trash_button.LED_on(brightness)
    elif label == 'plastic': # plastic
         plastic_button.LED_on(brightness)
    elif label == 'metal': # metal
        metal_button.LED_on(brightness)
    elif label == 'glass': # glass
        glass_button.LED_on(brightness)
    elif label == 'battery': # battery
        battery_button.LED_on(brightness)

def turn_off_button(label,brightness=0):
    if label == 'paper' or label == 'cardboard': # paper (1) and cardboard (2)
        paper_button.LED_on(brightness)
    elif label == 'trash': # trash
        trash_button.LED_on(brightness)
    elif label == 'plastic': # plastic
         plastic_button.LED_on(brightness)
    elif label == 'metal': # metal
        metal_button.LED_on(brightness)
    elif label == 'glass': # glass
        glass_button.LED_on(brightness)
    elif label == 'battery': # battery
        battery_button.LED_on(brightness)
 

# Function to rotate servo pertaining to identified item to a specified set of degrees 
def open_bin(label, r, g, b, frame, degrees=0):
    turn_on_button(label)
    run_dist_sensor(label)
    bin_lid = 'open'
    if label == 'paper' or label == 'cardboard': # paper (1) and cardboard (2)
        servo_paper_cardboard.angle = degrees
    elif label == 'trash': # trash
        servo_trash.angle = degrees
    elif label == 'plastic': # plastic
         servo_plastic.angle = degrees
    elif label == 'metal': # metal
        servo_metal.angle = degrees
    elif label == 'glass': # glass
        servo_glass.angle = degrees
    elif label == 'battery': # battery
        servo_battery.angle = degrees

    display_solid_window(label, r, g, b, frame)
    cv.waitKey(1) # Necessary in order for window to update.

    timer(label, r, g, b, frame)
    

# Function to rotate servo pertaining to identified item to a specified set of degrees 
def close_bin(label, degrees=90):
    turn_off_button(label)
    bin_lid = 'closed'
    if label == 'paper' or label == 'cardboard': # paper (1) and cardboard (2)
        servo_paper_cardboard.angle = degrees
    elif label == 'trash': # trash
        servo_trash.angle = degrees
    elif label == 'plastic': # plastic
         servo_plastic.angle = degrees
    elif label == 'metal': # metal
        servo_metal.angle = 97
    elif label == 'glass': # glass
        servo_glass.angle = degrees
    elif label == 'battery': # battery
        servo_battery.angle = degrees
        
def display_solid_window(label, r, g, b, frame):
    label_counter.process_word(label)
    if label == 'background':
        # Load the image.png from memory
        image_path = 'custom_bullseye_v4_black_background.png'
        background_image = cv.imread(image_path)
        text = "Place object on target displayed to start scan."
        text_size = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        text_x = (1000 - text_size[0]) // 2
        text_y = (1000 - text_size[1]) - 50
        cv.putText(background_image, text, (text_x, text_y), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)

        if background_image is None:
            # If the image loading fails, create a solid black background
            background_image = np.zeros((1000, 1000, 3), dtype=np.uint8)
            text_size = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            text_x = (1000 - text_size[0]) // 2
            text_y = (1000 + text_size[1]) // 2
            cv.putText(background_image, text, (text_x, text_y), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)

        # Display the window and wait for a key press
        cv.imshow('Object Classification', background_image)
    else:
        # Create a solid color image
        if label == 'trash':
            r, g, b = 0, 0, 0
        if label == 'battery':
            r, g, b = 255, 127, 0

        if label_counter.count == 10:
            # if label == 'trash':
            #     r, g, b = 255, 255, 255
            if label == 'trash':
                my_stick.set_all_LED_color(255, 255, 255)
            elif label == 'battery':
                    my_stick.set_all_LED_color(255, 13, 0)
            else: 
                my_stick.set_all_LED_color(r, g, b)
            # Determine text color based on class
            text_color = (255, 255, 255) if label in ['paper', 'plastic', 'trash'] else (0, 0, 0)

            # Create a solid color window
            window = np.ones((1000, 1000, 3), dtype=np.uint8) * np.array([b, g, r], dtype=np.uint8)

            # Display the class label in text, centered and large
            if (run_dist_sensor(label) == False):
                display_bin_fullness(label)
            else:
                font = cv.FONT_HERSHEY_SIMPLEX
                text_size = cv.getTextSize(label, font, 5, 10)[0]
                text_x = (1000 - text_size[0]) // 2
                text_y = (1000 + text_size[1]) // 2
                cv.putText(window, label.capitalize(), (text_x, text_y), font, 5, text_color, 10, cv.LINE_AA)

                cv.imshow('Object Classification', window)

            # time.sleep(1)
            save_item(label, frame) # save image to class folder
            last_saved_label = label
            file_counts = count_files_in_folders(misclassified_items)
            plot_bar_chart(file_counts)
            display_statistics_window()
            open_bin(last_saved_label, r, g, b, frame)
            

        
        # Check if label_counter.count is less than 10
        if label_counter.count < 10:
            if label_counter.count == 0:
                my_stick.LED_off()
                time.sleep(0.25) # Account for person placing object
                if label == 'trash':
                    my_stick.set_single_LED_color(0, 255, 255, 255)
                elif label == 'battery':
                    my_stick.set_single_LED_color(0, 255, 13, 0)
                else:
                    my_stick.set_single_LED_color(0, r, g, b)
                    time.sleep(0.25) # Account for person placing object
            time.sleep(0.15) # Necessary to avoid spamming the bus. Prevents I/O error
            if label == 'trash':
                    my_stick.set_single_LED_color(label_counter.count, 255, 255, 255)
            elif label == 'battery':
                my_stick.set_single_LED_color(label_counter.count, 255, 13, 0)
            else:
                my_stick.set_single_LED_color(label_counter.count, r, g, b)

            # Display solid white background with "Processing Item..." text
            window = np.ones((1000, 1000, 3), dtype=np.uint8) * 255  # White background
            processing_text = "Processing Item..."
            text_size = cv.getTextSize(processing_text, cv.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            text_x = (1000 - text_size[0]) // 2
            text_y = (1000 + text_size[1]) // 2
            cv.putText(window, processing_text, (text_x, text_y), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv.LINE_AA)

            cv.imshow('Object Classification', window)
        
def display_bin_fullness(label):
    # Create a black background image
    background_image = np.zeros((1000, 1000, 3), dtype=np.uint8)

    # Load warning image
    warning_image = cv.imread('path/to/warning_image.jpg')  # Replace with the actual path to your warning image

    # Resize warning image to match the background
    warning_image = cv.resize(warning_image, (1000, 1000))

    # Overlay warning image onto the background
    alpha = 0.5  # Adjust the transparency of the warning image
    background_image = cv.addWeighted(background_image, 1 - alpha, warning_image, alpha, 0)

    font = cv.FONT_HERSHEY_SIMPLEX
    text_size = cv.getTextSize(label, font, 5, 10)[0]
    text_x = (1000 - text_size[0]) // 2
    text_y = (1000 + text_size[1]) // 2
    text_color = (255, 255, 255)
    cv.putText(background_image, label.capitalize(), (text_x, text_y), font, 5, text_color, 10, cv.LINE_AA)

    # Display centered text
    text = "Bin is full"
    text_size = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
    text_x = (1000 - text_size[0]) // 2
    text_y = (1000 - text_size[1]) - 50
    cv.putText(background_image, text, (text_x, text_y), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)

    # Display the window and wait for a key press
    cv.imshow('Object Classification', background_image)


def initialize_mux():
    mux = qwiic_tca9548a.QwiicTCA9548A()
    if mux.is_connected() == False:
        print("The Qwiic TCA9548A device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        
    if mux.connected:
        print("Qwiic I2X Mux connected!")
        mux.enable_channels(0xFF)   # Enable ports 0-7
        return mux

    else:
        print("Qwiic I2X Mux not connected. Please check your connections.")
        return None

def distance_sensor():
    oProx = qwiic_proximity.QwiicProximity()
    oProx.begin()
    proxValue = oProx.get_proximity()
    return proxValue

def run_dist_sensor(label):
    mux = initialize_mux()
    dist_sensor_port = dist_port[label]
    
    mux.enable_channels(dist_sensor_port)
    distance = distance_sensor()  
    print(f"Channel {dist_sensor_port} - Proximity Value: {distance}")

    if distance > 1000:
        return True
    
    time.sleep(0.1)
   
    mux.disable_channels(0x00) 
    return False


def read_object():
    # Count the number of files in each folder
    file_counts = count_files_in_folders(misclassified_items)

    # Plot the bar chart
    plot_bar_chart(file_counts)
    display_statistics_window()

    
    label_counter.count = 0 # Reset counter everytime a new object is placed onto the tray

    while True: 

        # Get frame from camera
        ret, frame = cap.read()
        cv.imwrite(image_file_name, frame)

        # Classify current frame of camera
        results = tm_model.classify_frame(image_file_name)
        label = results['label']
        # label_counter.process_word(label)
        
        # Set the color scheme for the LED Stick & Label on Camera
        r, g, b = colors_dict[results['label']][0], colors_dict[results['label']][1], colors_dict[results['label']][2]
        # display_solid_window(label, r, g, b, frame)

        # Draw label on the frame
        if results['confidence'] > 0.5 and label != 'background':   # You can adjust the confidence threshold as needed
            if label == 'paper' or label == 'cardboard': # paper (1) and cardboard (2)
                # confirm_classification(label, r, g, b)
                display_solid_window(label, r, g, b, frame)
                # if label_counter.count == 10:
                #     display_solid_window(label, r, g, b, frame)
                #     save_item(label, frame) # save image to class folder
                #     last_saved_label = label
                #     open_bin(last_saved_label)
                #     break
            elif label == 'trash': # trash
                # confirm_classification(label, r, g, b)
                display_solid_window(label, r, g, b, frame)
                # if label_counter.count == 10:
                #     display_solid_window(label, r, g, b, frame)
                #     save_item(label, frame) # save image to class folder
                #     last_saved_label = label
                #     open_bin(last_saved_label)
                #     break
            elif label == 'plastic': # plastic
                # confirm_classification(label, r, g, b)
                display_solid_window(label, r, g, b, frame)
                # if label_counter.count == 10:
                #     display_solid_window(label, r, g, b, frame)
                #     save_item(label, frame) # save image to class folder 
                #     last_saved_label = label
                #     open_bin(last_saved_label)
                #     break
            elif label == 'metal': # metal
                # confirm_classification(label, r, g, b)
                display_solid_window(label, r, g, b, frame)
                # if label_counter.count == 10:
                #     display_solid_window(label, r, g, b, frame)
                #     save_item(label, frame) # save image to class folder 
                #     last_saved_label = label
                #     open_bin(last_saved_label)
                #     break
            elif label == 'glass': # glass
                # confirm_classification(label, r, g, b)
                display_solid_window(label, r, g, b, frame)
                # if label_counter.count == 10:
                #     display_solid_window(label, r, g, b, frame)
                #     save_item(label, frame) # save image to class folder 
                #     last_saved_label = label
                #     open_bin(last_saved_label)
                #     break
            elif label == 'battery': # battery
                # confirm_classification(label, r, g, b)
                display_solid_window(label, r, g, b, frame)
                # if label_counter.count == 10:
                #     display_solid_window(label, r, g, b, frame)
                #     save_item(label, frame) # save image to class folder 
                #     last_saved_label = label
                #     open_bin(last_saved_label)
                #     break
        else:
            display_solid_window(label, r, g, b, frame)
            my_stick.LED_off() # Turn off LED Stick if reading background

        # Display Camera & Prediction Label
        if label_counter.count < 10: # Only display camera output prior to prediction confirmation
            # cv.imshow('Cam', frame)
            # Save current image
            
            cv.imwrite(image_file_name, frame)
            # print(f"{label} has been observed this many times:", label_counter.count)
        # Visualize Results in Terminal
        # print("results:", results)

        # To terminate the program, press 'q' on the keyboard
        if cv.waitKey(1) & 0xFF == ord('q'):
            cap.release() # Close Camera Connection
            cv.destroyAllWindows() # Close Camera Window
            my_stick.LED_off() # Turn of LED Stick
            turn_off_all_buttons() # Turn off all buttons
            close_all_bins()
            # Break the loop if 'q' key is pressed
            sys.exit(0)
    
    
    return label, r, g, b, frame

# Decoration Function for LED Button
def perform_led_pattern(duration=0.05):
    # Create a snake pattern of the LED's turning on and turning off to signal to the user to press one
    battery_button.LED_on(150)  # Button in the 10 o'clock position
    time.sleep(duration)
    battery_button.LED_on(0)
    
    glass_button.LED_on(150)   # Button in the 8 o'clock position
    time.sleep(duration)
    glass_button.LED_on(0)

    metal_button.LED_on(150)    # Button in the 6 o'clock position
    time.sleep(duration)
    metal_button.LED_on(0)

    paper_button.LED_on(150)   # Button in the 12th o'clock position
    time.sleep(duration)
    paper_button.LED_on(0)

    plastic_button.LED_on(150) # Button in the 4 o'clock position
    time.sleep(duration)
    plastic_button.LED_on(0)

    trash_button.LED_on(150)   # Button in the 2 o'clock position
    time.sleep(duration)
    trash_button.LED_on(0)

def is_background_detected():
    # Check if the camera is already open
   
    # Get frame from the camera
    ret, frame = cap.read() 
    cv.imwrite(image_file_name, frame)

    # Classify the frame
    results = tm_model.classify_frame(image_file_name)

   
    # Visualize Results in Terminal
    print("results:", results)

    # Return True if the "background" class is detected with high confidence
    return results['label'] == 'background' and results['confidence'] > 0.5

def timer(label, r, g, b, frame, seconds=3):
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time

        if elapsed_time >= seconds:
            close_bin(label)
            break
        else:
            #TODO: check if red button was pressed
            
            if red_button.is_button_pressed():
                red_button.LED_on(150)
                # If the red button is pressed, wait for the user to press one of the correction buttons
                print("Misclassification detected. Press a correction button.")
                perform_led_pattern()

                # Wait for one of the correction buttons to be pressed
                corrected_label = None
                while corrected_label is None:
                    # To terminate the program, press 'q' on the keyboard
                    if cv.waitKey(1) & 0xFF == ord('q'):
                        cap.release() # Close Camera Connection
                        cv.destroyAllWindows() # Close Camera Window
                        my_stick.LED_off() # Turn of LED Stick
                        turn_off_all_buttons() # Turn off all buttons
                        close_all_bins()
                        # Break the loop if 'q' key is pressed
                        sys.exit(0)
                    if paper_button.is_button_pressed():
                        corrected_label = 'paper'
                        turn_off_all_buttons()
                        time.sleep(0.01)
                        paper_button.LED_on(150)
                        move_item_to_correct_folder(label, corrected_label, r, g, b, frame)
                        break 
                    elif trash_button.is_button_pressed():
                        corrected_label = 'trash'
                        turn_off_all_buttons()
                        time.sleep(0.01)
                        trash_button.LED_on(150)
                        move_item_to_correct_folder(label, corrected_label, r, g, b, frame)
                        break
                    elif plastic_button.is_button_pressed():
                        corrected_label = 'plastic'
                        turn_off_all_buttons()
                        time.sleep(0.01)
                        plastic_button.LED_on(150)
                        move_item_to_correct_folder(label, corrected_label, r, g, b, frame)
                        break
                    elif metal_button.is_button_pressed():
                        corrected_label = 'metal'
                        turn_off_all_buttons()
                        time.sleep(0.01)
                        metal_button.LED_on(150)
                        move_item_to_correct_folder(label, corrected_label, r, g, b, frame)
                        break
                    elif glass_button.is_button_pressed():
                        corrected_label = 'glass'
                        turn_off_all_buttons()
                        time.sleep(0.01)
                        glass_button.LED_on(150)
                        move_item_to_correct_folder(label, corrected_label, r, g, b, frame)
                        break
                    elif battery_button.is_button_pressed():
                        corrected_label = 'battery'
                        turn_off_all_buttons()
                        time.sleep(0.01)
                        battery_button.LED_on(150)
                        move_item_to_correct_folder(label, corrected_label, r, g, b, frame)
                        break
                    else:
                        perform_led_pattern()

                red_button.LED_off()
                break

        # You can add some other processing or print statements here if needed
        print(f"Time elapsed: {elapsed_time:.2f} seconds")

        # Adjust the delay based on your needs
        time.sleep(0.1)

    

# Main Loop
while True:
    try:
        # TODO: Always display statistics in full screen on the iPad (via VNC). Update statitcs (plot) once every time a new time is added.
        
        # Classify Item: Constantly be looking for objects (but don't predict if background is detected)
        
        label, r, g, b, frame = read_object()  # returns name (as a string) of classified object
        # label_counter.process_word(label)
        display_solid_window(label, r, g, b, frame) # Display Prediction
        

        # TODO: Open lid corresponding to item detected. Update block accordingly to support feedback.
        

        # TODO: Display Prediction on OLED Screen. 

        # TODO: Add feedback to correct wrong prediction using Qwiic Buttons. Make sure instruction to do so are clear (these can be written on the physical prototype)
        # This includes closing the lid for the miscclassification and opening the correct lid based on the button pressed by the user mapped to the correct classification.
        # Make sure to save picture of the object in the correct folder, and remove the picture of item in the folder that it was previously saved inside the read_object() function.
        

        # TODO: Close lid (when should the lid close? After how much time if the object was classified correctly?) 
        # Should we run a classification on when a hand is detected and then count 10 seconds from there? 
        # Should the distance sensor capture this when the lid is open? NOTE: The angle of the distance sensor is very tiny, likely to miss objects being placed inside.
        # Should we have a 2nd camera to indicate when a person moves/grabs object/ leaves away from the system? 
        # NOTE: Best Idea so far: If the lid is open, run a function to check when background is detected again. Only when background is detected again. 
        # If so, wait for 10 seconds before runing the read_object() function to classify a new object.   
        

        # TODO: Integrate distance sensors using i2c mux to show ow full each bin is. 

        # TODO: Use distance sensor to send information to the "maintenance department's" Raspberry Pi via MQTT indicating 
        # location of iRecycle trashcan and which bins are full / need to be emptied out. This should be display on the OLED screen
        # of the "maintence department's" Raspberry Pi. Once the bin is emptied out, the distance sensor should update the OLED screen
        # on Raspberry Pi of the maintenance departement showing that no bin needs to be emptied out. The maintenance department should 
        # not need to press any button to confirm the bins were emptied (this should be captured automatically by the distance sensor). 
        # We do NOT need a way (a code, that only the maintenance department knows) to open the lid when when the trash is full as the bins are not
        # physically attached to the lids, they simply sit underneath the lid. The bins are all independent from each other. The lids are attached to the 
        # "table" of the system, not the actual bins.

        # TODO: Nice to have: a button to pause/resume execution of the read_object() function in case the maintenance department needs to clean the spot 
        # where items are placed and avoid any noisy data from being captured.

    
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("Terminating iRecycle")
        my_stick.LED_off() # Turn off LED Stick
        # Break the loop if 'q' key is pressed
        sys.exit(0)
   
    k = cv.waitKey(1)
    if k% 255 == 27:
        # press ESC to close camera view.
        break
