# kb_search_chat.py
# Run with: streamlit run kb_search_chat.py

import os
import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# ✅ Must be first Streamlit call
st.set_page_config(page_title="📘 KB Search Agent", layout="centered")

# Set your OpenAI API key (replace or load from env securely)
os.environ["OPENAI_API_KEY"] = ""

# Load FAISS vectorstore
@st.cache_resource
def load_kb_index():
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local("kb_faiss_index", embeddings, allow_dangerous_deserialization=True)

vectorstore = load_kb_index()

# KB search logic
def kb_agent(query: str, k: int = 2) -> str:
    results = vectorstore.similarity_search(query, k=k)
    if not results:
        return "❌ No relevant KB articles found."

    response = "### 📚 KB Search Results:\n"
    for res in results:
        response += f"- **Content:** {res.page_content.strip()}\n"
        response += f"  _(KB ID: {res.metadata['kb_id']})_\n\n"
    return response

# Streamlit UI
st.title("🔍 Gen AI KB Search Assistant")
st.markdown("Ask a question or describe an issue. The assistant will return relevant knowledge base articles.")

# Chat interface
query = st.text_input("💬 What do you need help with?", placeholder="e.g., High CPU on app server during backup")

if query:
    with st.spinner("Searching KB articles..."):
        answer = kb_agent(query)
    st.markdown(answer)