#!/bin/env python3
import streamlit as st
import os
import tempfile
from rag import ChatDoc


st.title('💬十分钟编写大模型应用')
st.caption("🚀 和私有知识库聊天")


if "messages" not in st.session_state:
    st.session_state.messages = []

def ready_asistant():

    st.session_state["assistant"] = ChatDoc()

    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        with st.session_state["ingestion_spinner"], st.spinner(f"Ingesting {file.name}"):
            st.session_state["assistant"].ingest(file_path)
        os.remove(file_path)


files = st.file_uploader(
        "Upload document",
        type=["pdf"],
        key="file_uploader",
        on_change=ready_asistant,
        label_visibility="collapsed",
        accept_multiple_files=True,
    )

st.session_state["ingestion_spinner"] = st.empty()

if files:
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
                agent_text = st.session_state["assistant"].ask(prompt)
                st.markdown(agent_text)
                st.session_state.messages.append({"role": "assistant", "content": agent_text})