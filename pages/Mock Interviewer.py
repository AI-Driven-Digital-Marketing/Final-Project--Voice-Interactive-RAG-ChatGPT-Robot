import streamlit as st
import numpy as np
from st_custom_components import st_audiorec
import wave
import openai
import boto3
from streamlit_chat import message

# Continue the conversation
def continue_conversation(conversation_history, user_message):
    conversation_history.append({"role": "user", "content": user_message})


    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=conversation_history
    )

    assistant_message = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": assistant_message})
    
    return assistant_message

if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = [
        {"role": "system", "content": "You are a friendly interviewer."},
        {"role": "user", "content": """Let's do mock interview! You ask me a question, then I answer your question, 
                                        you ask more follow up question or start a new question.
                                        I will send you a job description and everything should be around that,
                                        excepts behavior question."""},
        {"role": "assistant", "content": "Got you! Please send me your Job Description."},
    ]

#Test
st.write(st.session_state)

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = ["Hey! Please enter your job description below then we can start the mock interview!"]

if len(st.session_state['chat_history']) == 1:
#User input the job description
    upload_text = st.text_area(label='Paste the job description here:', placeholder = 'accept job description')

    if st.button('Upload'):
        # st.session_state['conversation_history'].append({"role": "user", "content": upload_text})
        st.session_state['chat_history'].append('upload_text')
        message(st.session_state['chat_history'][-1],is_user=True)
        answer = continue_conversation( st.session_state['conversation_history'], upload_text)
        message(answer)
        

# save user input audio as .wav file
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

# transcribe audio to text using openai Whisper
def transcribe(audio):
    # model = initialize()
    openai.api_key = st.secrets['openai_key']
    audio_file= open("audio_file.wav", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript

# convert text to audio using aws Polly API
def TTS(text):
    polly_client = boto3.Session(
            aws_access_key_id=st.secrets['aws_access_key_id'],                     
            aws_secret_access_key=st.secrets['aws_secret_access_key'],
            region_name='us-east-1').client('polly')

    response = polly_client.synthesize_speech(VoiceId='Ruth',
                    OutputFormat='mp3', 
                    Text = text,
                    Engine = 'neural')
    speech = response['AudioStream'].read()
    # file = open('speech.mp3', 'wb')
    # file.write(speech)
    # file.close()
    return speech




# st.title("Audio Recorder")
audio_data = st_audiorec()
if audio_data is not None:
    # display audio data as received on the backend
    save_wav(audio_data)
    #st.audio(audio_data, format='audio/wav')
if st.button('Chat'):
    transcript = transcribe(audio_data)['text']
    st.session_state['chat_history'].append(str(transcript))
    answer = continue_conversation( st.session_state['conversation_history'], transcript)
    st.session_state['chat_history'].append(answer)
    out_audio = TTS(answer)
    st.audio(out_audio)


for i,v in enumerate(st.session_state['chat_history']):
    if i%2 == 1:
        message(v, is_user=True)
    else:
        message(v)


