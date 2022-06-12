import subprocess
import streamlit as st
import json
import predict
from streamlit import session_state
from threading import Thread
from pathlib import Path

def app():
    for key in st.session_state.keys():
        if key != "products" and key != "sharing":
            del st.session_state[key]
    st.write("Main page")
    st.write("Welcome, Name")

    mp = st.empty()
    if session_state["sharing"]["can_share"]:
        mp.write("It looks like some of your stuff could be shared")

        not_anymore_button = st.empty()

        def start_sharing():
            session_state["sharing"]["can_share"] = False
            with open("sharing.json", "w") as f:
                json.dump(session_state["sharing"], f)
        click = not_anymore_button.button("Nothing to share", on_click=start_sharing)

    else:
        mp.write("We don't think you have anything that needs sharing")
        
        share_anyway_button = st.empty()

        def share_anyway():
            if not Path("user_data/history.csv").is_file():
                st.error("Please add something to your previous shopping list first")
            else:
                del session_state["sharing"]
                try:
                    new_thread = Thread(target=predict.main())
                    new_thread.start()
                except FileNotFoundError as e:
                    print(e)
                    st.error("Prediction can't be performed on the cloud")


        click = share_anyway_button.button("I want to share anyway", on_click=share_anyway)
