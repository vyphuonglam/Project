import streamlit as st

import feature1
import feature2
import feature3



# Create a sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Water Testing Information Hub", "WATER TESTING GUIDE", "Smart Water Saver"])

# Render the selected page
if page == "Water Testing Information Hub":
    feature1.app()
elif page == "WATER TESTING GUIDE":
    feature2.app()
elif page == "Smart Water Saver":
    feature3.app()
