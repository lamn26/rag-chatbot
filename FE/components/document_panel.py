import requests
import streamlit as st

from api.documents import (
    delete_document,
    list_documents,
    upload_document,
)
from config import SUPPORTED_EXTENSIONS

def render_document_panel() -> None:
    session_id = st.session_state.session_id

    st.divider()
    st.subheader("Upload document")

    uploaded_file = st.file_uploader(
        "Choose a document",
        type=SUPPORTED_EXTENSIONS,
        accept_multiple_files=False,
        key=f"upload_{session_id}",
    )

    if uploaded_file is not None:
        if st.button(
            "Upload",
            type="primary",
            key=f"upload_button_{session_id}",
        ):
            try:
                with st.spinner("Processing document..."):
                    data = upload_document(session_id, uploaded_file)

                st.session_state.upload_success = (
                    f"Uploaded successfully: {data['filename']} "
                    f"({data['chunks_created']} chunks)"
                )
                st.rerun()

            except requests.HTTPError as e:
                detail = (
                    e.response.text
                    if e.response is not None
                    else str(e)
                )
                st.error(f"Upload failed: {detail}")

            except requests.RequestException as e:
                st.error(f"Could not connect to the API: {e}")

    success_message = st.session_state.pop("upload_success", None)
    if success_message:
        st.success(success_message)

    st.divider()
    st.subheader("Your documents")

    try:
        data = list_documents(session_id)

        documents = data.get("documents", [])
        total = data.get("total", len(documents))

        st.write(f"Total documents: **{total}**")

        if not documents:
            st.info("No documents uploaded in this session yet.")
            return

        for document in documents:
            document_id = document["document_id"]
            filename = document["filename"]
            chunks_count = document.get("chunks_count", 0)

            with st.container(border=True):
                col1, col2 = st.columns([4, 1])

                with col1:
                    st.markdown(f"**{filename}**")
                    st.caption(f"Document ID: `{document_id}`")
                    st.caption(f"Chunks: {chunks_count}")

                with col2:
                    if st.button(
                        "Delete",
                        key=f"delete_{session_id}_{document_id}",
                        use_container_width=True,
                    ):
                        try:
                            delete_document(session_id, document_id)
                            st.rerun()

                        except requests.HTTPError as e:
                            detail = (
                                e.response.text
                                if e.response is not None
                                else str(e)
                            )
                            st.error(f"Delete failed: {detail}")

                        except requests.RequestException as e:
                            st.error(
                                f"Could not connect to the API: {e}"
                            )

    except requests.HTTPError as e:
        detail = e.response.text if e.response is not None else str(e)
        st.error(f"Could not load documents: {detail}")

    except requests.RequestException as e:
        st.error(f"Could not connect to the API: {e}")
