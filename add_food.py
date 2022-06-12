import streamlit as st
import time
from pathlib import Path
import pandas as pd
from streamlit import session_state


def app():

    st.write("Insert what you bought")

    filter = st.text_input("Search for your food",'')

    sb = st.empty()

    def search_pressed(filter):
        filtered_names = [k for k in session_state["products"] if filter in k]
        if len(filtered_names) > 50:
            filtered_names = filtered_names[:50]

        session_state["filtered_names"] = filtered_names
        #selection = sb.selectbox("Best result",index=0,options= session_state["filtered_names"])        

    search_button = st.button("Search", on_click=search_pressed, args=(filter,))

    def submit_to_cart(selection):
        if "grocery_list" not in session_state:
            session_state["grocery_list"] = [selection]
        else:
            session_state["grocery_list"] += [el for el in [selection] if el not in session_state["grocery_list"]]

    if "filtered_names" in session_state:
        selection = sb.selectbox("Best result",index=0,options= session_state["filtered_names"])
    else:
        selection = sb.selectbox("Best result",index=0,options= [])
    
    submit_button = st.button("Submit", on_click=submit_to_cart, args=(selection,))

    if "grocery_list" not in session_state:
        st.write("Grocery list is empty")
    else:
        st.write("Current grocery list")

        for g in session_state["grocery_list"]:
            st.write("-" + g)

        final_button = st.button("Register this list", on_click=update_grocery_list, args=(session_state["products"], session_state["grocery_list"]))

    
@st.cache
def update_grocery_list(product_names, grocery_list):
    Path('user_data').mkdir(parents=True, exist_ok=True)

    history_file = Path("user_data/history.csv")
    if not history_file.is_file():
        # Create the df from scratch
        df = pd.DataFrame(columns=(product_names.tolist()+ ["date"]))

    else:
        df = pd.read_csv(history_file, index_col=0)

    new_row = {}
    for prod in product_names:
        if prod in grocery_list:
            new_row[prod] = 1

    new_row["date"] = pd.to_datetime("today")
    new_df = df.append(new_row, ignore_index=True)

    new_df.to_csv(history_file)

    for key in st.session_state.keys():
        del st.session_state[key]
