## 🎯 What is MCP?

Model Context Protocol (MCP) is a design pattern that dynamically assembles **relevant system context** (like incidents, telemetry, KBs, etc.) and delivers it to an **LLM agent** to perform decision-making, troubleshooting, and response generation.

Unlike traditional static dashboards, MCP enables:
- Smart tool invocation
- Context stitching across systems
- Conversational resolution flow

---

## 🧩 Key Components in This Project

| Component | Description |
|----------|-------------|
| `LangChain Agent` | The brain that routes queries to the right tools |
| `RCAAgent` | Pulls incident + telemetry, summarizes root cause |
| `TelemetryAgent` | Detects anomalies from recent telemetry |
| `KBAgent` | Searches KB articles via FAISS |
| `RecommendationAgent` | Suggests actions based on issue type |
| `AutomationAgent` | Recommends fix scripts (via `agentic_flow`) |

---

## 🧠 MCP Flow in Code

1. **User Input:**
   - Comes from Streamlit UI (`ui/mcp_chatbot_ui.py`)
   - Sent to the LangChain agent via `agent.run(user_query)`

2. **Agent Initialization:**
   - Defined in `core/mcp_chatbot_agent.py`
   - Uses `initialize_agent` with:
     - Tool list (`Tool(...)`)
     - Memory (`ConversationBufferMemory`)
     - LLM (`ChatOpenAI`)
   - Uses `chat-zero-shot-react-description` to let the LLM decide which tool to call

3. **Tool Execution:**
   - Each tool is a function wrapped with LangChain `Tool(...)`
   - Based on prompt + user query, the agent decides which tool(s) to invoke

4. **Context Routing:**
   - Tools pull data from:
     - SQLite DB (`incident_analysis_data.db`)
     - FAISS Index (`kb_faiss_index/`)
     - CSV files (e.g., KB articles, recs)
   - They return precise responses (RCA summaries, KB links, anomalies)

5. **LLM Final Answer:**
   - Agent uses outputs from tools to generate a final response
   - Adds attribution like:
     ```
     RCAAgent says: ...
     KBAgent recommends: ...
     ```

6. **Memory:**
   - Maintains conversation state using `ConversationBufferMemory`
   - Supports follow-up queries like:
     - "What caused it?"
     - "How to fix it?"
     - "Any scripts?"

---

## 💡 MCP in Action

Example Query:  
👉 “What caused inc032 and how do I fix it?”

**Agent Response Flow:**
1. RCAAgent → summarizes root cause from incident + logs
2. RecommendationAgent → suggests fix based on tag
3. KBAgent → returns supporting articles
4. AutomationAgent → suggests a script
5. Memory retains `inc032` context for follow-ups

---

## ✅ Summary

MCP here means:
- Modular LangChain tools = agents
- Each tool talks to a real backend (DB/FAISS)
- LangChain agent = coordinator
- Streamlit = conversational UI
- LLM = reasoning core

This design gives you a **smart, extensible, context-aware support chatbot** — not just a tab-based viewer.

