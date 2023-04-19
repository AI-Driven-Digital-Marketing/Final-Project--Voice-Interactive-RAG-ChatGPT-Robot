import streamlit as st
import numpy as np
from st_custom_components import st_audiorec
# import whisper

# from audiorecorder import audiorecorder
# audio = audiorecorder("Click to record", "Stop Recording...")

# if len(audio) > 0:
#     # To play audio in frontend:
#     st.audio(audio.tobytes())
    
#     # To save audio to a file:
#     wav_file = open("audio.mp3", "wb")
#     wav_file.write(audio.tobytes())
# input GUI for user
_,col1,_ = st.columns([1,6,1])
_,col2,_ = st.columns([1,6,1])
col1, col2 = st.columns(2,gap = "medium")

with col1:
    st.title("Audio Recorder")
    st.write("Click the button below to record your voice")
    audio_data = st_audiorec()

    if audio_data is not None:
        # display audio data as received on the backend
        st.audio(audio_data, format='audio/wav')
        # INFO: by calling the function an instance of the audio recorder is created
        # INFO: once a recording is completed, audio data will be saved to wav_audio_data
# with col2:
# # wav_audio_data
#     model = whisper.load_model("base")
#     def transcribe(audio):
#         # load audio and pad/trim it to fit 30 seconds
#         audio = whisper.load_audio(audio)
#         audio = whisper.pad_or_trim(audio)

#         # make log-Mel spectrogram and move to the same device as the model
#         mel = whisper.log_mel_spectrogram(audio_data).to(model.device)

#         # detect the spoken language
#         _, probs = model.detect_language(mel)
#         print(f"Detected language: {max(probs, key=probs.get)}")

#         # decode the audio
#         options = whisper.DecodingOptions()
#         result = whisper.decode(model, mel, options)
#         return result.text
#     st.title("Transcript")
#     st.write("Click the button below to get the transcript")
#     st.button("Transcript")
#     st.text_input(transcribe(audio_data))
    