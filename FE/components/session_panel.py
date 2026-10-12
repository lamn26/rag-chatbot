import requests
import streamlit as st

from api.sessions import create_session, delete_session

def render_session_panel() -> None:
    with st.sidebar:
        st.header("Session")

        if st.session_state.session_id is None:
            st.info("No active session.")

            if st.button(
                "Start Session",
                type="primary",
                use_container_width=True,
            ):
                try:
                    data = create_session()

                    st.session_state.session_id = data["session_id"]
                    st.session_state.collection_name = data["collection_name"]
                    st.session_state.messages = []

                    st.rerun()

                except requests.RequestException as e:
                    st.error(f"Could not create session: {e}")

        else:
            st.success("Session active.")

            st.caption("Session ID")
            st.code(st.session_state.session_id)

            st.caption("Collection")
            st.code(st.session_state.collection_name)

            if st.button(
                "End Session",
                type="secondary",
                use_container_width=True,
            ):
                try:
                    delete_session(st.session_state.session_id)

                    st.session_state.session_id = None
                    st.session_state.collection_name = None
                    st.session_state.messages = []

                    st.rerun()

                except requests.RequestException as e:
                    st.error(f"Could not end session: {e}")
