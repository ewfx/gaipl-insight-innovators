# rca_chat.py
# Requirements: pandas, sqlite3, langchain, openai
# Purpose: Load incident details and telemetry logs, then generate RCA summary via GPT

import os
import sqlite3
import pandas as pd
from datetime import timedelta

from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI  # Use langchain_openai for gpt-3.5-turbo and newer

# Set your OpenAI API Key
os.environ["OPENAI_API_KEY"] = ""

# Connect to SQLite database
conn = sqlite3.connect("data/incident_analysis_data.db")

# === Step 1: Select Incident ID ===
incident_id = "inc032"  # <-- You can change this

# Fetch incident details
incident_query = f"""
SELECT incident_id, timestamp, server_id, app_id, description, root_cause, resolution
FROM incident_management_data
WHERE incident_id = '{incident_id}'
"""
incident_df = pd.read_sql(incident_query, conn)

if incident_df.empty:
    print(f"❌ Incident {incident_id} not found.")
    conn.close()
    exit()

incident = incident_df.iloc[0]
incident_time = pd.to_datetime(incident["timestamp"])
server_id = incident["server_id"]

print(f"🔎 Loaded Incident {incident_id}")
print(f"   Description: {incident['description']}")
print(f"   Root Cause: {incident['root_cause']}")
print(f"   Resolution: {incident['resolution']}")

# === Step 2: Fetch Telemetry Logs Around the Incident ===
start_time = (incident_time - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
end_time = (incident_time + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S")

telemetry_query = f"""
SELECT timestamp, cpu_usage_percent, memory_usage_percent, disk_usage_percent, log_message
FROM system_logs_telemetry_data
WHERE server_id = '{server_id}' AND timestamp BETWEEN '{start_time}' AND '{end_time}'
ORDER BY timestamp ASC
"""
telemetry_df = pd.read_sql(telemetry_query, conn)

log_snippets = ""
if not telemetry_df.empty:
    for _, row in telemetry_df.iterrows():
        ts = row["timestamp"]
        cpu = row["cpu_usage_percent"]
        mem = row["memory_usage_percent"]
        disk = row["disk_usage_percent"]
        msg = row["log_message"] if pd.notna(row["log_message"]) else ""
        log_snippets += f"[{ts}] CPU: {cpu}%, MEM: {mem}%, DISK: {disk}% {msg}\n"
else:
    log_snippets = "No telemetry data found around the incident time."

# === Step 3: Ask GPT to Summarize RCA ===

prompt = PromptTemplate(
    input_variables=["incident", "logs"],
    template="""
You are a platform support assistant. Use the incident description and surrounding logs to explain the root cause.

Incident Info:
{incident}

Telemetry Logs:
{logs}

Answer in a concise, technical RCA format.
"""
)

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")  # model="gpt-3.5-turbo-0125" for latest

# New RunnableSequence using the pipe operator
rca_chain = prompt | llm

incident_context = f"""
Incident ID: {incident['incident_id']}
Time: {incident['timestamp']}
Server: {incident['server_id']}
App: {incident['app_id']}
Description: {incident['description']}
Root Cause: {incident['root_cause']}
Resolution: {incident['resolution']}
"""

print("\n🤖 GPT-Generated RCA Summary:\n")
response = rca_chain.invoke({"incident": incident_context, "logs": log_snippets[:3000]})
print(response.content)  # .content to access the model's reply

conn.close()