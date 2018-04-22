# events-example1.py
# Demos timer, mouse, and keyboard events

from Tkinter import *
import pyaudio
import threading, os
import wave
from recorder import Recorder
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import numpy as np
import wave
import sys
import librosa
from librosa import display
from microsoftSpeech import getTextFromSpeech
from forgottenText import countUmLike
import scipy.io.wavfile as wavfile
import math
from PIL import Image, ImageTk
'''from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types'''
import os.path
from analysis import graphf, saveToFile


####################################
# customize these functions
####################################

class Button(object):
    def __init__(self,data,x,y,width=100,height=100,text=""):
        self.data = data
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def inside(self,x,y):
        if(x >= self.x and x <= self.x + self.width and \
            y >= self.y and y <= self.y + self.height):
            return True
        return False

    def draw(self, canvas):
        canvas.create_rectangle(self.x - self.width/2,\
         self.y - self.height/2, \
            self.x + self.width/2,\
           self.y + self.height/2, \
            width = 3)
        canvas.create_text(self.x, self.y, text = self.text)

def init(data):  
    #scrolling
    data.cx = 0
    data.cy = 0
    #audio recording stuff
    data.CHUNK = 1024
    data.FORMAT = pyaudio.paInt16
    data.CHANNELS = 1
    data.RATE = 44100
    data.RECORD_SECONDS = 5
    data.WAVE_OUTPUT_FILENAME = "speech.wav"
    data.timeCount = 0
    #WHILE DATA.COLOR CHANGES, THE FILLS ARE STATIC BECAUSE IT'S NOT ALIASING
    data.color = '#%02x%02x%02x' % (128,125,128)
    data.timerDelay = 2 # milliseconds
    #stream will be false unless it's recording
    data.stream = 0
    data.rec = False
    data.frames = []
    data.recordedAFile = False
    data.showPlot = False
    data.p = pyaudio.PyAudio()
    data.text = ""
    data.speechlen = 0
    data.umlike = 0
    #raw text and confidence from msft api
    data.t = 0
    data.conf = 0
    #you can't do a tkinter quit w/o making root global
    data.graphToggle = Button(data,data.width/2,data.height/2 - 200,100,50, "Toggle Graph")
    data.graphToggle = Button(data, data.width - 20, data.height - 20)
    data.bpm = 0
    data.avgamp = 0

def mousePressed(event, data):
    #print("heyyyy")
    #data.mouseText = "last mousePressed: " + str((event.x, event.y))
    '''if(data.graphToggle.inside(event.x, event.y)):
        if(data.showPlot):
            data.showPlot = False
        else:
            data.showPlot = True'''

def keyPressed(event, data):
    '''data.keyText = ("last keyPressed: char=" + event.char + 
                    ", keysym=" + event.keysym)'''
    if(event.keysym == 'r' and data.rec == False):
        data.rec = True
        data.showPlot = False
    elif(event.keysym == 'r'):
        data.rec = False
    if(event.keysym == 'Down'):
        if(data.cy <= 300):
            data.cy += 10
    elif(event.keysym == 'Up'):
        if(data.cy >= -300):
            data.cy -= 10

