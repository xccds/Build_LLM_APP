#!/bin/env python3
import streamlit as st
import pandas as pd
from GPT import DataAI


st.title('💬十分钟编写大模型应用')
st.caption("🚀 自动分析Excel数据")


def analysis_data():
    st.session_state["assistant"].create_questions()
    st.session_state["assistant"].answer_questions()
    st.session_state["assistant"].create_report()


if "messages" not in st.session_state:
    st.session_state.messages = []

uploaded_file = st.file_uploader("Choose a excel file",type=["xlsx", "xls"],key="file_uploader")

if uploaded_file is not None:
    dataframe = pd.read_excel(uploaded_file)
    st.dataframe(dataframe.head(), use_container_width=True)
    st.session_state["assistant"] = DataAI(dataframe)

    is_analysis = st.button("自动数据分析")


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

        with st.chat_message("assistant"):
            with st.spinner("Thinking"):
                agent_text = st.session_state["assistant"].ask_question(prompt)['output']
                st.markdown(agent_text)
                st.session_state.messages.append({"role": "assistant", "content": agent_text})
    if is_analysis:
         with st.spinner("creating report"):
            analysis_data()
            agent_text = st.session_state["assistant"].report
            st.markdown(agent_text)
            st.session_state.messages.append({"role": "assistant", "content": agent_text})