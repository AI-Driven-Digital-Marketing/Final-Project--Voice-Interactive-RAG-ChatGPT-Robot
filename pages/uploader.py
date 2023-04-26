# import the libraries
import openai
import pinecone
import streamlit as st
import json
from random import random
from time import sleep

#defining DAG arguments
@st.cache_resource 
def initial_pinecone():
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
            metric='cosine'
           # metadata_config={'indexed': ['title']}
        )
    # check if index already exists (it shouldn't if this is first time)
    if index_name not in pinecone.list_indexes():
        # if does not exist, create index
        pinecone.create_index(
            index_name,
            dimension=1536,
            metric='cosine',
            metadata_config={'indexed': ['source']}
        )
    # connect to index
    index = pinecone.Index(index_name)
    # view index stats
    index.describe_index_stats()
    return index



def processing_article(arti):
    result = []
    content = arti
    sentence = ''
    for t in content.split('\n\n'):
        sentence += t+'\n'
        if len(sentence)>1000:
            result.append({
                'id': int(random()*6),
                'text':sentence
                })
            sentence = ''
    return result


def load2pinecone(sentences):
    openai.api_key = st.secrets['openai_key']
    index = initial_pinecone()
    embed_model = "text-embedding-ada-002"
    batch_size = 50  # how many embeddings we create and insert at once

    for i in range(0, len(sentences), batch_size):
        # find end of batch
        i_end = min(len(sentences), i+batch_size)
        meta_batch = sentences[i:i_end]
        # get ids
        ids_batch = [x['id'] for x in meta_batch]
        # get texts to encode
        texts = [x['text'] for x in meta_batch]
        # create embeddings (try-except added to avoid RateLimitError)
        try:
            res = openai.Embedding.create(input=texts, engine=embed_model)
        except:
            done = False
            while not done:
                sleep(5)
                try:
                    res = openai.Embedding.create(input=texts, engine=embed_model)
                    done = True
                except:
                    pass
        embeds = [record['embedding'] for record in res['data']]
        # cleanup metadata
        meta_batch = [{
            'text': x.get('text','NaN')
        } for x in meta_batch]
        to_upsert = list(zip(ids_batch, embeds, meta_batch))
        # upsert to Pinecone
        index.upsert(vectors=to_upsert)

upload_text = st.text_area(label='Paste your text here:', placeholder = 'accept plain text...')

if st.button('Upload'):
    processed_text = processing_article(upload_text)
    load2pinecone(processed_text)