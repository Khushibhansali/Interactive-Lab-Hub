from __future__ import print_function
import qwiic_tca9548a
import smbus2
import time
import qwiic_button 
import qwiic # import qwiic_tca9548a
import time

test = qwiic.QwiicTCA9548A()

# # List Channel Configuration
# test.list_channels()

# # Enable Channels 0 and 4
# test.enable_channels([112, 113, 114, 115, 116, 117, 118, 119])

# # Pause 1 sec
# time.sleep (1)

# # Enable Channel 7
# # test.enable_channels(7)

# # List Channel Configuration
# test.list_channels()
ports_class = { 
    'background' : 0, 
    'paper' :  1,
    'cardboard': 2,
    'plastic' :4,
    'trash' : 3,
    'metal' : 5,
    'glass' : 6 
}

def enable_port(mux: qwiic_tca9548a.QwiicTCA9548A, port):
    mux.enable_channels(port)


def disable_port(mux: qwiic_tca9548a.QwiicTCA9548A, port):
    mux.disable_channels(port)


def initialize_mux(address):
    mux = qwiic_tca9548a.QwiicTCA9548A(address=address)
    return mux


def create_instance():
    mux = []
    # addresses = [*range(0x70, 0x77 + 1)]
    addresses = [0x70]

    for address in addresses:
        instance = initialize_mux(address)

        if not instance.is_connected():
            continue

        print("Connected to mux {0} \n".format(address))

        instance.disable_all()
        
        mux.append({
            "instance": instance,
            "scales": [],
        })

    return mux


def create_bus():
    bus = smbus2.SMBus(1)
    return bus


def initialize_scales(mux):
    scales = []
    bus = create_bus()
    ports = [0, 1, 2, 3, 4, 5, 6, 7]

    for port in ports:
        enable_port(mux, port)
        my_button = qwiic_button.QwiicButton()
        my_button.LED_on(150)
        time.sleep(1)
        # my_button.LED_on(255)
        # time.sleep(1)
        # my_button.LED_on(20)
        # time.sleep(1)
        my_button.LED_off()
        time.sleep(0.5)

        print(f"Connected to port: {port} with mux: {mux.address} \n")

        scales.append({
            "port": port,
            "LED_button": my_button
        })
        disable_port(mux, port)

    print(f"scales initialised: {scales} with mux: {mux.address} \n")

    return scales

def button_LED(mux, port): # port is a number from 0 to 7
    scales = []
    bus = create_bus()
    ports = [0, 1, 2, 3, 4, 5, 6, 7]

    enable_port(mux, port)
    my_button = qwiic_button.QwiicButton()
    my_button.LED_on(100)
    time.sleep(2)
    my_button.LED_on(255)
    time.sleep(2)
    my_button.LED_on(20)
    time.sleep(2)
    my_button.LED_off()


# def get_calibration_data_file_name(mux):
#     return "tare_mux_" + str(mux["instance"].address) + ".json"


def main():
    mux = create_instance()

    for i, val in enumerate(mux):
        mux[i]["scales"] = initialize_scales(mux[i]["instance"])

    return mux


main()
# port = 1
# button_LED(mux1, port)
