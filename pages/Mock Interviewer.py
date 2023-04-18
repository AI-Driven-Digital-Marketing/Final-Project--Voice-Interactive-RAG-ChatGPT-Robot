import streamlit as st
import numpy as np
from audio_recorder_streamlit import audio_recorder

audio_bytes = audio_recorder(
    text="Record your Questions",
    recording_color="#e8b62c",
    neutral_color="#6aa36f",
    icon_name="user",
    icon_size="6x",
)

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")


# sample_rate = 44100  # 44100 samples per second
# seconds = 2  # Note duration of 2 seconds
# frequency_la = 440  # Our played note will be 440 Hz
# # Generate array with seconds*sample_rate steps, ranging between 0 and seconds
# t = np.linspace(0, seconds, seconds * sample_rate, False)
# # Generate a 440 Hz sine wave
# note_la = np.sin(frequency_la * t * 2 * np.pi)

# st.audio(note_la, sample_rate=sample_rate)
