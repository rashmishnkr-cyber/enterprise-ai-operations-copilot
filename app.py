import streamlit as st

from agent import agent

st.title("Enterprise AI Operations Copilot")

question = st.text_input("Ask a Supply Chain question")

if st.button("Ask"):

    answer = agent(question)

    st.write(answer)