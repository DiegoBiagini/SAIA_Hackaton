import streamlit as st
import pandas as pd
from multipage import MultiPage
import add_food, main_page, previously_bought, share_food 
from streamlit import session_state
import json
from pathlib import Path
from streamlit import session_state


# Load product types
if "products" not in session_state:
    products = pd.read_csv("dataset/products.csv")
    session_state["products"] = products["product_name"]

# Load sharing info
if "sharing" not in session_state:
    # Read the json file created by the system
    json_path = Path("sharing.json")
    if json_path.is_file():
        with open(json_path, "r") as f:
            in_json = json.load(f)
        session_state["sharing"] = in_json
    else:
        session_state["sharing"] = {"can_share":False, "users":[]}

# Create an instance of the app 
app = MultiPage()



# Title of the main page
st.title("FoodxChange")

# Add all your applications (pages) here
app.add_page("Main Page", main_page.app)
app.add_page("Add Food", add_food.app)
app.add_page("Your Shopping History", previously_bought.app)

if session_state["sharing"]["can_share"]:
    app.add_page("Share your food", share_food.app)

# The main app
app.run()