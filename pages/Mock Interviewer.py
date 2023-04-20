import streamlit as st
import numpy as np
from st_custom_components import st_audiorec
#import whisper
import wave
import openai
# from audiorecorder import audiorecorder
# audio = audiorecorder("Click to record", "Stop Recording...")

# if len(audio) > 0:
#     # To play audio in frontend:
#     st.audio(audio.tobytes())
    
#     # To save audio to a file:
#     wav_file = open("audio.mp3", "wb")
#     wav_file.write(audio.tobytes())
# input GUI for user
col1, col2 = st.columns(2,gap = "medium")

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



with col1:
    st.title("Audio Recorder")
    st.write("Click the button below to record your voice")
    audio_data = st_audiorec()

    if audio_data is not None:
        # display audio data as received on the backend
        save_wav(audio_data)
        st.audio(audio_data, format='audio/wav')
        
# @st.cache_resource
# def initialize():
#     model = whisper.load_model("base")
#     return model
# wav_audio_data
def transcribe(audio):
    # model = initialize()
    openai.api_key = st.secrets['openai_key']
    audio_file= open("audio_file.wav", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript

with col2:

    st.title("Transcript")
    st.write("Click the button below to get the transcript")
    if st.button("Transcript"):
       st.write(transcribe(audio_data))
    
