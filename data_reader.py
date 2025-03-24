import sqlite3
import pandas as pd

# Connect to your SQLite DB file
conn = sqlite3.connect("data/incident_analysis_data.db")

# Example query: View first 5 incidents
query = "SELECT * FROM automation_scripts;"
df = pd.read_sql_query(query, conn)

# Display results
print(df)

# Close connection
conn.close()