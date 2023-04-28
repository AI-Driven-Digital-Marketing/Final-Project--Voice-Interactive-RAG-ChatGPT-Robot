import streamlit as st
import numpy as np
from st_custom_components import st_audiorec
import openai


def transcribe(audio):
    # model = initialize()
    openai.api_key = st.secrets['openai_key']
    #audio_file= open("audio_file.wav", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio)
    return transcript

audio_data = st_audiorec()

if st.button('Chat') and audio_data is not None:
    test_text = transcribe(audio_data)
    st.write(test_text)