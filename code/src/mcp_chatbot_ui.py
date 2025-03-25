# ui/mcp_chatbot_ui.py
# Streamlit chatbot interface for MCP Chatbot with greetings and improved prompt guidance

import os
import streamlit as st
from mcp_chatbot_agent import get_mcp_chat_agent
from langchain.chat_models import ChatOpenAI

#st.set_page_config(page_title="🧠 MCP Chatbot", layout="wide")
def mcp_chatbot():
    # Load or initialize chat agent
    if "agent" not in st.session_state:
        st.session_state.agent = get_mcp_chat_agent()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.title("🤖 GenAI MCP Chatbot")
    st.markdown("Ask about incidents, anomalies, KB articles, or solutions. The chatbot uses multiple LangChain tools behind the scenes.")

    def is_greeting(text: str) -> bool:
        greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "yo", "hola"]
        return text.strip().lower() in greetings

    def is_farewell(text: str) -> bool:
        farewells = ["bye", "goodbye", "see you", "see ya", "later", "thanks", "thank you", "bye bye"]
        return text.strip().lower() in farewells

    # GPT classifier
    def is_support_query(text: str) -> bool:
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
        check_prompt = f"""You are a smart classifier for platform support queries.
    
    Determine whether the input is about incidents, telemetry, root cause analysis, automation, or knowledge base searches.
    Accept abbreviations like 'mem' for memory, 'cpu', 'rca', etc.
    
    Respond ONLY with 'YES' or 'NO'.
    
    User input: {text}
    """.strip()
        response = llm.predict(check_prompt).strip().lower()
        st.session_state.last_check = response
        return "yes" in response

    # Input box
    user_input = st.chat_input("Ask me something...")

    # Handle input
    if user_input:
        st.session_state.chat_history.append(("user", user_input))

        if is_greeting(user_input):
            greeting_msg = (
                "👋 Hello! I’m your platform support assistant.\n\n"
                "You can ask me things like:\n"
                "- `What caused inc045?`\n"
                "- `Any CPU spikes today?`\n"
                "- `Search KB for memory leak`"
            )
            st.chat_message("assistant").markdown(greeting_msg)
            st.session_state.chat_history.append(("agent", greeting_msg))

        elif is_farewell(user_input):
            farewell_msg = "👋 Glad I could help! Reach out anytime for platform support assistance. Stay awesome! ✨"
            st.chat_message("assistant").markdown(farewell_msg)
            st.session_state.chat_history.append(("agent", farewell_msg))

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

    # Show GPT classification response in sidebar (debugging)
    if "last_check" in st.session_state:
        st.sidebar.markdown(f"🧪 Last intent check: `{st.session_state.last_check}`")
