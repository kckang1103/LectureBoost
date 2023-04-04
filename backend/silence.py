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


def generate_silence_file(file_name, minimum_duration):
    command = [DETECTION_SCRIPT, file_name, THRESH, str(minimum_duration)]
    subprocess.run(command)


def cut_silence(file_name, minimum_duration):
    # generate silence file
    generate_silence_file(file_name, minimum_duration)

    # number of clips generated
    count = 0
    # start of next clip
    last = 0

    video = VideoFileClip(file_name)
    audio = AudioFileClip(file_name)
    video.resize((460,720))
    full_duration = video.duration
    video_clips = []
    audio_clips = []
    with open(SILENCE_FILE, 'r', errors='replace') as f_in:
        for line in tqdm(f_in):
            if 'x' in line: continue

            end, duration = line.strip().split()
            to = float(end) - float(duration)
            start = float(last)
            
            clip_duration = float(to) - start

            if clip_duration < minimum_duration:
                last = end
                continue

            if full_duration - to < minimum_duration:
                continue

            if start > EASE:
                start -= EASE

            video_clip = video.subclip(start, to)
            video_clips.append(video_clip)
            audio_clip = audio.subclip(start, to)
            audio_clips.append(audio_clip)
            last = end
            count += 1

    if full_duration - float(last) > minimum_duration:
        print('Clip {} (Start: {}, End: {})'.format(count, last, 'EOF'))
        video_clips.append(video.subclip(float(last)-EASE))

    processed_video = concatenate_videoclips(video_clips)
    processed_audio = concatenate_audioclips(audio_clips)
    combined = processed_video.set_audio(processed_audio)
    combined.write_videofile(
        file_name[:-4] + "_cut.mp4",
        audio_codec='aac',
        fps=20,
        preset='ultrafast',
        codec='libx264',
        threads=20
    )
    video.close()

    return file_name[:-4] + "_cut.mp4"
