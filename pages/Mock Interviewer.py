import streamlit as st
import numpy as np
from audiorecorder import audiorecorder

# audio_bytes = audio_recorder(
#     text="Record your Questions",
#     recording_color="#e8b62c",
#     neutral_color="#6aa36f",
#     icon_name="user",
#     icon_size="6x",
# )

# if audio_bytes:
#     st.audio(audio_bytes, format="audio/wav",sample_rate=44100)



st.title("Audio Recorder")
audio = audiorecorder("Click to record", "Recording...")

if len(audio) > 0:
    # To play audio in frontend:
    st.audio(audio.tobytes())
    
    # To save audio to a file:
    wav_file = open("audio.mp3", "wb")
    wav_file.write(audio.tobytes())
