# MCP Chatbot Architecture

This diagram illustrates the complete architecture and workflow of the GenAI-powered MCP Chatbot.

## Architecture Diagram

```mermaid
flowchart TD
    A[User_Streamlit_UI] -->|Interacts_with| B[LangChain_Chat_Agent]

    B -->|Utilizes| C1[RCAAgent]
    B -->|Utilizes| C2[KBAgent]
    B -->|Utilizes| C3[TelemetryAgent]
    B -->|Utilizes| C4[RecommendationAgent]
    B -->|Utilizes| C5[AutomationAgent]

    C1 -->|Accesses| D1[SQLite_incident_management_data]
    C1 -->|Accesses| D2[SQLite_system_logs_telemetry_data]

    C2 -->|Queries| E1[FAISS_Vector_Index]
    C2 -->|Reads| E2[CSV_KB_Articles]

    C3 -->|Monitors| F1[SQLite_telemetry_logs]

    C4 -->|Gathers_from| G1[SQLite_contextual_recommendation_data]

    C5 -->|Executes| H1[SQLite_automation_scripts]
```

---

## Data Sources

- `incident_analysis_data.db` (SQLite)
- `kb_faiss_index/` (FAISS index folder)
- `knowledge_base_articles_extended.csv`
- `contextual_recommendation_data` (embedded or separate CSV)

## Agent Tools

- **RCAAgent** – Summarizes incident root cause with logs
- **KBAgent** – Retrieves relevant KB articles
- **TelemetryAgent** – Detects anomalies in telemetry
- **RecommendationAgent** – Suggests next steps
- **AutomationAgent** – Suggests scripts to fix issues
