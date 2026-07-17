import streamlit as st
import requests

st.set_page_config(
    page_title="AI Banking Assistant",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 AI Banking Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===========================
# Sidebar
# ===========================

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

# ===========================
# New Chat
# ===========================

if st.sidebar.button("🆕 New Chat"):

    response = requests.post(
        "http://127.0.0.1:8000/clear-chat"
    )

    if response.status_code == 200:

        st.session_state.messages = []

        st.sidebar.success("✅ Started a new chat!")

        st.rerun()

    else:
        st.sidebar.error("❌ Failed to clear chat history.")

# ===========================
# Welcome Screen
# ===========================

if len(st.session_state.messages) == 0:

    st.markdown("## 👋 Welcome!")

    st.markdown(
        "Ask questions about your banking documents instantly."
    )

    st.markdown("### 💡 Try asking:")

    st.markdown("""
-  What is the minimum balance required?
-  Explain the credit card annual fee.
-  Summarize this document.
-  What are the ATM withdrawal charges?
""")

# ===========================
# Display Conversation
# ===========================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):
            st.markdown("**📖 Sources**")

            for source in message["sources"]:
                st.markdown(f"- {source}")

# ===========================
# Chat Input
# ===========================

question = st.chat_input(
    "Ask anything about your banking documents..."
)

if question:

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.spinner("Generating answer..."):

        response = requests.post(
            "http://127.0.0.1:8000/ask",
            json={
                "question": question
            }
        )

    if response.status_code == 200:

        result = response.json()

        answer = result["answer"]

        sources = result.get(
            "sources",
            []
        )

        # Store assistant response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": sources
            }
        )

        st.rerun()

    else:

        st.error(
            f"Error: {response.text}"
        )