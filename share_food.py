import streamlit as st
from streamlit import session_state

def app():
    for key in st.session_state.keys():
        if key != "products" and key != "sharing":
            del st.session_state[key]

    other_users = session_state["sharing"]["users"]
    if other_users:
        st.write("Here's the people which might like what you have")

        users_list = [(u["user_id"], u["similarity"]) for u in other_users]
        sorted_ulist = sorted(users_list, key=lambda tup: tup[1], reverse=True)

        # Only take the 3 best ones
        threshold = -1
        filter_best = lambda x : True if x[1] > threshold else False
        sorted_ulist = list(filter(filter_best, sorted_ulist))[:3]

        radio_choices = (str(el[0]) + ", Similarity:" + str(el[1]) for el in sorted_ulist)
        st.radio("Choose one of them", radio_choices)
        
        st.button("SHARE!")
    else:
        st.write("No one else found")