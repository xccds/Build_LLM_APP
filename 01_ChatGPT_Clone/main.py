import streamlit as st
from openai import OpenAI


st.title('💬十分钟编写大模型应用')
st.caption("🚀 用openai和streamlit复刻一个聊天机器人")

with st.sidebar:
    option = st.selectbox(
        '使用哪一种大模型引擎',
        ('GPT-3.5', 'GPT-4'))

if option == 'GPT-3.5':
    st.session_state["openai_model"] = "gpt-3.5-turbo"
else:
    st.session_state["openai_model"] = "gpt-4"

client = OpenAI()


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("What I can do for you?")

if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

# Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Thinking"):
            chat_response = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=st.session_state.messages
            )
            response = chat_response.choices[0].message.content
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})