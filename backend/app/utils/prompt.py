from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
"""
You are a banking assistant.

Answer the question only using the context below.

If the answer is not present, say:
"I couldn't find that information in the provided documents."

Context:
{context}

Question:
{question}
"""
)