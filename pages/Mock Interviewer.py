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
    st.audio(audio_bytes, format="audio/wav",sample_rate=44100)



