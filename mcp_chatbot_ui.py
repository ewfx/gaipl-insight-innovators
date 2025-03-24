# ui/mcp_chatbot_ui.py
# Streamlit chatbot interface for MCP LangChain agent

import os
import streamlit as st
from mcp_chatbot_agent import get_mcp_chat_agent

st.set_page_config(page_title="🧠 MCP Chatbot", layout="wide")

# Load or initialize chat agent
if "agent" not in st.session_state:
    st.session_state.agent = get_mcp_chat_agent()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🤖 GenAI MCP Chatbot")
st.markdown("Ask about incidents, anomalies, KB articles, or solutions. The chatbot uses multiple LangChain tools behind the scenes.")

# Input box
user_input = st.chat_input("Ask me something...")

# Handle new user input
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.spinner("Thinking..."):
        response = st.session_state.agent.run(user_input)
    st.session_state.chat_history.append(("agent", response))

# Display chat history
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.chat_message("user").markdown(msg)
    else:
        st.chat_message("assistant").markdown(msg)
