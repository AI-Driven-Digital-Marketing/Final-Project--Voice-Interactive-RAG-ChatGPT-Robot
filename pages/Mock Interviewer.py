import streamlit as st
from streamlit_audio_recorder import st_audio_recorder

st.write('## Welcome :)')


audio_file = st_audio_recorder(start_recording=False, 
                               stop_recording=False, 
                               recording_time=5, 
                               sample_rate=44100, 
                               audio_type='wav')

if audio_file:
    st.audio(audio_file)


