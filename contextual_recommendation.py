# contextual_recommendation.py
# Requirements: pandas, sqlite3
# Purpose: Identify current anomalies and suggest contextual recommendations

import sqlite3
import pandas as pd
from datetime import datetime, timedelta

# Connect to the SQLite database
conn = sqlite3.connect("data/incident_analysis_data.db")

# Step 1: Query recent telemetry for anomalies (last 1 hour window)
one_hour_ago = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")

query = f"""
SELECT timestamp, server_id, cpu_usage_percent, memory_usage_percent, disk_usage_percent, log_message
FROM system_logs_telemetry_data
WHERE timestamp >= '{one_hour_ago}'
  AND (cpu_usage_percent > 90 OR memory_usage_percent > 90 OR log_message LIKE '%ERROR%' OR log_message LIKE '%unauthorized%')
ORDER BY timestamp DESC
"""

anomalies = pd.read_sql(query, conn)

if anomalies.empty:
    print("✅ No new anomalies detected in the past hour.")
    conn.close()
    exit()

# Step 2: Classify anomaly type
def classify_anomaly(row):
    if row["cpu_usage_percent"] > 90:
        return "HighCPU"
    elif row["memory_usage_percent"] > 90:
        return "MemoryLeak"
    elif isinstance(row["log_message"], str) and ("unauthorized" in row["log_message"].lower() or "login" in row["log_message"].lower()):
        return "SecurityBreach"
    else:
        return "GeneralAnomaly"

anomalies["anomaly_type"] = anomalies.apply(classify_anomaly, axis=1)

# Step 3: Match with contextual recommendations
for _, row in anomalies.iterrows():
    server_id = row["server_id"]
    timestamp = row["timestamp"]
    anomaly_type = row["anomaly_type"]

    print(f"\n🔍 Anomaly detected on {server_id} at {timestamp}")
    print(f"   Type: {anomaly_type}")
    print(f"   CPU: {row['cpu_usage_percent']}%, MEM: {row['memory_usage_percent']}%")
    if pd.notna(row["log_message"]):
        print(f"   Log: {row['log_message']}")

    # Step 4: Look up contextual recommendation
    rec_query = f"""
    SELECT recommendation
    FROM contextual_recommendation_data
    WHERE similarity_tag = '{anomaly_type}'
    LIMIT 1
    """
    rec_df = pd.read_sql(rec_query, conn)

    if not rec_df.empty:
        print(f"💡 Recommended Action: {rec_df.iloc[0]['recommendation']}")
    else:
        print("⚠️ No direct recommendation found. Suggest manual triage or deeper investigation.")

conn.close()