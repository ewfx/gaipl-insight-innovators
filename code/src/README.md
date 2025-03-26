# 🤖 GenAI MCP Chatbot – Platform Support Assistant

This project is a full-stack GenAI-powered chatbot for platform support teams. It integrates telemetry, incident logs, KB articles, and automation scripts to provide real-time, context-aware incident resolution using LangChain agents and OpenAI GPT.

---

## 🚀 Features

- 🧠 **Multi-Agent MCP Chatbot** powered by LangChain + OpenAI
- 🗃️ Integrated with SQLite for telemetry, incidents, KB, and automation data
- 🔍 Vector-based semantic search of KB articles using FAISS
- 🔧 RCA, telemetry anomaly detection, recommendations, and simulated remediation
- 💬 Streamlit UI with multi-turn conversational memory
- 📦 Modular architecture with agents, core, and UI layers

---

## 📁 Project Structure

```
genai-ipe-chatbot/
├── agents/                      ← All agent tools (RCA, KB, telemetry, etc.)
├── /kb_*                        ← FAISS index & builder for KB articles
├── data/                        ← SQLite database (MCP context store)
├── /mcp_chatbot_ui.py           ← Streamlit UI entry point
├── /mcp_chatbot_agent.py        ← LangChain unified agent setup
├── requirements.txt             ← App dependencies
├── README.md
```

---

## 🛠️ Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

```
Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-... (Edit with your OpenAI API key)
```

### 3. Run the Chatbot UI

```bash
/code/src -> python kb_index_builder.py
/code/src -> streamlit run mcp_chatbot_ui.py
```

---

## 💡 Example Queries

- “What caused incident inc045?”
- “Are there any active CPU anomalies?”
- “Search KB for memory leaks.”
- “Is there a recommended script for high CPU?”

---

## 🧪 Powered By

- [LangChain](https://www.langchain.com/)
- [OpenAI GPT](https://platform.openai.com/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [Streamlit](https://streamlit.io/)
- SQLite, Pandas

---

## 📄 License

MIT License – feel free to build on top of this!
