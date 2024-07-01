#!/bin/env python3
import streamlit as st
import os
import tempfile
from GPT import PowerpointAI
from pathlib import Path


st.title('💬十分钟编写大模型应用')
st.caption("🚀 AI自动生成PPT")

if "file_name" not in st.session_state:
    st.session_state.file_name = ""

def ready_asistant():
    st.session_state["assistant"] = PowerpointAI()
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
    with st.form("pass_form"):
            topic = st.text_input("输入PPT的主题")
            num = st.number_input('PPT页数', min_value=1, max_value=10)
            search = st.toggle("使用搜索",key="search")
            rag = st.toggle("使用文档",key="rag")
            submitted = st.form_submit_button("确认")
            if submitted:
                with st.spinner("正在生成ppt文档..."):
                    st.session_state["assistant"].ask(topic,num,search,rag)
                    st.session_state["assistant"].json2dict()
                    st.session_state.file_name = st.session_state["assistant"].create_ppt(topic)

if st.session_state.file_name:
    FILE_PATH = Path(st.session_state.file_name)
    if FILE_PATH.is_file():
        with open(FILE_PATH, 'rb') as ppt_file:
            btn = st.download_button(
                    label="下载生成PPT",
                    data=ppt_file,
                    file_name=st.session_state.file_name
                )
