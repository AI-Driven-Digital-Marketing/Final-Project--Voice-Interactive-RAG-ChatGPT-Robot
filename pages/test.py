from streamlit_chat import message
import streamlit as st
import boto3


def TTS(text):
    polly_client = boto3.Session(
            aws_access_key_id='AKIAWF3N7LA6NVW422NZ',                     
            aws_secret_access_key='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',
            region_name='us-east-1').client('polly')

    response = polly_client.synthesize_speech(VoiceId='Ruth',
                    OutputFormat='mp3', 
                    Text = text,
                    Engine = 'neural')
    speech = response['AudioStream'].read()
    file = open('speech.mp3', 'wb')
    file.write(speech)
    file.close()
    return speech



input = st.text_input(label='test-input')
if st.button('click'):
    out_audio = TTS(input)
    st.audio(out_audio)