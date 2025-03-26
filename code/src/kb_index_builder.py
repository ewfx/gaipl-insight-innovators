# kb/kb_index_builder.py
# One-time script to build FAISS vector index for KB articles

import os
import pandas as pd
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

# Load KB article CSV
df_kb = pd.read_csv("kb/knowledge_base_articles_extended.csv")

# Combine title + summary + resolution for semantic embedding
kb_texts = (
    df_kb["title"] + ". " +
    df_kb["summary"] + " Resolution: " +
    df_kb["resolution_steps"]
).tolist()

kb_ids = df_kb["kb_id"].tolist()
metadata = [{"kb_id": id_} for id_ in kb_ids]

# Create embeddings and vectorstore
embedding_model = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(kb_texts, embedding_model, metadatas=metadata)

# Save index
vectorstore.save_local("kb_faiss_index")

print("✅ FAISS KB index saved to: kb/kb_faiss_index/")
