# agents/contextual_recommendation.py
# Suggests recommendations based on anomaly type or similarity tag

import sqlite3
import pandas as pd

def recommendation_agent(tag: str, db_path="data/incident_analysis_data.db") -> str:
    conn = sqlite3.connect(db_path)
    query = f"""
    SELECT recommendation
    FROM contextual_recommendation_data
    WHERE similarity_tag = '{tag}'
    LIMIT 1
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        return "🤔 RecommendationAgent suggests: No direct match found. Please review the incident manually."

    return f"💡 RecommendationAgent suggests: {df.iloc[0]['recommendation']}"

# CLI test
if __name__ == "__main__":
    tag = input("🔍 Enter similarity tag (e.g., HighCPU, MemoryLeak): ").strip()
    print(recommendation_agent(tag))
