import streamlit as st
from pathlib import Path
import pandas as pd

def app():
    for key in st.session_state.keys():
        del st.session_state[key]

    history_file = Path("user_data/history.csv")
    hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    if history_file.is_file():
        st.write("This is what you previously bought")
        df = pd.read_csv(history_file, index_col=0)
        df = df.sort_values(by="date", ascending=False)
        #df.reset_index(drop=True, inplace=True)

        previously_bought = []
        for r in df.iterrows():
            previously_bought.append(list(df.columns[r[1].notna()]))


        for i,t in enumerate(previously_bought):
            date = df.iloc[i, df.columns.get_loc("date")]
            date = date[:date.rfind(".")]
            st.write("Date:", date, t[:-1])
    else:
        st.write("There is no history about you...")