# agents/kb_search_agent.py
# Loads FAISS vector index and searches KB articles by similarity

import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# Set OpenAI key from environment
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

# Load FAISS vectorstore index
def load_kb_vectorstore(index_path="kb_faiss_index"):
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

vectorstore = load_kb_vectorstore()

def kb_agent(query: str, k: int = 2) -> str:
    results = vectorstore.similarity_search(query, k=k)
    if not results:
        return "❌ No relevant KB articles found."

    response = "📘 KBAgent recommends: "
    for res in results:
        content = res.page_content.strip()
        kb_id = res.metadata.get("kb_id", "Unknown")
        response += f"- **KB ID:** {kb_id} **Summary:** {content}"
    return response

# CLI Test
if __name__ == "__main__":
    query = input("🔍 Enter issue/question: ").strip()
    print(kb_agent(query))
