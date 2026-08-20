import streamlit as st

from agent import agent


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Enterprise AI Ops Copilot",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------------------------
# Application Header
# --------------------------------------------------

st.title("Enterprise AI Ops Copilot — Multi-Tool AI Assistant")

st.write(
    "An AI-powered enterprise assistant that uses company knowledge "
    "and operational data to answer business questions."
)


# --------------------------------------------------
# User Input
# --------------------------------------------------

question = st.text_input(
    "Ask a question",
    placeholder="Example: What is OTIF?"
)


# --------------------------------------------------
# Ask Button
# --------------------------------------------------

if st.button("Ask"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Thinking..."):

            try:

                answer = agent(question)

                st.write(answer)

            except Exception as e:

                st.error(
                    f"Unable to process your question: {e}"
                )