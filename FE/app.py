import requests
import streamlit as st

from components.document_panel import render_document_panel
from components.session_panel import render_session_panel
from components.chat_panel import render_chat_panel

st.set_page_config(
    page_title="RAG Chatbot",
    layout="wide",
)
st.title("RAG Chatbot")
st.caption("Chat with your own documents.")

if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "collection_name" not in st.session_state:
    st.session_state.collection_name = None
if "messages" not in st.session_state:
    st.session_state.messages = []

render_session_panel() # render sidebar

# render main page
if st.session_state.session_id is None:
    st.info("Start a session from the sidebar to begin.")
else:
    st.subheader("Welcome!")

    st.write(
        "Your session is ready. "
        "In the next steps, please add document upload and chat."
    )

    render_document_panel()
    render_chat_panel()