import streamlit as st
from streamlit_option_menu import option_menu
from incident_resolver import incident_resolver
from mcp_chatbot_ui import mcp_chatbot
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(
    page_title="SmartOps",
    layout='wide',
    page_icon="home",
)

st.markdown("""
    <h1 style='text-align: center;'>SmartOps</h1>
    """, unsafe_allow_html=True)


st.write("""This app provides AI-enabled Integrated Platform Environment for platform support teams to streamline troubleshooting and decision-making.
            The SmartOps is an applciation that integrates with multiple AI agents to provide a comprehensive view of the platform health and performance.
""")

def ui():
    with st.sidebar:
        selected = option_menu("Main Menu", ["Home", 'Resolve/RCA Incident',
                                             'Chatbot',
                                            ], 
            icons=['house', 'search','chat'], menu_icon="cast", default_index=0)
        
    if selected == "Resolve/RCA Incident":
        incident_resolver()
    elif selected == "Chatbot":
        mcp_chatbot()

if __name__=='__main__':
    ui()