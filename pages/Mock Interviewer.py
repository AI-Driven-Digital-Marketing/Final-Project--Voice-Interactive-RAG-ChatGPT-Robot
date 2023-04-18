import streamlit as st
import numpy as np
from st_custom_components import st_audiorec
# from audiorecorder import audiorecorder
# audio = audiorecorder("Click to record", "Stop Recording...")

# if len(audio) > 0:
#     # To play audio in frontend:
#     st.audio(audio.tobytes())
    
#     # To save audio to a file:
#     wav_file = open("audio.mp3", "wb")
#     wav_file.write(audio.tobytes())
st.title("Audio Recorder")
st.write("Click the button below to record your voice")
wav_audio_data = st_audiorec()

if wav_audio_data is not None:
    # display audio data as received on the backend
    st.audio(wav_audio_data, format='audio/wav')
    
# INFO: by calling the function an instance of the audio recorder is created
# INFO: once a recording is completed, audio data will be saved to wav_audio_data