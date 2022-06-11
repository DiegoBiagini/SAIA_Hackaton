import streamlit as st
import pandas as pd
from multipage import MultiPage
import add_food, main_page, previously_bought, share_food 
from streamlit import session_state
import json
from pathlib import Path

# Load product types
products = pd.read_csv("dataset/products.csv")

# Create an instance of the app 
app = MultiPage()

# Read the json file created by the system
json_path = Path("sharing.json")
if json_path.is_file():
    with open(json_path, "r") as f:
        in_json = json.load(f)
    is_share_possible = in_json["can_share"]

    other_users = in_json["users"]
else:
    is_share_possible = False

# Title of the main page
st.title("Do not waste")

# Add all your applications (pages) here
app.add_page("Main Page", main_page.app, in_json)
app.add_page("Add Food", add_food.app, products)
app.add_page("Your Shopping History", previously_bought.app)

if is_share_possible:
    app.add_page("Share your food", share_food.app, other_users)

# The main app
app.run()