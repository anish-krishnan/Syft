from __future__ import print_function
import librosa

y, sr = librosa.load("speech.wav")

tempo, beat_frames = librosa.beat.beat_track(y=y, sr = sr)

print('Estimated tempo: {:.2f} beats per minute'.format(tempo))

#beat_times = librosa.frames_to_time(beat_frames, sr=sr)

#print('Saving output to beat_times.csv')
#librosa.output.times_csv('beat_times.csv', beat_times)
