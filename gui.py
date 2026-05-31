import streamlit as st
import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from main import ask_judge, setup_llm, EMBEDDING_MODEL_NAME, LLM_MODEL, CHROMA_PATH


@st.cache_resource
def load_ai():
    llm = setup_llm(LLM_MODEL)
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    if os.path.isdir(CHROMA_PATH):
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_model)
    else:
        st.error("Database not found! Please run main.py once first.")
        st.stop()

    return llm, db


st.set_page_config(page_title="Poker Judge AI", page_icon="🃏")
st.title("🃏 Poker Tournament Judge AI")
st.caption("A strict but fair AI referee who knows the rules by heart.")

llm, db = load_ai()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("E.g.: What is the penalty for acting out of turn?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("The judge is flipping through the rulebook..."):
            response = ask_judge(prompt, db, llm)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})