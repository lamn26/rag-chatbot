import requests
import streamlit as st

from api.chat import ask_question

# def render_sources(
#     sources: list[dict]
# ) -> None:
#     if not sources:
#         return

#     with st.expander(f"Sources ({len(sources)})"):
#         for idx, source in enumerate(sources, start=1):
#             filename = source.get("filename", "Unknown")
#             page_number = source.get("page_number")
#             chunk_index = source.get("chunk_index")
#             score = source.get("score")

#             st.markdown(f"**{idx}. {filename}**")

#             details = []

#             if page_number is not None:
#                 details.append(f"Page: {page_number}")
#             if chunk_index is not None:
#                 details.append(f"Chunk: {chunk_index}")
#             if score is not None:
#                 details.append(f"Score: {score:.4f}")

#             if details:
#                 st.caption(" | ".join(details))

def render_chat_panel() -> None:
    session_id = st.session_state.session_id

    st.divider()
    st.subheader("Chat with your documents")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            # if message["role"] == "assistant":
            #     render_sources(message.get("source", []))

    question = st.chat_input(
        "Ask a question about your documents..."
    )

    if not question:
        return

    user_message = {
        "role": "user",
        "content": question
    }

    st.session_state.messages.append(user_message)

    with st.chat_message("user"):
        st.markdown(user_message["content"])

    with st.chat_message("assistant"):
        try:
            with st.spinner("Searching documents and generating answer..."):
                data = ask_question(
                    session_id=session_id,
                    question=question
                )

                assistant_message = {
                    "role": "assistant",
                    "content": data["answer"],
                    "sources": data.get("sources", []),
                }

                st.session_state.messages.append(assistant_message)

                st.markdown(assistant_message["content"])
                # render_sources(assistant_message["sources"])

        except requests.HTTPError as e:
            detail = (
                e.response.text
                if e.response is not None
                else str(e)
            )

            st.error(f"Chat request failed: {detail}")

        except requests.RequestException as e:
            st.error(f"Could not connect to the API: {e}")