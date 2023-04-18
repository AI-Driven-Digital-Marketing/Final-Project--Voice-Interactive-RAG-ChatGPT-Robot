import streamlit as st
import numpy as np
from audio_recorder_streamlit import st_audio_recorder
st.selectbox('Select a mock interview', ['Mock Interviewer', 'Mock Interviewee'])

audio_file = st_audio_recorder(start_recording=False, 
                               stop_recording=False, 
                               recording_time=5, 
                               sample_rate=44100, 
                               audio_type='wav')


if audio_file:
    st.audio(audio_file)

audio_bytes = audio_file.read()

st.audio(audio_bytes, format='audio/ogg')

sample_rate = 44100  # 44100 samples per second
seconds = 2  # Note duration of 2 seconds
frequency_la = 440  # Our played note will be 440 Hz
# Generate array with seconds*sample_rate steps, ranging between 0 and seconds
t = np.linspace(0, seconds, seconds * sample_rate, False)
# Generate a 440 Hz sine wave
note_la = np.sin(frequency_la * t * 2 * np.pi)

st.audio(note_la, sample_rate=sample_rate)
