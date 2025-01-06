import streamlit as st
import requests
import threading
from itertools import pairwise

from server import start_server, BASE_URL

DEFAULT_CHAT_PLACEHOLDER = "Ihre Suchanfrage"


def start_server_thread() -> None:
    # Blocking vermeiden
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()


def init_page() -> None:
    # Informationen zur App
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
    # Titel der App
    st.title("Prusseit und Reiss - Suchtool für Ausschreibungstexte")
    # Erklärungstext für die Nutzer
    with st.expander("Benutzung", icon="ℹ", expanded=False):
        st.markdown("Hier steht ein Erklärungstext")


def main():

    # start the backend so it listens to the incoming queries;
    # it runs in a different thread to prevent blocking
    start_server_thread()

    init_page()
    make_title()

    search_bar = st.container(border=False)
    if query := search_bar.chat_input(  # wenn der Nutzer eine Anfrage eingibt
        placeholder=st.session_state.chat_placeholder,
        on_submit=reset,
        # args=(query, )  # make the query the new placeholder
    ) or st.session_state.query_set:    # oder wenn es schon eine gibt
        
        # es wird gecheckt ob es schon relevante Chunks gefunden wurden
        if not st.session_state.docs:

            # wenn nicht, dann werden sie mit dem Pipeline abgerufen (siehe utils/pipeline.py)
            response = requests.get(f"{BASE_URL}/get", params={"query": query})
            if response.status_code == 200:
                docs = response.json()
                # die gefundenen Chunks speichern
                st.session_state.docs = docs
                st.session_state.query_set = True
                # st.session_state.chat_placeholder = query

            else:
                st.error(
                    response.json() + "\n\nWenden Sie sich bitte an "
                    "die zuständigen Entwickler."
                )

        else:
            # die gefundenen Chunks einlesen
            docs = st.session_state.docs
            

        # wenn die Chunks abgerufen / eingelesen wurden, werden sie gezeigt
        if n_docs := len(docs):

            n_docs_col, n_show_col_txt, n_show_col = st.columns(
                [7, 2, 2],
                vertical_alignment="center"
            )
            n_docs_col.markdown(f"**{n_docs}** Ergebnisse gefunden.")
            n_show_col_txt.markdown("Vorschläge pro Seite")
            n = n_show_col.selectbox(
                "Vorschläge pro Seite",
                (5, 10, 20),
                label_visibility="collapsed"
            )

            boundaries = list(range(0, n_docs, n)) + [n_docs]
            ranges = list(pairwise(boundaries))
            range_descs = [f"Seite {i + 1}" for i in range(len(ranges))]
            tabs = st.tabs(range_descs) # Seiten mit Ergebnissen
            for i, tab in enumerate(tabs):
                with tab:
                    start, end = ranges[i]
                    for j in range(start, end):
                        doc = docs[j]
                        # für jeden Chunk gibt es eine Beschreibung aus den Metadaten
                        descr = f"**{j + 1}**. " + ", ".join(f"**{k}**: __{v}__" for k, v in doc["metadata"].items())
                        with st.expander(descr, expanded=True):
                            # der formatierte Text
                            st.markdown(doc["text"])

        else:
            # wenn all die Chunks einen niedrigeren als SIMILARITY_THRESHOLD Score haben
            st.info(
                "Keine Ergebnisse auf Ihre Anfrage gefunden."
            )
            reset()


if __name__ == '__main__':
    main()