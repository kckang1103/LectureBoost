import math
import speech_recognition as sr
from moviepy.editor import *

def transcribe(video_file, uploads_path):
    # file names
    #video_file = "chenShort.mp4"
    transcription_file = uploads_path + "transcription.txt"
    transcribed_audio_file = uploads_path + "transcribed_speech.wav"

    # get the audio clip from the video
    audio_clip = AudioFileClip(video_file)
    audio_clip.write_audiofile(transcribed_audio_file)

    # number of seconds for each chunk
    chunk_size = 30

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

        # write to the transcription file
        start_min, start_sec = divmod(i * chunk_size, 60)
        start_hour, start_min = divmod(start_min, 60)

        end_min, end_sec = divmod(i * chunk_size + chunk_size, 60)
        end_hour, end_min = divmod(end_min, 60)

        f.write('Time Stamp: {:d}:{:02d}:{:02d}-'.format(start_hour, start_min, start_sec))
        f.write('{:d}:{:02d}:{:02d}\n'.format(end_hour, end_min, end_sec))

        # get transcription for the current chunk of the audio
        transcribed_text = ""
        try:
            transcribed_text = r.recognize_google(audio, language='en-IN', show_all=True)
            print(transcribed_text)
        except Exception as e:
            print(e)
            continue

        if len(transcribed_text) == 0:
            continue

        # write to the transcription file
        try:
            f.write(transcribed_text['alternative'][0]['transcript'])
            f.write(" ")
        except Exception as e:
            print(e)

        f.write("\n\n")

    f.close()

