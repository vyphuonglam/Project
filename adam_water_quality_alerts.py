import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import openai

# Initialize the OpenAI client
openai.api_key = "YOUR-API-KEY-HERE"

# Function to get AI-generated safety tips based on prediction
def get_completion(prompt, model="gpt-3.5-turbo"):
    completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant providing water safety recommendations based on predicted contamination risk levels."},
            {"role": "user", "content": prompt},
        ]
    )
    return completion.choices[0].message.content.strip()

# Load synthetic water testing data 
data = pd.read_csv("synthetic_water_testing_data.csv")

st.title("Water Quality Prediction & Emergency Alert System")
st.write("Monitor potential water quality issues and receive safety recommendations.")

# User input for water source and testing history
source_options = st.selectbox(
    "Select your water source:",
    ["Tap water", "Filtered water", "Bottled water", "Rainwater Collection", "Well water", "Ocean water"]
)

# Simulate historical water quality data based on source
st.write("Generating predictive analysis for:", source_options)
selected_data = data[data["Water Source"] == source_options]

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
st.button("Set Reminder", help="Click to set a reminder for water testing on risky days.")
