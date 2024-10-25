import streamlit as st 
from openai import OpenAI
client = OpenAI(api_key="MY-API-KEY-HERE")

#Feature Personalized recomendations
def get_completion(prompt, model="gpt-3.5-turbo"):
  completion = client.chat.completions.create(
      model=model,
      messages=[
       {"role": "system", "content": "You are a chatbot to help assist people schedule their parks and rec reservations. Provide useful information about parking and state the rules of a park. Provide available times and dates for the user based on their needs."},
       {"role": "user", "content": prompt},
      ]
  )
  return completion.choices[0].message.content

with st.form(key = "chat"):
    prompt = st.text_input("Ask for available parks or specific recommendations based on your preferences (e.g., 'Show me morning options for hiking')") # TODO!
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.write(get_completion(prompt))


#Feature2
#Real-Time Assistance for Reservations and Applications - Enables users to ask common questions and receive step-by-step guidance through the reservation or application process.def get_completion(prompt, model="gpt-3.5-turbo"):
    # Determine if the user is asking for a common question or needs step-by-step guidance
    is_reservation_query = any(keyword in prompt.lower() for keyword in ["reservation", "apply", "process", "steps", "guide"])
def get_completion(prompt, model="gpt-3.5-turbo"):    
    if is_reservation_query:
        system_message = (
            "You are an AI chatbot that assists users with reservations and applications. "
            "You will guide them step-by-step through the process and ensure they don't get lost or frustrated."
        )
    else:
        system_message = (
            "You are an AI chatbot that answers common questions in real-time, "
            "such as availability of picnic areas"
        )

    completion = client.chat.completions.create(
            model=model,
            messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
        ]
    )
    return completion.choices[0].message.content





#Feature3: Map of the parks in city/ allow users to enter zip/city and find available areas

import pydeck as pdk
import pandas as pd

# Sample park data (this can be dynamically fetched or updated based on actual data)
parks_data = [
    {"name": "Central Park", "latitude": 40.785091, "longitude": -73.968285, "availability": "Available"},
    {"name": "Prospect Park", "latitude": 40.660204, "longitude": -73.968956, "availability": "Available"},
    {"name": "Flushing Meadows", "latitude": 40.749824, "longitude": -73.840784, "availability": "Fully Booked"},
    {"name": "Riverside Park", "latitude": 40.800277, "longitude": -73.970694, "availability": "Available"},
    {"name": "Battery Park", "latitude": 40.703277, "longitude": -74.017028, "availability": "Available"},
]

# Convert the parks data to a DataFrame for easier processing
parks_df = pd.DataFrame(parks_data)

# Feature 3: Display a map of parks based on user input (city or zip code)
def display_parks_map(parks):
    st.write("Available parks based on your search:")

    # Create a map layer with park locations
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=parks,
        get_position="[longitude, latitude]",
        get_color="[200, 30, 0, 160]",
        get_radius=200,
    )

    # Define the initial view of the map (centered around the first park)
    view_state = pdk.ViewState(
        latitude=parks["latitude"].mean(), longitude=parks["longitude"].mean(), zoom=10, pitch=50
    )

    # Create the map with the layer
    r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{name}\n{availability}"})
    
    # Display the map using Stream
st.pydeck_chart(r)

# Input: User enters a city or zip code
with st.form(key="location_form"):
    location_input = st.text_input("Enter your city or zip code to find available parks:")
    submitted = st.form_submit_button("Search")

    if submitted:
        # For this demo, we are showing all parks as if they match the user input.
        # In a real-world app, you'd filter parks based on geolocation or proximity.
        display_parks_map(parks_df)