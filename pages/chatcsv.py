#pip install streamlit langchain openai faiss-cpu tiktoken

import streamlit as st
from io import StringIO
import pandas as pd
from streamlit_chat import message
from langchain.agents import create_csv_agent
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
import tempfile


import streamlit as st
from streamlit_chat import message
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS
from langchain.document_loaders.csv_loader import CSVLoader
import tempfile
from io import StringIO
import pandas as pd

user_api_key = st.sidebar.text_input(
    label="#### Your OpenAI API key 👇",
    placeholder="Paste your OpenAI API key, sk-",
    type="password")

uploaded_file = st.sidebar.file_uploader("Upload CSV file", type="csv")

if uploaded_file:
    csv_data = StringIO(uploaded_file.getvalue().decode('utf-8'))
    data = pd.read_csv(csv_data)

    llm = ChatOpenAI(temperature=0, openai_api_key=user_api_key)
    agent = create_csv_agent(llm=llm, data=data, verbose=True)

    def conversational_chat(query):
        result = agent({"text": query, "chat_history": st.session_state['history']})
        st.session_state['history'].append((query, result["response"]))
        return result["response"]

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask me anything about the CSV file 🤗"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey! 👋"]

    response_container = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Query:", placeholder="Talk about your CSV data here (:",
                                       key='input')
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            output = conversational_chat(user_input)
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")
