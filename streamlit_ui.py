# streamlit_ui.py
# Run this app with: streamlit run streamlit_ui.py
# Requirements: streamlit, pandas, sqlite3, langchain, openai

import os
import sqlite3
import pandas as pd
import streamlit as st
from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = ""

# Connect to SQLite DB
conn = sqlite3.connect("data/incident_analysis_data.db")

# Load incidents
incidents_df = pd.read_sql_query("SELECT * FROM incident_management_data", conn)
telemetry_df = pd.read_sql_query("SELECT * FROM system_logs_telemetry_data", conn)

st.set_page_config(page_title="Gen AI IPE Console", layout="wide")
st.title("🧠 AI-Powered Incident Management Console")

# Sidebar – Select Incident
incident_id = st.sidebar.selectbox("Select an Incident ID", incidents_df["incident_id"].tolist())

# Display Incident Details
incident = incidents_df[incidents_df["incident_id"] == incident_id].iloc[0]
st.subheader(f"Incident Details – {incident_id}")
st.write(f"**Timestamp:** {incident['timestamp']}")
st.write(f"**Server:** {incident['server_id']} | **App:** {incident['app_id']}")
st.write(f"**Description:** {incident['description']}")
st.write(f"**Root Cause:** {incident['root_cause']}")
st.write(f"**Resolution:** {incident['resolution']}")

# Display Telemetry Around the Incident
incident_time = pd.to_datetime(incident["timestamp"])
start_time = incident_time - pd.Timedelta(minutes=15)
end_time = incident_time + pd.Timedelta(minutes=15)

telemetry_df["timestamp"] = pd.to_datetime(telemetry_df["timestamp"])
relevant_logs = telemetry_df[
    (telemetry_df["server_id"] == incident["server_id"]) &
    (telemetry_df["timestamp"].between(start_time, end_time))
].sort_values("timestamp")

st.markdown("### 📊 Telemetry Logs Around Incident")
if relevant_logs.empty:
    st.info("No telemetry data available within ±15 minutes of this incident.")
else:
    st.dataframe(relevant_logs[["timestamp", "cpu_usage_percent", "memory_usage_percent", "disk_usage_percent", "log_message"]])

# RCA Chat (LLM Integration)
st.markdown("### 🤖 RCA Assistant")
user_question = st.text_input("Ask AI about this incident (e.g., What caused this?)", value="What caused this incident?")

if user_question:
    # Prepare context for GPT
    log_snippets = ""
    for _, row in relevant_logs.iterrows():
        msg = row["log_message"] if pd.notna(row["log_message"]) else ""
        log_snippets += f"[{row['timestamp']}] CPU:{row['cpu_usage_percent']}% MEM:{row['memory_usage_percent']}% {msg}\n"

    incident_context = (
        f"Incident {incident['incident_id']} on server {incident['server_id']} (App: {incident['app_id']})\n"
        f"Time: {incident['timestamp']}\n"
        f"Description: {incident['description']}\n"
        f"Root Cause: {incident['root_cause']}\n"
        f"Resolution: {incident['resolution']}"
    )

    prompt = PromptTemplate(
        input_variables=["context", "logs", "question"],
        template="""
You are a helpful platform support assistant. Use the incident details and telemetry logs to answer the user.

Incident Context:
{context}

Telemetry Logs:
{logs}

Question: {question}

Answer as a concise and knowledgeable assistant:
"""
    )

    #llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt)

    with st.spinner("AI is thinking..."):
        answer = chain.run({
            "context": incident_context,
            "logs": log_snippets[:3000],
            "question": user_question
        })

    st.markdown("#### 💬 AI Response:")
    st.success(answer)

# Simulated Automation Execution
st.markdown("### ⚙️ Simulated Automation")
if st.button("Run Suggested Automation"):
    # Dummy logic – pick based on incident description
    if "CPU" in incident["description"]:
        script = "scale_out_infrastructure.sh"
    elif "memory" in incident["description"].lower():
        script = "restart_service.sh"
    elif "security" in incident["description"].lower():
        script = "block_ip.sh"
    else:
        script = "generic_diagnostic.sh"

    st.success(f"Executed {script} (simulation) ✅")

conn.close()