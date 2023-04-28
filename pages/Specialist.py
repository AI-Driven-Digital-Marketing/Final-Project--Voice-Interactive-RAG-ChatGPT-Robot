import streamlit as st
import numpy as np
import pandas as pd
from st_custom_components import st_audiorec
import wave
import openai
import pinecone
import os 
import pymysql
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain import SQLDatabase, SQLDatabaseChain
import langchain
import sqlalchemy



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
    openai.api_key = st.secrets['OPENAI_API_KEY']
    audio_file= open("audio_file.wav", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript

@st.cache_resource
def initialize():
    index_name = "langchain2"

    # initialize connection to pinecone (get API key at app.pinecone.io)
    pinecone.init(
        api_key=st.secrets['PINECONE_API_KEY'],
        environment=st.secrets['PINECONE_API_ENV']  # may be different, check at app.pinecone.io
    )
    OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    docsearch = Pinecone.from_existing_index(index_name, embeddings)
    # connect to index
    llm = OpenAI(temperature=0.5, openai_api_key=OPENAI_API_KEY )
    chain = load_qa_chain(llm, chain_type="stuff")

    return docsearch, chain
docsearch, chain  = initialize()


# with col1:
#     st.title("Audio Recorder")
#     st.write("Click the button below to record your voice")
#     audio_data = st_audiorec()

#     if audio_data is not None:
#         # display audio data as received on the backend
#         save_wav(audio_data)
#         #st.audio(audio_data, format='audio/wav')
    
# with col2:

#     st.title("Transcript")
#     st.write("Click the button below to get the transcript")
#     if st.button("Transcript"):
#        st.write(transcribe(audio_data)['text'])
col1, col2 = st.columns(2)
# _,col3,_ = st.columns([1,8,1])
with col1: 
    form = st.form(key='myform1')
    query = form.text_input( "Enter some text 👇",
        placeholder="Write your prompt here...",
    )
    submit = form.form_submit_button('Submit')
if submit:
    # get context, additional info from pinecone
    docs = docsearch.similarity_search(query= query, include_metadata=True)
    # call openai API
    result = chain.run(input_documents=docs, question=query)
    with st.expander("See searched docs here."):
        st.write(docs)
    st.write(result)

# _,col4,_ = st.columns([1,8,1])
with col2: 
    form = st.form(key='myform')
    query = form.text_input( "Enter some text 👇",
        placeholder="Write your prompt here...",
    )
    submit = form.form_submit_button('Submit')
if submit:
    SQL_KEY = st.secrets['sql_key']
    db_uri = "mysql+pymysql://" + SQL_KEY
    db = SQLDatabase.from_uri(db_uri)
    llm = OpenAI(temperature=0, openai_api_key= OPENAI_API_KEY)
    db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True) 
    result = db_chain.run(query)
    st.write(result)


