import streamlit as st
import pandas as pd
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key="YOUR_API_KEY_HERE")

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

# Further filter by contaminants if specified
if contaminants_options:
    for contaminant in contaminants_options:
        if contaminant in filtered_data.columns:
            filtered_data = filtered_data[filtered_data[contaminant].notna()]

# Summarize filtered data
filtered_data_summary = filtered_data.to_dict(orient="records") if not filtered_data.empty else "No matching data found."

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

