import math
import speech_recognition as sr
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import *
import os

# this might need to be changed depending on the os/computer
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/Cellar/ffmpeg/5.1.2_3/bin/ffmpeg"

# file names

def add_subtitles(video_file):

    #video_file = "chenShort.mp4"
    result_video_file = "subtitles.mp4"
    transcribed_audio_file = "transcribed_speech.wav"

    # loading video file clip
    video_clip = VideoFileClip(video_file)
    video_clip.resize(height=720)

    # get the audio clip from the video
    audio_clip = AudioFileClip(video_file)
    audio_clip.write_audiofile(transcribed_audio_file)

    # number of seconds for each chunk
    chunk_size = 10
    subtitles = []

    # speech recognition recognizer
    r = sr.Recognizer()

    # iterate the audio clip for (audio clip duration / chunk_size) times
    for i in range(0, math.floor(audio_clip.duration / chunk_size)):
        if i * chunk_size > audio_clip.duration:
            break

        # open the audio file with speech recognizer and chunk the audio file
        with sr.AudioFile(transcribed_audio_file) as source:
            audio = r.record(source, offset=i * chunk_size, duration=chunk_size)

        # get transcription for the current chunk of the audio
        transcribed_text = ""
        try:
            transcribed_text = r.recognize_google(audio, language='en-IN', show_all=True)
        except Exception as e:
            print(e)
            continue

        if len(transcribed_text) == 0 or transcribed_text == "":
            continue

        # add the current chunk of transcribed text with duration (start sec, end sec)
        try:
            subtitles.append(((i * chunk_size, i * chunk_size + chunk_size), transcribed_text['alternative'][0]['transcript']))
        except Exception as e:
            subtitles.append(((i * chunk_size, i * chunk_size + chunk_size), transcribed_text))


    # create subtitles clip with below attributes
    generator = lambda txt: TextClip(txt, font='Arial', fontsize=30, color='white', bg_color='black')
    subtitles_clip = SubtitlesClip(subtitles, generator)

    # create video with the subtitles
    video = CompositeVideoClip([video_clip, subtitles_clip.set_pos(('center', 'bottom'))])
    video.write_videofile(result_video_file, audio=True, fps=video.fps, temp_audiofile="temp-audio.m4a",
                          remove_temp=True, codec="libx264", threads=8, audio_codec="aac")


