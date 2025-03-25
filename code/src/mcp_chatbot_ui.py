# ui/mcp_chatbot_ui.py
# Streamlit chatbot interface for MCP Chatbot with improved GPT classifier prompt

import os
import streamlit as st
from mcp_chatbot_agent import get_mcp_chat_agent
from langchain.chat_models import ChatOpenAI

# st.set_page_config(page_title="🧠 MCP Chatbot", layout="wide")
def mcp_chatbot():
    # Load or initialize chat agent
    if "agent" not in st.session_state:
        st.session_state.agent = get_mcp_chat_agent()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # st.title("🤖 GenAI MCP Chatbot")
    st.markdown("Ask about incidents, anomalies, KB articles, or solutions. The chatbot uses multiple LangChain tools behind the scenes.")

    # Enhanced GPT-based classifier with improved flexibility
    def is_support_query(text: str) -> bool:
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo",)
        check_prompt = f"""You are a smart classifier for platform support questions.

    User inputs may include abbreviations like 'mem' for memory, 'cpu', 'rca', etc.

    Your task is to detect if the input is about:
    - Incidents or RCA
    - Telemetry (e.g., memory, cpu, error logs)
    - Knowledge Base (KB) searches
    - Automation or remediation scripts

    Respond ONLY with 'YES' or 'NO'.

    Input: {text}
    """.strip()
        response = llm.predict(check_prompt).strip().lower()
        st.session_state.last_check = response
        return "yes" in response

    # Input box
    user_input = st.chat_input("Ask me something...")

    # Handle new user input
    if user_input:
        st.session_state.chat_history.append(("user", user_input))

        if not is_support_query(user_input):
            filtered_msg = """⚠️ I'm designed to help with platform support topics like:
    - Incidents (e.g., `What caused inc045?`)
    - Telemetry issues (e.g., `Any memory or CPU spikes?`)
    - KB articles
    - Automation suggestions"""
            st.chat_message("assistant").markdown(filtered_msg)
            st.session_state.chat_history.append(("agent", filtered_msg))
        else:
            with st.spinner("Thinking..."):
                response = st.session_state.agent.run(user_input)
            st.session_state.chat_history.append(("agent", response))

    # Display chat history
    for role, msg in st.session_state.chat_history:
        if role == "user":
            st.chat_message("user").markdown(msg)
        else:
            st.chat_message("assistant").markdown(msg)
