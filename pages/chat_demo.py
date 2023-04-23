from streamlit_chat import message
import streamlit as st
import openai
# get API key from top-right dropdown on OpenAI website
openai.api_key = st.secrets['openai_key']
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = [
        {"role": "system", "content": "You are a friendly interviewer."},
        {"role": "user", "content": """Let's do mock interview! You ask me a question, then I answer your question, 
                                        you ask more follow up question or start a new question.
                                        I will send you a job description and everything should be around that,
                                        excepts behavior question."""},
        {"role": "assistant", "content": "Got you! Please send me your Job Description."},
    ]
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = ["Hey!"]

# Continue the conversation
def continue_conversation(conversation_history, user_message):
    conversation_history.append({"role": "user", "content": user_message})


    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=conversation_history
    )

    assistant_message = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": assistant_message})
    
    return assistant_message

# for i,v in enumerate(st.session_state['chat_history']):
#     if i//2 == 1:
#         message(v, is_user=True)
#     else:
#         message(v)

for i,v in enumerate(st.session_state['chat_history']):
    if i%2 == 1:
        message(v, is_user=True)
    else:
        message(v)

user_input = st.text_area(label= 'User Input', placeholder = 'Type your input here..')
if st.button('submit'):
    st.session_state['chat_history'].append(user_input)
    answer = continue_conversation( st.session_state['conversation_history'], user_input)
    st.session_state['chat_history'].append(answer)
