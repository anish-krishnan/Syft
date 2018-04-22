"""
brew install portaudio
pip install pyaudio

"""

import pyaudio
import threading, os
import wave
from recorder import Recorder
import pynput
from pynput.keyboard import Key, Listener
# Basic Animation Framework

print("Starts recording when file starts")


#audio recording stuff
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "speech.wav"
global recording
recording = True

#event listener stuff
'''FOR SOME REASON ONLY CMY AND SHIFT WORK FOR EVENT LISTENER'''
def on_press(key):
    try:
        recording = False
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        recording = False
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    recording = False
    if key == Key.cmd or key == Key.shift_r or key == Key.shift:
        # Stop listener
        print("key pressed")
        #stop event listener
        print("recording is: " + str(recording))
        stream.stop_stream()
        stream.close()
        p.terminate()

#pyaudio object for recording
p = pyaudio.PyAudio()

#start recording
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

#frames for output file
frames = []

'''for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)'''
with Listener(on_press = on_press, on_release = on_release) as listener:
    while(True):
            if not recording:
                print("out of loop")
                listener.stop()
                break;
            print("recording is: " + str(recording))
            data = stream.read(CHUNK, exception_on_overflow = False)
            frames.append(data)
            listener.join()
            print("next loop")

print("done recording")

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(''.join(frames))
wf.close()