def timerFired(data):
    data.timeCount += 1
    #background color function for smooth color change in title screen
    time = int(127*math.cos(math.pi*data.timeCount/180) + 128)
    data.color = '#%02x%02x%02x' % (255-time,125, time)


    if(data.rec):
        if(data.stream == 0):
            #start recording
            print("recording starrted!")
            data.stream = data.p.open(format=data.FORMAT,
                            channels=data.CHANNELS,
                            rate=data.RATE,
                            input=True,
                            frames_per_buffer=data.CHUNK)
        d = data.stream.read(data.CHUNK, exception_on_overflow = False)
        data.frames.append(d)
    else:
        #close stream and transcribe into text w api
        if(data.stream != 0):
            data.stream.stop_stream()
            data.stream.close()
            data.p.terminate()
            #output file
            wf = wave.open(data.WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(data.CHANNELS)
            wf.setsampwidth(data.p.get_sample_size(data.FORMAT))
            wf.setframerate(data.RATE)
            wf.writeframes(''.join(data.frames))
            wf.close()
            print('recording completed!')
            try:
                data.t, data.conf = getTextFromSpeech(data.WAVE_OUTPUT_FILENAME)
            except:
                data.t = "Didn't get it, try again!"
                data.conf = 0
            data.text = "Text: \"" + data.t + "\"\n" + "Confidence: " + str(data.conf)
            data.stream = 0
            data.recordedAFile = True

def redrawAll(canvas, data):
    
    canvas.create_rectangle(0,0,data.width,data.height, fill = data.color)
    #print("data.showPlot is: " + str(data.showPlot))
    #print("data.rec is: " + str(data.rec))
    #canvas.create_text(data.width/2, 20, text="Recording is: " + str(data.rec))
    '''if(data.recordedAFile):
        data.graphToggle.draw(canvas)'''
    pic = Image.open('photo.gif')
    tkpic = ImageTk.PhotoImage(pic)
    canvas.create_image(50,10,image = tkpic,anchor = NW)
    canvas.create_text(data.width/2, 100, text="Syft", fill="white", font="Helvetica 40")
    if data.recordedAFile and not data.showPlot:
        #print('data.showPlot is: ' + str(data.showPlot))
        #print('showing data')
        graph(data)
    if not data.rec and len(data.frames) == 0:
        canvas.create_text(data.width/2, 150, text="To record, press 'r'")
        data.showPlot = False
    elif(not data.showPlot and data.t == 0):
        canvas.create_text(data.width/2, 40, text="Recording... press 'r' to stop!")
    print("at the conditional before printing")
    if(data.recordedAFile):
        data.umlike = countUmLike(data.t)
        canvas.create_text(data.width/2, 70 - data.cy, text="Beats per minute: " + str(data.bpm))
        #save to file
        saveToFile(data.bpm, data.avgamp, data.umLike)
        if(data.bpm >= 60):
            speed = "slower side"
        if(data.bpm >= 90):
            speed = "average! That's a good pace."
        if(data.bpm >= 120):
            speed = "faster side- consider slowing down a tiny bit."
        if(data.bpm >= 160):
            speed = "too fast- "
        if(data.bpm < 60):
            speed = "too slow"
        print('printing data...')
        if(data.avgamp >= 0):
            vol = "too quiet. Speak louder!"
        if(data.avgamp >= 30):
            vol = "like that of a conversation. Maybe raise your voice."
        if(data.avgamp >= 35):
            vol = "in the general range of a speech in front of a classroom."
        if(data.avgamp >= 37):
            vol = "in the general range of a speech in a hall if you don't have a mic."
        if(data.avgamp >= 40):
            vol = "too loud even for a public speech in a classroom! Quiet down a tiny bit."
        canvas.create_text(data.width/2, 50-data.cy, text = "ANALYSIS: (Press up/down keys to scroll)")
        canvas.create_text(data.width/2, 90 - data.cy, text = "Relative speed: " + speed)
        canvas.create_text(data.width/2, 110 - data.cy, text = "Average volume: " + str(data.avgamp) + " dB")
        canvas.create_text(data.width/2, 130 - data.cy, text = "Your volume is " + vol)
        canvas.create_text(data.width/2, 150 - data.cy, text= "Number of hesitations (um/like): " + str(data.umlike))
        canvas.create_text(data.width/2 + 10, 188 - data.cy, text= "    There are three graphs: a graph of the volume over time,\n"+\
            "a graph of the volume of your vowels vs consonant sounds over time, \n" + \
            "    and the power of your voice in dB/time, in that order.")
        canvas.create_text(data.width/2- 10 , 280 - data.cy, text= data.text, width = 400)
        #graphf()
    #canvas.create_text(data.width/2, 80, text=data.timerText, font = "2")



def graph(data):
    #plot the graphs of the file
    f, (signalplot, harmpercplot, specplot)  = plt.subplots(3, sharex = True)
    plt.figure(1)
    plt.title('Speech Data')
    y, sr = librosa.load(data.WAVE_OUTPUT_FILENAME)
    #get average amplitude
    rate, amparr = wavfile.read(data.WAVE_OUTPUT_FILENAME)
    amptotal = 0
    for amp in (amparr):
        amptotal += abs(amp)
    data.avgamp = 10*math.log10(amptotal / 44100)
    print(data.avgamp)
    #get bpm of it
    data.bpm = librosa.beat.tempo(y,sr)
    '''SIGNAL WAVE PLOT'''
    '''spf = wave.open(data.WAVE_OUTPUT_FILENAME,'r')
    #Extract Raw Audio from Wav File
    signal = spf.readframes(-1)
    signal = np.fromstring(signal, 'Int16')
    #plt.plot(signal)
    signalplot.plot(signal)
    signalplot.set_title('Signal Waveform')'''
    '''Signal Wave Plot'''
    plt.subplot(3,1,1)
    display.waveplot(y, sr = sr)
    signalplot.set_title('Signal Waveform')
    '''Harmonic and Percussive'''
    plt.subplot(3,1,2)
    y_harm, y_perc = librosa.effects.hpss(y)
    librosa.display.waveplot(y_harm, sr=sr, alpha=0.25)
    librosa.display.waveplot(y_perc, sr=sr, color='r', alpha=0.5)
    harmpercplot.set_title('Harmonic + Percussive Waveform')
    #for some reason only works with plt and not subplot
    #specax = specplot.imshow(log_spec)
    #plt.tight_layout()
    '''Mel Power Spectrogram'''
    plt.subplot(3,1,3)
    spec = librosa.feature.melspectrogram(y, sr = sr, n_mels = 128)
    log_spec = librosa.power_to_db(spec, ref = np.max)
    display.specshow(log_spec, sr = sr, x_axis = 'time', y_axis = 'mel')
    plt.colorbar(format = '%+02.0f dB')
    specplot.set_title('Mel Power Spectrogram')
    #show data
    data.showPlot = True
    plt.show()


####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(800, 800)