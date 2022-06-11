import streamlit as st
import time
from pathlib import Path
import pandas as pd

food_list = ["bread", "apple", "meat"]


def app():

    with st.form("grocery_list"):
        st.write("Insert what you bought")

        checkboxes = {}
        for el in food_list:
            checkboxes[el] = st.checkbox(el)

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            gl = {item : checkboxes[item] for item in food_list}
            update_grocery_list(gl)
            mk = st.markdown("Grocery List updated successfully")
            time.sleep(1)
            mk.empty()


def update_grocery_list(grocery_list):
    history_file = Path("user_data/history.csv")
    print(grocery_list)
    if not history_file.is_file():
        # Create the df from scratch
        df = pd.DataFrame(columns=list(grocery_list.keys())+ ["date"])

    else:
        df = pd.read_csv(history_file, index_col=0)
    new_row = grocery_list
    new_row["date"] = pd.to_datetime("today")
    new_df = df.append(grocery_list, ignore_index=True)

    new_df.to_csv(history_file)