import paho.mqtt.client as mqtt
import uuid
import ssl

# Caesar cipher implementation for decryption
def decrypt(encrypted_message, shift):
    decrypted_message = ""
    for char in encrypted_message:
        if char.isalpha():
            decrypted_message += chr((ord(char) - shift - ord('A')) % 26 + ord('A'))
        else:
            decrypted_message += char
    return decrypted_message

# Every client needs a random ID
client = mqtt.Client(str(uuid.uuid1()))

# configure network encryption etc
# Configure SSL context
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Set the SSL context
client.tls_set_context(ssl_context)

# this is the username and pw we have set up for the class
client.username_pw_set('idd', 'device@theFarm')

# connect to the broker
client.connect('farlab.infosci.cornell.edu', port=8883)

def on_message(client, userdata, msg):
    decrypted_message = decrypt(msg.payload.decode(), shift=3)
    print(f"Received encrypted message: {msg.payload.decode()}")
    print(f"Decrypted message: {decrypted_message}")

# Set the callback function for message reception
client.on_message = on_message

# Subscribe to a specific topic to receive notifications
subscribe_topic = "IDD/encrypted_notification"
client.subscribe(subscribe_topic)

# Continue the loop to keep the client running and receiving messages
client.loop_forever()
