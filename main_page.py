import streamlit as st
import json

def app(in_json):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.write("Main page")
    st.write("Welcome, Name")

    mp = st.empty()
    if in_json["can_share"]:
        mp.write("It looks like some of your stuff could be shared")

        not_anymore_button = st.empty()
        click = not_anymore_button.button("Nothing to share")

        if click:
            in_json["can_share"] = False
            with open("sharing.json", "w") as f:
                json.dump(in_json, f)
            not_anymore_button.empty()
            mp.empty()