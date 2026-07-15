import streamlit as st
import requests

st.set_page_config(
    page_title="AI Banking Assistant",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 AI Banking Assistant")

# Sidebar
st.sidebar.header("Upload Banking PDF")

uploaded_file = st.sidebar.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

if uploaded_file:
    st.sidebar.success(f"{uploaded_file.name} selected successfully!")

    if st.sidebar.button("Upload PDF"):
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        with st.spinner("Uploading and indexing PDF..."):
            response = requests.post(
                "http://127.0.0.1:8000/upload",
                files=files
            )

        if response.status_code == 200:
            st.sidebar.success("✅ PDF uploaded successfully!")
        else:
            st.sidebar.error(f"❌ Upload failed: {response.text}")

# Query Section
st.subheader("Ask a Banking Question")

question = st.text_input("Enter your question")

if st.button("Ask"):

    if not question:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating answer..."):
            response = requests.post(
                "http://127.0.0.1:8000/ask",
                json={"question": question}
            )

        if response.status_code == 200:

            answer = response.json()["answer"]

            st.success(answer)

        else:
            st.error(f"Error: {response.text}")