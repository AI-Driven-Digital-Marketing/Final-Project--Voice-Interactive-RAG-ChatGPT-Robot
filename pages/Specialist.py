import streamlit as st
import pandas as pd
import wave
import openai
import pinecone
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain import SQLDatabase, SQLDatabaseChain
from audio_recorder_streamlit import audio_recorder




tab1, tab2, tab3 = st.tabs(["Domain Data Q&A", "Knowledge Base Q&A", "Private Database Query"])


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

@st.cache_resource
def initialize_CRM():
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
        "Answer the question based on the context below. If not related, ignore it.\n\n"+
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


default_input= ''
audio_data = audio_recorder(pause_threshold=3.0, icon_size = '2x')
with tab1: 
    st.write('External Data(Fintech & Healthcare))')
    docsearch, chain  = initialize()
    if audio_data is not None:
        # display audio data as received on the backend
        save_wav(audio_data)
        default_input = transcribe(audio_data)['text']
    form = st.form(key='myform1')
    query = form.text_input( "Let's ask any questions about crpto or nanomedicine/covid 👇",
        placeholder="Write your prompt here...",
        value= default_input
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
    st.write('Hubspot Company Knowledge Base (Internal-Public)')
    index = initialize_CRM()
    if audio_data is not None:
        # display audio data as received on the backend
        save_wav(audio_data)
        default_input = transcribe(audio_data)['text']
    form = st.form(key='myform2')
    query2 = form.text_input( "Ask how to use CRM 👇",
        placeholder="Write your prompt here...",
        value= default_input
    )
    submit2 = form.form_submit_button('Submit')
    if submit2:
        # get context, additional info from pinecone
        query_with_contexts = retrieve(query2)
        # call openai API
        output = complete(query_with_contexts)
        with st.expander("See contexts prompt from the RAG"):
            st.write(query_with_contexts)
        st.write(output)

with tab3:
    st.write('Enterprise Private/Production Database Query (Internal-Private)')
    form = st.form(key='myform3')
    query = form.text_input( "Query your data based on business requirment 👇",
        placeholder="Write your prompt here...",
        value= default_input
    )
    submit = form.form_submit_button('Submit')
    if submit:
        SQL_KEY = st.secrets['sql_key']
        OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']
        db_uri = "mysql+pymysql:" + SQL_KEY
        db = SQLDatabase.from_uri(db_uri)
        llm = OpenAI(temperature=0, openai_api_key= OPENAI_API_KEY)
        db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True,return_intermediate_steps=True) 
        result = db_chain(query)
        with st.expander("See Generative SQL Query here."):
            st.markdown("```sql\n{}\n```".format(result["intermediate_steps"][0]))
        result_data = result["intermediate_steps"][1]
        df = pd.DataFrame(
            result_data,
            columns=('col %d' % i for i in range(len(result_data[0]))))
        st.write(df)



