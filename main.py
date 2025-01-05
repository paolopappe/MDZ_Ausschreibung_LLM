import streamlit as st
import requests
import threading

from server import start_server, BASE_URL


def start_server_thread():
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()


def init_page():
    menu = {
        "About": "..."
    }
    st.set_page_config(
        page_title="...",
        initial_sidebar_state="collapsed",
        menu_items=menu
    )
    st.session_state["query"] = None


def make_title():
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
    # if not (query := st.session_state["query"]):
    #     st.session_state["query"] = search_bar.chat_input(placeholder="Ihre Suchanfrage")
    # if query:
    if query := search_bar.chat_input(placeholder="Ihre Suchanfrage"):
        response = requests.get(f"{BASE_URL}/get", params={"query": query})
        if response.status_code == 200:
            docs = response.json()
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
                for i in range(0, min(n_docs, n)):
                    doc = docs[i]
                    descr = ", ".join(f"**{k}**: __{v}__" for k, v in doc["metadata"].items())
                    with st.expander(descr, expanded=True):
                        st.markdown(doc["text"])
            else:
                st.info(
                    "Keine Ergebnisse nach Ihrer Anfrage gefunden."
                )
        else:
            pass


if __name__ == '__main__':
    main()