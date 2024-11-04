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
    st.title("Water Testing Information Hub")
    st.write("Welcome to Water Testing Information Hub")
    # Initialize the OpenAI client
    client = OpenAI(api_key="OPENAI_API_KEY")



    # Function to get completion from OpenAI API
    def get_water_expert_completion(prompt, model="gpt-3.5-turbo"):
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a water testing expert with a background in environmental science, focused on providing simple guides, tips, and FAQs for DIY water testing. Provide a clear, concise response of up to three paragraphs, using bullet points for clarity. Use verbs like guide, explain, clarify, recommend, and identify to keep instructions actionable and easy to follow. This is a DIY water testing guide for residents. The goal is to help readers understand the importance of testing, recognize common contaminants, and interpret results without professional assistance. Use a friendly, informative, and approachable tone, suitable for homeowners and families. Avoid technical jargon. Exclude overly technical terms, complex chemical names, and steps requiring lab equipment or professional tools."},
                {"role": "user", "content": prompt},
            ]
        )
        return completion.choices[0].message.content

    # Load the CSV file
    data = pd.read_csv("synthetic_water_testing_data.csv")

    st.title("Water Testing Information Hub")
    st.write("Learn about interpreting water testing results! Select your water type, contaminants, and testing method!")

    # Select box for water source
    source_options = st.selectbox(
        "What type is the Water Source?",
        ["Tap water", "Filtered water", "Bottled water", "Rainwater Collection", "Well water", "Ocean water"],
    )
    st.write("You selected:", source_options)

    # Multiselect for contaminants
    contaminants_options = st.multiselect(
        "What contaminants are you testing for?",
        ["Lead (ppb)", "Chlorine (ppm)", "Nitrates/Nitrites (ppm)", "Bacteria (e.g., E. coli)", "Pesticides (ppm)", "Herbicides (ppm)"]
    )
    st.write("You selected:", contaminants_options)

    # Selectbox for testing methods
    methods_options = st.selectbox(
        "What methods are being used to test the water?",
        ["Test strips", "Digital Test Kits", "Visual Inspection"],
    )
    st.write("You selected:", methods_options)

    # Filter the dataset based on user inputs
    filtered_data = data[
        (data["Water Source"] == source_options) &
        (data["Testing Method"] == methods_options)
    ]

    # Further filter by contaminants if specified
    if contaminants_options:
        for contaminant in contaminants_options:
            if contaminant in filtered_data.columns:
                filtered_data = filtered_data[filtered_data[contaminant].notna()]

    # Summarize filtered data
    filtered_data_summary = filtered_data.to_dict(orient="records") if not filtered_data.empty else "No matching data found."
    # Form for submitting questions
    with st.form(key="water_testing_chat1"):
        # User input prompt
        user_prompt = st.text_input("Enter your questions about your results! (e.g., 'My chlorine level is at 7, is that safe?' , 'If my nitrate level is greater than 5, is it safe to drink?)")

        # Submit button
        submitted = st.form_submit_button("Submit")

        if submitted:
            # Integrate the selected values and data summary into the prompt
            full_prompt = f"{user_prompt}\n\nAdditional Information:\n- Water Source: {source_options}\n- Contaminants: {', '.join(contaminants_options)}\n- Testing Methods: {methods_options}\n- Data Summary: {filtered_data_summary}"

            # Get response from OpenAI API
            response = get_water_expert_completion(full_prompt)
            st.write(response)


    # Function to get completion from OpenAI API
    def get_completion(prompt, model="gpt-3.5-turbo"):
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a water testing expert with a background in environmental science, focused on providing simple guides, tips, and FAQs for DIY water testing."},
                {"role": "user", "content": prompt},
            ]
        )
        return completion.choices[0].message.content

    # Load the CSV file for water testing data
    try:
        testing_data = pd.read_csv("water_potability.csv")
    except FileNotFoundError:
        st.error("The dataset file 'water_potability.csv' was not found. Please ensure it is in the same directory as this script.")
        st.stop()

    # Display the available columns for debugging
    st.write("Available columns:", testing_data.columns.tolist())
    st.write("Sample data:", testing_data.head())

    # Title of the app
    st.title("Water Potability Testing Information Hub")
    st.write("Learn about interpreting water testing results!")

    # Create a dropdown for selecting water type
    water_types = ["Tap Water", "Well Water", "Bottled Water"]  # Customize these options
    source_options = st.selectbox("What type of Water Source?", water_types)
    st.write("You selected:", source_options)

    # Create a multiselect for contaminants based on the provided column descriptions
    contaminants_options = st.multiselect(
        "What water quality parameters are you interested in?",
        [
            "ph", "Hardness", "Solids", "Chloramines", 
            "Sulfate", "Conductivity", "Organic_carbon", 
            "Trihalomethanes", "Turbidity"
        ]
    )
    st.write("You selected:", contaminants_options)

    # Initialize filtered_data variable
    filtered_data = testing_data.copy()  # Start with the full dataset

    # Filter for potable water if the 'Potability' column exists
    if 'Potability' in filtered_data.columns:
        filtered_data = filtered_data[filtered_data['Potability'] == 1]  # Assuming 1 means potable
    else:
        st.error("Column 'Potability' not found in the dataset. Please check the dataset and update the code accordingly.")


    # Form for submitting questions
    with st.form(key="water_testing_chat"):
        user_prompt = st.text_input("Enter your questions about your results (max 200 characters):", max_chars=200)

        submitted = st.form_submit_button("Submit")

        if submitted:
            # Reduce the size of the additional information
            filtered_data_summary = f"{len(filtered_data)} records found." if not filtered_data.empty else "No matching data found."

            # Get response from OpenAI API
            full_prompt = f"{user_prompt}\n\nAdditional Information:\n- Water Source: {source_options}\n- Parameters: {', '.join(contaminants_options)}\n- Data Summary: {filtered_data_summary}"

            try:
                response = get_completion(full_prompt)
                st.write(response)
            except Exception as e:
                st.error(f"An error occurred while getting a response: {e}")
        
    # Further filter by contaminants if specified
    if contaminants_options:
        filtered_data = filtered_data[filtered_data[contaminants_options].notna().any(axis=1)]

    # Summarize filtered data
    filtered_data_summary = filtered_data.to_dict(orient="records") if not filtered_data.empty else "No matching data found."



    # Function to get AI-generated safety tips based on prediction
    def get_water_assistant_completion(prompt, model="gpt-3.5-turbo"):
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant providing water safety recommendations based on predicted contamination risk levels."},
                {"role": "user", "content": prompt},
            ]
        )
        return completion.choices[0].message.content

    # Load synthetic water testing data
    data = pd.read_csv("water_potability_sources.csv")

    st.title("Water Quality Prediction & Emergency Alert System")
    st.write("Monitor potential water quality issues and receive safety recommendations.")

    # Ensure 'Water Source' is in the data columns and get unique options
    if 'Water Source' in data.columns:
        source_options = data['Water Source'].unique().tolist()
    else:
        st.error("The 'Water Source' column is missing in the dataset. Please check the CSV file structure.")
        st.stop()

    # User input for water source
    source_options = st.selectbox(
        "Select your water source:",
        source_options
    )

    # Filter data based on the selected water source
    selected_data = data[data["Water Source"] == source_options]

    # Check if there are matching rows for the selected source
    if not selected_data.empty:
        st.write("Generating predictive analysis for:", source_options)
    else:
        st.warning(f"No data found for the selected source: {source_options}")
        st.stop()

    # Dummy prediction based on past data (e.g., contamination trends)
    days_ahead = 7
    future_dates = [datetime.now() + timedelta(days=i) for i in range(1, days_ahead + 1)]
    predicted_quality = np.random.choice(["Low", "Moderate", "High"], days_ahead, p=[0.6, 0.3, 0.1])

    # Display predicted risk levels
    st.subheader("Predicted Water Quality Over the Next Week:")
    for i, date in enumerate(future_dates):
        st.write(f"{date.strftime('%Y-%m-%d')}: Risk Level - {predicted_quality[i]}")

    # Check for any high-risk predictions and provide safety tips
    if "High" in predicted_quality:
        st.warning("High risk detected on upcoming days. Follow safety recommendations below.")
        prompt = "The water quality has been predicted to have a high risk of contamination. What are the recommended safety measures for users until they can conduct a proper test?"
        tips = get_completion(prompt)
        st.write("Safety Tips:", tips)
    else:
        st.success("No high-risk days detected. Continue regular monitoring.")

    # Reminder for testing
    if st.button("Set Reminder", help="Click to set a reminder for water testing on risky days."):
        st.success("Reminder has been set for water testing.")  

