import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import openai

# Initialize the OpenAI client
openai.api_key = "YOUR-API-KEY-HERE"

# Function to get AI-generated safety tips based on prediction
def get_safety_tips(risk_level):
    prompt = f"The water quality has been predicted to have a {risk_level} risk of contamination. What are the recommended safety measures for users until they can conduct a proper test?"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
    )
    return response.choices[0].text.strip()

# Load synthetic water testing data 
data = pd.read_csv("/path/to/synthetic_water_testing_data.csv")

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
    tips = get_safety_tips("high")
    st.write("Safety Tips:", tips)
else:
    st.success("No high-risk days detected. Continue regular monitoring.")

# Reminder for testing
st.button("Set Reminder", help="Click to set a reminder for water testing on risky days.")
