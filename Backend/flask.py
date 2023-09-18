from flask import Flask, request, jsonify
import pandas as pd
import streamlit as st
import wave
import openai
import pinecone
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain import SQLDatabase, SQLDatabaseChain
from audio_recorder_streamlit import audio_recorder


app = Flask(__name__)
@app.route('/api/tab1', methods=['POST'])
def tab1():
    tab1_data = request.json  # 获取从新前端发送的数据

    # 复制和粘贴原始的Streamlit代码，确保缩进和代码逻辑保持一致

    # 替换st相关函数调用为Flask提供的函数
    default_input = ''
    audio_data = audio_recorder(pause_threshold=3.0, icon_size='2x', **tab1_data['audio_recorder_params'])

    # 在这里插入 tab1 代码块的其余部分

    # 将结果返回给新前端
    return jsonify(result)

@app.route('/api/tab2', methods=['POST'])
def tab2():
    tab2_data = request.json  # 获取从新前端发送的数据

    # 复制和粘贴原始的Streamlit代码，确保缩进和代码逻辑保持一致

    # 替换st相关函数调用为Flask提供的函数
    default_input = ''
    audio_data = audio_recorder(pause_threshold=3.0, icon_size='2x', **tab2_data['audio_recorder_params'])

    # 在这里插入 tab2 代码块的其余部分

    # 将结果返回给新前端
    return jsonify(result)

@app.route('/api/tab3', methods=['POST'])
def tab3():
    tab3_data = request.json  # 获取从新前端发送的数据

    # 复制和粘贴原始的Streamlit代码，确保缩进和代码逻辑保持一致

    # 替换st相关函数调用为Flask提供的函数
    default_input = ''
    audio_data = audio_recorder(pause_threshold=3.0, icon_size='2x', **tab3_data['audio_recorder_params'])

    # 在这里插入 tab3 代码块的其余部分

    # 将结果返回给新前端
    return jsonify(result)

def save_wav(audio_data):
    # save_wav 函数的代码

def transcribe(audio):
    # transcribe 函数的代码

@st.cache_resource
def initialize():
    # initialize 函数的代码

@st.cache_resource
def initialize_CRM():
    # initialize_CRM 函数的代码

def complete(prompt):
    # complete 函数的代码

limit = 4000
embed_model = "text-embedding-ada-002"

def retrieve(query):
    # retrieve 函数的代码

# 将下面的代码放在文件末尾以运行Flask应用程序
if __name__ == '__main__':
    app.run()