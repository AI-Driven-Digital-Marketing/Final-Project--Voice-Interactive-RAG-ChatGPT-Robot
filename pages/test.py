from streamlit_chat import message
import streamlit as st
import openai

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = ["Hey!"]

input = st.text_input(label='test-input')
if st.button('click'):
    st.session_state['chat_history'].append(input)
#Mock interivew promot, still under working
st.write(st.session_state['chat_history'] )
