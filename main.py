import streamlit as st

from multipage import MultiPage
import add_food, main_page, previously_bought, share_food 
# Create an instance of the app 
app = MultiPage()

is_share_possible = True

# Title of the main page
st.title("Do not waste")

# Add all your applications (pages) here
app.add_page("Main Page", main_page.app, is_share_possible)
app.add_page("Add Food", add_food.app)
app.add_page("Your Shopping History", previously_bought.app)

if is_share_possible:
    app.add_page("Share your food", share_food.app)

# The main app
app.run()