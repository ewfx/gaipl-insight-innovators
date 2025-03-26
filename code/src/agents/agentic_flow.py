# agents/agentic_flow.py
# Detects anomalies from telemetry and correlates them to past incidents
# Recommends automation scripts based on known issues

import sqlite3
import pandas as pd

def detect_anomalies(db_path="data/incident_analysis_data.db"):
    conn = sqlite3.connect(db_path)
    query = """
    SELECT timestamp, server_id, cpu_usage_percent, memory_usage_percent, log_message
    FROM system_logs_telemetry_data
    WHERE cpu_usage_percent > 90 OR memory_usage_percent > 90
    ORDER BY timestamp DESC
    LIMIT 10
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def correlate_with_incidents(server_id, db_path="data/incident_analysis_data.db"):
    conn = sqlite3.connect(db_path)
    query = f"""
    SELECT incident_id, timestamp, description, root_cause, resolution
    FROM incident_management_data
    WHERE server_id = '{server_id}'
    ORDER BY timestamp DESC
    LIMIT 1
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def recommend_script(anomaly_type, db_path="data/incident_analysis_data.db"):
    conn = sqlite3.connect(db_path)
    query = f"""
    SELECT name, description
    FROM automation_scripts
    WHERE description LIKE '%{anomaly_type}%'
    LIMIT 1
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    if not df.empty:
        return df.iloc[0]["name"], df.iloc[0]["description"]
    return "generic_diagnostic.sh", "Default diagnostic script"

def classify_anomaly(row):
    if row["cpu_usage_percent"] > 90:
        return "HighCPU"
    elif row["memory_usage_percent"] > 90:
        return "MemoryLeak"
    elif pd.notna(row["log_message"]) and "unauthorized" in row["log_message"].lower():
        return "SecurityBreach"
    else:
        return "GeneralAnomaly"

def agentic_flow_summary():
    anomalies = detect_anomalies()
    if anomalies.empty:
        return "✅ No critical anomalies detected."

    responses = []
    for _, row in anomalies.iterrows():
        server = row["server_id"]
        ts = row["timestamp"]
        anomaly_type = classify_anomaly(row)

        summary = f"🚨 Anomaly detected on `{server}` at `{ts}` – Type: **{anomaly_type}**"

        incident = correlate_with_incidents(server)
        if not incident.empty:
            inc = incident.iloc[0]
            summary += f"🔗 Related Incident `{inc['incident_id']}`: {inc['description']} – RCA: {inc['root_cause']}"

        script_name, script_desc = recommend_script(anomaly_type)
        summary += f"🤖 Suggested Automation: `{script_name}` – {script_desc}"

        responses.append(summary)

    return "\n---\n".join(responses)

if __name__ == "__main__":
    print(agentic_flow_summary())
