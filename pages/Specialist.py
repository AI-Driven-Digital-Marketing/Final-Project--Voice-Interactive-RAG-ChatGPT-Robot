import streamlit as st
import numpy as np
import pandas as pd
from st_custom_components import st_audiorec
import wave
import openai
import pinecone
import os 
import pymysql
# import langchain
# from langchain.llms import OpenAI
# from langchain.chains.question_answering import load_qa_chain
# from langchain import OpenAI, SQLDatabase, SQLDatabaseChain


# input GUI for user
col1, col2 = st.columns(2)

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

def transcribe(audio):
    # model = initialize()
    openai.api_key = st.secrets['openai_key']
    audio_file= open("audio_file.wav", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript

@st.cache_resource
def initialize():
    openai.api_key = st.secrets['openai_key']
    index_name = 'openai-embedding-data'

    # initialize connection to pinecone (get API key at app.pinecone.io)
    pinecone.init(
        api_key=st.secrets['pinecone_key'],
        environment=st.secrets['pinecone_region']  # may be different, check at app.pinecone.io
    )

    # check if index already exists (it shouldn't if this is first time)
    if index_name not in pinecone.list_indexes():
        # if does not exist, create index
        pinecone.create_index(
            index_name,
            dimension=1536,
            metric='cosine',
            metadata_config={'indexed': ['title']}
        )
    # connect to index
    index = pinecone.Index(index_name)
    return index
index = initialize()

def complete(prompt):
    # query text-davinci-003
    res = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        temperature=0,
        max_tokens=400,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    return res['choices'][0]['text'].strip()


limit = 4000
embed_model = "text-embedding-ada-002"
def retrieve(query):
    res = openai.Embedding.create(
        input=[query],
        engine=embed_model
    )

    # retrieve from Pinecone
    xq = res['data'][0]['embedding']

    # get relevant contexts
    res = index.query(xq, top_k=3, include_metadata=True)
    contexts = [
        x['metadata']['text'] for x in res['matches']
    ]

    # build our prompt with the retrieved contexts included
    prompt_start = (
        "Answer the question based on the context below.\n\n"+
        "Context:\n"
    )
    prompt_end = (
        f"\n\nQuestion: {query}\nAnswer:"
    )
    # append contexts until hitting limit
    for i in range(1, len(contexts)):
        if len("\n\n---\n\n".join(contexts[:i])) >= limit:
            prompt = (
                prompt_start +
                "\n\n---\n\n".join(contexts[:i-1]) +
                prompt_end
            )
            break
        elif i == len(contexts)-1:
            prompt = (
                prompt_start +
                "\n\n---\n\n".join(contexts) +
                prompt_end
            )
    return prompt

with col1:
    st.title("Audio Recorder")
    st.write("Click the button below to record your voice")
    audio_data = st_audiorec()

    if audio_data is not None:
        # display audio data as received on the backend
        save_wav(audio_data)
        #st.audio(audio_data, format='audio/wav')
        


with col2:

    st.title("Transcript")
    st.write("Click the button below to get the transcript")
    if st.button("Transcript"):
       st.write(transcribe(audio_data)['text'])
    


_,col3,_ = st.columns([1,8,1])
with col3: 
    form = st.form(key='myform')
    query = form.text_input( "Enter some text 👇",
        placeholder="Write your prompt here...",
    )
    submit = form.form_submit_button('Submit')
if submit:
    # get context, additional info from pinecone
    query_with_contexts = retrieve(query)
    # call openai API
    output = complete(query_with_contexts)
    with st.expander("See contexts prompt from the RAG"):
        st.write(query_with_contexts)
    st.write(output)
