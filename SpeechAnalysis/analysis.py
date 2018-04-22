# import librosa
#
# y, sr = librosa.load(librosa.util.example_audio_file())
# y_harmonic = librosa.effects.harmonic(y)
# print(y_harmonic)
# print(y_harmonic.shape)

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import numpy as np
import os.path
import matplotlib.pyplot as plt

# def print_result(annotations):
#     score = annotations.document_sentiment.score
#     magnitude = annotations.document_sentiment.magnitude
#
#     for index, sentence in enumerate(annotations.sentences):
#         sentence_sentiment = sentence.sentiment.score
#         print('Sentence {} has a sentiment score of {}'.format(
#             index, sentence_sentiment))
#
#     print('Overall Sentiment: score of {} with magnitude of {}'.format(
#         score, magnitude))
#     return 0

# def countUmLikeAnd(speech):
#     count = 0
#     Um = []
#     Like = []
#     And = []
#     result = []
#     client = language.LanguageServiceClient()
#
#     document = types.Document(
#         content=speech,
#         type=enums.Document.Type.PLAIN_TEXT)
#     annotations = client.analyze_syntax(document=document).tokens
#
#     for i in range(len(annotations)):
#         if(annotations[i].text.content == "um"):
#             Um.append(i)
#         elif (annotations[i].text.content == "like"):
#             Like.append(i)
#         elif (annotations[i].text.content == "and"):
#             And.append(i)
#     print(Um)
#     tmp = []
#     for i in range(len(Um)):
#         if(i == 0):
#             tmp.append(Um[i])
#         if (i > 0):
#             if tmp[i-1]+1 == Um[i]:
#                 tmp.append(i)
#             else:
#                 print("HER")
#                 if tmp[i-1] - 3 >= 0 and tmp[i-1] + 3 < len(annotations):
#                     result.append(str(annotations[tmp[i-1]-3].text.content) +
#                                   str(annotations[tmp[i-1]-2].text.content) +
#                                   str(annotations[tmp[i-1]-1].text.content) +
#                                   str(annotations[tmp[i-1]].text.content) +
#                                   str(annotations[tmp[i-1]+1].text.content) +
#                                   str(annotations[tmp[i-1] + 2].text.content)+
#                                   str(annotations[tmp[i-1] + 3].text.content))
#                 tmp = []
#                 tmp.append(Um[i])
#         elif tmp[i] - 3 >= 0 and tmp[i] + 3 < len(annotations):
#
#             result.append(str(annotations[tmp[i] - 3].text.content) + " "+
#                           str(annotations[tmp[i] - 2].text.content) +" "+
#                           str(annotations[tmp[i] - 1].text.content) +" "+
#                           str(annotations[tmp[i]].text.content) +" "+
#                           str(annotations[tmp[i] + 1].text.content) +" "+
#                           str(annotations[tmp[i] + 2].text.content) +" "+
#                           str(annotations[tmp[i] + 3].text.content))
#             tmp = []
#         print(result)
#     return len(Um) + len(Like) + len(And), result

# print("Count", countUmLikeAnd("I have done like um shit like like dogs I have done like um um shit like like dogs"))

def countUmLikeAnd(speech):
    count = 0

    client = language.LanguageServiceClient()

    document = types.Document(
        content=speech,
        type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_syntax(document=document).tokens

    for i in range(len(annotations)):
        if (i + 1 <len(annotations)):
            if(annotations[i].text.content == "um"):
                count += 1
            elif (annotations[i].text.content == "like" and annotations[i+1].text.content == "like"):
                count += 1
            elif (annotations[i].text.content == "and" and annotations[i+1].text.content == "and"):
                count += 1
    return count
# print("Count", countUmLikeAnd("I have done like um shit like like dogs I have done like um um shit like like dogs"))


def saveToFile(bpm, volume, countOfUmLikeAnd):
    if os.path.exists("bpm.npy") and os.path.exists("volume.npy") and os.path.exists("countOfUmLikeAnd.npy"):
        b = np.load("bpm.npy")
        v = np.load("volume.npy")
        c = np.load("countOfUmLikeAnd.npy")
        b = np.ndarray.tolist(b)
        v = np.ndarray.tolist(v)
        c = np.ndarray.tolist(c)
        b.append(bpm)
        v.append(volume)
        c.append(countOfUmLikeAnd)
        np.save("bpm", np.asarray(b))
        np.save("volume", np.asarray(v))
        np.save("countOfUmLikeAnd", np.asarray(c))
    else:
        np.save("bpm", np.asarray([bpm]))
        np.save("volume", np.asarray([volume]))
        np.save("countOfUmLikeAnd", np.asarray([countOfUmLikeAnd]))

def makeList(n):
    result = []
    for i in range(n):
        result.append(i)
    return np.asarray(result)

def graphf():
    bpm = np.load("bpm.npy")
    volume = np.load("volume.npy")
    countOfUmLikeAnd = np.load("countOfUmLikeAnd.npy")
    print(countOfUmLikeAnd)
    # print(volume)
    f, (signalplot, harmpercplot, specplot) = plt.subplots(nrows=3)
    # plt.figure(1)
    f.tight_layout()
    plt.subplot(311)
    plt.plot(makeList(len(volume)), volume, 'ro', color="blue")
    plt.axis([0, len(volume), 0, volume[np.argmax(volume)]+1])
    plt.ylabel('Decibels (Db)')
    plt.xlabel('Number Of Trials')

    # plt.figure(2)
    plt.subplot(312)
    plt.plot(makeList(len(bpm)), bpm, 'ro', color="blue")
    plt.axis([0, len(bpm), 0, bpm[np.argmax(bpm)] + 10])
    plt.ylabel('BPM (beat / min)')
    plt.xlabel('Number Of Trials')

    # plt.figure(2)
    plt.subplot(313)
    plt.plot(makeList(len(countOfUmLikeAnd)), countOfUmLikeAnd, 'ro', color="blue")
    plt.axis([0, len(countOfUmLikeAnd), 0, countOfUmLikeAnd[np.argmax(countOfUmLikeAnd)] + 10])
    plt.ylabel('Number of Hesitations')
    plt.xlabel('Number Of Trials')

    plt.show()
