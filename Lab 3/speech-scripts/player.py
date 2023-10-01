#!/usr/bin/env python3

# prerequisites: as described in https://alphacephei.com/vosk/install and also python module `sounddevice` (simply run command `pip install sounddevice`)
# Example usage using Dutch (nl) recognition model: `python test_microphone.py -m nl`
# For more help run: `python test_microphone.py -h`
from __future__ import print_function
import argparse
import queue
import sys
import sounddevice as sd
import subprocess
from vosk import Model, KaldiRecognizer
import qwiic_button
import time

q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l", "--list-devices", action="store_true",
    help="show list of audio devices and exit")
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    "-f", "--filename", type=str, metavar="FILENAME",
    help="audio file to store recording to")
parser.add_argument(
    "-d", "--device", type=int_or_str,
    help="input device (numeric ID or substring)")
parser.add_argument(
    "-r", "--samplerate", type=int, help="sampling rate")
parser.add_argument(
    "-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
args = parser.parse_args(remaining)

try:

    ##### Initialize Recording Button ####
    my_button = qwiic_button.QwiicButton()

    if my_button.begin() == False:
        print("\nThe Qwiic Button isn't connected to the system. Please check your connection", \
            file=sys.stderr)
    
    print("\nButton ready!")
    ########################################

    if args.samplerate is None:
        device_info = sd.query_devices(args.device, "input")
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info["default_samplerate"])
        
    if args.model is None:
        model = Model(lang="en-us")
    else:
        model = Model(lang=args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device,
            dtype="int16", channels=1, callback=callback):
        print("#" * 80)
        print("Press Ctrl+C to stop the recording")
        print("#" * 80)

        rec = KaldiRecognizer(model, args.samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                print(rec.Result())
            else:
                result = rec.PartialResult()
                print(result)
                if "sounds" in result.lower():  # play sounds from touch sensor
                    touch_process = subprocess.Popen(["python3", "touch.py"])
                if "guitar" in result.lower():  # play sounds from touch sensor
                    guitar_process = subprocess.Popen(["python3", "guitar.py"])
                if "instruction" in result.lower():  # repeat instructions
                    # subprocess.call(['sh', './dj_instructions.sh'])
                    subprocess.call(['sh', './dj_instructions.sh'])
                    data = " " # Avoid repeating instructions over and over again
                if "record" in result.lower():
                    print("Press the green button to start recording:")

                    while True:
                        if my_button.is_button_pressed() == True:
                            # print("\nThe button is pressed!")
                            my_button.LED_on(brightness=100)
                            print("Recording in progress...")
                            subprocess.call(['arecord', '-d', '5', '-c', '2', 'sounds/recording.wav']) 
                            print("Recording complete!")
                            my_button.LED_off()
                            break
                        
                        # else:
                        #     print("\nThe button is not pressed.")

            if dump_fn is not None:
                dump_fn.write(data)

except KeyboardInterrupt:
    print("\nDone")
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ": " + str(e))
