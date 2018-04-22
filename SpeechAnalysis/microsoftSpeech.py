#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import httplib
import uuid
import forgottenText
from forgottenText import getForgotten, getExtra, countUmLike
import json

'''MAIN FILE IS GETTING THE TEXT FROM THE WAV FILE USING
MICROSOFT AZURE (getTextFromSpeech(filename))'''

class Microsoft_ASR():
    def __init__(self):
        self.sub_key = '8036ae21fc1d4bba82312eb0489247ea'
        self.token = None
        pass

    def get_speech_token(self):
        FetchTokenURI = "/sts/v1.0/issueToken"
        header = {'Ocp-Apim-Subscription-Key': self.sub_key}
        conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
        body = ""
        conn.request("POST", FetchTokenURI, body, header)
        response = conn.getresponse()
        str_data = response.read()
        conn.close()
        self.token = str_data
        print "Got Token: ", self.token
        return True

    def transcribe(self,speech_file):
        # Grab the token if we need it
        if self.token is None:
            print "No Token... Getting one"
            self.get_speech_token()

        endpoint = 'https://speech.platform.bing.com/recognize'
        request_id = uuid.uuid4()
        # Params form Microsoft Example 
        params = {'scenarios': 'ulm',
                  'appid': 'D4D52672-91D7-4C74-8AD8-42B1D98141A5',
                  'locale': 'en-US',
                  'version': '3.0',
                  'format': 'json',
                  'instanceid': '565D69FF-E928-4B7E-87DA-9A750B96D9E3',
                  'requestid': uuid.uuid4(),
                  'device.os': 'linux'}
        content_type = "audio/wav; codec=""audio/pcm""; samplerate=16000"

        def stream_audio_file(speech_file, chunk_size=1024):
            with open(speech_file, 'rb') as f:
                while 1:
                    data = f.read(1024)
                    if not data:
                        break
                    yield data

        headers = {'Authorization': 'Bearer ' + self.token, 
                   'Content-Type': content_type}
        resp = requests.post(endpoint, 
                            params=params, 
                            data=stream_audio_file(speech_file), 
                            headers=headers)
        val = json.loads(resp.text)
        try:
            return val["results"][0]["name"], val["results"][0]["confidence"]
        except:
            print("Error with the API")
            return "No English words detected!"

def getTextFromSpeech(filename):
    ms_asr = Microsoft_ASR()
    ms_asr.get_speech_token()
    text, confidence = ms_asr.transcribe(filename)
    s = ""
    s += "Text: \"" + text + "\"\n" + "Confidence: " + confidence
    #s += 
    print(s)
    return text, confidence

if __name__ == '__main__':
    getTextFromSpeech('speech.wav')