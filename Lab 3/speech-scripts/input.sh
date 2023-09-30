#!/bin/bash

# Define a function to check if a command is available.
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if 'python3' and 'pip' are available.
if ! command_exists python3 || ! command_exists pip; then
    echo "Python 3 and pip are required to run this script."
    exit 1
fi

# Check if 'vosk' and 'sounddevice' Python packages are installed.
if ! python3 -c "import vosk" || ! python3 -c "import sounddevice"; then
    echo "Please install the 'vosk' and 'sounddevice' Python packages."
    exit 1
fi

# Define a function to handle Ctrl+C gracefully.
ctrl_c() {
    echo -e "\nDone"
    exit 0
}

# Set up a trap to catch Ctrl+C and execute the 'ctrl_c' function.
trap ctrl_c INT

# Define the Python script content as a heredoc.
python_script=$(cat <<EOF
import argparse
import queue
import sys
import sounddevice as sd

from vosk import Model, KaldiRecognizer

q = queue.Queue()

def int_or_str(text):
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
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
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, "input")
        args.samplerate = int(device_info["default_samplerate"])
        
    if args.model is None:
        model = Model(lang="en-us")
    else:
        model = Model(lang=args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize=8000, device=args.device,
            dtype="int16", channels=1, callback=callback):
        print("#" * 80)
        print("Press Ctrl+C to stop the recording")
        print("#" * 80)

        rec = KaldiRecognizer(model, args.samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = rec.Result()
                if result.strip():  # Check if the result is not empty
                    print(result.strip())  # Print the recognized text without leading/trailing spaces
            if dump_fn is not None:
                dump_fn.write(data)

except KeyboardInterrupt:
    print("\\nDone")
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ": " + str(e))
EOF
)

# Run the Python script using 'python3'.
python3 -c "$python_script"
