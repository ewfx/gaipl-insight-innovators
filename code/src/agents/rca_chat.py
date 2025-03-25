# agents/rca_chat.py
# Given an incident ID, fetch incident details and telemetry, then summarize RCA via LLM

import os
import sqlite3
import pandas as pd
from datetime import timedelta
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI

# Load your OpenAI key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

def get_incident_context(incident_id, db_path="data/incident_analysis_data.db"):
    conn = sqlite3.connect(db_path)
    incident_query = f"""
        SELECT * FROM incident_management_data WHERE incident_id = '{incident_id}'
    """
    incident_df = pd.read_sql_query(incident_query, conn)
    if incident_df.empty:
        conn.close()
        return None, None, None

    incident = incident_df.iloc[0]
    timestamp = pd.to_datetime(incident["timestamp"])
    server_id = incident["server_id"]

    # Fetch telemetry around the incident (±30 min)
    telemetry_query = f"""
        SELECT * FROM system_logs_telemetry_data
        WHERE server_id = '{server_id}' AND timestamp BETWEEN '{(timestamp - timedelta(minutes=30))}' AND '{(timestamp + timedelta(minutes=30))}'
        ORDER BY timestamp
    """
    telemetry_df = pd.read_sql_query(telemetry_query, conn)
    conn.close()

    return incident, telemetry_df, server_id

def summarize_rca(incident, telemetry_df):
    # Format context
    incident_context = (
        f"Incident ID: {incident['incident_id']}\n"
        f"Time: {incident['timestamp']}\n"
        f"Server: {incident['server_id']}\n"
        f"App: {incident['app_id']}\n"
        f"Description: {incident['description']}\n"
        f"Root Cause: {incident['root_cause']}\n"
        f"Resolution: {incident['resolution']}"
    )

    log_snippets = ""
    for _, row in telemetry_df.iterrows():
        log_msg = row['log_message'] if pd.notna(row['log_message']) else ""
        log_snippets += f"[{row['timestamp']}] CPU:{row['cpu_usage_percent']}% MEM:{row['memory_usage_percent']}% {log_msg}\n"

    # Build prompt
    prompt = PromptTemplate(
        input_variables=["incident", "logs"],
        template="""
                You are a helpful RCA assistant. Use the incident description and telemetry logs to explain the root cause.
                
                Incident Info:
                {incident}
                
                Telemetry Logs:
                {logs}
                
                Return a concise, technical RCA summary:
                """
    )

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run({"incident": incident_context, "logs": log_snippets[:3000]})

    return "🧠 RCAAgent says: " + response

# CLI test
if __name__ == "__main__":
    incident_id = input("🔍 Enter incident ID: ").strip()
    incident, telemetry_df, _ = get_incident_context(incident_id)
    if incident is not None:
        print(summarize_rca(incident, telemetry_df))
    else:
        print("❌ Incident not found.")
