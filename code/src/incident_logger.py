import sqlite3
import pandas as pd

# File paths for all uploaded CSVs
csv_files = {
    "enterprise_system_metadata": "data/enterprise_system_metadata.csv",
    "incident_management_data": "data/incident_management_data_extended.csv",
    "system_logs_telemetry_data": "data/system_logs_telemetry_data_enriched.csv",
    "knowledge_base_articles": "data/knowledge_base_articles_extended.csv",
    "contextual_recommendation_data": "data/contextual_recommendation_data.csv",
    "security_compliance_data": "data/security_compliance_data.csv"
}

extra_csv_files = {
    "automation_scripts": "data/automation_scripts.csv",
    "ci_config_data": "data/ci_config_data.csv",
    "dependency_graph": "data/dependency_graph.csv",
    "incident_to_kb_mapping": "data/incident_to_kb_mapping.csv",
    "user_feedback": "data/user_feedback.csv"
}

# Create SQLite DB
sqlite_db_path = "data/incident_analysis_data.db"
conn = sqlite3.connect(sqlite_db_path)

# Read CSVs and write to SQLite tables
for table_name, file_path in extra_csv_files.items():
    df = pd.read_csv(file_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)

conn.close()