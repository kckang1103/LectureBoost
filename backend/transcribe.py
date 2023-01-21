import math
import speech_recognition as sr
from moviepy.editor import *

# file names
video_file = "../shortShortVideo.mp4"
transcription_file = "transcription.txt"
transcribed_audio_file = "transcribed_speech.wav"

# loading video file clip
video_clip = VideoFileClip(video_file)

# get the audio clip from the video
audio_clip = AudioFileClip(video_file)
audio_clip.write_audiofile(transcribed_audio_file)

# number of seconds for each chunk
chunk_size = 10
subtitles = []

# speech recognition recognizer
r = sr.Recognizer()

# empty the transcription file
open(transcription_file, 'w').close()
f = open(transcription_file, "a")

# iterate the audio clip for (audio clip duration / chunk_size) times
for i in range(0, math.floor(audio_clip.duration / chunk_size)):
    # open the audio file with speech recognizer and chunk the audio file
    with sr.AudioFile(transcribed_audio_file) as source:
        audio = r.record(source, offset=i * chunk_size, duration=chunk_size)

    # get transcription for the current chunk of the audio
    transcribed_text = r.recognize_google(audio)

    # write to the transcription file
    start_min, start_sec = divmod(i * chunk_size, 60)
    start_hour, start_min = divmod(start_min, 60)

    end_min, end_sec = divmod(i * chunk_size + chunk_size, 60)
    end_hour, end_min = divmod(start_min, 60)

    f.write('{:d}:{:02d}:{:02d}-'.format(start_hour, start_min, start_sec))
    f.write('{:d}:{:02d}:{:02d}\n'.format(end_hour, end_min, end_sec))
    f.write(transcribed_text)
    f.write("\n\n")

f.close()
