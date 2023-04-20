import streamlit as st
import numpy as np
from st_custom_components import st_audiorec
import wave
import openai
import boto3

# input GUI for user
col1, col2 = st.columns(2)

# save user input audio as .wav file
def save_wav(audio_data):
    nchannels = 1
    sampwidth = 2
    framerate = 48000*2
    nframes = len(audio_data) // sampwidth
    comptype = "NONE"
    compname = "not compressed"

    # Create a new .wav file and write the audio data to it
    with wave.open("audio_file.wav", "wb") as audio_file:
        audio_file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
        audio_file.writeframes(audio_data)

# transcribe audio to text using openai Whisper
def transcribe(audio):
    # model = initialize()
    openai.api_key = st.secrets['openai_key']
    audio_file= open("audio_file.wav", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript

# convert text to audio using aws Polly API
def TTS():
    polly_client = boto3.Session(
            aws_access_key_id=st.secrets['aws_access_key_id'],                     
            aws_secret_access_key=st.secrets['aws_secret_access_key'],
            region_name='us-east-1').client('polly')

    response = polly_client.synthesize_speech(VoiceId='Ruth',
                    OutputFormat='mp3', 
                    Text = 'This is a sample text to be synthesized.',
                    Engine = 'neural')
    speech = response['AudioStream'].read()
    file = open('speech.mp3', 'wb')
    file.write(speech)
    file.close()
    return speech

with col1:
    st.title("Audio Recorder")
    st.write("Click the button below to record your voice")
    audio_data = st_audiorec()

    if audio_data is not None:
        # display audio data as received on the backend
        save_wav(audio_data)
        #st.audio(audio_data, format='audio/wav')
        


with col2:

    st.title("Transcript")
    st.write("Click the button below to get the transcript")
    if st.button("Transcript"):
    #    st.text_input(transcribe(audio_data)['text'])     
       transcript_input = st.text_input("Adjust transcript", transcribe(audio_data)['text'])
       st.write("Prompt:", transcript_input)
    
