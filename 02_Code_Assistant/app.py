import streamlit as st
import ai


st.title('💬十分钟编写大模型应用')
st.caption("🚀 编写一个代码助手")

keys_to_initialize = ["fix_code", "explain_code", "generate_code"]
for key in keys_to_initialize:
    if key not in st.session_state:
        st.session_state[key] = ""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "you are a code assistant"}]


with st.sidebar:
    LLM_option = st.selectbox(
        '选择大模型引擎',
        ('gpt-3.5-turbo', 'gpt-4','codegemma'))
    
    language = st.selectbox(
        '选择代码语言',
        ('python', 'javascript', 'c++'))
    

tab1, tab2, tab3= st.tabs(["代码生成", "代码理解","代码查错"])


with tab1:
    with st.form("代码生成"):
        query = st.text_area('输入代码需求')
        submitted = st.form_submit_button("提交")
    if submitted:
        with st.spinner("thinking..."):
            st.session_state["generate_code"] = ai.generate_code(LLM_option,
                                                            language,
                                                            query,
                                                            st.session_state.messages)
        

    st.markdown(st.session_state["generate_code"])

with tab2:
    with st.form("代码理解"):
        query = st.text_area('输入代码',height = 200)
        submitted = st.form_submit_button("提交")
    if submitted:
        with st.spinner("thinking..."):
            st.session_state["explain_code"] = ai.explain_code(LLM_option,
                                                            language,
                                                            query,
                                                            st.session_state.messages)
        

    st.markdown(st.session_state["explain_code"])

with tab3:

    with st.form("代码查错"):

        code_input = st.text_area('输入有问题的代码',height = 200)
        error_input = st.text_area('输入相应报错信息',height = 100)
        submitted = st.form_submit_button("提交")
    if submitted:
        with st.spinner("thinking..."):
            st.session_state["fix_code"] = ai.fix_code(LLM_option,
                                                   language,
                                                    code=code_input,
                                                    error=error_input,
                                                    messages=st.session_state.messages)
        

    st.markdown(st.session_state["fix_code"])

        
       



