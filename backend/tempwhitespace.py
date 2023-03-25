#!/usr/bin/env python

import sys
import subprocess
import os
import shutil
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips

# Input file path
file_in = sys.argv[1]
# Output file path
file_out = sys.argv[2]
# Silence timestamps
silence_file = sys.argv[3]

# Ease in duration between cuts
try:
    ease = float(sys.argv[4])
except IndexError:
    ease = 0.0

minimum_duration = 1.0

def main():
    # number of clips generated
    count = 0
    # start of next clip
    last = 0

    in_handle = open(silence_file, "r", errors='replace')
    video = VideoFileClip(file_in)
    audio = AudioFileClip(file_in)
    video.resize( (460,720) )
    full_duration = video.duration
    video_clips = []
    audio_clips = []
    while True:
        line = in_handle.readline()

        if not line:
            break

        end,duration = line.strip().split()

        if 'x' in end: continue
        to = float(end) - float(duration)

        start = float(last)
        
        clip_duration = float(to) - start
        # Clips less than one seconds don't seem to work
        print("Clip Duration: {} seconds".format(clip_duration))

        if clip_duration < minimum_duration:
            last = end
            continue

        if full_duration - to < minimum_duration:
            continue

        if start > ease:
            start -= ease

        print("Clip {} (Start: {}, End: {})".format(count, start, to))
        video_clip = video.subclip(start, to)
        video_clips.append(video_clip)
        audio_clip = audio.subclip(start, to)
        audio_clips.append(audio_clip)
        last = end
        count += 1

    if full_duration - float(last) > minimum_duration:
        print("Clip {} (Start: {}, End: {})".format(count, last, 'EOF'))
        video_clips.append(video.subclip(float(last)-ease))

    #TODO: multiproc thease two
    processed_video = concatenate_videoclips(video_clips)
    processed_audio = concatenate_audioclips(audio_clips)
    combined = processed_video.set_audio(processed_audio)
    combined.write_videofile(
        file_out,
        audio_codec='aac',
        fps=20,
        preset='ultrafast',
        codec='libx264',
        threads=20
    )

    in_handle.close()
    video.close()

main()