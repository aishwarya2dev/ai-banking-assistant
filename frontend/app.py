import streamlit as st
import requests

st.set_page_config(
    page_title="AI Banking Assistant",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 AI Banking Assistant")

# ===========================
# Initialize Chat History
# ===========================

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
            st.sidebar.error(
                f"❌ Upload failed: {response.text}"
            )

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
        st.sidebar.error(
            "❌ Failed to clear chat history."
        )

# ===========================
# Display Conversation
# ===========================

for message in st.session_state.messages:

    if message["role"] == "assistant":

        with st.chat_message(
            "assistant",
            avatar="🏦"
        ):

            st.markdown(message["content"])

            if message.get("sources"):

                st.markdown("**📖 Sources**")

                for source in message["sources"]:
                    st.markdown(f"- {source}")

    else:

        with st.chat_message("user", avatar="👤"):

            st.markdown(message["content"])

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

    # Show user message immediately
    with st.chat_message("user", avatar="👤"):
        st.markdown(question)

    # Show assistant placeholder
    with st.chat_message(
        "assistant",
        avatar="🏦"
    ):

        with st.spinner("Thinking..."):

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

            st.markdown(answer)

            if sources:

                st.markdown("**📖 Sources**")

                for source in sources:
                    st.markdown(f"- {source}")

            # Save assistant response
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                }
            )

        else:

            st.error(
                f"Error: {response.text}"
            )