import streamlit as st
from io import StringIO
import pandas as pd
from streamlit_chat import message
from langchain.agents import create_csv_agent
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.csv_loader import CSVLoader
# from langchain.vectorstores import FAISS
import tempfile
from datetime import datetime
import seaborn as sns
from pathlib import Path
from pandas_profiling import ProfileReport
from pandas_profiling.utils.cache import cache_zipped_file
from streamlit_pandas_profiling import st_profile_report
import sweetviz as sv
import streamlit.components.v1 as components


st.expander("About this app")
st.write(" ")
st.markdown(
"""
##### 1. Objective: 
Use natural language to query the enterprise private/production databases and output the SQL code.
##### 2. Quick Start!:
Write the prompt in the text input area/Record your business requirement audio to transcript and click submit.
##### 3. Anticipated Result: 
Then you can query the MySQL Database data based on any department business requirement in a remote MySQL server connection by incorporating OpenAI GPT model with Langchain to return the SQL query and results.

"""
)
tab1, tab2 = st.tabs(["Know your Data", "Chat with your data"])
user_api_key = st.sidebar.text_input(
    label="#### Your OpenAI API key 👇",
    placeholder="Paste your OpenAI API key, sk-",
    type="password")

uploaded_file = st.sidebar.file_uploader("Upload CSV file", type="csv")
if uploaded_file:
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(uploaded_file.read())

    llm = ChatOpenAI(temperature=0, openai_api_key=user_api_key)
    agent = create_csv_agent(llm=llm, path=temp_file.name, verbose=True)

    temp_file.close()


with tab1:
    with st.expander("Know your Data"):
        if uploaded_file:
            df2= pd.read_csv(temp_file.name,index_col=0)
            st.dataframe(df2)
        else:
            st.write("Please upload a CSV file to start the conversation.")

    with st.expander("Profiling your Data"):
        if uploaded_file:
            df2= pd.read_csv(temp_file.name,index_col=0)

            profile = ProfileReport(df2, title="Profile Report of your data", explorative=True)
            st_profile_report(profile)
            st.download_button(
            'Download  Report',
            data=profile.to_html(),
                file_name = 'Transactions.html',
            help='Click  to get you own insights!'
        )
        else:
            st.write("Please upload a CSV file to start the conversation.")


    with st.expander('Visualizing your Data'):
        st.write('Visualizing your Data')
        if uploaded_file is not None:
            df2 = pd.read_csv(temp_file.name,index_col=0)
            st.write("DataFrame:")
            st.write(print(type(df2)))

        try:
            st.write("Calling sv.analyze")
            analysis = sv.analyze(df2)
            st.write("Creating HTML report...")
            report_name = "Sweetviz_Report.html"
            analysis.show_html(report_name)

            st.write("Displaying Sweetviz report...")
            HtmlFile = open(report_name, 'r', encoding='utf-8')
            source_code = HtmlFile.read()
            components.v1.html(source_code, height=600, width=800)

        except Exception as e:
            st.write("Error in Sweetviz analyze:")
            st.write(e)



with tab2:
        def conversational_chat(query, history):
            inputs = {
                "input": query,
                "chat_history": history
            }
            result = agent(inputs)
            
            response = ""
            if "choices" in result:
                response = result["choices"][0]["message"]["content"]
            elif "response" in result:
                response = result["response"]
            elif "output" in result:
                response = result["output"]
                
            history.append((query, response))
            return response


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
                output = conversational_chat(user_input, st.session_state['history'])
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)


        if st.session_state['generated']:
            with response_container:
                for i in range(len(st.session_state['generated'])):
                    message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                    message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")

