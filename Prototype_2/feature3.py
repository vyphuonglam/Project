import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from openai import OpenAI
import fitz
import os
import folium
from streamlit_folium import st_folium



def app():
    st.title("Smart Water Saver")
    st.write("Welcome to Smart Water Saver")


    # Initialize the OpenAI client
    client = OpenAI(api_key="OPENAI_API_KEY")




    # Sample water usage data
    data = pd.DataFrame({
        "zip_code": [95112, 95113, 95114, 95115, 95116],
        "average_daily_use": [50, 60, 55, 45, 65],  # example usage in gallons per day
        "water_rate": [0.005, 0.007, 0.006, 0.0055, 0.0072]  # example rate in cost per gallon
    })

    # Recommended usage rates per activity (in gallons per week per person)
    recommended_usage = {
        "showers": 70,  # 10 gallons per shower, assuming 7 showers per week
        "washing_machine": 40,  # assuming 4 loads per week, 10 gallons per load
        "dishwasher": 15,  # 15 gallons per week for dishwashing
        "garden": 50  # assuming 50 gallons per week for outdoor watering
    }

    # Title and Introduction
    st.title("Smart Water Saver")
    st.write("Estimate your household’s water usage and find ways to save.")

    # User Input: Household Details
    st.header("Household Details")
    household_size = st.slider("Number of people in household", 1, 10, 3)
    home_type = st.selectbox("Type of home", ["Apartment", "Single-Family House", "Multi-Family House"])

    # Input water-using activities
    st.header("Water-Using Activities")
    showers_per_week = st.number_input("Showers per week per person", min_value=0, max_value=100, value=20)
    wash_loads_per_week = st.number_input("Washing machine loads per week", min_value=0, max_value=50, value=10)
    dish_washes_per_week = st.number_input("Dishwashing cycles per week", min_value=0, max_value=50, value=15)
    garden_watering_hours = st.number_input("Hours of garden watering per week", min_value=0, max_value=100, value=5)

    # User Input for Zip Code
    st.header("Check Your Local Water Data")
    zip_code = st.text_input("Enter your San Jose Zip Code", max_chars=5)

    if zip_code:
        # Validate zip code
        if not zip_code.isdigit() or len(zip_code) != 5:
            st.error("Please enter a valid 5-digit zip code.")
        else:
            zip_code_int = int(zip_code)
            # Filter data based on zip code
            filtered_data = data[data['zip_code'] == zip_code_int]
            
            if not filtered_data.empty:
                # Display relevant water data
                st.subheader(f"Water Data for Zip Code {zip_code}")
                avg_daily_use = filtered_data['average_daily_use'].values[0]
                water_rate = filtered_data['water_rate'].values[0]
                estimated_monthly_cost = avg_daily_use * water_rate * 30  # 30 days in a month
                
                st.write(f"**Average Daily Use:** {avg_daily_use} gallons")
                st.write(f"**Water Rate:** ${water_rate} per gallon")
                st.write(f"**Estimated Monthly Cost:** ${estimated_monthly_cost:.2f}")
                
                # Calculate ideal usage based on household size
                ideal_showers = recommended_usage['showers'] * household_size
                ideal_washing = recommended_usage['washing_machine'] * household_size
                ideal_dishwashing = recommended_usage['dishwasher'] * household_size
                ideal_garden = recommended_usage['garden']  # Assuming garden watering is independent of household size
                
                st.write("### Recommended Weekly Water Usage (gallons)")
                st.write(f"- Showers: {ideal_showers} gallons")
                st.write(f"- Washing Machine: {ideal_washing} gallons")
                st.write(f"- Dishwashing: {ideal_dishwashing} gallons")
                st.write(f"- Garden Watering: {ideal_garden} gallons")
                
                # Compare user input to recommendations
                st.write("### Your Household's Weekly Water Usage Compared to Recommendations")
                st.write(f"- **Showers**: You use {showers_per_week * household_size} gallons vs. recommended {ideal_showers}")
                st.write(f"- **Washing Machine**: You use {wash_loads_per_week * 10} gallons vs. recommended {ideal_washing}")
                st.write(f"- **Dishwashing**: You use {dish_washes_per_week * 5} gallons vs. recommended {ideal_dishwashing}")
                st.write(f"- **Garden Watering**: You use {garden_watering_hours * 10} gallons vs. recommended {ideal_garden}")
                
                # Optional: Display on a map if you have latitude and longitude data
                zip_coords = {
                    95112: [37.3541, -121.9552],
                    95113: [37.3324, -121.8930],
                    95114: [37.3337, -121.8853],
                    95115: [37.3061, -121.8471],
                    95116: [37.3165, -121.8583],
                }
                
                if zip_code_int in zip_coords:
                    m = folium.Map(location=zip_coords[zip_code_int], zoom_start=13)
                    folium.Marker(location=zip_coords[zip_code_int], popup=f"Zip Code {zip_code}").add_to(m)
                    st_folium(m, width=700, height=500)
                else:
                    st.write("Map coordinates for this zip code are not available.")
            else:
                st.write("No data available for this zip code.")

    # Educational Content
    st.header("Water Conservation Tips")
    st.markdown("""
    - **Fix Leaks**: A dripping faucet can waste up to 20 gallons of water per day.
    - **Install Low-Flow Fixtures**: Low-flow showerheads and faucets can significantly reduce water usage.
    - **Use a Broom Instead of a Hose**: When cleaning driveways or sidewalks, use a broom instead of a hose to save water.
    - **Collect Rainwater**: Use rain barrels to collect water for gardening and other outdoor uses.
    - **Insulate Your Water Pipes**: Insulating pipes can reduce the time it takes for hot water to reach your taps, saving both water and energy.
    """)