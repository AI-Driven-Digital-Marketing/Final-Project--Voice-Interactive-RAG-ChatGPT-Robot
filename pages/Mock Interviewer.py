import streamlit as st
import numpy as np
from audiorecorder import audiorecorder


st.title("Audio Recorder")
audio = audiorecorder("Click to record", "Stop Recording...")

if len(audio) > 0:
    # To play audio in frontend:
    st.audio(audio.tobytes())
    
    # To save audio to a file:
    wav_file = open("audio.mp3", "wb")
    wav_file.write(audio.tobytes())
