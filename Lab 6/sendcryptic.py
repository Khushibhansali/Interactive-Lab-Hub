import paho.mqtt.client as mqtt
import uuid
import ssl

# Caesar cipher implementation for encryption
def encrypt(message, shift):
    encrypted_message = ""
    for char in message:
        if char.isalpha():
            encrypted_message += chr((ord(char) + shift - ord('A')) % 26 + ord('A'))
        else:
            encrypted_message += char
    return encrypted_message

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

while True:
    topic = input('>> topic: IDD/')
    if ' ' in topic:
        print('Sorry, white space is not allowed in topics.')
    else:
        topic = f"IDD/{topic}"
        print(f"Now writing to topic {topic}")
        print("Type 'new-topic' to switch topics")
        while True:
            message = input(">> message: ")
            if message == 'new-topic':
                break
            else:
                encrypted_message = encrypt(message, shift=3)
                client.publish(topic, encrypted_message)