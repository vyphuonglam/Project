import streamlit as st
import pandas as pd
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key="MY-API-KEY-HERE")

# Function to get completion from OpenAI API
def get_completion(prompt, model="gpt-3.5-turbo"):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a water testing expert with a background in environmental science, focused on providing simple guides, tips, and FAQs for DIY water testing. Provide a clear, concise response of up to three paragraphs, using bullet points for clarity. Use verbs like guide, explain, clarify, recommend, and identify to keep instructions actionable and easy to follow. This is a DIY water testing guide for residents. The goal is to help readers understand the importance of testing, recognize common contaminants, and interpret results without professional assistance. Use a friendly, informative, and approachable tone, suitable for homeowners and families. Avoid technical jargon. Exclude overly technical terms, complex chemical names, and steps requiring lab equipment or professional tools."},
            {"role": "user", "content": prompt},
        ]
    )
    return completion.choices[0].message.content

# Load the CSV file
data = pd.read_csv("/Users/joannele/Downloads/synthetic_water_testing_data.csv")

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
    filtered_data = filtered_data[filtered_data[contaminants_options].notna().any(axis=1)]

# Summarize filtered data
filtered_data_summary = filtered_data.to_dict(orient="records") if not filtered_data.empty else "No matching data found."

# Form for submitting questions
with st.form(key="water_testing_chat"):
    # User input prompt
    user_prompt = st.text_input("Enter your questions about your results! (e.g., 'My chlorine level is at 7, is that safe?' , 'If my nitrate level is greater than 5, is it safe to drink?)")

    # Submit button
    submitted = st.form_submit_button("Submit")

    if submitted:
        # Integrate the selected values and data summary into the prompt
        full_prompt = f"{user_prompt}\n\nAdditional Information:\n- Water Source: {source_options}\n- Contaminants: {', '.join(contaminants_options)}\n- Testing Methods: {methods_options}\n- Data Summary: {filtered_data_summary}"

        # Get response from OpenAI API
        response = get_completion(full_prompt)
        st.write(response)
