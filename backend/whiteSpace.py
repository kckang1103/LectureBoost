import binascii
import math

import matplotlib.pyplot as plt
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


def openMP4File(filename):
    """
    Open .mp4 file and read in binary stream.
    :param filename: (str) path to the .mp4
    :return:
        hexGroups: (list(str)) list of 16 byte hex strings
        hexOffsets: (list(str)) corresponding list of offsets for each 16 byte hex string
    """
    with open(file=filename, mode="rb") as file:
        contents = file.read()
    numBytes = len(contents)
    hexGroups = []
    hexOffsets = []

    for i in range(0, numBytes, 16):
        hexString = str(binascii.hexlify(contents[i:i+16]))
        hexGroups.append(hexString[2:-1])
        hexOffsets.append(i)

    return hexGroups, hexOffsets


def createHexViewer(hexGroups, hexOffsets):
    """
    Create table layout of 16 byte hex strings, their offset from the start of the file, and their ASCII values.
    :param hexGroups: (list(str)) list of 16 byte hex strings
    :param hexOffsets: (list(str)) corresponding list of offsets for each 16 byte hex string
    :return:
        hexViewer: (str) table layout
    """
    hexViewer = ""
    hexViewer += """
            offset   | 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 |   ASCII
            ---------|-------------------------------------------------|--------
                """
    for count, group in enumerate(hexGroups):
        # Get ascii string
        asciiString = str(binascii.unhexlify(group))
        asciiString = asciiString.replace("b", "")
        asciiString = asciiString.replace("'", "")
        asciiString = asciiString.replace("\\x00", ".")

        # Get offset
        offset = str(hexOffsets[count]).rjust(8, '0')

        # Get hex digits
        byteOne = group[:2]
        byteTwo = group[2:4]
        byteThree = group[4:6]
        byteFour = group[6:8]
        byteFive = group[8:10]
        byteSix = group[10:12]
        byteSeven = group[12:14]
        byteEight = group[14:16]
        byteNine = group[16:18]
        byteTen = group[18:20]
        byteEleven = group[20:22]
        byteTwelve = group[22:24]
        byteThirteen = group[24:26]
        byteFourteen = group[26:28]
        byteFifteen = group[28:30]
        byteSixteen = group[30:32]
        nextRow = """
            {0} | {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11} {12} {13} {14} {15} {16} | {string}
            """.format(offset, byteOne, byteTwo, byteThree, byteFour, byteFive, byteSix, byteSeven, byteEight,
                       byteNine, byteTen, byteEleven, byteTwelve, byteThirteen, byteFourteen, byteFifteen,
                       byteSixteen, string=asciiString)
        hexViewer += nextRow

    return hexViewer


def getWavData(filename):
    """
    Open .wav file and retrieve its data not including headers.
    :param filename: (str) path to .wav
    :return: (bytes) return binary following the "data" tag and length in the .wav header
    """
    with open(filename, 'rb') as file:
        s = file.read()

    dataTag = 4
    dataLenTag = 4
    return s[s.find(b'data')+dataTag+dataLenTag:]


def getWavSamples(wavData):
    """
    Retrieve audio samples from a .wav file, given its binary audio data.
    :param wavData: (bytes) binary representation of .wav audio data. Expected to only include data, not any headers.
    :return: All returned lists have the same length
        byteNumbers: (list(int)) position number of each byte, corresponding to the samples
        sampleNumbers: (list(float)) position number of each sample, corresponding to the samples
        binarySamples: (list(bytes)) values of each sample in binary
        decimalSamples: (list(int)) values of each sample in decimal
    """
    byteNumbers = []
    sampleNumbers = []
    binarySamples = []
    decimalSamples = []
    for i in range(0, len(wavData), 4):
        sample = wavData[i:i+2]
        byteNumbers.append(i)
        sampleNumbers.append(i / 4)
        binarySamples.append(sample)
        decimalSamples.append(int.from_bytes(sample, byteorder="little"))
    return byteNumbers, sampleNumbers, binarySamples, decimalSamples


def decimalAudioValuesToRelativeDecibels(samples, maxVolume):
    """
    Convert audio sample values to relative decibels.
    :param samples: (list(int)) decimal values of audio samples
    :param maxVolume: (int) maximum audio sample
    :return: len(decibels) == len(samples)
        decibels: (list(float)) decibels values of audio samples
    """
    decibels = []
    for sample in samples:
        decibels.append(20 * math.log10(abs(sample)+1 / maxVolume))
    return decibels


def byteNumbersToSeconds(byteNumbers):
    """
    Convert byte position numbers to time in seconds.
    :param byteNumbers: (list(int)) position number of each byte, corresponding to the samples
    :return: len(byteNumbers) == len(timestamps)
        timestamps: (list(float)) fraction of a second at which each byte in the .wav data occurs
    """
    timestamps = []
    for byte in byteNumbers:
        timestamps.append(byte / 176400)
    return timestamps


