from moviepy.editor import *

from deepgram import Deepgram

MIMETYPE = 'audio/wav'

def transcribe(video_file):
    # Initializes the Deepgram SDK
    dg_client = Deepgram(os.getenv('DEEPGRAM_API_KEY'))
    
    transcription_file = "./uploads/transcription.txt"
    transcribed_audio_file = "./uploads/transcribed_speech.wav"

    # get the audio clip from the video
    audio_clip = AudioFileClip(video_file)
    audio_clip.write_audiofile(transcribed_audio_file)
    
    with open(transcribed_audio_file, 'rb') as audio:
        source = {'buffer': audio, 'mimetype': MIMETYPE}
        options = { "paragraphs": True, "punctuate": True, "model": "general", "language": "en-US", "tier": "enhanced" }
    
        print('Requesting transcript from Deepgram...')
    
        response = dg_client.transcription.sync_prerecorded(source, options)
        paragraphs = response['results']['channels'][0]['alternatives'][0]['paragraphs']['paragraphs']
        
        open(transcription_file, 'w').close()
        f = open(transcription_file, "a")
        
        for paragraph in paragraphs:

          start_min, start_sec = divmod(paragraph['start'], 60)
          end_min, end_sec = divmod(paragraph['end'], 60)
          
          time_stamp = "{0:02d}:{1:02d} - {2:02d}:{3:02d}\n".format(int(start_min), int(start_sec), int(end_min), int(end_sec))
          f.write(time_stamp)
          
          for sentence in paragraph['sentences']:
            f.write(sentence['text'])
            f.write('\n')
          
          f.write('\n\n')
          
        f.close()
