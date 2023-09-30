import time
import qwiic_keypad

def read_keypad():
    keypad = qwiic_keypad.QwiicKeypad()

    if not keypad.connected:
        print("Qwiic Keypad not connected. Check your connections.")
        return

    keypad.begin()
    print("Press Ctrl+C to exit.")

    try:
        while True:
            key = keypad.get_button()

            if key != 0xFF:
                print(f"Key pressed: {chr(key)}")

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    read_keypad()