def createGraph(x, y, xaxis, yaxis, title):
    plt.plot(x, y)
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)
    plt.title(title)
    plt.show()


def getLowDecibelTimestamps(timestamps, decibels):
    lowTimestamps = set()
    threshold = 25
    for count, timestamp in enumerate(timestamps):
        if decibels[count] < threshold:
            lowTimestamps.add(round(timestamp, 3))

    lowTimestampsSorted = [elem for elem in lowTimestamps]
    lowTimestampsSorted.sort()
    start = lowTimestampsSorted[0]
    end = lowTimestampsSorted[0]
    lowRanges = []
    for timestamp in lowTimestampsSorted:
        if timestamp != start:
            if timestamp <= end + .01:
                end = timestamp
            else:
                if end - start > 0.5:
                    lowRanges.append((start, end))
                start = timestamp
                end = timestamp
    return lowRanges


def cutoutRangeToSubclipRange(cutoutRange):
    subclipRange = []
    start = 0
    runningSum = 0
    for range in cutoutRange:
        end = range[0]
        deltax = end - start
        if deltax != 0:
            subclipRange.append((start, end))
        start = range[1]

    return subclipRange


def cutoutVideo(inFile, outFile, timestamps):
    video = VideoFileClip(inFile)
    audio = AudioFileClip(inFile)

    runningSum = 0
    for startTime, endTime in timestamps:
        video = video.cutout(startTime - runningSum, endTime - runningSum)
        audio = audio.cutout(startTime - runningSum, endTime - runningSum)
        runningSum += (endTime - startTime)
    new_audio = CompositeAudioClip([audio])
    video.audio = new_audio
    video.write_videofile(outFile, audio=True, fps=video.fps, temp_audiofile="temp-audio.m4a",
                          remove_temp=True, codec="libx264", audio_codec="aac")


def ffmpegSubclipVideo(inFile, outFolder, timestamps):
    # runningSum = 0
    for count, (startTime, endTime) in enumerate(timestamps):
        outFile = outFolder + str(count) + ".mp4"
        ffmpeg_extract_subclip(inFile, startTime, endTime, targetname=outFile)
    path = os.getcwd() + "/videos/"
    fileNames = [name for name in os.listdir(path)]  # Filtering only the files.
    clips = []
    for fileName in fileNames:
        if "mp4" in fileName:
            clips.append(VideoFileClip(path + fileName))
    video = CompositeVideoClip(clips=clips)
    # video = concatenate_videoclips(clips)
    video.write_videofile("outVideo.mp4", audio=True, fps=video.fps, temp_audiofile="temp-audio.m4a",
                      remove_temp=True, codec="libx264", audio_codec="aac")
    # runningSum += (endTime - startTime)


def subclipVideo(inFile, outFile, timestamps):
    video = VideoFileClip(inFile)
    audio = AudioFileClip(inFile)

    videos = []
    audios = []
    for startTime, endTime in timestamps:
        videos.append(video.subclip(startTime, endTime))
        audios.append(audio.subclip(startTime, endTime))
    # new_audios = CompositeAudioClip(audios)
    # new_videos = CompositeVideoClip(videos)
    final_audios = concatenate_audioclips(audios)
    final_videos = concatenate_videoclips(videos)
    final_videos.audio = final_audios
    #new_videos.audio = new_audios
    final_videos.write_videofile(outFile, audio=True, fps=video.fps, temp_audiofile="temp-audio.m4a",
                          remove_temp=True, codec="libx264", audio_codec="aac")


def removeWhiteSpace(folderName, videoName):
    # Retrieve .wav set of samples
    audioName = videoName[:-4] + "_audio.wav"
    audioClip = AudioFileClip(folderName + videoName)
    audioClip.write_audiofile(folderName + audioName)
    wavData = getWavData(folderName + audioName)
    byteNumbers, sampleNumbers, binSamples, decSamples = getWavSamples(wavData)

    # Convert .wav data (decimal audio values -> relative decibels) (byte numbers -> seconds)
    relativeDecibels = decimalAudioValuesToRelativeDecibels(samples=decSamples, maxVolume=max(decSamples))
    timestamps = byteNumbersToSeconds(byteNumbers=byteNumbers)

    # Get timestamps to use in cutting
    cutoutRange = getLowDecibelTimestamps(timestamps=timestamps, decibels=relativeDecibels)  # timestamp ranges less than threshold
    subclipRange = cutoutRangeToSubclipRange(cutoutRange)  # timestamp ranges greater than threshold
    subclipVideo(inFile=folderName + videoName, outFile=folderName + videoName[:-4] + "_cut.mp4", timestamps=subclipRange)

if __name__ == "__main__":
    removeWhiteSpace(folderName="uploads/", videoName="10_sec.mp4")
