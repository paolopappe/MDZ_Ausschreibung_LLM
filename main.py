import streamlit as st
import requests
import threading
from itertools import pairwise

from server import start_server, BASE_URL

DEFAULT_CHAT_PLACEHOLDER = "Ihre Suchanfrage"


def start_server_thread() -> None:
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()


def init_page() -> None:
    menu = {
        "About": "..."
    }
    st.set_page_config(
        page_title="...",
        initial_sidebar_state="collapsed",
        menu_items=menu
    )
    if "docs" not in st.session_state:
        st.session_state.docs = None
    if "query_set" not in st.session_state:
        st.session_state.query_set = None
    if "chat_placeholder" not in st.session_state:
        st.session_state.chat_placeholder = DEFAULT_CHAT_PLACEHOLDER


def reset(chat_placeholder: str=DEFAULT_CHAT_PLACEHOLDER) -> None:
    st.session_state.docs = None
    st.session_state.query_set = False
    st.session_state.chat_placeholder = chat_placeholder


def make_title() -> None:
    st.title("...")
    with st.expander("Benutzung", icon="ℹ", expanded=False):
        st.markdown("...")


def main():

    # start the backend so it listens to the incoming queries;
    # it runs in a different thread to prevent blocking
    start_server_thread()

    init_page()
    make_title()

    search_bar = st.container(border=False)
    if query := search_bar.chat_input(
        placeholder=st.session_state.chat_placeholder,
        on_submit=reset,
        # args=(query, )  # make the query the new placeholder
    ) or st.session_state.query_set:

        if not st.session_state.docs:

            response = requests.get(f"{BASE_URL}/get", params={"query": query})
            if response.status_code == 200:
                docs = response.json()
                st.session_state.docs = docs
                st.session_state.query_set = True
                # st.session_state.chat_placeholder = query

            else:
                st.error(
                    response.json() + "\n\nWenden Sie sich bitte an "
                    "die zuständigen Developer."
                )

        else:
            docs = st.session_state.docs
            

        if n_docs := len(docs):

            n_docs_col, n_show_col_txt, n_show_col = st.columns(
                [7, 2, 2],
                vertical_alignment="center"
            )
            n_docs_col.markdown(f"**{n_docs}** Ergebnisse gefunden.")
            n_show_col_txt.markdown("Pro Seite Zeigen")
            n = n_show_col.selectbox(
                "Pro Seite Zeigen",
                (5, 10, 20),
                label_visibility="collapsed"
            )

            boundaries = list(range(0, n_docs, n)) + [n_docs]
            ranges = list(pairwise(boundaries))
            range_descs = [f"Seite {i + 1}" for i in range(len(ranges))]
            tabs = st.tabs(range_descs)
            for i, tab in enumerate(tabs):
                with tab:
                    start, end = ranges[i]
                    for j in range(start, end):
                        doc = docs[j]
                        descr = f"**{j + 1}**. " + ", ".join(f"**{k}**: __{v}__" for k, v in doc["metadata"].items())
                        with st.expander(descr, expanded=True):
                            st.markdown(doc["text"])

        else:
            st.info(
                "Keine Ergebnisse nach Ihrer Anfrage gefunden."
            )
            reset()


if __name__ == '__main__':
    main()