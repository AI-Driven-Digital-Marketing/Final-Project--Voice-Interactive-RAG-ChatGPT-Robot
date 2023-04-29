# import the libraries
import openai
import pinecone
import streamlit as st
import json
from random import random
from time import sleep
import pandas as pd
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
                'id': 'CRM_'+str(int(random()*6)),
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
    st.write('Success!')


out = [(1002, 'Murphy', 'Diane', None, 'President', 0), (1056, 'Patterson', 'Mary', 1002, 'VP Sales', 1), (1076, 'Firrelli', 'Jeff', 1002, 'VP Marketing', 1), (1102, 'Bondur', 'Gerard', 1056, 'Sale Manager (EMEA)', 2), (1143, 'Bow', 'Anthony', 1056, 'Sales Manager (NA)', 2), (1621, 'Nishi', 'Mami', 1056, 'Sales Rep', 2), (1088, 'Patterson', 'William', 1056, 'Sales Manager (APAC)', 2), (1401, 'Castillo', 'Pamela', 1102, 'Sales Rep', 3), (1286, 'Tseng', 'Foon Yue', 1143, 'Sales Rep', 3), (1501, 'Bott', 'Larry', 1102, 'Sales Rep', 3), (1323, 'Vanauf', 'George', 1143, 'Sales Rep', 3), (1504, 'Jones', 'Barry', 1102, 'Sales Rep', 3), (1625, 'Kato', 'Yoshimi', 1621, 'Sales Rep', 3), (1611, 'Fixter', 'Andy', 1088, 'Sales Rep', 3), (1702, 'Gerard', 'Martin', 1102, 'Sales Rep', 3), (1612, 'Marsh', 'Peter', 1088, 'Sales Rep', 3), (1165, 'Jennings', 'Leslie', 1143, 'Sales Rep', 3), (1619, 'King', 'Tom', 1088, 'Sales Rep', 3), (1166, 'Thompson', 'Leslie', 1143, 'Sales Rep', 3), (1337, 'Bondur', 'Loui', 1102, 'Sales Rep', 3), (1188, 'Firrelli', 'Julie', 1143, 'Sales Rep', 3), (1370, 'Hernandez', 'Gerard', 1102, 'Sales Rep', 3), (1216, 'Patterson', 'Steve', 1143, 'Sales Rep', 3)]
df = pd.DataFrame(
   out,
   columns=('col %d' % i for i in range(len(out[0]))))
st.table(out)