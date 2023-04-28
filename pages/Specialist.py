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



tab1, tab2, tab3 = st.tabs(["Internal", "External", "Private"])


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



#
with tab1: 
    docsearch, chain  = initialize()
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

with tab2:
    st.write('Hubspot')


with tab3: 
    form = st.form(key='myform')
    query = form.text_input( "Enter some text 👇",
        placeholder="Write your prompt here...",
    )
    submit = form.form_submit_button('Submit')
if submit:
    SQL_KEY = st.secrets['sql_key']
    OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']
    db_uri = "mysql+pymysql:" + SQL_KEY
    db = SQLDatabase.from_uri(db_uri)
    llm = OpenAI(temperature=0, openai_api_key= OPENAI_API_KEY)
    db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True) 
    # , return_intermediate_steps=True
    result = db_chain.run(query)
    # with st.expander("See Intermediate Steps here."):
    #     st.write(result["intermediate_steps"])
    st.write(result)



