import streamlit as st

def app(is_share_possible):
    st.write("Main page")
    st.write("Welcome, Name")

    mp = st.empty()
    if is_share_possible:
        mp.write("It looks like some of your stuff could be shared")