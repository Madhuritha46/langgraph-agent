import streamlit as st

from agent import run_agent


st.set_page_config(
    page_title="LangGraph Agent",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 LangGraph Agent")

st.write(
    "A simple Agentic AI application built with "
    "LangGraph, LangChain, Gemini and a Calculator Tool."
)

question = st.text_input(
    "Ask your question:",
    placeholder="Example: What is LangGraph?"
)

if st.button("Run Agent"):

    if question.strip():

        with st.spinner("Agent is thinking..."):

            answer = run_agent(question)

        # Extract the actual text from Gemini's response
        if isinstance(answer, list):
            if len(answer) > 0 and isinstance(answer[0], dict):
                answer = answer[0].get("text", str(answer))
            else:
                answer = str(answer)

        st.subheader("Answer")
        st.markdown(answer)

    else:
        st.warning("Please enter a question.")