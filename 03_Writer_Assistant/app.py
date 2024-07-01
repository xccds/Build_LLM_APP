import streamlit as st
import ai


st.title('💬十分钟编写大模型应用')
st.caption("🚀 中英双语写作助手")

keys_to_initialize = ["improve_write", "fix_grammar", "new_article"]
for key in keys_to_initialize:
    if key not in st.session_state:
        st.session_state[key] = ""

if "writeAI" not in st.session_state:
    st.session_state["writeAI"] = ai.WriterAssistant()   


with st.sidebar:
    LLM_option = st.selectbox(
        '选择大模型引擎',
        ('gpt-3.5-turbo', 'gpt-4','llama3'))

    st.session_state["writeAI"].set_model(LLM_option)

tab1, tab2, tab3= st.tabs(["润色修改文章", "拼写语法纠错","文章自动生成"])


with tab1:
    with st.form("修改文章"):
        query = st.text_area('输入需要修改的文本',height=500)
        submitted = st.form_submit_button("提交")
    if submitted:
        with st.spinner("thinking..."):
            st.session_state["writeAI"].improve_write(query)
            st.session_state["improve_write"] = st.session_state["writeAI"].get_reply()
        

    st.markdown(st.session_state["improve_write"])

with tab2:
    with st.form("拼写语法纠错"):
        query = st.text_area('输入需要纠错的文本',height=500)
        submitted = st.form_submit_button("提交")
    if submitted:
        with st.spinner("thinking..."):
            st.session_state["writeAI"].fix_grammar(query)
            st.session_state["fix_grammar"] = st.session_state["writeAI"].get_reply()
        

    st.markdown(st.session_state["fix_grammar"])

with tab3:

    with st.form("文章生成"):

        query = st.text_area('输入主题')
        submitted = st.form_submit_button("提交")
    if submitted:
        with st.spinner("thinking..."):
            st.session_state["writeAI"].new_article(query)
            st.session_state["new_article"] = st.session_state["writeAI"].get_reply()
        

    st.markdown(st.session_state["new_article"])




