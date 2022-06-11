import streamlit as st
from pathlib import Path
import pandas as pd

def app():
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
        df.reset_index(drop=True, inplace=True)

        st.table(df)
    else:
        st.write("There is no history about you...")