import streamlit as st

st.title("🏦 AI Banking Assistant")

question = st.text_input("Ask your banking question")

if question:
    st.write("Answer will appear here...")