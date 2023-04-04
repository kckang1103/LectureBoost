#!/usr/bin/env python

import subprocess
from tqdm import tqdm
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips

# Silence timestamps
SILENCE_FILE = 'uploads/silence.txt'
DETECTION_SCRIPT = './find_silence.sh'
# dbs to mark clip as silent 
THRESH = '-20'
# time between cuts
EASE = 0.0
MIN_CLIP_DURATION = 0.1


def generate_silence_file(file_name, minimum_duration):
    command = [DETECTION_SCRIPT, file_name, THRESH, str(minimum_duration)]
    subprocess.run(command)


def cut_silence(file_name, minimum_duration):
    # generate silence file
    generate_silence_file(file_name, minimum_duration)

    # number of clips generated
    # start of next clip
    next_start = 0

    video = VideoFileClip(file_name)
    audio = AudioFileClip(file_name)
    video.resize((460,720))
    full_duration = video.duration
    video_clips = []
    audio_clips = []
    with open(SILENCE_FILE, 'r', errors='replace') as f_in:
        # create clips using the end time and duration up silent sections
        for line in tqdm(f_in):
            if 'x' in line: continue

            silence_end, silence_duration = line.strip().split()
            clip_end = float(silence_end) - float(silence_duration)
            clip_start = float(next_start)
            
            clip_duration = float(clip_end) - clip_start

            if float(silence_duration) < minimum_duration or clip_duration == 0:
                next_start = silence_end
                continue

            if clip_start > EASE:
                clip_start -= EASE

            video_clip = video.subclip(clip_start, clip_end)
            video_clips.append(video_clip)
            audio_clip = audio.subclip(clip_start, clip_end)
            audio_clips.append(audio_clip)

            # update for start of next clip
            next_start = silence_end

    # get last clip of video and audio
    if full_duration - float(next_start) > MIN_CLIP_DURATION:
        print(full_duration, next_start)
        video_clips.append(video.subclip(float(next_start)-EASE))
        audio_clips.append(audio.subclip(float(next_start)-EASE))


    processed_video = concatenate_videoclips(video_clips)
    processed_audio = concatenate_audioclips(audio_clips)
    combined = processed_video.set_audio(processed_audio)
    combined.write_videofile(
        file_name[:-4] + '_cut.mp4',
        audio_codec='aac',
        fps=20,
        preset='ultrafast',
        codec='libx264',
        threads=20
    )
    video.close()

    return file_name[:-4] + '_cut.mp4'
